#!/usr/bin/env python3
"""
Extract Part 1, Part 2 (cue cards) and Part 3 (follow-ups) from the Makkar IELTS PDF text.
Output: /home/z/my-project/scripts/data.json
"""
import json
import re
import unicodedata

SRC = "/home/z/my-project/scripts/makkar_full.txt"

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

# ---------- ligature / OCR cleanup ----------
LIG = {
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬆ": "st",
    "ﬅ": "st",
}
def fix_lig(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s

# Common OCR substitutions seen in this PDF (mostly fi->fi in 'time', 'often' etc.)
# We only apply SAFE whole-word replacements to avoid corrupting other text.
WORD_FIXES = {
    "bme": "time", "Bme": "Time",
    "ken": "often", "oken": "often", "Oken": "Often",
    "sbll": "still", "Sbll": "Still",
    "leners": "letters", "Leners": "Letters",
    "wrinen": "written", "handwrinen": "handwritten",
    "meebng": "meeting", "meebngs": "meetings",
    "condibons": "conditions",
    "adverbsement": "advertisement", "adverbsements": "advertisements",
    "adverbsing": "advertising",
    "planbng": "planting",
    "favouri te": "favourite", "favourive": "favourite",
    "quesbons": "questions", "Quesbons": "Questions",
    "excibng": "exciting", "exciEng": "exciting",
    "waiEng": "waiting", "noEced": "noticed", "graEtude": "gratitude",
    "saEsfacEon": "satisfaction", "saEsfied": "satisfied",
    "diﬀerent": "different", "diﬀerence": "difference", "diﬀerently": "differently",
    "pref er": "prefer",
    "every day": "every day",
    "celeberity": "celebrity", "Celeberity": "Celebrity",
    "craks": "crafts", "crak": "craft",
    "okice": "office",
    "Ema": "time",
    "Emes": "times",
    "Eme": "time",
    "aRend": "attend", "aRended": "attended",
    "encourE": "encourage",
    "ﬁrst": "first",
}

def clean(s):
    s = fix_lig(s)
    # normalize unicode (NFKC) — converts ﬁ etc. already done above + smart quotes
    s = unicodedata.normalize("NFKC", s)
    # smart quotes / dashes
    repl = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u00a0": " ",
        "\ufb01": "fi", "\ufb02": "fl",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    # word-level fixes
    def wrep(m):
        w = m.group(0)
        return WORD_FIXES.get(w, w)
    s = re.sub(r"\b\w+\b", wrep, s)
    # collapse whitespace
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

text = clean(raw)
lines = text.split("\n")

# ---------- split into the two main regions ----------
# Part 2 cue cards: lines 50 .. ~14838
# Part 1 intro: from "SPEAKING PART 1 / INTRO QUESTIONS" around line 14839 to end
# Find the ACTUAL Part 1 section header in the body (not the TOC entry, which has ".... 346" after it).
# The body header is a standalone line "SPEAKING PART 1" followed soon by "INTRO QUESTIONS",
# WITHOUT trailing dots / page number.
p1_start = None
candidates = []
for i, ln in enumerate(lines):
    s = ln.strip()
    if s == "SPEAKING PART 1" or s.startswith("SPEAKING PART 1"):
        candidates.append(i)
# pick the candidate with no dots in the line
body_candidates = [i for i in candidates if "..." not in lines[i] and "…." not in lines[i]]
if body_candidates:
    p1_start = body_candidates[-1]  # last one is the body header
else:
    p1_start = candidates[-1] if candidates else 0
print("Part 1 starts at line", p1_start, ":", repr(lines[p1_start]))

part2_lines = lines[:p1_start]
part1_lines = lines[p1_start:]

# Save cleaned text for inspection
with open("/home/z/my-project/scripts/makkar_clean.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ===================================================================
# PART 2 — CUE CARDS  (rewritten robust parser)
# ===================================================================
# Header:  <num>. Describe ... / <num>. Talk about ...
# Title can span multiple lines (until "You should say" or until the first bullet line)
# Bullets: lines beginning with "-", "•", or short indented lines right after the title
#   Stop collecting bullets when we hit a "¥" / "•" sample-answer line, or "Or", or "Part 3"
# Part 3 follow-ups: find a line containing "Part 3" and "Follow"; collect numbered questions
#   OR paragraph-style questions until next cue card header / end of cue card block

header_re = re.compile(r"^\s{0,8}(\d{1,3})\.\s+(Describe|Talk about)\b\s*(.*)$", re.IGNORECASE)
ys_re = re.compile(r"you should say\s*:?\s*$", re.IGNORECASE)
# Bullets in cue cards use "-" or "o " (lowercase letter o followed by space) in this PDF.
# "•" is used by sample-answer paragraphs in this PDF, NOT as a bullet marker.
bullet_re = re.compile(r"^\s{0,4}(?:[-]|o\s+)\s*(.+)$")
bullet_re_ml = re.compile(r"^\s{0,4}(?:[-]|o\s+)\s*(.+)$", re.MULTILINE)
qnum_re = re.compile(r"^\s{0,12}(\d{1,2})[\.\)]\s+(.+)$")
# Part 3 markers — strict ("Part 3 ... Follow"), loose ("Part 3"), and "Follow up(s) Questions"
part3_re = re.compile(r"Part\s*3[\s\-–:]*\s*(Follow[\s\-]*[Uu]p|Follow\s*Up)\s*Q", re.IGNORECASE)
part3_loose_re = re.compile(r"Part\s*3\b", re.IGNORECASE)
# Match standalone "Follow up Questions" / "Follow ups" / "Follow Up Questions"
followups_header_re = re.compile(r"^\s*Follow[\s\-]*[Uu]ps?\s*:?\s*$|^\s*Follow[\s\-]*[Uu]p\s+Questions?\s*:?\s*$", re.IGNORECASE)

def is_ad_line(s):
    sl = s.lower()
    AD_MARKERS = [
        "makkarielts","instagram.com","youtube.com","www.makkar",
        "study abroad","visa guidance","office & coaching","call/whatsapp","call / whatsapp",
        "office and coaching","expertise you can see","straight answers","visa approved",
        "visa application check","real student outcomes","get your profile","discuss your",
        "ask about","start your","book your","aim for","planning germany","curious about",
        "italy scholarships","canada plans","schengen visa","student visa (canada",
        "one book.","we don't sell courses","the makkar way","visa 360",
        "study visa exclusive","students exclusive","visitor visa/parent","money transfer",
        "flight booking","travel planning","departure","documentation","application support",
        "process guidance","use official","visa approved","profile discussion",
        "circle your answer","flights / hotels","gic / block","ielts / pte","pte / toefl",
        "what's your next","are you stuck","be honest","why do students","planning a family",
        "what students say","our services","our offices","our approach","makkar ielts books",
        "study loan","ielts / pte /","visa 360","ielts • pte","complete and honest",
        "choose makkarielts","get free counselling","follow us on instagram",
        "list of books shops",
        # ad footer phrases from cue cards
        "call us today","step into our office","without stress","step-by-step guidance",
        "afraid of visa refusal","want experts to check","one small mistake can lead",
        "follow for visa tips","our offices & coaching",
        "looking for the lowest","safe transfer","get free guidance",
        "still stuck at","time to level up","call us today or follow",
        # additional ad phrases seen in cue-card sample-answer regions
        "what's your","what do you need","where do you want to go",
        "this ielts book","plan what comes after","simple question can start",
        "circle your answer","office & coaching centre","office and coaching centre",
        "office & coaching","office and coaching",
        "o n e","v i s i t o r","s t u d y","w h y","r e a l","v i s a","w h a t",
        "g e r m a n y","i e l t s","p t e","c e l p i p","u s a","u k","a u s",
        "j a p a n","n e w","e u r o p e","b r i n g","g e t","a s k","b o o k",
        "a i m","p l a n n i n g","c u r i o u s","t h e","s u c c e s s",
        "c a n a d a","v i s i t o r","s t u d y","i e l t s  o v e r a l l",
        "y o u r","a u s t r a l i a","s u b c l a s s","r e a l",
        "u s a","f 1 s t u d e n t","s c h e n g e n","b a v",
        "✈","✅","✓","✔","\u2713","\u2714","✓ ","○",
    ]
    for m in AD_MARKERS:
        if m in sl:
            return True
    # short ALL-CAPS marketing posters
    if len(s) < 80 and s == s.upper() and any(c.isalpha() for c in s) and "  " in s:
        return True
    # ad-style fragments: lines containing " . " or " / " with mixed ad-like content
    if (" . " in s and " / " in s) or (" . -" in s) or (" . /" in s):
        return True
    # Phone numbers (8360957299 etc.) are strong ad indicators
    if re.search(r"\b\d{10}\b", s) or re.search(r"\b\d{3}\s\d{3}\s\d{4}\b", s):
        return True
    return False

# Find cue card headers (body only — not TOC entries)
# A TOC entry has dots anywhere in itself OR in the next 8 lines (the title wraps with dots)
cue_headers = []
for i, ln in enumerate(part2_lines):
    m = header_re.match(ln)
    if not m:
        continue
    if "....." in ln or "…." in ln:
        continue
    # check if any continuation line (next 8 lines) has TOC dots BEFORE "You should say"
    is_toc = False
    for k in range(i+1, min(i+8, len(part2_lines))):
        cln = part2_lines[k]
        if "You should say" in cln or "you should say" in cln.lower():
            break
        if "....." in cln or "…." in cln:
            is_toc = True
            break
        # if next line is another "<num>. Describe" -> also TOC
        if re.match(r"^\s*\d{1,3}\.\s+(Describe|Talk about)\b", cln, re.IGNORECASE):
            is_toc = True
            break
    if is_toc:
        continue
    # also reject lines that end with a page number
    if re.search(r"\s\d{1,3}\s*$", ln):
        continue
    num = int(m.group(1))
    if num < 1 or num > 148:
        continue
    title_first = (m.group(2) + " " + m.group(3)).strip()
    # require some cue-card-like content within next 12 lines
    window = "\n".join(part2_lines[i:i+12])
    if "You should say" in window or bullet_re_ml.search(window) or part3_loose_re.search(window):
        cue_headers.append((i, num, title_first))

# Deduplicate by number, keeping first occurrence
seen_nums = {}
unique_headers = []
for (i, num, title_first) in cue_headers:
    if num in seen_nums:
        continue
    seen_nums[num] = True
    unique_headers.append((i, num, title_first))
unique_headers.sort(key=lambda x: x[0])
print(f"Found {len(unique_headers)} cue card headers")

cue_cards = []
for idx, (start_i, num, title_first) in enumerate(unique_headers):
    end_i = unique_headers[idx+1][0] if idx+1 < len(unique_headers) else len(part2_lines)
    block = part2_lines[start_i:end_i]

    # ---- title: collect until "You should say" or first bullet or "Part 3"
    title_parts = [title_first]
    title_done = False
    ys_at = None
    bullet_start = None
    for j in range(1, min(8, len(block))):
        ln = block[j].rstrip()
        s = ln.strip()
        if not s:
            continue
        if ys_re.match(s):
            ys_at = j
            title_done = True
            break
        if bullet_re.match(ln):
            bullet_start = j
            title_done = True
            break
        if part3_re.search(s):
            title_done = True
            break
        if s.startswith("¥") or s.startswith("•\u200b"):
            title_done = True
            break
        # continuation of title
        title_parts.append(s)
        if j > 6:
            break
    title = " ".join(title_parts).strip()
    # normalise whitespace
    title = re.sub(r"\s+", " ", title)

    # ---- bullets
    bullets = []
    bullet_begin = ys_at + 1 if ys_at is not None else (bullet_start if bullet_start is not None else None)
    bullets_end = None  # track where bullets ended (for sample-answer scanning)
    if bullet_begin is not None:
        k = bullet_begin
        while k < len(block):
            ln = block[k].rstrip()
            s = ln.strip()
            if not s:
                # allow one blank line; if next is also non-bullet, stop
                k += 1
                continue
            # stop on sample answer markers (¥, •, •\u200b)
            if s.startswith("¥") or s.startswith("•") or s.startswith("\u2022"):
                break
            if s.lower() == "or" or s == "Or":
                break
            if part3_re.search(s):
                break
            if is_ad_line(s):
                k += 1
                continue
            bm = bullet_re.match(ln)
            if bm:
                btext = bm.group(1).strip()
                # if this bullet text is a full sentence (ends with "."), it's a sample-answer paragraph
                if btext.endswith(".") and len(btext) > 30:
                    break
                bullets.append(btext)
                bullets_end = k
                k += 1
                continue
            # plain bullet line (no - prefix): accept if short & not a sample-answer sentence
            if len(s) < 120 and not s.endswith("."):
                # treat as bullet
                bullets.append(s)
                bullets_end = k
                k += 1
                continue
            # otherwise this is a sample answer paragraph (full sentence) -> stop
            break

    # ---- Sample answer(s)
    # The sample answer is the body of paragraphs marked with ¥ or • that appear AFTER the bullets
    # and BEFORE the Part 3 follow-ups. Multiple sample answers can be separated by "Or".
    sample_answers = []
    if bullets_end is not None or ys_at is not None:
        scan_start = (bullets_end + 1) if bullets_end is not None else (ys_at + 1 if ys_at is not None else 0)
        # find the end of the sample answer section (start of Part 3, or next cue card header)
        sample_end = len(block)
        for j in range(scan_start, len(block)):
            ln = block[j].strip()
            if part3_re.search(ln) or part3_loose_re.search(ln) or followups_header_re.match(ln):
                sample_end = j
                break
            # also stop at next "You should say" (shouldn't happen, but defensive)
            if ys_re.match(ln) and j > (ys_at or 0) + 5:
                sample_end = j
                break
        # collect paragraphs from scan_start to sample_end
        # Strategy: split into "answer blocks" — each answer block starts when we see a ¥/• marker
        # AFTER a blank line (or after "Or"). Consecutive ¥/• lines (no blank between) belong to the same answer.
        # Lines WITHOUT ¥/• markers that appear after a blank line and aren't a continuation of a
        # ¥-marked paragraph are likely ad text — skip them.
        current_answer_lines = []
        answers_found = []
        prev_was_blank = True
        saw_marker_in_current_block = False
        prev_answer_text = ""  # text of the most recently flushed answer (for continuation heuristic)
        for j in range(scan_start, sample_end):
            ln = block[j]
            s = ln.strip()
            if not s:
                if current_answer_lines:
                    prev_answer_text = " ".join(current_answer_lines)
                    answers_found.append(prev_answer_text)
                    current_answer_lines = []
                prev_was_blank = True
                saw_marker_in_current_block = False
                continue
            # skip ad lines (these often appear in the middle of sample answer sections
            # as full-page marketing breaks)
            if is_ad_line(s):
                continue
            # detect "Or" separator (alternative answer)
            if s.lower() == "or" or s == "Or":
                if current_answer_lines:
                    prev_answer_text = " ".join(current_answer_lines)
                    answers_found.append(prev_answer_text)
                    current_answer_lines = []
                prev_was_blank = True
                saw_marker_in_current_block = False
                # reset prev_answer_text so a continuation check doesn't merge across "Or"
                prev_answer_text = ""
                continue
            # strip the ¥ or • prefix if present
            has_marker = s.startswith("¥") or s.startswith("•") or s.startswith("\u2022")
            cleaned = re.sub(r"^[¥•\u2022\u00b7]\s*", "", s).strip()
            if not cleaned:
                continue
            if has_marker:
                if prev_was_blank:
                    # Check if this is the start of a new answer or continuation of the previous one.
                    # Heuristic: if the previous answer was short (< 800 chars) AND this new ¥ paragraph
                    # starts with a continuation word ("We", "After", "Then", "When", "He", "She",
                    # "The", "It", "But", "So", pronoun, etc.) AND there was no "Or" separator,
                    # treat it as a continuation of the previous answer.
                    cont_starters = ("we ","after ","then ","when ","he ","she ","the ","it ","but ","so ",
                                      "they ","finally ","later ","soon ","upon ","within ","in ",
                                      "later ","still ","actually ","overall ","although ","however ")
                    if (current_answer_lines and prev_answer_text
                            and len(prev_answer_text) < 1000
                            and cleaned.lower().startswith(cont_starters)):
                        # continuation of previous answer
                        current_answer_lines.append(cleaned)
                    else:
                        # start a new answer block
                        if current_answer_lines:
                            prev_answer_text = " ".join(current_answer_lines)
                            answers_found.append(prev_answer_text)
                            current_answer_lines = []
                        current_answer_lines.append(cleaned)
                        saw_marker_in_current_block = True
                else:
                    # consecutive ¥ line — same answer block (multi-line answer)
                    current_answer_lines.append(cleaned)
                prev_was_blank = False
            else:
                # No marker
                if saw_marker_in_current_block and not prev_was_blank:
                    # continuation of the previous ¥-marked paragraph
                    current_answer_lines.append(cleaned)
                elif saw_marker_in_current_block and prev_was_blank:
                    # a new paragraph in the same answer (no marker) — only accept if it looks
                    # like a sentence continuation (capital letter, sentence-like)
                    if len(s) > 30 and (s.endswith(".") or s.endswith(",") or s.endswith(";")):
                        current_answer_lines.append(cleaned)
                        prev_was_blank = False
                    # otherwise skip (likely an ad line that slipped through is_ad_line)
                else:
                    # No marker yet — could be the first paragraph of an answer with no marker
                    # only accept if it looks like a sentence AND the next non-blank line continues the same thought
                    if len(s) > 30 and (s.endswith(".") or s.endswith(",") or s.endswith(";")):
                        current_answer_lines.append(cleaned)
                        saw_marker_in_current_block = True
                        prev_was_blank = False
        if current_answer_lines:
            prev_answer_text = " ".join(current_answer_lines)
            answers_found.append(prev_answer_text)
        # filter out junk / empty / ad-only answers
        for ans in answers_found:
            ans = ans.strip()
            # require the answer to be substantive (>50 chars) and not contain too much ad content
            if len(ans) > 50 and not is_ad_line(ans):
                # reject answers that contain URLs or phone numbers (signs of ad pollution)
                ans_lower = ans.lower()
                if "https://" in ans_lower or "http://" in ans_lower or "www." in ans_lower:
                    continue
                if re.search(r"\b\d{10}\b", ans):
                    continue
                # reject answers with too many ad phrases — but use specific URL-style markers
                # (the word "instagram" alone in a normal sentence is fine)
                ad_score = 0
                if "makkarielts" in ans_lower: ad_score += 1
                if "phagwara" in ans_lower and "jalandhar" in ans_lower: ad_score += 1
                if "study abroad" in ans_lower and "visa" in ans_lower: ad_score += 1
                if "office & coaching" in ans_lower: ad_score += 1
                if "8360957299" in ans or "9888195776" in ans or "9560820208" in ans: ad_score += 1
                if ad_score >= 2:
                    continue
                sample_answers.append(ans)
    # Dedupe identical answers (sometimes the same answer gets captured twice)
    seen_ans = set()
    deduped_answers = []
    for ans in sample_answers:
        key = ans[:200]
        if key not in seen_ans:
            seen_ans.add(key)
            deduped_answers.append(ans)
    sample_answers = deduped_answers

    # ---- Part 3 follow-ups
    p3_qs = []
    p3_start = None
    # First try the strict "Part 3 ... Follow" marker
    for j, ln in enumerate(block):
        if ys_at is not None and j <= ys_at:
            continue
        if part3_re.search(ln):
            p3_start = j
            break
    # Fallback 1: any "Part 3" mention (even without "Follow")
    if p3_start is None:
        for j, ln in enumerate(block):
            if ys_at is not None and j <= ys_at:
                continue
            if part3_loose_re.search(ln) and not is_ad_line(ln):
                if len(ln.strip()) < 80:
                    p3_start = j
                    break
    # Fallback 2: standalone "Follow up Questions" / "Follow ups" header
    if p3_start is None:
        for j, ln in enumerate(block):
            if ys_at is not None and j <= ys_at:
                continue
            if followups_header_re.match(ln.strip()):
                p3_start = j
                break
    # Last fallback: if still no marker, look for the FIRST question line (numbered "1. ...?" OR
    # a paragraph-style question ending with "?") that appears AFTER the cue card bullets.
    if p3_start is None:
        # Determine where to start scanning: after the bullets
        scan_from = (ys_at + 1) if ys_at is not None else 1
        if bullets and ys_at is not None:
            # find the last bullet position in the block
            last_bullet_pos = ys_at + 1
            for j in range(ys_at + 1, len(block)):
                if bullet_re.match(block[j]):
                    last_bullet_pos = j
                elif block[j].strip() and last_bullet_pos > ys_at:
                    break
            scan_from = last_bullet_pos + 1
        # Now scan for the first question line — numbered "1. ...?" OR paragraph-style
        # short line ending with "?" that isn't an answer.
        for j in range(scan_from, len(block)):
            s = block[j].strip()
            if not s or is_ad_line(s):
                continue
            # numbered "1. <question>?"
            if re.match(r"^\s*1[\.\)]\s+.{5,300}\?\s*$", s):
                p3_start = j
                break
            # paragraph-style: a short line ending with "?" (not part of an answer)
            if (len(s) < 250 and s.endswith("?") and not s.startswith("¥")
                    and not s.startswith("•") and not s.startswith("I ")
                    and not s.startswith("Yes,") and not s.startswith("No,")
                    and not s.startswith("(Note") and not s.startswith("Well,")
                    and not s.startswith("According to me") and not s.startswith("Honestly")
                    and not s.startswith("Definitely") and not s.startswith("Actually")
                    # require it doesn't end with a comma (so it's a complete question, not a fragment)
                    and not s.endswith(",")):
                p3_start = j
                break
    if p3_start is not None:
        # Collect Part 3 questions AND their sample answers as {q, a} pairs
        p3_items = []
        p3_cur_q = [None]       # use list for mutability in helper
        p3_cur_a = [[]]
        p3_prev_frag = [None]
        # If p3_start was found via fallback (a question line itself), include it as the first cur_q
        first_line = block[p3_start].strip()
        if first_line and not is_ad_line(first_line):
            m_num = re.match(r"^\s*\d{1,2}[\.\)]\s+(.+)$", first_line)
            if m_num:
                p3_cur_q[0] = m_num.group(1).strip()
            elif first_line.endswith("?"):
                p3_cur_q[0] = first_line

        for ln in block[p3_start+1:]:
            s = ln.strip()
            if not s:
                # blank line — flush current Q&A pair
                if p3_cur_q[0]:
                    p3_items.append({"q": p3_cur_q[0].strip(), "a": " ".join(p3_cur_a[0]).strip()})
                    p3_cur_q[0] = None
                    p3_cur_a[0] = []
                p3_prev_frag[0] = None
                continue
            if is_ad_line(s):
                p3_prev_frag[0] = None
                continue

            # Detect if this line is a new question
            is_new_question = False
            new_q_text = None

            # numbered question
            m = qnum_re.match(s)
            if m:
                qtext = m.group(2).strip()
                if "?" in qtext or qtext.endswith("?") or len(qtext) < 200:
                    new_q_text = qtext
                    is_new_question = True
            if not is_new_question:
                # paragraph-style question (a single line that ends with ?)
                if "?" in s and len(s) < 500 and not s.startswith("¥") and not s.startswith("•"):
                    # If this question is short and starts with lowercase (e.g., "you agree?"),
                    # it's likely a continuation of the previous fragment — merge
                    if (p3_prev_frag[0] and len(s) < 60
                            and (s[0].islower() or s.startswith("you ") or s.startswith("agree"))):
                        new_q_text = p3_prev_frag[0] + " " + s
                        is_new_question = True
                        p3_prev_frag[0] = None
                    else:
                        new_q_text = s
                        is_new_question = True

            if is_new_question:
                # Flush previous Q&A pair
                if p3_cur_q[0]:
                    p3_items.append({"q": p3_cur_q[0].strip(), "a": " ".join(p3_cur_a[0]).strip()})
                p3_cur_q[0] = new_q_text
                p3_cur_a[0] = []
                p3_prev_frag[0] = None
            else:
                # Not a question — could be a continuation fragment OR an answer paragraph
                # If we don't have a current question yet AND this line doesn't end with ".",
                # treat it as a fragment that may continue into a "?" line later
                if (not p3_cur_q[0] and not s.endswith(".") and not s.endswith(",")
                        and len(s) < 250 and not s.startswith("Yes,") and not s.startswith("No,")
                        and not s.startswith("I ") and not s.startswith("(Note")
                        and not s.startswith("Well,") and not s.startswith("Honestly")
                        and not s.startswith("Definitely") and not s.startswith("Actually")
                        and not s.startswith("According to me") and not s.startswith("According to")):
                    p3_prev_frag[0] = s
                elif p3_cur_q[0]:
                    # this is answer text for the current question
                    p3_cur_a[0].append(s)
                    p3_prev_frag[0] = None
                else:
                    p3_prev_frag[0] = None

        # Flush last Q&A pair
        if p3_cur_q[0]:
            p3_items.append({"q": p3_cur_q[0].strip(), "a": " ".join(p3_cur_a[0]).strip()})

        # filter junk
        p3_qs = [item for item in p3_items
                 if item["q"].strip() and len(item["q"].strip()) > 6 and not is_ad_line(item["q"])]

    bullets = [b.strip() for b in bullets if b.strip() and not is_ad_line(b)]
    cue_cards.append({
        "num": num,
        "title": title,
        "bullets": bullets,
        "sampleAnswers": sample_answers,
        "part3": p3_qs,
    })

print(f"Extracted {len(cue_cards)} cue cards")
total_p3 = sum(len(c["part3"]) for c in cue_cards)
total_sa = sum(len(c.get("sampleAnswers", [])) for c in cue_cards)
cards_with_sa = sum(1 for c in cue_cards if c.get("sampleAnswers"))
print(f"Total Part 3 follow-up questions: {total_p3}")
print(f"Cue cards with sample answers: {cards_with_sa} of {len(cue_cards)}")
print(f"Total sample answers: {total_sa}")
empty_bullets = [c["num"] for c in cue_cards if not c["bullets"]]
empty_p3 = [c["num"] for c in cue_cards if not c["part3"]]
print(f"Cue cards with no bullets parsed: {empty_bullets[:30]}")
print(f"Cue cards with no Part 3 parsed: {empty_p3[:30]}")

# ===================================================================
# PART 1 — TOPICS AND QUESTIONS
# ===================================================================
# Part 1 section starts at p1_start (the "SPEAKING PART 1 / INTRO QUESTIONS" cover)
# Topics are headings:  <num>. TopicName
# Questions inside are: <num>. Question text  (often followed by answer paragraphs we skip)

p1_text = "\n".join(part1_lines)

# Better topic-heading detection: a heading line is a SHORT non-question line that is
# not a continuation of an answer, not a marketing line, and not itself a question.
# A topic heading matches:  ^\s{0,12}<num>.\s+<Capitalised words>$
# but does NOT match question-like text (starts with May/What/How/etc. or ends with ?)

Q_STARTERS = {"may","what","how","where","why","when","would","do","is","are","were","have","will","which","did","please","could","can","who","whose"}

topics = []
i = 0
N = len(part1_lines)
while i < N:
    ln = part1_lines[i].rstrip()
    m = re.match(r"^\s{0,12}(\d{1,3})\.\s+([A-Za-z][^\n]{1,90})$", ln)
    if m:
        num = int(m.group(1))
        topic_name = m.group(2).strip()
        first_word = topic_name.split()[0].lower().rstrip(",.;:!?")
        if first_word in Q_STARTERS:
            i += 1
            continue
        # Skip Part 2 cue card titles that got misfiled into the Part 1 section
        # (they start with "Describe" or "Talk about")
        if topic_name.lower().startswith("describe ") or topic_name.lower().startswith("talk about"):
            i += 1
            continue
        if topic_name.endswith("?") or topic_name.endswith("."):
            i += 1
            continue
        if "?" in topic_name:
            i += 1
            continue
        if any(x in topic_name for x in [
            "Makkar","IELTS","www","instagram","youtube","Visa","Study Abroad",
            "Coaching","Office","Phagwara","Mohali","Jalandhar","Canada","Australia",
            "Germany","Europe","Japan","New Zealand","USA","UK","Dubai",
        ]):
            i += 1
            continue
        if is_ad_line(topic_name):
            i += 1
            continue
        # looks like a topic heading
        topics.append((i, num, topic_name))
    i += 1

# Deduplicate by (num, name) keeping first
seen = set()
unique_topics = []
for (i, num, name) in topics:
    key = (num, name.lower().strip())
    if key in seen:
        continue
    seen.add(key)
    unique_topics.append((i, num, name))
print(f"Part 1: {len(unique_topics)} unique topic headings")

p1_qnum_re = re.compile(r"^\s{0,16}(\d{1,2})[\.\)]\s+(.+)")
# Lines that start with common answer phrases (the answer is inlined with the question)
ANSWER_STARTERS = ("Yes,","No,","I ","(Note","Well,","Honestly","Definitely","Actually",
                   "According to me","According to","My ","Sometimes","Most","Generally",
                   "Of course","Sure","Absolutely","Perhaps","Honestly","Maybe","It ",
                   "There ","That ","This ","Yes ","No ","Oh ","Hmm","Well ")
def extract_inline_question(s):
    """Given a line that contains a '?' mixed with answer text, return just the question part.
    Conservative: only merges the first sentence-ending-with-? with no preceding text."""
    if "?" not in s:
        return None
    # If the line is short, just take everything up to and including the first '?'
    if len(s) < 250:
        # split on first '?'
        idx = s.find("?")
        return s[:idx+1].strip()
    # For long lines, look for the FIRST '?' — the question is everything before it
    idx = s.find("?")
    if idx == -1:
        return None
    question = s[:idx+1].strip()
    return question

p1_topics = []
for idx, (start_i, num, name) in enumerate(unique_topics):
    end_i = unique_topics[idx+1][0] if idx+1 < len(unique_topics) else N
    block = part1_lines[start_i:end_i]
    qs = []          # list of {q, a}
    cur_q = None     # current question text
    cur_a_lines = []  # answer lines for current question
    for ln in block[1:]:  # skip heading line
        s = ln.strip()
        if is_ad_line(s) and s:
            continue

        # Detect whether this line is a question
        is_question = False
        question_text = None

        if s:
            m = p1_qnum_re.match(s)
            if m:
                qtext = m.group(2).strip()
                if "?" in qtext:
                    q_idx = qtext.find("?")
                    question_text = qtext[:q_idx+1].strip()
                    is_question = True
                # else: sub-heading like "WORK"/"STUDIES" — not a question
            if not is_question:
                # Paragraph-style question: short line ending with "?"
                if (s.endswith("?") and len(s) < 250
                        and not any(s.startswith(p) for p in ANSWER_STARTERS)):
                    question_text = s
                    is_question = True
                # Long line with inline "?" — extract just the question part
                elif ("?" in s and not any(s.startswith(p) for p in ANSWER_STARTERS) and len(s) > 10):
                    q_idx = s.find("?")
                    if q_idx >= 0:
                        extracted = s[:q_idx+1].strip()
                        if 5 < len(extracted) < 250:
                            question_text = extracted
                            is_question = True

        if is_question:
            # Flush previous Q&A pair
            if cur_q:
                answer = " ".join(cur_a_lines).strip()
                qs.append({"q": cur_q, "a": answer})
            cur_q = question_text
            cur_a_lines = []
        elif s:
            # Non-question line — this is answer text (or a sub-heading we skip)
            if cur_q:
                cur_a_lines.append(s)
            # else: no current question — skip (probably a sub-heading before the first question)
        # blank lines: do nothing — keep collecting answer lines

    # Flush last Q&A pair
    if cur_q:
        answer = " ".join(cur_a_lines).strip()
        qs.append({"q": cur_q, "a": answer})

    # Filter: keep only entries with a valid question (>3 chars); answers can be empty
    qs = [item for item in qs if item["q"].strip() and len(item["q"].strip()) > 3]
    # Clean question text
    for item in qs:
        item["q"] = item["q"].strip(" -•?:")
        item["a"] = item["a"].strip()

    p1_topics.append({"num": num, "name": name, "questions": qs})

total_p1_q = sum(len(t["questions"]) for t in p1_topics)
total_p1_ans = sum(1 for t in p1_topics for q in t["questions"] if q.get("a"))
print(f"Total Part 1 questions: {total_p1_q}")
print(f"Part 1 questions with answers: {total_p1_ans}")
zero_q = [t['num'] for t in p1_topics if not t['questions']]
print(f"Topics with 0 questions: {len(zero_q)} of {len(p1_topics)}: {zero_q[:20]}")

# ===================================================================
# Categorise cue cards
# ===================================================================
CATEGORY_KEYWORDS = {
    "People": ["person","people","friend","family member","family","relative","child","neighbour","neighbor","teacher","successful person","singer","sportsperson","athlete","actor","celebrity","famous person","older than you","older person","popular person","happy person","creative person","who taught","who learnt","who solved","who often helps","who works","who would like to choose","who loves to grow plants","who likes to look after","who is good at","who really likes taking photos","who has a successful business","who did something difficult","who learns history","who makes plans","who enjoys working"],
    "Places": ["place","city","country","tourist","peaceful","near water","historical place","would like to visit","crowded place","noisy place","boring place","quiet place","natural place","place you went","place you have travelled","place you would like","short trip","long journey","long-term goal","short-term job"],
    "Buildings and Accommodation": ["building","home","house","apartment","flat","tall building","interesting building","room","home of someone","someone else's room"],
    "Objects and Possessions": ["gift","useful object","piece of technology","something you bought","something you lost","item of clothing","something that you can't live without","item on which you spent","something special","special cake","old thing","a piece of technology","piece of local news","wild animal"],
    "Events and Experiences": ["event","celebration","party","journey","experience","happy occasion","unforgettable day","time when you","occasion when","live sports event","sports event","great dinner","enjoyable evening","memorable event","time when you helped","time when you lost","time when you received","time when you watched","time you made","time when you changed","time when you organized","time when you sent","time when you got up","time when you were stuck","time when you had a problem","time when you needed","time when you were waiting","time when you encouraged","time when you felt proud","time when you broke","time when you forgot","time when you saw","time when you saved","time when you worked","time when you made an important","time when you talked","time when you watched a famous","time you saw something interesting","event you attended"],
    "Activities and Hobbies": ["sport","outdoor activity","hobby","activity","something you do","bicycle","motorcycle","car trip","trip you would like","short trip you often"],
    "Art, Books and Entertainment": ["book","film","song","painting","photograph","artwork","performance","movie","TV show","TV or online","program","video","advertisement","story","traditional story","interesting video","TV series","program you like","least favourite movie","film that made you laugh"],
    "Skills and Achievements": ["skill","learned","achievement","goal","difficult task","new skill","natural talent","long-term goal","important decision","perfect job","short-term job","successful business","course","thing you did to learn"],
    "Nature and Environment": ["animal","plant","natural place","landscape","environmental","natural place","river","lake","wild animal","plants","law on environmental","person who likes to look after the natural","person who loves to grow plants"],
    "Food and Traditions": ["food","meal","restaurant","festival","cultural tradition","traditional","special cake","unusual meal","great dinner","food that people eat"],
    "Future Plans and Decisions": ["future ambition","important decision","something you want to change","country you want to visit","long-term goal","perfect job","new law","plan that you had to change","change that you made","positive change","change that helps you save","short-term job","ambition"],
    "Problems and Challenges": ["problem","difficult situation","time you helped someone","time you received advice","time when you gave advice","challenging","problem using an electronic","problem in a smart way","time when you needed to use your imagination","time when you had a problem","time when you were stuck","time when you encouraged someone"],
}

def categorise(title):
    t = title.lower()
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                cats.append(cat)
                break
    if not cats:
        cats.append("Other")
    return cats

for c in cue_cards:
    c["categories"] = categorise(c["title"])

# ===================================================================
# Save
# ===================================================================
out = {
    "part1": p1_topics,
    "part2": cue_cards,
    "stats": {
        "part1_topics": len(p1_topics),
        "part1_questions": total_p1_q,
        "part2_cue_cards": len(cue_cards),
        "part3_questions": total_p3,
        "total_questions": total_p1_q + len(cue_cards) + total_p3,
    },
}
with open("/home/z/my-project/scripts/data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Saved data.json")
print(json.dumps(out["stats"], indent=2))
