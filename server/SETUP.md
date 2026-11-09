# TAREQ IELTS — Gemini AI Evaluation Setup Guide

This guide explains how to set up and run the Gemini-powered IELTS Speaking evaluation system that has been integrated into your existing TAREQ IELTS website.

---

## 📋 What was implemented

### Backend (server/server.js)
- Added **Google Gemini SDK** (`@google/generative-ai`) integration
- Added **dotenv** for loading `GEMINI_API_KEY` from `.env`
- The server uses **Gemini** when `GEMINI_API_KEY` is set, falling back to **z-ai SDK** otherwise
- New `/api/health` returns `{provider: "gemini" | "z-ai", geminiAvailable, geminiModel}`
- `/api/evaluate` (single answer) — sends transcript + audio metrics to Gemini with a strict IELTS evaluation prompt
- `/api/evaluate-mock-test` (full mock test) — sends all answers across Part 1/2/3 to Gemini with extended prompt
- Structured JSON output schema enforced via `responseMimeType: 'application/json'`
- 90-second timeout for single evaluations, 180-second for mock tests
- Comprehensive error handling, schema validation, JSON-parsing fallback

### Frontend (download/TAREQ_IELTS_Speaking_Practice.html)
- **Auto-evaluation**: After each Part 1/2/3 recording stops, the transcript + audio metrics are automatically sent to Gemini. No "Submit Evaluation" button needed for individual questions.
- **Inline evaluation result block** appears inside each question card showing:
  - Overall band score (with color-coded badge: green/blue/orange)
  - Provider badge ("gemini" or "z-ai")
  - 4-criteria row (FC, LR, GRA, PR)
  - Expandable "Show detailed feedback" section
  - Grammar corrections with original → corrected + natural alternative
  - Vocabulary improvements with collocations + example sentences
  - Fluency feedback (repetition, hesitation, weak development, natural alternatives)
  - Pronunciation feedback (only when audio metrics available; otherwise explicitly says "not assessed")
  - Personalised improvement plan (top weaknesses, top strengths, exercises, next-answer tips)
  - Retry button
- **Loading animation**: Three bouncing dots with "🤖 Analysing your speaking performance with Gemini AI…" message
- **Retry button**: On failure, recording + transcript preserved; user can retry evaluation
- **Evaluation History page** (new sidebar nav item "📈 Evaluation History"):
  - Summary stats (total evaluations, average band, best band)
  - Each item: band badge, question text, provider, date, criteria scores
  - View button (opens the question and scrolls to the inline eval)
  - Delete button (per-item or clear-all)
  - Data storage explanation (localStorage + IndexedDB, only transcript sent to Gemini)
- **Mock test evaluation**: After Part 3 completes, full test auto-submits to Gemini; loading screen shows "Analysing your speaking performance..." with bouncing dots; results page includes all the new fields (improvement plan, fluency/pronunciation feedback, grammar cards with natural alternatives, vocab cards with collocations, provider badge, reliability warning if answers are too short)
- **Restore on revisit**: When user navigates back to a previously-evaluated question, the inline evaluation block is automatically restored

---

## 🔑 How to get a Gemini API key

1. Visit **https://aistudio.google.com/app/apikey**
2. Sign in with a Google account
3. Click **"Create API Key"**
4. Choose a project (or create a new one)
5. Copy the key (starts with `AIza...` or `AQ.Ab...`)

The free tier gives generous limits suitable for individual IELTS practice (rate-limited but enough for personal use).

---

## ⚙️ Where to configure GEMINI_API_KEY

The key is stored in **`server/.env`** (gitignored). The file looks like:
```
GEMINI_API_KEY=your-key-here
```

**The `.env` file is already created and your key is already in it.** (Done during setup.)

To change the key later, edit `server/.env` and restart the server.

---

## 🚀 How to start the backend

Open a terminal and run:

```bash
cd /home/z/my-project/server
npm install        # installs all dependencies (dotenv, @google/generative-ai, express, etc.)
npm start          # starts the server on http://localhost:3001
```

You should see:
```
✅ z-ai SDK initialized
✅ Google Gemini SDK initialized (model: gemini-1.5-flash)

🚀 TAREQ IELTS AI Server running on http://localhost:3001
🤖 Active AI provider: GEMINI
   Gemini model: gemini-1.5-flash
```

The server stays running. Keep this terminal open while you use the website.

---

## 🌐 How to open the website

### Option A — Open via the backend (recommended)
Visit **http://localhost:3001** in your browser. The server serves the HTML file directly, so it's the same origin as the API.

