# Project Documentation — Kasparro Applied AI / Agentic Content System

## 1. Problem Statement
The goal of this assignment is to design and implement a modular, deterministic, agentic content generation system that processes a single product JSON and produces three machine-readable JSON outputs:

1.product_page.json — A structured, block-based product description

2.faq.json — At least 15 fact-grounded, rule-based FAQs

3.comparison_page.json — A deterministic comparison between Product A and a fictional Product B

The system must:

- Use only the information explicitly provided in the input JSON

- Guarantee zero hallucinations

- Produce strict JSON output conforming to fixed schemas

- Follow clean, modular AI engineering practices

- Support deterministic reproducibility (same input → same output)

The system must operate **only on provided input facts**, introduce **no external or invented information**, and follow clear software engineering principles such as modularity, deterministic behavior, maintainability, and testability.  
All outputs must be strictly structured JSON — not prose.

---

## 2. Solution Overview
The implemented solution follows a multi-agent pipeline architecture, where each agent performs a single, isolated responsibility.

The final system consists of:

- Deterministic ingest & validation

- Fact extraction

- Structured content generation

- Strict JSON templating

- A LangChain-powered orchestrator using GPT-4o-mini for reliably structured content

- A robust fallback and sanitization layer to ensure no invalid output

The entire pipeline is coordinated through a central orchestrator (langchain_orchestrator.py), ensuring:

✔ deterministic execution
✔ strict schema compliance
✔ retry & validation behaviour
✔ JSON-only outputs
✔ clean modularity

---

## 3. Scopes & Assumptions
### 3.1 In-Scope
- Process exactly one product JSON per run
- Generate three deterministic JSON outputs
- All agents operate in an explainable, rule-based fashion
- No part of the system may hallucinate content
- No external lookups, no dynamic data sources

### 3.2 Out-of-Scope
- Natural language rewriting or creative text generation
- Non-json or free-form output
- UI, interfaces, or deployment
- Batch processing or multi-product handling  

### 3.3 Assumptions
- Input product follows expected key/value patterns
- Missing optional values are replaced by  deterministic defaults
- Product B must be fictional but strictly derived from Product A
-The same input always yields identical outputs (excluding timestamps)

---

## 4. System Design 

The system follows the Single Responsibility Principle, with each agent transforming structured input into structured output. Modular decomposition allows isolated testing and clarity of intent.

### 4.1 High-Level Architecture
```bash
Input Product JSON
│
▼
[Ingest Agent] → canonical normalized structure
│
▼
[Sanity Agent] → validations, issue detection
│
▼
[Facts Extractor] → atomic fact-bag
│
├──► [FAQ Generator] → 15 deterministic FAQs
│
├──► [Content Block Agent] → summary, benefits, ingredients, usage, safety
│
├──► [Comparison Agent] → fictional Product B + comparison
│
└──► [Template Engine] → structured product_page + faq assembly
│
▼
[Renderer Agent] → writes final JSON artifacts
```
---

### 4.2 Agent Responsibilities (Conceptual)
This section focuses on *responsibility definitions*, not code-level descriptions.

| Agent | Core Responsibility |
|-------|---------------------|
| **IngestAgent** | Load and normalize input JSON into a canonical internal model |
| **SanityCheckAgent** | Validate required fields, check types, and identify issues |
| **FactsExtractorAgent** | Convert product into atomic fact units for reuse |
| **QuestionGeneratorAgent** | Generate ≥15 rule-based factual questions |
| **ContentBlockAgent** | Build modular reusable content blocks (summary, benefits, usage, etc.) |
| **TemplateEngineAgent** | Assemble blocks into page-level structured JSON |
| **ComparisonAgent** | Build fictional Product B and compute structured A–B differences |
| **RendererAgent** | Write JSON outputs to disk with schema-compliant structure |

Each agent adheres to **single responsibility**, enabling composability and isolation.

---

### 4.3 Deterministic Content Generation
To satisfy requirements, the system avoids:
- randomness
- external knowledge
- free-form LLM content
- Every transformation is deterministic, rule-driven, and reversible.

#### Key Deterministic Rules

- Missing fields → deterministic defaults
- Product B:
- Remove last ingredient
    - Increase price by exactly +15%
    - Benefits copied as-is
