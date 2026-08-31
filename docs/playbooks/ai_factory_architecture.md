# Deloitte AI Factory as a Service Architecture

## 1. Architectural Principles
Deloitte's **AI Factory** model industrializes the lifecycle of enterprise AI solutions, transitioning from bespoke, fragile prototypes to scalable, repeatable, and governed micro-services.

```text
       ┌─────────────────────────────────────────────────────────────┐
       │                   Control & Governance Plane                │
       │     (EVD Orchestrator, Policy Engine, Trustworthy Audit)    │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
┌──────────────┐              ┌──────────────┐               ┌──────────────┐
│ Memory Layer │              │ Tool Engine  │               │ Compute & LLM│
│ - Working Context           │ - Schemas    │               │ - API Routing│
│ - Episodic DB               │ - Sandboxes  │               │ - Local vLLM │
│ - Vector / RAG              │ - Circuit Breakers           │ - Quantization│
└──────────────┘              └──────────────┘               └──────────────┘
```

---

## 2. Core Architectural Pillars

### A. Memory Hierarchy
1. **Working Context (Short-Term)**:
   - High-speed token-governed context window.
   - Dynamic sliding window / summarization for multi-turn conversations.
2. **Episodic Memory (Mid-Term)**:
   - Structured JSON logs tracking action-observation trajectories.
   - Preserves state across multi-agent handoffs without replaying complete transcripts.
3. **Semantic Memory (Long-Term / RAG)**:
   - Vector embeddings (HNSW / cosine similarity) indexed over enterprise documentation.
   - Hybrid retrieval (BM25 + Dense Vectors) with cross-encoder re-ranking.

### B. Tool Execution Engine & Deterministic Contracts
* **Strict JSON Schemas**: Every tool must specify JSON Schema Draft 2020-12 parameters.
* **Sandbox Execution**: Commands run sandboxed by default with least-privilege principles.
* **Resilience Patterns**:
  * Exponential backoff: $t_{\text{wait}} = \text{base} \times 2^{\text{retry}} + \text{jitter}$.
  * Circuit breakers: Trip after 3 consecutive failures to prevent cascading latency spikes.

### C. Compute & Token Economics
* **Model Routing**:
  * Complex reasoning & synthesis: High-capacity frontier models (e.g. Gemini 3.7 Flash Pro / High).
  * Rapid extraction & deterministic validation: Low-latency fast models (e.g. Flash Lite / 8B quantized).
* **Token Budget Governance**:
  * Strict upper bounds per turn ($< 4,000$ input tokens, $< 2,000$ output tokens).
  * Caching layers (Redis / MemoryStore) for repetitive queries.
