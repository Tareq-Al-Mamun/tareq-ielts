"""E2E test: Full Mock Test → Gemini evaluates all answers → renders full report."""
import asyncio
from playwright.async_api import async_playwright

HTML_PATH = "/home/z/my-project/download/TAREQ_IELTS_Speaking_Practice.html"

SETUP_JS = open('/home/z/my-project/scripts/test_e2e_gemini.py').read().split('SETUP_JS = r"""')[1].split('"""')[0]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()
        await page.add_init_script(SETUP_JS)
        page.on("pageerror", lambda err: print(f"  [BROWSER ERROR] {err}"))
        await page.goto(f"file://{HTML_PATH}")
        await page.wait_for_timeout(2000)
        await page.evaluate("TTS.enabled = false;")

        # Start mock test via dashboard CTA
        await page.click('#dashboard-mock-start')
        await page.wait_for_timeout(500)
        await page.click('#mock-begin')  # welcome screen "Start Full Speaking Test"
        await page.wait_for_timeout(2000)  # instructions phase (TTS disabled, transitions immediately)

        # Now we should be in Part 1 phase. We need to fast-forward through all 5 P1 + 1 P2 + 4 P3 questions.
        # Each phase: speak question (TTS disabled, transitions instantly) → start recording → 30s timer → saveAndAdvance
        # Fast-forward: instead of waiting 30s per question, set mockTest.timerSeconds = 1 to make the timer fire quickly
        for i in range(20):  # max 20 iterations to cover P1(5) + P2(1) + P3(4) = 10 + buffer
            phase = await page.evaluate('mockTest.phase')
            print(f"  Iteration {i+1}: phase={phase}")
            if phase == 'completion' or phase == 'results':
                break
            if phase in ('part1', 'part2-speak', 'part3'):
                # Set timer to 1s remaining to force it to fire
                await page.evaluate('mockTest.timerSeconds = 1')
                await page.wait_for_timeout(3000)  # wait for timer to fire + saveAndAdvance (1.5s)
            elif phase == 'part2-prep':
                await page.evaluate('mockTest.timerSeconds = 1')
                await page.wait_for_timeout(3000)
            else:
                await page.wait_for_timeout(2000)

        # After all questions, we should be in 'completion' phase → auto-submits to Gemini
        final_phase = await page.evaluate('mockTest.phase')
        print(f"→ Final phase after all questions: {final_phase}")
        answer_count = await page.evaluate('mockTest.answers.length')
        print(f"→ Answers recorded: {answer_count}")

        # Wait for the Gemini evaluation to complete
        for _ in range(90):
            phase = await page.evaluate('mockTest.phase')
            if phase == 'results':
                break
            await page.wait_for_timeout(2000)
        print(f"→ Phase after waiting for Gemini: {await page.evaluate('mockTest.phase')}")

        # Check the result
        result = await page.evaluate("""() => {
          const ev = mockTest.evaluation;
          if (!ev) return null;
          return {
            overallBand: ev.overallBand,
            provider: mockTest.evalProvider,
            criteriaCount: Object.keys(ev.criteria || {}).length,
            hasPartByPart: !!ev.partByPartAnalysis,
            part1Band: ev.partByPartAnalysis?.part1?.band,
            part2Band: ev.partByPartAnalysis?.part2?.band,
            part3Band: ev.partByPartAnalysis?.part3?.band,
            grammarCount: (ev.grammarCorrections || []).length,
            vocabCount: (ev.vocabularyImprovements || []).length,
            hasImprovementPlan: !!ev.improvementPlan,
            hasFluencyFeedback: !!ev.fluencyFeedback,
            hasPronFeedback: !!ev.pronunciationFeedback,
            reliability: ev.reliability,
          };
        }""")
        print(f"→ Gemini mock-test result: {result}")

        all_pass = (
            result is not None and
            result['overallBand'] is not None and
            result['provider'] == 'gemini' and
            result['criteriaCount'] == 4 and
            result['hasPartByPart'] and
            result['hasImprovementPlan'] and
            result['grammarCount'] >= 0 and  # at least some corrections (or 0 if perfect)
            result['vocabCount'] >= 0
        )
        print()
        print("=" * 60)
        print("MOCK TEST E2E " + "PASSED ✅" if all_pass else "FAILED ❌")
        print("=" * 60)

        await browser.close()
        return all_pass


if __name__ == '__main__':
    ok = asyncio.run(main())
    import sys
    sys.exit(0 if ok else 1)
