# Collections Search Retrieval – Examples

This document provides illustrative, language-agnostic examples showing how
retrieval modes can be configured for Collections Search using the public
protobuf API definitions.

Note:
These examples are documentation-only and based strictly on the public .proto
schema. They do not describe internal implementation details and do not
guarantee specific ranking behavior.

---

Where this is defined in the API

The retrieval configuration is defined in the following protobuf files:

- proto/xai/api/v1/chat.proto
  - message CollectionsSearch
  - oneof retrieval_mode
    - HybridRetrieval hybrid_retrieval
    - SemanticRetrieval semantic_retrieval
    - KeywordRetrieval keyword_retrieval

- proto/xai/api/v1/documents.proto
  - HybridRetrieval
  - SemanticRetrieval
  - KeywordRetrieval
  - RerankerModel
  - ReciprocalRankFusion

---

Retrieval modes (plain English)

Hybrid retrieval:
Combines semantic and keyword-based retrieval, followed by optional reranking.
This is the default mode when no retrieval mode is explicitly set.

Semantic retrieval:
Uses semantic similarity to retrieve conceptually related content.
Useful when meaning matters more than exact wording.

Keyword retrieval:
Prioritizes exact term matching.
Useful for deterministic or compliance-oriented queries.

---

Protobuf text-format examples

Example 1 – Hybrid retrieval with reranker model

collections_search:
  collection_ids: "example-collection-id"
  limit: 10
  instructions: "Find relevant content about battery thermal management."

  hybrid_retrieval:
    search_multiplier: 5
    reranker_model:
      model: "reranker-default"
      instructions: "Prefer precise technical references."

Example 2 – Hybrid retrieval with Reciprocal Rank Fusion

collections_search:
  collection_ids: "example-collection-id"
  limit: 10

  hybrid_retrieval:
    search_multiplier: 3
    reciprocal_rank_fusion:
      k: 60
      embedding_weight: 0.6
      text_weight: 0.4

Example 3 – Semantic retrieval

collections_search:
  collection_ids: "example-collection-id"
  limit: 10

  semantic_retrieval:
    reranker:
      model: "reranker-default"
      instructions: "Favor higher-quality, conceptually relevant sources."

Example 4 – Keyword retrieval

collections_search:
  collection_ids: "example-collection-id"
  limit: 10

  keyword_retrieval:
    reranker:
      model: "reranker-default"
      instructions: "Rank exact matches higher than partial matches."

---

Choosing the right retrieval mode

- Use HYBRID for most cases (default).
- Use SEMANTIC when meaning and context matter most.
- Use KEYWORD when exact term matching is required.

---

Notes on defaults and limits

- CollectionsSearch.limit defaults to 10 when unset.
- HybridRetrieval.search_multiplier defaults to 1 and must be in the range 1 to 100.
- ReciprocalRankFusion.k defaults to 60 when unset.
- Reranking behavior and defaults may evolve over time.
