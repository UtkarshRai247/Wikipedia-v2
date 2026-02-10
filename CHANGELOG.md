# Changelog

All notable changes to the Wikipedia Talk Page Policy Analyzer are listed here in plain language. Newest changes appear at the top.

---

## [Unreleased]

_Nothing yet._

---

## February 10, 2026

- **Changelog added** — This changelog file was added so everyone can see what’s changed in the project in plain language.
- **Project link updated** — The reference to this project’s GitHub page in the app code was updated to point to the correct repository.

---

## January 27, 2026

- **Routes updated** — Internal updates to how the app handles web requests and pages.

---

## January 20, 2026

- **Accuracy improvements** — The analyzer was tuned so it reports policy and guideline mentions more accurately and consistently.
- **Exact phrase matching** — The app now looks for exact phrases where needed, reducing missed or incorrect matches in tricky cases.
- **No duplicate or made-up results** — Rules were added so the analyzer does not repeat the same finding or invent mentions that aren’t in the text.
- **Better guideline detection** — Prompts and logic were refined so guidelines are detected more reliably.
- **Stronger occurrence detection** — The system was switched to a more capable model and stricter prompts so it finds more real mentions.
- **All occurrences listed** — When a policy or guideline appears multiple times, the app now lists each occurrence instead of collapsing them into one.
- **Highlighting and auto-scroll restored** — Matches in the discussion text are highlighted again, and the page scrolls to the relevant section for easier reading.
- **Loose interpretation option** — An option was added to allow a slightly looser interpretation of policy mentions, helping reach very high accuracy in tests.
- **Prompt refinements** — Multiple rounds of prompt updates to improve accuracy and reduce errors on real Wikipedia talk pages.

---

## January 17, 2026

- **Policy detection improvements** — More policy and guideline shortcuts were added, and support was improved for patterns like “MOS:” (Manual of Style) so more types of mentions are recognized.
- **Branch merge** — Changes from the “vigilant-brown” branch were merged into the main project.

---

## January 13, 2026

- **First release** — Initial version of the Wikipedia Talk Page Policy Analyzer.
- **AI-powered analysis** — Integration of an AI service to detect mentions of policies, guidelines, and essays in talk page discussions.
- **Stable analysis when AI is unavailable** — If the AI service fails or is unavailable, the app falls back to pattern-based detection so the tool still works.
- **Easier deployment** — A proper entry point and configuration were added so the app can run reliably on hosting platforms (e.g. Gunicorn).
- **Import and path fixes** — Corrected how the app is loaded so it starts correctly in production.
- **App loading fix** — The app factory is now loaded directly so startup works in all environments.
- **Smarter text splitting** — Long discussions are split into chunks in a way that works better with the AI and keeps context intact.
- **Memory optimization** — Reduced memory use so the app can run on limited hosting resources without running out of memory.
- **Fewer API calls** — The analyzer now uses one API call per category with structured sections, making it faster and more efficient.
- **Richer policy detection** — More shortcuts and MOS-style patterns were added so more policy and guideline mentions are found.

---

*This changelog is written for non-technical readers. For exact commit history, see the project’s Git log.*
