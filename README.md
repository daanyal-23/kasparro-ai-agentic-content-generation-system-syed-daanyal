# Kasparro Agentic Content Generation System

A fully modular, deterministic, multi-agent content generation pipeline that converts a single product JSON into three machine-readable outputs: a Product Page, an FAQ Page, and a Comparison Page.
Built with a strong focus on clean architecture, reproducibility, validation, and real engineering design.

## 🚀 Overview

This project implements a production-grade content generation system where each agent performs a single responsibility, similar to how micro-components operate inside real-world AI pipelines.

Given one product JSON, the system produces:

| Output File          | Description                                                            |
|----------------------|------------------------------------------------------------------------|
| product_page.json    | Structured product page using deterministic content blocks             |
| faq.json             | ≥ 15 rule-based Q&A items derived solely from input facts              |
| comparison_page.json | Product A vs. Fictional Product B comparison (ingredients, benefits, price, verdict) |

The system is has the following features:
✔ Modular agents
✔ Deterministic behavior
✔ No hallucinations
✔ Strict JSON schemas
✔ Clean orchestration using LangChain
✔ LLM-repair and sanitization layers
✔ Professional engineering-quality code

## 📦 Features
### 1. Multi-Agent Modular Architecture

The pipeline is divided into isolated agents:

Agent	Responsibility
IngestAgent	Reads & normalizes product JSON
SanityAgent	Validates schema and detects issues
FactsExtractorAgent	Converts product into atomic reusable facts
FAQ Generator (LLM)	Builds FAQs using a fixed template + sanitization
Product Page Generator (LLM)	Generates structured product page via strict JSON template
ComparisonAgent (LLM + deterministic rules)	Builds Fictional Product B and structured A/B comparison
RendererAgent	Writes all final JSON artifacts

### 🧠 Agentic Orchestration (UPDATED)

The system now uses LangGraph (StateGraph) as the primary orchestration layer.

What this enables:

- Explicit state machine (PipelineState)

- Node-level execution (sanity → facts → generation → validation → render)

- Conditional routing

- Validation loop with retry counter

- Automatic regeneration when constraints fail

- Hard stop after max retries to avoid infinite loops

This replaces a simple sequential runner and satisfies agentic orchestration requirements.

### 🔁 Deterministic-First with LLM Fallback (UPDATED)

All generation nodes follow this pattern:

- Primary path: Deterministic agent logic

- Fallback path: LLM-based generation (strict JSON prompts)

- Validation: Schema + content checks

- Retry loop: Graph re-enters generation if validation fails

This ensures:

- Predictable outputs

- Minimal LLM usage

- Repair of malformed or incomplete results

- Zero hallucinations

### ⚙️ Technology Stack
| Component          | Description                         |
| ------------------ | ----------------------------------- |
| Python 3.10+       | Core runtime                        |
| **LangGraph**      | Agentic state-machine orchestration |
| LangChain (v1.1.3) | Prompt + LLM abstraction            |
| OpenAI GPT-4o-mini | JSON-locked fallback generation     |
| Pydantic           | Schema validation                   |
| python-dotenv      | Credential management               |
| pytest             | Test suite                          |


### 🧠 Deterministic Content Guarantees

- Same input → same output (timestamps excluded)

- No external data or API calls

- No invented facts

- Fictional Product B derived only from Product A

- Hard schema enforcement at validation stage

#### The system ensures:

-always exactly 15 FAQs

-no empty answers

-answers grounded only in facts_json

-auto-fallback for missing values

### 📋 Validation Rules
#### Product Page

- All required blocks present

- Titles must not be empty

- Values must reflect facts only

#### FAQ

- Exactly 15 FAQs

- Numeric IDs ("1" → "15")

- No empty answers

- Answers derived strictly from facts

#### Comparison Page

- Product B derived deterministically

- Price comparison formatted as:
```bash
"A_only": ["A price: X INR"]
"B_only": ["B price: Y INR"]
"common": ["currency: INR"]
```

Verdict must be one of:

- Product A is cheaper

- Product B is cheaper

- Both priced equally


