# Accuracy test

Run the analyzer against a discussion URL and compare results to a CSV of expected policies/guidelines/essays.

## Usage

```bash
# From project root (with venv activated if you use one)
python scripts/test_accuracy.py --csv "Test - WorldCupControversy.csv"
python scripts/test_accuracy.py --url "https://en.wikipedia.org/wiki/Talk:Page#Section"
python scripts/test_accuracy.py --csv "Test-Longer Threads.csv" --url "https://..."
```

- **`--csv`**  
  Path to CSV (default: looks for `Test-Longer Threads.csv` then `Test - WorldCupControversy.csv`).
- **`--url`**  
  Discussion URL. If omitted, the script uses the URL from the CSV (row 1, second column).

## CSV format

- **Row 0:** `discussion link,SB (answer),V.2 - ...,V.3 - ...`
- **Row 1 (optional):** Leave first cell empty, put the discussion URL in the second cell.
- **Sections:** Rows starting with `Policy`, `Guideline`, or `Essay` start a new section.
- **Expected items:** Each row is like `WP:WEIGHT [↗] (NPOV),5,...` — shortcut and optional count in column B (SB).
- **False positives:** After a row containing `Detection Error (false positive)`, list shortcuts that should *not* be detected.

Example:

```csv
discussion link,SB (answer),V.2 - 11/17/2025,V.3 - 11/27/2025
,https://en.wikipedia.org/wiki/Talk:Article#Section_Name,
Policy,,,
WP:NPOV [↗],1,,
WP:V [↗],3,,
Guideline,,,
WP:RS [↗],2,,
Essay,,,
WP:1AM [↗],1,,
Detection Error (false positive),,,
,,(NOT),
,,IMAGE,
```

## Metrics

- **Precision:** TP / (TP + FP) — of what we detected, how much was correct.
- **Recall:** TP / (TP + FN) — of what was expected, how much we found.
- **F1:** Harmonic mean of precision and recall.

The report also lists true positives, false negatives (expected but missed), and false positives (detected but not expected).

## Notes

- The script uses the **pattern-based** detector if `OPENAI_API_KEY` is not set or if the OpenAI call fails. With a valid key it uses the **OpenAI** analyzer.
- Make sure the discussion URL points to a section that exists on the page; otherwise the scraper falls back to the full page and results may not match the CSV.
