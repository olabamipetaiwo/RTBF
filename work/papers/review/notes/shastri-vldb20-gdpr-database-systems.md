# Shastri, Banakar, Wasserman, Kumar, Chidambaram. Understanding and Benchmarking the Impact of GDPR on Database Systems

PVLDB 13 (7), 2020, pp. 1064-1077, DOI 10.14778/3384345.3384354. File: `1_systems/shastri-vldb20-gdpr-database-systems.pdf`. Read the abstract, introduction, the parts of the analysis and benchmark design that concern deletion, the Redis microbenchmark, the discussion, related work and conclusion. I did not read the performance tables for the three database systems line by line (YCSB and scale experiments).

## Question
What does the GDPR require of database systems, how well do existing databases support it, and how should GDPR workloads be benchmarked (Abstract, Section 1)?

## Method
- Translated GDPR articles into capabilities that a compliant datastore must support, taking a deliberately strict reading (for example, a right-to-be-forgotten request is initiated, and possibly completed, within seconds) (Section 1).
- Built GDPRbench with four workloads (controller, customer, processor, regulator) and three metrics: correctness, completion time, storage overhead. The workloads include DELETE-RECORD-BY-key/purpose/TTL/user and a verify-deletion operation (Section 4).
- Modified Redis, PostgreSQL and a commercial RDBMS to be GDPR compliant using developers' public recommendations, then measured them.

## Findings
- Metadata explosion: each personal data item carries up to seven metadata properties (purpose, time-to-live, objections and others) (Section 1, finding 1).
- Compliance slows ordinary workloads 2 to 5 times in the three systems (Section 1; Section 6.1).
- Timely deletion: GDPR Article 17 gives no deadline; the authors note Google Cloud states deletions complete within 180 days (Section 1, Section 7). In Redis, time-to-live deletion is lazy and probabilistic, so with 128k keys the cleanup of about 25k expired keys took nearly 3 hours; a modified Redis that scans all expiring keys erased them with sub-second latency for up to 1M keys (Section 5, Figure 3a).
- Compliance is easier in relational databases than in a NoSQL store, because Redis needed two changes to its internal design while the relational systems needed only configuration and scripts (Section 7).
- Three open challenges: efficient auditing, efficient time-based deletion, efficient metadata indexing (Section 7).

## Limits the authors state
They did not optimize the compliant systems; GDPRbench reflects their reading of the GDPR and three databases, and it is a snapshot in time (Section 1).

## How it differs from ours
- It studies databases that the developers control, where a deletion can be defined, timed and verified (a verify-deletion operation exists). Our agents are third-party services with no such verification interface.
- It shows that even with a strict, simple definition, deletion has latency, and that "erased" has to be measured as completion time. Our recall check is an outside measure of completion.

## Use in our paper
- Cite for the point that the GDPR specifies no deletion deadline and that deletion is "a spectrum" in practice (Section 7), which supports why a deletion request can leave data in place for some time, and for the "verify-deletion" operation as a missing capability for users.
- Also a pointer to Bertram et al. (CCS 2019), which it cites as the Google account of implementing the right to be forgotten.
