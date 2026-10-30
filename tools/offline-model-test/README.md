# Offline model test

Picks the 7–8B model for the Formcraft hub's offline default tier. It runs 10 Formcraft tasks: tool calls (deals, tasks, notices, metrics, register rows, memory) and JSON extraction (email sorting, receipts, minutes). The aim is to check that a model can do the hub's real work.

1. Install [Ollama](https://ollama.com). Pull 2–3 current 7–8B models that support tool calling.
2. Run `node run.mjs <model>` for each model.
3. Compare the scores in `results.csv`. Pick the model with the most passes. If scores tie, pick the faster one.

Aim for 9 or 10 out of 10. A model that fails tool calls cannot run agents, however good its prose is.
