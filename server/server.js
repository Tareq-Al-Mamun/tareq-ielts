/**
 * TAREQ IELTS — AI Evaluation Backend Server
 *
 * Provides:
 *   POST /api/transcribe           — speech-to-text via z-ai ASR
 *   POST /api/evaluate             — IELTS Speaking evaluation
 *                                    → uses Google Gemini when GEMINI_API_KEY is set
 *                                    → falls back to z-ai LLM otherwise
 *   POST /api/evaluate-mock-test   — full mock-test evaluation (same provider logic)
 *   GET  /api/health               — health check + active provider info
 *
 * API keys are kept on the server; the frontend never sees them.
 *
 * ENVIRONMENT VARIABLES
 *   GEMINI_API_KEY   (optional, recommended)  Google Gemini API key.
 *                                              Get one at https://aistudio.google.com/app/apikey
 *   PORT             (optional, default 3001) Port to listen on.
 *
 * RUN
 *   export GEMINI_API_KEY="your-key-here"
 *   npm start
 *   (or: GEMINI_API_KEY="your-key-here" npm start)
 */

const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

// Load environment variables from .env (for local development).
// In production, set GEMINI_API_KEY directly in the environment.
require('dotenv').config();

// ----- Google Gemini SDK (optional; falls back to z-ai if unavailable) -----
let GoogleGenerativeAI = null;
try {
  GoogleGenerativeAI = require('@google/generative-ai').GoogleGenerativeAI;
} catch (e) {
  console.warn('⚠ @google/generative-ai not installed; Gemini provider unavailable.');
}

// ----- z-ai-web-dev-sdk (existing fallback) -----
let ZAI = null;
try {
  ZAI = require('/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk').default;
} catch (e) {
  try {
    ZAI = require('z-ai-web-dev-sdk').default;
  } catch (e2) {
    console.error('Failed to load z-ai-web-dev-sdk. Install with: npm install z-ai-web-dev-sdk');
    process.exit(1);
  }
}

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Multer for file uploads (audio files)
const upload = multer({
  dest: '/tmp/tareq-uploads/',
  limits: { fileSize: 25 * 1024 * 1024 } // 25MB max
});

// Serve the static HTML file
app.use(express.static(path.join(__dirname, '..', 'download')));

// ===== Provider selection =====
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-1.5-flash';
// ^ "gemini-1.5-flash" is the cheapest model that supports reliable JSON output.
//   Use "gemini-1.5-pro" for higher-quality (more expensive) evaluation.
//   See https://ai.google.dev/gemini-api/docs/models for the current list.

let zaiInstance = null;
let geminiInstance = null;

async function initZAI() {
  if (!zaiInstance) {
    zaiInstance = await ZAI.create();
    console.log('✅ z-ai SDK initialized');
  }
  return zaiInstance;
}

function initGemini() {
  if (!GoogleGenerativeAI) return null;
  if (!GEMINI_API_KEY) return null;
  if (!geminiInstance) {
    geminiInstance = new GoogleGenerativeAI(GEMINI_API_KEY);
    console.log('✅ Google Gemini SDK initialized (model: ' + GEMINI_MODEL + ')');
  }
  return geminiInstance;
}

function getActiveProvider() {
  if (GEMINI_API_KEY && GoogleGenerativeAI) return 'gemini';
  return 'z-ai';
}

// ===== Health Check =====
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: Date.now(),
    provider: getActiveProvider(),
    geminiAvailable: !!(GEMINI_API_KEY && GoogleGenerativeAI),
    geminiModel: GEMINI_MODEL,
  });
});

