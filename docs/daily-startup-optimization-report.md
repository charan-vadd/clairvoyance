# Daily Startup Optimization Report

## Scope

Backend-only optimization for Breeze Buddy Daily startup. Frontend/Loom was not touched.

Target: reduce Assist Daily startup from the observed 15-20 seconds toward less than 5 seconds by removing backend startup overhead and adding phase timings for the remaining runtime path.

## Methodology

- Static import profiling used `uv run python -X importtime`.
- Repeated cold process timings used five separate `uv run python -c ...` subprocesses and report the median.
- Execution timing used `start_daily_session()` with the Daily API and bot launch mocked to avoid creating external Daily rooms locally. The local DB accessor path was left active.
- Child process timing used `bot_runner._amain()` with `daily_bot` monkeypatched to a no-op to measure Python process/import/payload/DB-pool overhead without joining a real Daily room.
- Real production Daily join/provider timings still need one instrumented environment run using the new `[daily-startup]` logs.

## Results

| Measurement | Before | After | Notes |
| --- | ---: | ---: | --- |
| Parent `daily.py` import, cumulative importtime | ~4281 ms | 558 ms | Removed eager agent/schema/DB import fan-out. |
| Parent `daily.py` repeated import median | Not captured | 353 ms | Five cold subprocesses through `uv run python`. |
| Child `bot_runner` import, cumulative importtime | ~4854 ms | 632 ms | Removed eager agent/provider/Pipecat/IVR/observer imports. |
| Child `bot_runner` repeated import median | ~8800 ms wall earlier / 4854 ms importtime | 566 ms | Five cold subprocesses through `uv run python`. |
| Parent `start_daily_session()` mocked execution | ~71 ms earlier after parent fixes | 44.5 ms median | Daily API and bot launch mocked; DB pool warm. First run was 379 ms due DB pool init. |
| Child `bot_runner` no-op process overhead | Not captured | 686.6 ms median | Includes process startup, imports, payload parse, DB pool init; excludes real Daily join/pipeline. |

## Biggest Findings

1. The original startup cost was dominated by import-time work, not the parent HTTP handler logic.
2. Import barrels pulled in providers and subsystems unrelated to the current call path:
   - LLM/STT/TTS provider barrels loaded Azure/Gemini/provider dependencies eagerly.
   - `agent` import loaded observers, tracing, IVR/inbound, end-conversation handlers, and voice UI processor code.
   - Processor/package barrels and utility modules pulled in Pipecat frames, VAD, scipy, pydub, soundfile, GCP, and OpenAI before any call needed them.
3. Daily token creation was serial despite user and bot tokens being independent after room creation.

## Changes

- Added `DailyStartupTimer` and phase logs for parent Daily session creation, bot launch handoff, child runner startup, and agent setup/generation phases.
- Lazy-loaded heavyweight provider exports in voice LLM/STT/TTS modules.
- Deferred Daily agent imports for observers, tracing, IVR, inbound handling, end-conversation, transport setup, audio mixer, audio conversion, template context frames, and voice UI processor code.
- Converted processor package exports to lazy module-level `__getattr__`.
- Parallelized Daily user-token and bot-token creation with `asyncio.gather()`.
- Narrowed schema imports in Daily routes/accessors to avoid importing broad schema barrels.

## Remaining Runtime Breakdown To Capture In A Real Run

With the current patch, production logs will show:

- `start_daily_session`: room creation, token creation, DB updates, subprocess launch, response ready.
- `daily_launch`: subprocess flag, payload serialization, process creation, payload write.
- `bot_runner_main`: stdin payload read.
- `bot_runner`: DB pool init and `daily_bot` handoff.
- `agent_daily_setup`: lead load, template load, service creation, transport creation.
- `agent_generation`: pipeline build, pipeline task creation, flow/observer setup, runner start.

The likely next runtime bottlenecks, if production is still over 5 seconds, are real Daily room/token latency, DB pool initialization, provider service construction, and transport room join. The new logs isolate each one directly.