- Price comparison uses:
    - "A price: X currency"
    - "B price: Y currency"
    - "currency: XYZ"
---

### 4.4 Product B Generation Logic
Product B is created using **only** Product A’s fields

Field	Rule
name	A.name + " (Fictional B)"
ingredients	All A.ingredients minus the last
benefits	Copy A.benefits exactly
price.amount	round(A.amount * 1.15, 2)
price.currency	Same as A

The comparison output includes:
- A-only ingredients/benefits
- B-only ingredients/benefits
- Common overlap
- Price details as strings
- A deterministic verdict
---

### 4.5 Template Engine Design
The template engine ensures:

- strict JSON structure

- required titles are always filled (Summary, Usage Instructions, Safety Information)

- no empty required keys

- correct ordering of blocks

- no malformed structures
---

### 4.6 LangChain Orchestrator — Pipeline Coordinator

langchain_orchestrator.py is the central execution brain of the system.

It ensures:

1. Agent Flow Coordination:

    Maintains the full pipeline order:

    - ingest

    - sanity check

    - extract facts

    - product page generation

    - FAQ generation

    - comparison generation

    - rendering

2. Structured LLM Invocation

    Uses:

    - ChatOpenAI (GPT-4o-mini)

    - Strict JSON-only prompts

    - Deterministic templates

    - No creative language generation

3. JSON Enforcement + Auto-Repair

    The orchestrator includes:

    - A _invoke() wrapper that:

    - retries on invalid JSON

    - trims noisy output

    - enforces JSON-only behavior

    - This prevents invalid or malformed outputs during evaluation.

4. FAQ Sanitization Layer

    The orchestrator includes _sanitize_and_fill_faq() which guarantees:

    ✔ Exactly 15 FAQs<br>
    ✔ No empty answers<br>
    ✔ Answers grounded only in provided facts<br>
    ✔ Backup fallbacks for missing answers<br>
    ✔ Logging raw FAQ output into raw_faq_response.txt for debugging<br>

5. Price Comparison Patch

    Ensures:

    - correct string formatting

    - no numeric arrays

    - deterministic evaluation

6. Rendering

    Orchestrator ensures:

    - correct filenames

    - valid JSON

    - output directory exists

    - This provides a fully reproducible, testable system that can run instantly.

### Pipeline Sequence Diagram 

```mermaid
flowchart TD
    flowchart TD
    A[Input: product.json] --> B[IngestAgent\nload + normalize]
    B --> C[SanityCheckAgent\nvalidate structure]
    C --> D[FactsExtractorAgent\nextract atomic facts]

    %% Branch 1: Product Page
    D --> E[LLM Orchestrator\ngenerate_product_page()]
    E --> M1[JSON Validator\nProductPageSchema]

    %% Branch 2: FAQ
    D --> F[LLM Orchestrator\ngenerate_faq()]
    F --> F2[FAQ Sanitizer + Fallbacks\nensure 15 answers]
    F2 --> M2[JSON Validator\nFAQItem]

    %% Branch 3: Comparison
    D --> G[LLM Orchestrator\ngenerate_comparison()]
    G --> G2[Price Patch Layer\nA_only/B_only/common strings]
    G2 --> M3[JSON Validator\nComparisonSchema]

    %% Rendering Stage
    M1 --> H[RendererAgent\nwrite_outputs()]
    M2 --> H
    M3 --> H

    %% Final Outputs
    H --> O[product_page.json]
    H --> P[faq.json]
    H --> Q[comparison_page.json]

```

## 5. Future Improvements

- Plugin-based agent registry for more flexible extension

- Configurable comparison strategies (beyond ingredients/price/benefits)

- Support for multiple product inputs in a batch pipeline

- JSON schema validation enforcement at output stage

- More advanced template rules (conditional rendering, prioritization)

- Optional natural-language rewrite layer (still deterministic)

## 6. Closing Notes
This system prioritizes:

- Clarity over complexity

- Determinism over randomness

- Modularity over monolithic logic

- Testability over implicit behavior

The implementation is aligned with Kasparro’s focus on clarity, modularity, and robust AI system design, transcending the limitations of simple automation scripts.