// ===== Speech-to-Text (z-ai ASR — Gemini does not have a cheaper STT path) =====
app.post('/api/transcribe', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    const zai = await initZAI();
    const audioFile = fs.readFileSync(req.file.path);
    const base64Audio = audioFile.toString('base64');

    console.log(`Transcribing audio: ${req.file.originalname} (${(audioFile.length / 1024).toFixed(1)} KB)`);

    const response = await zai.audio.asr.create({
      file_base64: base64Audio
    });

    fs.unlinkSync(req.file.path);

    const transcript = response.text || '';
    console.log(`Transcript: "${transcript.substring(0, 100)}..."`);

    res.json({
      success: true,
      transcript: transcript,
      wordCount: transcript.split(/\s+/).filter(w => w).length
    });
  } catch (error) {
    console.error('Transcription error:', error.message);
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ===== IELTS System Prompt (shared by both single + mock-test evaluations) =====
const IELTS_SYSTEM_PROMPT = `You are an experienced IELTS Speaking assessment assistant. You evaluate the candidate's spoken response according to the official IELTS Speaking assessment criteria.

Be objective, strict, accurate and educational.

Do NOT flatter the candidate or award unnecessarily high scores. Award high scores (7.0+) only when the response genuinely demonstrates the relevant band-descriptor qualities. Do NOT inflate a score simply because the answer is long.

Assess the response across the four official criteria:

1. Fluency and Coherence (FC)
   - Fluency and natural flow
   - Logical organisation of ideas
   - Use of linking words and cohesive devices
   - Unnecessary repetition
   - Hesitation and pauses (use audio metrics when provided)
   - Ability to develop and extend answers

2. Lexical Resource (LR)
   - Vocabulary range
   - Appropriate word choice
   - Collocations and natural expressions
   - Repetition of basic vocabulary
   - Incorrect or unnatural word usage
   - Concrete suggestions for better vocabulary

3. Grammatical Range and Accuracy (GRA)
   - Grammatical accuracy
   - Mix of simple and complex sentence structures
   - Tense consistency
   - Subject-verb agreement
   - Articles and prepositions
   - Sentence variety
   - Concrete grammatical mistakes with corrections and explanations

4. Pronunciation (PR)
   - Use the audio-analysis metrics provided (speaking rate, pauses, pitch variation, volume variation) as the basis for this assessment.
   - NEVER invent pronunciation specifics (individual sounds, word stress, intonation patterns) that you cannot actually hear.
   - If audio metrics are missing or insufficient, set the pronunciation band to null and clearly explain that pronunciation could not be reliably assessed from the transcript alone.
   - When audio metrics ARE available, comment on: rhythm and connected speech (from wordsPerMinute), hesitation (from totalPauses / pauseRatio), intonation range (from pitchRange), stress and emphasis (from volumeVariation).

OUTPUT FORMAT — STRICTLY a single JSON object. No markdown fences, no prose before or after. The JSON MUST match this schema exactly:

{
  "overallBand": <number 0-9 in 0.5 steps>,
  "criteria": {
    "fluency":          { "band": <number|null>, "explanation": "<string>", "strengths": [<string>...], "weaknesses": [<string>...], "improvements": [<string>...] },
    "lexicalResource":  { "band": <number|null>, "explanation": "<string>", "strengths": [<string>...], "weaknesses": [<string>...], "improvements": [<string>...] },
    "grammar":          { "band": <number|null>, "explanation": "<string>", "strengths": [<string>...], "weaknesses": [<string>...], "improvements": [<string>...] },
    "pronunciation":    { "band": <number|null>, "explanation": "<string>", "strengths": [<string>...], "weaknesses": [<string>...], "improvements": [<string>...] }
  },
  "grammarCorrections": [
    { "original": "<exact phrase from the candidate's transcript>", "corrected": "<natural IELTS-style rewrite>", "explanation": "<why this is wrong and how to fix it>", "naturalAlternative": "<a more native-sounding full-sentence rewrite>" }
  ],
  "vocabularyImprovements": [
    { "original": "<word/phrase the candidate used>", "suggested": "<better alternative>", "reason": "<why this is better>", "collocations": ["<common collocation 1>", "<common collocation 2>"], "exampleSentence": "<example using the suggested word>" }
  ],
  "fluencyFeedback": {
    "repetitions":        [<string>...],
    "hesitations":        [<string>...],
    "weakDevelopment":   [<string>...],
    "naturalAlternatives": [<string>...]
  },
  "pronunciationFeedback": {
    "assessedFromAudio": <true|false>,
    "summary": "<string>",
    "specificAreasForImprovement": [<string>...]
  },
  "improvementPlan": {
    "topWeaknesses":  [<string>...],
    "topStrengths":   [<string>...],
    "exercises":     [<string>...],
    "nextAnswerTips": [<string>...]
  },
  "overallFeedback": "<string>",
  "reliability": {
    "isReliable": <true|false>,
    "reasonIfUnreliable": "<string|null>"
  },
  "estimatedOfficialScore": "This is an AI-estimated practice score, not an official IELTS result."
}

RULES:
- If the response is too short (fewer than ~15 words of meaningful content), irrelevant, or unintelligible, set isReliable=false, provide band scores of null where appropriate, and explain why a reliable score cannot be given. Do NOT invent a score.
- Calculate overallBand as the AVERAGE of the four criterion band scores that are NOT null, rounded to the nearest 0.5. If all four are null, overallBand = null.
- Provide AT LEAST 2 grammarCorrections and AT LEAST 2 vocabularyImprovements when the response is reliable. If the response is grammatically perfect, say so explicitly in overallFeedback and provide empty arrays.
- For pronunciationFeedback.assessedFromAudio, set true ONLY when audioMetrics are provided in the user message AND contain at least wordsPerMinute and audioDurationSec. Otherwise set false and explain that pronunciation was not assessed from audio.
- All text MUST be in simple, clear English.
- Output ONLY the JSON. No \`\`\`json fences. No prose. No explanations outside the JSON.`;

// ===== Helper: call Gemini with structured-output JSON =====
async function callGemini(systemPrompt, userContent) {
  const genAI = initGemini();
  if (!genAI) throw new Error('Gemini SDK not initialized (no GEMINI_API_KEY)');

  const model = genAI.getGenerativeModel({
    model: GEMINI_MODEL,
    systemInstruction: systemPrompt,
    generationConfig: {
      temperature: 0.4,           // deterministic-ish; we want consistency for grading
      topP: 0.95,
      maxOutputTokens: 8192,
      responseMimeType: 'application/json',  // Gemini will return strict JSON
    },
  });

  // 90-second timeout via AbortController
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 90000);

  try {
    const result = await model.generateContent({
      contents: [{ role: 'user', parts: [{ text: userContent }] }],
    });
    const responseText = result.response.text();
    return responseText;
  } finally {
    clearTimeout(timeout);
  }
}

