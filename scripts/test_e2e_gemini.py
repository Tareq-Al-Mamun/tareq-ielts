"""End-to-end test: user records an answer in Part 1 → Gemini auto-evaluates → result renders inline."""
import asyncio
import time
from playwright.async_api import async_playwright

HTML_PATH = "/home/z/my-project/download/TAREQ_IELTS_Speaking_Practice.html"

# Mock browser APIs (we don't actually record audio — we simulate the recording flow)
SETUP_JS = r"""
// Mock SpeechRecognition (live transcript)
class MockSR {
  constructor() { this.continuous=false; this.interimResults=false; this.lang='en-US'; this.onend=null; this.onresult=null; this.onerror=null; }
  start() {
    // Simulate live transcript coming in chunks
    const text = "Well I think my hometown is a really nice place to live. It is not too big and not too small. The people are friendly and there are many shops. I have lived there all my life and I really enjoy it.";
    const words = text.split(' ');
    let i = 0;
    this._interval = setInterval(() => {
      if (i >= words.length) { this.stop(); return; }
      const chunk = words.slice(0, i+5).join(' ');
      if (this.onresult) {
        const event = { resultIndex: 0, results: [{ 0: { transcript: chunk }, isFinal: i+5 >= words.length }] };
        this.onresult(event);
      }
      i += 5;
    }, 80);
  }
  stop() { if (this._interval) clearInterval(this._interval); setTimeout(() => { if (this.onend) this.onend(); }, 30); }
  abort() { this.stop(); }
}
window.SpeechRecognition = MockSR;
window.webkitSpeechRecognition = MockSR;

// Mock MediaRecorder + audio APIs
window.MediaRecorder = function(stream) {
  return {
    state: 'inactive',
    start() { this.state = 'recording'; },
    stop() {
      this.state = 'inactive';
      setTimeout(() => { if (this.onstop) this.onstop(); }, 50);
    },
    pause() { this.state = 'paused'; },
    resume() { this.state = 'recording'; },
    requestData() {},
    ondataavailable: null,
    onstop: null,
  };
};
Object.defineProperty(navigator, 'mediaDevices', {
  value: { getUserMedia: () => Promise.resolve({
    getAudioTracks: () => [{ stop: () => {}, getSettings: () => ({ sampleRate: 44100 }) }],
    getVideoTracks: () => [],
    stop: () => {},
  }) },
  configurable: true,
});

// Mock AudioContext
window.AudioContext = function() {
  return {
    createAnalyser: () => ({ frequencyBinCount: 1024, getByteTimeDomainData: () => {}, getByteFrequencyData: () => {} }),
    createMediaStreamSource: () => ({ connect: () => {} }),
    destination: {},
    close: () => Promise.resolve(),
  };
};
window.webkitAudioContext = window.AudioContext;

// Mock speechSynthesis — leave the real one alone, we'll just disable TTS after page load
// (the page's speak() function checks TTS.enabled and skips speechSynthesis.speak() if false)

// Stub IndexedDB
window.indexedDB = { open: () => { const r={}; setTimeout(()=>{ if(r.onsuccess) r.onsuccess({target:r}); }, 5); return r; } };
"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        await page.add_init_script(SETUP_JS)
        page.on("pageerror", lambda err: print(f"  [BROWSER ERROR] {err}"))
        await page.goto(f"file://{HTML_PATH}")
        await page.wait_for_timeout(2000)
        # Disable TTS so the page doesn't try to use real speechSynthesis (which would slow the test)
        await page.evaluate("TTS.enabled = false;")

        # Verify server is reachable from the page
        health = await page.evaluate("""async () => {
          try { const r = await fetch('http://localhost:3001/api/health'); return await r.json(); }
          catch(e) { return { error: e.message }; }
        }""")
        print(f"Server health from page: {health}")
        if not health.get('geminiAvailable'):
            print("⚠ Gemini not available — test cannot proceed")
            await browser.close()
            return False

        # Navigate to Part 1 page and select first topic
        await page.evaluate("showPage('part1')")
        await page.wait_for_timeout(300)
        await page.evaluate("""() => {
          if (typeof selectPart1Topic === 'function' && DATA.part1.length > 0) {
            selectPart1Topic(DATA.part1[0].num);
          }
        }""")
        await page.wait_for_timeout(500)

        # Click the "Record Answer" button on the first question card
        record_btn = await page.query_selector('.rec-btn.rec-start[data-rec-id]')
        if not record_btn:
            print("✗ Could not find Record Answer button")
            await browser.close()
            return False
        print("→ Clicking 'Record Answer' button...")
        await record_btn.click()
        await page.wait_for_timeout(3000)  # let the live transcript accumulate

        # Click Stop button
        stop_btn = await page.query_selector('.rec-btn[data-rec-act="stop"]:not([disabled])')
        if not stop_btn:
            # Try clicking the same record button (which toggles to stop)
            await record_btn.click()
            await page.wait_for_timeout(500)
        else:
            await stop_btn.click()
        print("→ Stopped recording. Auto-evaluation should kick in now...")

        # Wait for the loading animation to appear
        loading_appeared = False
        for _ in range(10):
            loading = await page.query_selector('.q-eval-result.eval-loading')
            if loading:
                loading_appeared = True
                break
            await page.wait_for_timeout(500)
        print(f"→ Loading state appeared: {loading_appeared}")

        # Wait for the evaluation to complete (real Gemini API call, ~20-40s)
        result_appeared = False
        for _ in range(60):
            result = await page.query_selector('.q-eval-result:not(.eval-loading):not(.eval-failed)')
            if result:
                # Make sure it has actual content (band number rendered)
                text = await result.text_content()
                if 'Band' in text or 'AI-Estimated' in text:
                    result_appeared = True
                    break
            await page.wait_for_timeout(2000)

        if not result_appeared:
            # Check if there's an error state
            error = await page.query_selector('.q-eval-result.eval-failed')
            if error:
                err_text = await error.text_content()
                print(f"✗ Evaluation errored: {err_text}")
                await browser.close()
                return False

        print(f"✓ Evaluation result rendered inline!")

        # Verify the structure of the rendered result
        result_info = await page.evaluate("""() => {
          const el = document.querySelector('.q-eval-result:not(.eval-loading):not(.eval-failed)');
          if (!el) return null;
          return {
            band: el.querySelector('.q-eval-band')?.textContent?.trim(),
            hasProviderBadge: !!el.querySelector('.provider-badge'),
            provider: el.querySelector('.provider-badge')?.textContent?.trim(),
            critCount: el.querySelectorAll('.q-eval-crit').length,
            hasToggle: !!el.querySelector('.q-eval-toggle'),
            hasRetryBtn: !!el.querySelector('[data-eval-retry]'),
          };
        }""")
        print(f"→ Result structure: {result_info}")

        # Open the detailed feedback
        await page.click('.q-eval-toggle')
        await page.wait_for_timeout(500)

        detail_info = await page.evaluate("""() => {
          const detail = document.querySelector('.q-eval-detail.open');
          if (!detail) return null;
          return {
            hasGrammarCorrections: !!detail.querySelector('.eval-grammar-card'),
            grammarCount: detail.querySelectorAll('.eval-grammar-card').length,
            hasVocabImprovements: !!detail.querySelector('.eval-vocab-card'),
            vocabCount: detail.querySelectorAll('.eval-vocab-card').length,
            hasImprovementPlan: !!detail.querySelector('.eval-improvement-plan'),
            hasFluencyFeedback: !!detail.querySelector('.eval-fluency-feedback'),
            hasPronFeedback: !!detail.querySelector('.eval-pron-feedback'),
          };
        }""")
        print(f"→ Detailed feedback: {detail_info}")

        # Check evaluation history page
        await page.evaluate("showPage('eval-history')")
        await page.wait_for_timeout(500)
        history_info = await page.evaluate("""() => {
          const items = document.querySelectorAll('.eval-history-item');
          return {
            itemCount: items.length,
            firstItemBand: items[0]?.querySelector('.ehi-band')?.textContent?.trim() || null,
            firstItemQ: items[0]?.querySelector('.ehi-q')?.textContent?.trim()?.slice(0, 60) || null,
          };
        }""")
        print(f"→ Evaluation History page: {history_info}")

        # Verify the evaluation was saved to localStorage
        saved = await page.evaluate("""() => {
          const s = JSON.parse(localStorage.getItem('tareq_ielts_v1') || '{}');
          return {
            evalHistoryCount: (s.evalHistory || []).length,
            hasFirstEval: !!(s.evalHistory && s.evalHistory[0] && s.evalHistory[0].evaluation),
          };
        }""")
        print(f"→ Saved to localStorage: {saved}")

        # All tests pass?
        all_pass = (
            loading_appeared and
            result_appeared and
            result_info and result_info['band'] and
            result_info['critCount'] == 4 and
            result_info['hasRetryBtn'] and
            detail_info and
            detail_info['hasImprovementPlan'] and
            history_info['itemCount'] >= 1 and
            saved['evalHistoryCount'] >= 1
        )
        print()
        print("=" * 60)
        print("E2E TEST " + "PASSED ✅" if all_pass else "FAILED ❌")
        print("=" * 60)

        await browser.close()
        return all_pass


if __name__ == '__main__':
    ok = asyncio.run(main())
    import sys
    sys.exit(0 if ok else 1)
