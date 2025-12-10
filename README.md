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

The system is deterministic (same input → same output, except timestamps), fully tested, and easy to extend.

## 📦 Features
### ✔ Modular multi-agent architecture

Each agent handles a clear role: ingest → sanity → facts → questions → blocks → templates → comparison → rendering.

### ✔ Template-driven structured output

Final pages are composed using reusable, testable content blocks.

### ✔ Deterministic & rule-based

No external calls, no hallucinations, no randomness.

### ✔ Fictional Product B generation

Product B is created using constraints from Product A only (subset of ingredients + controlled price delta).

### ✔ 10 automated tests (unit + pipeline)

Ensures reliability, repeatability, and clean IO boundaries.

## 🗂 Project Structure
```bash
kasparro-ai-agentic-content-generation-system-syed-daanyal
├─ run.py
├─ README.md
├─ requirements.txt
├─ examples/
│   └─ product_glowboost.json
├─ out/
│   ├─ product_page.json
│   ├─ faq.json
│   └─ comparison_page.json
├─ src/
│   ├─ __init__.py
│   ├─ models.py
│   ├─ utils.py
│   ├─ orchestrator.py
│   └─ agents/
│       ├─ __init__.py
│       ├─ ingest_agent.py
│       ├─ sanity_agent.py
│       ├─ facts_extractor_agent.py
│       ├─ question_generator_agent.py
│       ├─ content_block_agent.py
│       ├─ template_engine_agent.py
│       ├─ comparison_agent.py
│       └─ renderer_agent.py
├─ tests/
│   ├─ conftest.py
│   ├─ test_facts.py
│   ├─ test_questions.py
│   ├─ test_product_page.py
│   ├─ test_comparison.py
│   ├─ test_pipeline.py
│   ├─ test_blocks.py
│   ├─ test_templates.py
│   └─ test_run_mvp.py
└─ docs/
    └─ projectdocumentation.md
```

## ⚙️ Installation & Setup
### 1️⃣ Create and activate a virtual environment

Windows
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux
```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 3️⃣ Run the pipeline
```bash
python run.py --input examples/product_glowboost.json --outdir out/
```

### 4️⃣ Run the test suite
```bash
python -m pytest -q
```
### Expected: 10 passed

## 🔁 End-to-End Pipeline Flow
```bash
Product JSON
      │
      ▼
[IngestAgent] → Parse input → ProductModel
      │
      ▼
[SanityCheckAgent] → Validate fields
      │
      ▼
[FactsExtractorAgent] → Atomic facts bag
      │
      ├──► [QuestionGeneratorAgent] → FAQ generation
      │
      ├──► [ContentBlockAgent] → Reusable blocks
      │
      ├──► [TemplateEngineAgent] → Product Page
      │
      └──► [ComparisonAgent] → Product B + comparison
      │
      ▼
[RendererAgent] → Write final JSON files
```
## 🧩 Output Files Description
### product_page.json

Contains structured content blocks:

-Summary

-Ingredients

-Benefits

-Usage

-Safety

-Price

-Metadata

### faq.json

-≥ 15 rule-based questions

-Each entry includes: {id, category, question, answer}

### comparison_page.json

-Product A details

-Fictional Product B

-Ingredient comparison

-Benefit comparison

-Price comparison

-Final verdict

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

## 🔒 Determinism & Constraints

-The system does not fetch external data.

-All content is derived strictly from the input JSON.

-The pipeline produces repeatable output (excluding timestamps).

-Product B is a deterministic transformation of Product A.

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