### Option B — Open the HTML file directly
Double-click `/home/z/my-project/download/TAREQ_IELTS_Speaking_Practice.html` to open it in a browser. The frontend automatically connects to `http://localhost:3001` for API calls.

---

## 🧪 How to verify it's working

1. **Open the website** (either option above)
2. **Sidebar** → click "AI Evaluation". The badge should say **"● AI Server Online"**
3. **Sidebar** → click "Speaking Part 1" → pick any topic → click "🎙 Record Answer" on any question → speak → click "⏹ Stop"
4. Within ~30 seconds, you should see the **inline evaluation block** appear below the question with:
   - Band badge (e.g. 6.5)
   - "gemini" provider badge
   - 4 criteria scores
   - "Show detailed feedback" toggle

---

## 📁 Files created/modified

| File | Status | Purpose |
|---|---|---|
| `server/server.js` | Modified | Added Gemini SDK + dotenv + structured prompts |
| `server/package.json` | Modified | Added `@google/generative-ai` + `dotenv` dependencies |
| `server/.env` | Created (gitignored) | Stores `GEMINI_API_KEY` |
| `server/.gitignore` | Created | Prevents `.env` from being committed |
| `scripts/build_html.py` | Modified | Added auto-eval, inline rendering, history page, CSS |
| `download/TAREQ_IELTS_Speaking_Practice.html` | Rebuilt | The final website (1.25 MB) |
| `scripts/start_server.sh` | Created | Helper script to start server detached |
| `scripts/test_e2e_gemini.py` | Created | E2E test: single-answer evaluation |
| `scripts/test_mock_e2e.py` | Created | E2E test: full mock-test evaluation |

---

## 💰 Cost control

- Uses **`gemini-1.5-flash`** (cheapest model with reliable JSON output)
- Sends **only the transcript + audio metrics** (not the audio file itself) — keeps request size tiny (~1KB per answer)
- Evaluations are saved in localStorage — **no re-evaluation** unless user clicks Retry
- Mock test sends all answers in a single Gemini call (instead of one call per question)
- The free tier of Gemini is sufficient for individual practice

To switch to the higher-quality (more expensive) model, edit `server/server.js`:
```js
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-1.5-pro';  // was 'gemini-1.5-flash'
```

Or set the `GEMINI_MODEL` env var: `GEMINI_MODEL=gemini-1.5-pro npm start`

---

## 🔒 Security

- ✅ API key is stored in `server/.env` (never in HTML/JS)
- ✅ `.env` is in `.gitignore` (won't be committed)
- ✅ Frontend never sees the API key — all Gemini calls go through the backend
- ✅ Only transcript + audio metrics are sent to Gemini (not the audio file)
- ✅ Audio recordings stay in your browser's IndexedDB

---

## 🧪 Tests performed

| Test | Result |
|---|---|
| Server starts cleanly with Gemini | ✅ PASS |
| `/api/health` returns `provider: "gemini"` | ✅ PASS |
| Single-answer evaluation (curl + real Gemini API) | ✅ PASS — overall band 6.5, all 4 criteria, 2 grammar corrections, 2 vocab improvements, full improvement plan |
| E2E single-answer (Playwright: record → stop → auto-eval → inline render) | ✅ PASS |
| E2E Full Mock Test (10 answers → Gemini → full report) | ✅ PASS — band 3.0, part-by-part analysis, all feedback sections |
| Dashboard banner tests (regression) | ✅ 15/15 PASS |
| Mock-test bug-fix tests (regression) | ✅ 10/10 PASS |
| Strict practice timer tests (regression) | ✅ 4/4 PASS |

---

## ❓ Troubleshooting

**"AI Server Offline" badge in the website**
→ The backend server isn't running. Open a terminal and run `cd /home/z/my-project/server && npm start`

**"provider": "z-ai"** instead of "gemini" in /api/health
→ The `GEMINI_API_KEY` is not being loaded. Verify `server/.env` exists and contains `GEMINI_API_KEY=...` (no quotes, no spaces around `=`)

**Evaluation fails with 500 error**
→ Check the server console log for the actual error. Common causes: invalid API key, rate limit exceeded (free tier), network issue. The frontend shows a Retry button.

**Evaluation takes too long**
→ Gemini single-answer evaluations take ~15–30s; mock tests take ~30–60s. If it consistently times out, switch to a faster network or use `gemini-1.5-flash` (the default).

**The band score seems too low / too high**
→ Gemini evaluates based on the actual transcript quality. Off-topic, short, or grammatically poor answers correctly receive low scores. This is intentional — Gemini does NOT inflate scores.
