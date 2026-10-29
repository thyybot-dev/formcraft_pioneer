# Simulations

Monte Carlo models of Formcraft and Emlyn's ventures, built step by step. Most runs use 1,000,000 simulated futures per scenario (numpy, vectorised). Results are in the matching `.json`.

| File | Run | What it adds |
|---|---|---|
| `mc.py`, `model.py`, `model2.py`, `run1m*.py`, `v3*.py`, `vec*.py`, `billion.py`, `big.py`, `lev.py` | Early | All five ventures (Formcraft, Soko Foods, Logistics, Nyumba, Trade Assistant), YouTube, AI effects, the billion question |
| `alone.py`, `fcalone.py` | Ventures alone | Each venture simulated on its own |
| `soko.py`, `nyfee.py`, `noai.py`, `sims_more.py`, `ta_opt.py` | Variants | Soko strategy, Nyumba fee, no-AI baseline, more scenarios, trade assistant options |
| `sim5.py`, `fcrule.py` | Run 5 | The rulebook method |
| `fcsuite.py` | Run 6 | Simulation lab suite |
| `fcrun7.py` | Run 7 | Capacity, hiring, key person, cash (monthly model) |
| `fcrun8.py` | Run 8 | Legal and financial plan, sceptic settings |
| `fcrun9.py` | Run 9 | Content factory, sales, project management |
| `fcrun10.py` | Run 10 | Standards bank (index vs hosting texts) |
| `fcrun11.py` | Run 11 | The Command Centre: benefits if used, build-time cost, partial adoption |

Run: `python3 fcrun11.py` (about 3 minutes for 6 scenarios × 1M futures). `HZB=0.36` calibrates the no-AI baseline to about 42% still running in 2036.

Honest limits: growth after 2031 is assumed (30% then 20% a year for decades in the base case), so lifetime USD 100M and USD 1B odds are soft; survival and 2031/2036 revenue are the figures to trust and to test against real data.
