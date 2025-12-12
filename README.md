# Kasparro Agentic Content Generation System

A fully modular, deterministic, multi-agent content generation pipeline that converts a single product JSON into three machine-readable outputs: a Product Page, an FAQ Page, and a Comparison Page.
Built for the Kasparro Applied AI / Agentic Content System Assignment with a strong focus on clean architecture, reproducibility, and real engineering design.

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

### ⚙️ Technology Stack
Component	Description
Python 3.10+	Core runtime
LangChain (v1.1.3)	Orchestration + Prompt/LLM abstraction
OpenAI GPT-4o-mini	Strict JSON generation model
Pydantic	JSON schema validation
dotenv	Credential management
Chroma / utils	Simple JSON writing utilities

### 🧠 Deterministic LLM Agentic System

Unlike generative systems, this pipeline:

-uses LLMs strictly with schema-locked prompts

-enforces JSON-only output

-includes retry & trimming logic

-corrects LLM output via sanitization + fallback systems

-applies hard validation using Pydantic

-enforces zero hallucinations

-FAQ Sanitizer Guarantees

#### The system ensures:

-always exactly 15 FAQs

-no empty answers

-answers grounded only in facts_json

-auto-fallback for missing values

-raw LLM output is logged for debugging

##### Price Comparison Fix

The orchestrator enforces:

"A_only": ["A price: X currency"]
"B_only": ["B price: Y currency"]
"common": ["currency: XYZ"]

## 🗂 Project Structure
```bash
kasparro-agentic-content-system/
│
├── run.py
├── requirements.txt
├── docs/
│   └── projectdocumentation.md
│
└── src/
    ├── langchain_orchestrator.py
    ├── utils.py
    ├── agents/
    │   ├── ingest_agent.py
    │   ├── sanity_agent.py
    │   ├── facts_extractor_agent.py
    │   ├── renderer_agent.py
    │   ├── comparison_agent.py
    │   ├── content_block_agent.py
    │   ├── question_generator_agent.py    
    │   └── template_agent.py
    │
    └── out/
        ├── product_page.json
        ├── faq.json
        └── comparison_page.json
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

### Generate all Outputs Using LangChain Agentic Mode
```bash
python run.py --mode langchain --input examples/product.json
```
Outputs will appear in:
```bash
/out/product_page.json
/out/faq.json
/out/comparison_page.json
```

## Validation Rules 
### Product Page

-Must use all required blocks

-Titles cannot be empty

-Must reflect facts only

### FAQ

-Exactly 15 questions

-Questions follow fixed template

-Answers derived strictly from facts

-No empty answers

### Comparison Page

-Product B strictly follows deterministic transformation

-No missing fields

Verdict must be one of:

-Product A is cheaper

-Product B is cheaper

-Both priced equally

## 🧩 Key Design Principles
1. Modularity

Each agent does exactly one task.

2. Determinism

Same input → same output.

3. Traceability

LLM raw outputs logged for debugging.

4. Validation

Pydantic schema enforcement prevents invalid JSON.

5. Maintainability

Clear separation of concerns, testable units, clean orchestration.

## 🧪 Testing

The project includes 10 tests across:

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

-Plugin-style agent registry

-Multi-product batch processing

-More sophisticated template rules

-Configurable comparison strategies

-JSON schema validation at runtime

-Optional natural-language enhancement layer (still deterministic)

## 📤 Submission Notes for Evaluators

This project was designed with production engineering practices in mind:

-Modular multi-agent pipeline

-Clear domain boundaries

-Deterministic behavior

-Automated tests

-Readable architecture

-No unnecessary dependencies

-Maintainable, extendable codebase

## 🙌 Final Notes

Everything here follows an engineering-first mindset: clean modules, predictable behavior, and no hidden magic. It stays readable, testable, and extensible.

If you have any questions about the structure or implementation, feel free to explore the docs/ folder or the individual agent files under src/agents/.