// ===== Helper: call z-ai LLM (existing fallback) =====
async function callZAI(systemPrompt, userContent) {
  const zai = await initZAI();
  const completion = await zai.chat.completions.create({
    messages: [
      { role: 'assistant', content: systemPrompt },
      { role: 'user', content: userContent }
    ],
    thinking: { type: 'disabled' }
  });
  return completion.choices[0]?.message?.content || '';
}

// ===== Helper: try to parse JSON robustly =====
function parseEvaluationJSON(text) {
  if (!text) throw new Error('Empty response from AI');
  // Try direct parse first
  try { return JSON.parse(text); } catch (e) {}
  // Try to extract JSON object from text (z-ai sometimes wraps in code fences)
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try { return JSON.parse(jsonMatch[0]); } catch (e) {}
  }
  throw new Error('Could not parse JSON from AI response');
}

// ===== Helper: validate evaluation schema (light-touch) =====
function validateEvaluation(ev) {
  if (!ev || typeof ev !== 'object') return false;
  // Required top-level keys
  if (!('criteria' in ev)) return false;
  // Each criterion should be an object (or null)
  const c = ev.criteria;
  if (!c || typeof c !== 'object') return false;
  // At least 2 of the 4 criteria should have a band number (or null explicitly)
  return true;
}

// ===== Helper: dispatch to active provider =====
async function evaluateWithActiveProvider(systemPrompt, userContent) {
  const provider = getActiveProvider();
  console.log(`→ Evaluating with provider: ${provider}`);
  let responseText;
  if (provider === 'gemini') {
    try {
      responseText = await callGemini(systemPrompt, userContent);
    } catch (geminiErr) {
      console.error('Gemini call failed, falling back to z-ai:', geminiErr.message);
      responseText = await callZAI(systemPrompt, userContent);
    }
  } else {
    responseText = await callZAI(systemPrompt, userContent);
  }
  return responseText;
}

