
# Guarded Agent

A multi-tool AI agent built with LangGraph that calls external tools, handles their failures gracefully, and refuses to loop indefinitely when it gets stuck.

## What it does

The agent answers a question by deciding, on its own, whether it needs a tool to answer accurately. It has access to four tools:

- **calculator** — evaluates arithmetic expressions
- **db_lookup** — queries a local SQLite database of sample products
- **web_search** — searches the web via DuckDuckGo
- **flaky_api** — a deliberately unreliable tool (simulates a real flaky external service) used to prove the agent handles failure without crashing

## Why this project exists

Most agent demos show the happy path. This one is built around the failure path instead. The real engineering problem in a tool-calling agent isn't picking the right tool — it's what happens when a tool returns garbage, times out, or the model gets stuck in a loop. This project demonstrates:

- A hard step-limit guardrail that stops the agent from looping forever
- A fallback response when that limit is hit mid-task, instead of a silent cutoff or a crash
- Structured JSON logging of every tool call, its arguments, and its result, so the agent's behavior is auditable after the fact
- Graceful handling of both failure modes a real API can produce: a hard exception (connection dropped) and a soft failure (a response that technically returns but is unusable)

## Architecture

Three LangGraph nodes:

- **agent** — calls the LLM, which decides to answer or call a tool
- **tools** — executes whichever tool the LLM requested, logs the result
- **fallback** — returns an honest "I couldn't finish this" message if the step limit is reached before the agent produces a final answer

START → agent → (tool requested?) → tools → agent → ... → (done or limit) → END
                                                        ↘ limit reached → fallback → END


The step counter increments only on agent turns, not on individual tool calls — a single agent turn can request more than one tool at once.

## Setup

```bash
uv venv
.venv\Scripts\activate      # Windows
uv add langgraph langchain langchain-groq langchain-community ddgs python-dotenv
uv add pytest --dev
```

Create a `.env` file (see `.env.example`) with a free Groq API key from [console.groq.com](https://console.groq.com):

  GROQ_API_KEY=your_key_here

Seed the sample product database (required before `db_lookup` will work):

```bash
python src\tools\seed_db.py
```

## Running it

```bash
python -m src.main
```

You'll be prompted for a question. Try:

- `What's 23 times 47?` — exercises the calculator
- `Is the Mechanical Keyboard in stock?` — exercises the database lookup
- `What's a recent headline in AI news?` — exercises web search
- `What's the order status for order #4521?` — exercises the flaky tool; run it a few times to see both its success and failure paths

Every run appends structured JSON logs to `agent.log` — one line per event (`tool_call_requested`, `tool_result`, `final_answer`, or `step_limit_reached`), each tagged with the step number it occurred on.

## Running the tests

```bash
python -m pytest tests/test_agent.py -v
```

Tests cover the routing logic in isolation (`should_continue`) — the piece responsible for the step-limit guardrail — without depending on a live LLM call or network access.

## Known limitations

- The LLM model name (`openai/gpt-oss-120b` via Groq) is hardcoded rather than configurable; Groq periodically deprecates older models, so this may need updating over time.
- `db_lookup` uses partial (`LIKE`) matching, which is forgiving but can return multiple rows for ambiguous queries.
- Web search results depend on DuckDuckGo's unofficial API and can vary in quality or occasionally return no results.
- `uv.lock` is committed intentionally, to pin exact dependency versions and avoid drift (this project already hit two dependency-related breaks during development: a renamed search package and a deprecated LLM model).