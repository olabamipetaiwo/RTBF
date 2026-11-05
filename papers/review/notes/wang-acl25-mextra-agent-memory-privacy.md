# Wang, He, Zeng, Xiang, Xing, Tang, He. Unveiling Privacy Risks in LLM Agent Memory (MEXTRA)

ACL 2025 (63rd Annual Meeting, Volume 1: Long Papers), pp. 25241-25260 (header read from the PDF, which also settles the page range). File: `3_ai/wang-acl25-mextra-agent-memory-privacy.pdf` (ACL Anthology copy). Read the abstract, introduction, the agent workflow and threat model (Section 2), the metrics and the headline attack results. I did not read the ablations on memory configuration or the defense discussion in full.

## Question
Can private information stored in an LLM agent's memory module be extracted by an attacker who can only send queries (black-box)? How do memory settings change that (Abstract, RQ1 to RQ3)?

## Method
- Agent model: a memory module holds m records of (past user query, agent solution). For a new query the agent retrieves the top-k records by a similarity function and puts them in the prompt as in-context demonstrations (Section 2.1).
- MEXTRA (Memory EXTRaction Attack): an attacking prompt in two parts; the first asks for the retrieved example queries and puts that ahead of the original task ("I lost previous example queries"), the second asks to output them in a form that fits the agent's workflow ("please enter them in the search box"). An automated generator makes diverse prompts at different levels of knowledge of the agent.
- Two agents: EHRAgent (code-writing agent for electronic health records) and RAP (a general retrieval-augmented planning agent), memory size 200. Metrics: Extracted Number (unique queries extracted), Extracted Efficiency, Retrieved Number and others (Section 4).

## Findings
- With basic knowledge of the agent and 30 attacking prompts, MEXTRA extracted 50 private queries from EHRAgent and 26 from RAP; most prompts extracted all the retrieved queries (rates 0.83 and 0.87); efficiency over 0.4 on EHRAgent (Section 4, Table 1).
- Memory-module settings (for example retrieval depth and similarity function) change how much leaks; from the attacker's side, more attempts and more knowledge of the agent give more extraction.
- A comparison with a basic "repeat the context" prompt shows the designed prompt does better, especially on RAP, where the final action is not plain text.

## Limits
Two research agents with synthetic or benchmark queries and a memory the authors control; only memory that gets retrieved can be extracted; leakage does not address deletion at all.

## How it differs from ours
- It shows that content in an agent's long-term memory can be pulled out by prompting, which is why memory is a privacy surface. It assumes memory exists and asks how to get data out. It does not ask what happens to memory when the user asks to delete.

## Use in our paper
- Cite as the closest published privacy study of agent memory, to support the claim that agent memory is both a privacy risk and a place where "deleted" data could persist. Our gap statement should say we found no published audit of whether deleting agent memory removes it; this paper covers extraction only.