## 🗂 Project Structure
```bash
kasparro-ai-agentic-content-generation-system-syed-daanyal/
│
├── run.py                     # Entry point (LangGraph-based pipeline)
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── docs/
│   └── projectdocumentation.md
│
├── examples/
│   └── product_glowboost.json # Sample input
│
├── out/                       # Generated outputs
│   ├── product_page.json
│   ├── faq.json
│   └── comparison_page.json
│
├── src/
│   ├── graph.py               # LangGraph StateGraph orchestration
│   ├── state.py               # Typed PipelineState (shared state)
│   ├── models.py              # ProductModel + schemas
│   ├── langchain_orchestrator.py  # LLM fallback + JSON repair
│   ├── orchestrator.py        # Legacy sequential pipeline (kept for reference)
│   ├── utils.py
│   │
│   └── agents/
│       ├── ingest_agent.py
│       ├── sanity_agent.py
│       ├── facts_extractor_agent.py
│       ├── validator_agent.py
│       ├── renderer_agent.py
│       ├── comparison_agent.py
│       ├── content_block_agent.py
│       ├── question_generator_agent.py
│       └── template_engine_agent.py
│
├── tests/
│   ├── test_pipeline.py       # Updated to use LangGraph
│   ├── test_blocks.py
│   ├── test_facts.py
│   ├── test_questions.py
│   ├── test_product_page.py
│   ├── test_comparison.py
│   ├── test_templates.py
│   └── conftest.py
│
├── examples.zip               # Submission artifact
└── src.zip                    # Submission artifact

```

## 📄 Input Format

Your input file must be a JSON file with product details, for example:
```bash
{
  "name": "GlowBoost Vitamin C Serum",
  "ingredients": ["Vitamin C", "Hyaluronic Acid", "Glycerin"],
  "benefits": ["Brightening", "Fades dark spots", "Hydration"],
  "usage": "Apply 2–3 drops in the morning before sunscreen.",
  "safety": "Mild tingling in some users; patch test recommended.",
  "price": { "amount": 699, "currency": "INR" }
}
```
## ⚙️ Installation & Setup
### 1️⃣ Clone Repository

```bash
git clone https://github.com/daanyal-23/kasparro-ai-agentic-content-generation-system-syed-daanyal
cd kasparro-ai-agentic-content-generation-system-syed-daanyal
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add API Key

Create a .env file:
```bash
OPENAI_API_KEY=your_key
```
## ▶️ Running the System

### Generate all Outputs 
```bash
python run.py --input examples/product.json
```
Outputs will appear in:
```bash
/out/product_page.json
/out/faq.json
/out/comparison_page.json
```

## 🧩 Key Design Principles
1. Modularity

Each agent does exactly one task.

2. Determinism

Same input → same output.

3. Agentic orchestration

State + routing + retries

4. Validation-first

Pydantic schema enforcement prevents invalid JSON.

5. Maintainability

Clear separation of concerns, testable units, clean orchestration.

## 🧪 Testing

The project includes tests covering:

-Fact extraction

-Question generation

-Product page rendering

-Comparison logic

-End-to-end pipeline

-Template correctness

-Block generation

## Run all tests:
```bash
python -m pytest -q
```

#### Expected output:

10 passed in X.XXs

## 📝 Assumptions

-Input follows the given product schema.

-Output must be purely machine-readable JSON.

-System must remain modular (each agent = one responsibility).

-No hallucinations or invented facts beyond allowed fictional transformations.

## 🌱 Future Improvements

- Graph-level node retries per agent

- Metrics & tracing per node

- Batch multi-product execution

- Configurable comparison strategies

- Optional explainability layer

## 📤 Submission Notes for Evaluators

This system demonstrates:

- True agentic orchestration (LangGraph)

- Deterministic-first engineering

- Robust validation & retry logic

- Clean separation of concerns

- Production-quality structure

## 🙌 Final Notes

Everything here follows an engineering-first mindset: clean modules, predictable behavior, and no hidden magic. It stays readable, testable, and extensible.

If you have any questions about the structure or implementation, feel free to explore the docs/ folder or the individual agent files under src/agents/.