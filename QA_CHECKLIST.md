# Homepage release QA

- [ ] The Buildiful organization's repository is named `buildiful.github.io` and its GitHub Pages source points to `main` / root.
- [ ] All project files are in repository root, including `.gitignore` and `.nojekyll`.
- [ ] The official Buildiful® white logo and favicon appear correctly (prefer local copied assets).
- [ ] The hero shows the latest real released tool and a working direct link.
- [ ] Every card opens a deployed tool and its correct public source repository.
- [ ] Search, category tabs, sorting, and reset work using mouse and keyboard.
- [ ] Phone-width, tablet, and desktop layouts work; no clipped controls or horizontal page scrolling.
- [ ] The page works for reading and following links without JavaScript.
- [ ] With unanswered or rejected consent, no Google Analytics script or GA4 events are sent.
- [ ] Allow consent loads GA4; link events contain only allowlisted tool slugs, no catalog searches.
- [ ] Declining and revisiting preserves the choice; footer analytics settings reopens consent.
- [ ] Privacy notice is accurate and linked from the footer/consent.
- [ ] `python3 build.py` succeeds; RSS and sitemap are valid XML.
- [ ] New tool release test: add a test object to `tools.json` locally, rebuild, verify count/latest/cards/feed, then revert the test.
- [ ] Review all source, README, and comments for public release; no secrets or placeholder marketing promises.
- [ ] Each standalone tool's separate repository remains free of Buildiful 365 campaign/day references.
