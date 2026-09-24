\# Collections Search Retrieval – Examples



This document provides illustrative, language-agnostic examples showing how

retrieval modes can be configured for Collections Search using the public

protobuf API definitions.



> Note:

> These examples are documentation-only and based strictly on the public `.proto`

> schema. They do not describe internal implementation details and do not

> guarantee specific ranking behavior.



---



\## Where this is defined in the API



The retrieval configuration is defined in the following protobuf files:



\- `proto/xai/api/v1/chat.proto`

&nbsp; - `message CollectionsSearch`

&nbsp; - `oneof retrieval\_mode`

&nbsp;   - `HybridRetrieval hybrid\_retrieval`

&nbsp;   - `SemanticRetrieval semantic\_retrieval`

&nbsp;   - `KeywordRetrieval keyword\_retrieval`



\- `proto/xai/api/v1/documents.proto`

&nbsp; - `HybridRetrieval`

&nbsp; - `SemanticRetrieval`

&nbsp; - `KeywordRetrieval`

&nbsp; - `RerankerModel`

&nbsp; - `ReciprocalRankFusion`



---



\## Retrieval modes (plain English)



\- \*\*Hybrid retrieval\*\*  

&nbsp; Combines semantic and keyword-based retrieval, followed by optional reranking.  

&nbsp; This is the default mode when no retrieval mode is explicitly set.



\- \*\*Semantic retrieval\*\*  

&nbsp; Uses semantic similarity to retrieve conceptually related content.  

&nbsp; Useful when meaning matters more than exact wording.



\- \*\*Keyword retrieval\*\*  

&nbsp; Prioritizes exact term matching.  

&nbsp; Useful for deterministic or compliance-oriented queries.



---



\## Protobuf text-format examples



The examples below use protobuf text format to remain language-agnostic and avoid

binding to a specific SDK or client implementation.



---



\### Example 1 — Hybrid retrieval with reranker model



```text

collections\_search: {

&nbsp; collection\_ids: "example-collection-id"

&nbsp; limit: 10

&nbsp; instructions: "Find relevant content about battery thermal management."



&nbsp; hybrid\_retrieval: {

&nbsp;   search\_multiplier: 5



&nbsp;   reranker\_model: {

&nbsp;     model: "reranker-default"

&nbsp;     instructions: "Prefer precise technical references."

&nbsp;   }

&nbsp; }

}

Example 2 — Hybrid retrieval with Reciprocal Rank Fusion

text



collections\_search: {

&nbsp; collection\_ids: "example-collection-id"

&nbsp; limit: 10



&nbsp; hybrid\_retrieval: {

&nbsp;   search\_multiplier: 3



&nbsp;   reciprocal\_rank\_fusion: {

&nbsp;     k: 60

&nbsp;     embedding\_weight: 0.6

&nbsp;     text\_weight: 0.4

&nbsp;   }

&nbsp; }

}

Example 3 — Semantic retrieval

text

collections\_search: {

&nbsp; collection\_ids: "example-collection-id"

&nbsp; limit: 10



&nbsp; semantic\_retrieval: {

&nbsp;   reranker: {

&nbsp;     model: "reranker-default"

&nbsp;     instructions: "Favor higher-quality, conceptually relevant sources."

&nbsp;   }

&nbsp; }

}

Example 4 — Keyword retrieval

text



collections\_search: {

&nbsp; collection\_ids: "example-collection-id"

&nbsp; limit: 10



&nbsp; keyword\_retrieval: {

&nbsp;   reranker: {

&nbsp;     model: "reranker-default"

&nbsp;     instructions: "Rank exact matches higher than partial matches."

&nbsp;   }

&nbsp; }

}

Choosing the right retrieval mode

Use HYBRID for most cases (default).



Use SEMANTIC when meaning and context matter most.



Use KEYWORD when exact term matching is required.



Notes on defaults and limits

CollectionsSearch.limit defaults to 10 when unset.



HybridRetrieval.search\_multiplier defaults to 1 and must be in the range \[1, 100].



ReciprocalRankFusion.k defaults to 60 when unset.



Reranking behavior and defaults may evolve over time.

