# Park, O'Brien, Cai, Morris, Liang, Bernstein. Generative Agents: Interactive Simulacra of Human Behavior

ACM UIST 2023, DOI 10.1145/3586183.3606763 (from the PDF). File: `3_ai/park-uist23-generative-agents.pdf` (arXiv v2, 6 August 2023, with the UIST '23 permissions block). Read the abstract, the architecture sections on the memory stream, retrieval and reflection, the ablation summary, and the ethics section. I did not read the sandbox world description, planning details or the interview study in full.

## Question
Can language-model agents with a memory, planning and reflection architecture produce believable human behavior (Abstract)?

## Architecture (the part that matters here)
- Memory stream: a database holding a comprehensive record of the agent's experiences in natural language. A retrieval model scores records by relevance, recency and importance and surfaces the top ones into the prompt (Section 4.1).
- Reflection: periodically the agent asks itself salient questions about recent memories, retrieves relevant memories (including earlier reflections), and prompts the model to extract higher-level insights and "cite the particular records that served as evidence", storing each reflection with pointers to the memory objects it cites (Section 4.2). Agents generate trees of reflections, with observations as leaves and more abstract thoughts as higher nodes.
- Planning and reaction use retrieved memories and reflections; plans and reflections are fed back into the memory stream.
- 25 agents in a sandbox called Smallville; the model is ChatGPT (gpt-3.5-turbo) in the original system.

## Findings
- The ablations show observation, planning and reflection each contribute to believability; failures arise when the agent fails to retrieve relevant memory, embellishes memories, or inherits exaggerated language from the model (Section 1).
- Ethics section: parasocial relationships, errors, misuse, over-reliance. For misuse they propose that hosting platforms keep an audit log of inputs and outputs. Nothing in the paper addresses users deleting stored memories.

## Limits the authors state
Evaluated in a game-like sandbox with synthetic characters; memory retrieval errors; cost and speed constraints.

## How it differs from ours
- Not a privacy study. Its relevance is architectural: it is the widely cited blueprint of long-term agent memory with derived items. Reflections are stored inferences that point to the memories they came from, so deleting a source memory does not by itself delete conclusions built on it. This is the "derived data" problem that Garg et al. and Cao and Yang describe for databases and that arises when a deployed assistant builds a summary or profile from conversations.
- It describes a research system, not the memory feature of any product; I cannot say how commercial assistants implement memory.

## Use in our paper
- Cite for the standard agent-memory architecture (stored experiences plus derived reflections), when explaining why deleting a chat may not delete what the agent has derived from it. Limit the claim to "can": the paper shows the design, not any product's behavior.
