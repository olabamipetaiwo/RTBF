# Sarkar, Papon, Staratzis, Athanassoulis. Lethe: A Tunable Delete-Aware LSM Engine

ACM SIGMOD 2020, pp. 893-908, DOI 10.1145/3318464.3389757. File: `1_systems/sarkar-sigmod20-lethe.pdf`. Read the abstract, introduction (including the deletion-as-privacy motivation), the data-privacy part of Section 3.2.4 and the conclusion. I did not work through the compaction design (FADE), the physical layout (KiWi) or the evaluation plots in detail; the performance figures below come from the abstract.

## Question
In log-structured merge (LSM) key-value stores, a delete only inserts a tombstone, and nothing bounds how long the old data stays on disk. Can an engine guarantee that a deletion becomes persistent within a user-set time, without hurting reads (Abstract, Section 1)?

## Method
A new storage engine, Lethe, with two parts (Section 1): FADE, delete-aware compaction policies that enforce a user-defined delete persistence threshold, and KiWi, a physical layout that supports efficient deletes on a secondary delete key (for example a timestamp). Compared with RocksDB and other LSM engines on read throughput, space amplification and write amplification.

## Findings
- State-of-the-art LSM engines give no guarantee on delete persistence latency; it is "potentially unbounded", and current fixes use costly full-tree compaction (Abstract, Section 1).
- Lethe supports any user-defined persistence threshold with 1.17 to 1.4 times higher read throughput and 2.1 to 9.8 times lower space amplification, at a 4% to 25% increase in write amplification (Abstract).
- Privacy motivation (Section 1, "Deletion as privacy"): an unbounded delete latency "may lead to a breach of privacy". They cite a report that Twitter retained user messages years after deletion, even after account deactivation. With GDPR and CCPA rights such as the right to be forgotten, "persistent deletion within a fixed threshold is critical".

## Limits the authors state
Benefits and costs depend on workload and tuning; write amplification rises; the work is about the storage layer of one family of engines.

## How it differs from ours
- Concerns where a deleted record physically stays inside a storage engine, which a service operator controls. Our agents expose no such engine; we observe the effect at the conversation level.
- It supplies a concrete mechanism for why "deleted" data can persist: a logical delete (tombstone) hides the entry, while the old data remains until later maintenance. This is a plausible technical reading of recall success after a deletion, but we cannot confirm that any agent works this way (Related Work should present it as an example of the general mechanism, not as an explanation of our results).

## Use in our paper
- Cite for the logical-versus-persistent deletion distinction and the unbounded persistence latency, in the "Data deletion in computer systems" group, alongside Shastri et al. (the GDPR gives no deletion deadline) and Reardon et al. (unlinking leaves content).
- Quote candidate for the Twitter report: it is a secondhand example; if we use it, cite the original report only after verifying it.