// ===== IELTS Speaking Evaluation (single answer) =====
app.post('/api/evaluate', async (req, res) => {
  try {
    const { transcript, audioMetrics, questionText, questionPart, cueCardTitle, cueCardBullets } = req.body;

    if (!transcript || !transcript.trim()) {
      return res.status(400).json({ error: 'No transcript provided' });
    }

    const hasAudioMetrics = audioMetrics && (audioMetrics.wordsPerMinute != null || audioMetrics.audioDurationSec != null);

    let userContent = `Please evaluate the following IELTS Speaking answer.

QUESTION CONTEXT:
- Part: ${questionPart || 'Not specified'}
- Question/Cue Card: ${questionText || cueCardTitle || 'Not specified'}
${cueCardBullets && cueCardBullets.length ? `- Cue card bullets: ${cueCardBullets.join(', ')}` : ''}

CANDIDATE'S TRANSCRIPT (what they actually said):
"""
${transcript}
"""
`;

    if (hasAudioMetrics) {
      userContent += `
AUDIO ANALYSIS METRICS (from the recorded audio):
${JSON.stringify(audioMetrics, null, 2)}

These metrics include:
- wordsPerMinute: speaking rate (normal IELTS range is 100-150 WPM; too slow suggests hesitation, too fast suggests rushing)
- audioDurationSec: total recording duration
- volumeVariation: variation in volume (higher = more natural stress/rhythm)
- pitchRange: variation in pitch (higher = more natural intonation)
- wordCount: total words spoken

Use these metrics alongside the transcript to assess pronunciation, fluency, and natural delivery.
Set pronunciationFeedback.assessedFromAudio = true.
`;
    } else {
      userContent += `
AUDIO ANALYSIS METRICS: NOT AVAILABLE.
Set pronunciationFeedback.assessedFromAudio = false.
Explain that pronunciation could not be reliably assessed from the transcript alone, and set the pronunciation band to null.
`;
    }

    userContent += `
Respond with ONLY the JSON object described in your system instructions. No markdown fences, no prose.`;

    console.log('→ Evaluating single answer. Transcript length:', transcript.length, 'chars; audio metrics:', hasAudioMetrics ? 'yes' : 'no');

    const responseText = await evaluateWithActiveProvider(IELTS_SYSTEM_PROMPT, userContent);

    let evaluation;
    try {
      evaluation = parseEvaluationJSON(responseText);
      if (!validateEvaluation(evaluation)) {
        throw new Error('Schema validation failed');
      }
    } catch (parseError) {
      console.error('JSON parse error:', parseError.message);
      return res.json({
        success: true,
        evaluation: null,
        rawFeedback: responseText,
        error: 'Could not parse structured evaluation. Raw feedback provided.'
      });
    }

    console.log(`✓ Evaluation complete. Overall band: ${evaluation.overallBand}`);

    res.json({
      success: true,
      evaluation: evaluation,
      transcript: transcript,
      provider: getActiveProvider(),
      evaluatedAt: new Date().toISOString()
    });
  } catch (error) {
    console.error('Evaluation error:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ===== Full Mock Test Evaluation =====
app.post('/api/evaluate-mock-test', async (req, res) => {
  try {
    const { testSession } = req.body;

    if (!testSession || !testSession.answers || testSession.answers.length === 0) {
      return res.status(400).json({ error: 'No test session or answers provided' });
    }

    // Build a comprehensive summary of all answers
    let answersSummary = testSession.answers.map((ans, i) => {
      const am = ans.audioMetrics || {};
      return `--- Answer ${i + 1} (Part ${ans.part}) ---
Question: ${ans.questionText}
Transcript: "${ans.transcript}"
Audio Metrics: ${JSON.stringify(am)}
Duration: ${am.audioDurationSec || 'N/A'}s, WPM: ${am.wordsPerMinute || 'N/A'}
${ans.cueCardBullets ? 'Cue Card Bullets: ' + ans.cueCardBullets.join(', ') : ''}`;
    }).join('\n\n');

    const hasAnyAudioMetrics = testSession.answers.some(a => a.audioMetrics && (a.audioMetrics.wordsPerMinute != null || a.audioMetrics.audioDurationSec != null));

    const userContent = `Please evaluate this complete IELTS Speaking mock test holistically across all three parts.

TEST DETAILS:
- Test ID: ${testSession.testId}
- Date: ${testSession.date}
- Total answers: ${testSession.answers.length}
- Part 1 answers: ${testSession.answers.filter(a => a.part === 1).length}
- Part 2 answers: ${testSession.answers.filter(a => a.part === 2).length}
- Part 3 answers: ${testSession.answers.filter(a => a.part === 3).length}

CANDIDATE'S ANSWERS:
${answersSummary}

AUDIO ANALYSIS SUMMARY:
${hasAnyAudioMetrics
  ? 'Audio metrics are available for at least some answers. Use them to assess pronunciation. Set pronunciationFeedback.assessedFromAudio = true.'
  : 'Audio metrics are NOT available. Set pronunciationFeedback.assessedFromAudio = false and explain that pronunciation could not be reliably assessed.'}

The audioMetrics for each answer include:
- wordsPerMinute: speaking rate (normal IELTS: 100-150 WPM)
- audioDurationSec: how long they spoke
- volumeVariation: natural stress/rhythm variation
- pitchRange: intonation variation (higher = more natural)
- wordCount: total words spoken

EXTENDED OUTPUT FORMAT (mock test):
In addition to the schema in your system instructions, your JSON object MUST also include a top-level "partByPartAnalysis" key:
  "partByPartAnalysis": {
    "part1": { "band": <number|null>, "feedback": "<string>" },
    "part2": { "band": <number|null>, "feedback": "<string>" },
    "part3": { "band": <number|null>, "feedback": "<string>" }
  }

For grammarCorrections and vocabularyImprovements, include a "part" field (1, 2, or 3) indicating which answer the correction is from.

Calculate overallBand as the average of the four criterion scores (excluding nulls), rounded to the nearest 0.5. Provide specific examples from the candidate's actual answers.

Respond with ONLY the JSON object. No markdown, no prose.`;

    console.log(`→ Evaluating mock test with ${testSession.answers.length} answers...`);

    const responseText = await evaluateWithActiveProvider(IELTS_SYSTEM_PROMPT, userContent);

    let evaluation;
    try {
      evaluation = parseEvaluationJSON(responseText);
      if (!validateEvaluation(evaluation)) {
        throw new Error('Schema validation failed');
      }
    } catch (parseError) {
      console.error('JSON parse error:', parseError.message);
      return res.json({
        success: true,
        evaluation: null,
        rawFeedback: responseText,
        error: 'Could not parse structured evaluation. Raw feedback provided.'
      });
    }

    console.log(`✓ Mock test evaluation complete. Overall band: ${evaluation.overallBand}`);

    res.json({
      success: true,
      evaluation: evaluation,
      testId: testSession.testId,
      provider: getActiveProvider(),
      evaluatedAt: new Date().toISOString()
    });
  } catch (error) {
    console.error('Mock test evaluation error:', error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ===== Serve the main HTML file =====
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'download', 'TAREQ_IELTS_Speaking_Practice.html'));
});

// ===== Start server =====
initZAI().then(() => {
  if (GEMINI_API_KEY) initGemini();
  app.listen(PORT, () => {
    console.log(`\n🚀 TAREQ IELTS AI Server running on http://localhost:${PORT}`);
    console.log(`📄 Open http://localhost:${PORT} in your browser`);
    console.log(`🤖 Active AI provider: ${getActiveProvider().toUpperCase()}`);
    if (getActiveProvider() === 'gemini') {
      console.log(`   Gemini model: ${GEMINI_MODEL}`);
    } else {
      console.log(`   ⚠ GEMINI_API_KEY not set — using z-ai fallback.`);
      console.log(`   Set GEMINI_API_KEY to enable Google Gemini (recommended).`);
    }
    console.log(`📡 API endpoints:`);
    console.log(`   POST /api/transcribe           — Speech-to-text (z-ai ASR)`);
    console.log(`   POST /api/evaluate             — Single-answer IELTS evaluation`);
    console.log(`   POST /api/evaluate-mock-test   — Full mock-test evaluation`);
    console.log(`   GET  /api/health               — Health check + provider info\n`);
  });
}).catch(err => {
  console.error('Failed to initialize z-ai SDK:', err.message);
  process.exit(1);
});
