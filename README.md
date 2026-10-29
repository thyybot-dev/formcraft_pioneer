# Formcraft Pioneer

Everything behind the plan to make **Formcraft Design and Construction** (Kampala) a leading firm in East Africa and to test the road to USD 1 billion: the feasibility report, the Formcraft Command Centre (code), every Monte Carlo simulation, the branding used, and Emlyn Atochon's professional profile. Kept as reference for planning and for building Formcraft's own tools later.

| Folder | What is in it |
|---|---|
| `feasibility/` | **Formcraft-Feasibility-Report-2026.pdf** (branded: cover, run 11 summary, contents, full Pioneer plan, appendix). `source/` has the Pioneer plan as Markdown and the original PDF export; `charts/` has the chart images made during the work. |
| `command-centre/` | `index.html`: the whole Command Centre app (one file, about 400 KB). See `docs/command-centre.md`. |
| `simulations/` | Every simulation engine (`.py`) and its results (`.json`), runs 1 to 11. See `simulations/README.md`. |
| `profile/` | Emlyn Atochon's professional profile and development plan (branded PDF, Markdown and original exports), honest scenarios and risks, each venture on its own. |
| `branding/` | Main Formcraft and division logos (PNG) and the brochure. |
| `brand-docs/` | Pitch deck, Template Master Register, Template Master Catalogue, Healthcare Family Catalogue sample. |
| `docs/` | How the Command Centre works, the data model, and the log of everything asked for. |
| `tools/` | `build_report.py` rebuilds the branded PDFs; test harness for the Command Centre. |

Live versions: the Command Centre at https://claude.ai/artifact/QZwNFsyfC1TNZJeJu5PiRG and the Pioneer document at https://claude.ai/artifact/XhHE8xqA6KbhMHiAdjqtaw (private to the owner).

## Latest simulation (run 11, 1,000,000 futures per scenario)

| Scenario | Running in 2036 | USD 1M a year by 2031 | USD 100M lifetime | USD 1B lifetime |
|---|---|---|---|---|
| Run 10 plan, no Command Centre | 66.7% | 23.2% | 51.7% | 30.0% |
| Plan + Command Centre (likely use) | 67.6% | 25.3% | 52.9% | 31.2% |
| Plan + Command Centre used every day | 67.8% | 25.9% | 53.2% | 31.5% |
| Plan + Command Centre + best practice | 71.1% | 26.8% | 57.1% | 34.8% |
| Plan + Command Centre, sceptic | 64.3% | 21.2% | 43.4% | 21.2% |
| Plan + Command Centre, growth capped at 10% after 2036 | 67.6% | 25.3% | 50.5% | 26.7% |

These rest on the plan's own growth assumptions; near-term results are the real test. Lifetime figures are soft.

## Not included
The Brand Guide and Company Profile PDFs are over the 20 MB download limit of the session that built this repository; add them by hand. The full logo set (about 270 SVG, PNG and PDF variants) is in the claude.ai project "FORMCRAFY FEASIBILITY"; only the main logos are here.
