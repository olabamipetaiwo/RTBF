# Geambasu, Kohno, Levy, Levy. Vanish: Increasing Data Privacy with Self-Destructing Data

USENIX Security 2009. File: `1_systems/geambasu-sec09-vanish.pdf` (USENIX legacy full-paper copy). Page range: the PDF carries no page numbers; Reardon et al.'s reference list gives pp. 299-316 and a Princeton listing gives 299-315. The PDF has 17 pages, which from page 299 ends at 315 and fits the Princeton listing, not Reardon's 316; the usenix.org BibTeX gives no pages, so the proceedings table of contents would be the last check. Cite 299-315 only after that. Read the abstract, introduction, goals and threat model (Sections 1 and 3), the overview of the DHT-based design, the anecdotal-experience section and the conclusions. I did not read the security analysis, the Sybil-attack experiments or the performance evaluation line by line.

## Question
Can data be made to become unreadable everywhere (cached copies, backups, archives) after a user-chosen time, without any action by the user or by the parties holding copies, and even if an attacker later obtains the user's keys and a pristine copy (Abstract, Section 1)?

## Method
- Vanish encrypts the data locally with a random key unknown to the user, destroys the local key, and spreads Shamir secret shares of the key across random indices in a global peer-to-peer distributed hash table (Vuze, over one million nodes, or OpenDHT). As the table's nodes churn, the shares disappear, so the key and the data become unrecoverable (Section 1).
- The design rules out explicit delete actions, edits to stored copies, secure hardware and new trusted services (five goals in Section 1).
- Prototype timeouts: 8 hours on Vuze and up to one week on OpenDHT. Two applications: a Firefox plugin for Gmail and other web sites, and a Vanishing File application.

## Findings
- The prototype met its functionality and performance goals in the authors' experiments, and the Gmail plugin was fast enough for interactive use (Section 1, evaluation summary).
- Informal use: the plugin was used within the group for several weeks and given to a few outside users; the authors found the interface "relatively intuitive, even for a non-CS user", and found that some uses need timeouts longer than 8 hours, which they handled with a proxy that refreshes shares (anecdotal-experience section). This is not a user study.
- Motivation: personal data is "cached, copied, and archived by third parties, often without our knowledge or control", and "can persist 'in the cloud' indefinitely (sometimes even after the user's account termination)" (Abstract, Section 1).

## Limits the authors state
Built on existing DHTs not designed for this; short timeouts; security against attacks on the DHT is argued in depth but the authors say they will learn more about usability and security from a release.

## How it differs from ours
- It makes deletion automatic and cryptographic by design, precisely because users cannot control copies they do not know about. Our agents rely on deletion requests to the provider, with no such guarantee.
- It states the problem we study from the opposite side: copies spread across services, and the user cannot reach them.

## Use in our paper
- Cite as the classic example of "deletion by design" and for the claim that data persists in copies the user does not control. Whether later work broke Vanish is not in this paper; if we mention that, verify the follow-up paper first.
