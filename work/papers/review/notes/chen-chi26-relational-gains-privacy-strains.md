# Chen, Molina, Liao, Snyder. Relational Gains, Privacy Strains: Exploring Users' Perceptions and Experiences with ChatGPT's Memory Feature

ACM CHI 2026 (April 13-17, 2026, Barcelona), 17 pages, DOI 10.1145/3772318.3791635. File: `4_users/chen-chi26-relational-gains-privacy-strains.pdf` (publisher PDF, downloaded by the user through the UCF library). Authors and affiliations confirmed from the PDF first page (Oregon State, Michigan State, Georgia, NJIT). Read the abstract, introduction, research questions, method, the unforgetfulness and mental-model-shift results (RQ1, RQ2), the transparency and control needs (RQ3) and the limitations. I skimmed the relational-benefit sections and the design-implication tables.

## Question
How do users perceive ChatGPT's memory feature compared with human memory (RQ1), how do their mental models change after they see what ChatGPT remembers about them (RQ2), and what do they want changed (RQ3)?

## Method
- Semi-structured Zoom interviews with 20 ChatGPT users recruited on Prolific, US residents aware of the memory feature (12 male, 8 female, ages 19 to 54), after a pre-interview questionnaire on ChatGPT use (Section 3).
- In the interview, participants viewed what ChatGPT stored about them, saw two short OpenAI tutorial videos (viewing and managing memory; turning memory on and off), and were asked, among other things, "Do you think ChatGPT can truly forget users' memories?" Interviews were transcribed and analysed thematically.

## Findings
- Participants saw ChatGPT's memory as different from human memory in four ways: unforgetfulness, detailedness, accuracy and lack of emotion (Section 4.1).
- Perceived unforgetfulness led to doubts that deletion works. P20: "It's forgotten to me, but I think it is still used by ChatGPT in some forms." P14: "the question is, is it done or not? I don't know." P3 did not believe deleting chat histories protects privacy: "I have a feeling that they still have it in the database somewhere" (Section 4.1.1).
- Most participants had a negative expectancy violation on seeing what ChatGPT remembered (Abstract). One account of a possible deletion failure: P3 had accidentally cleared all memories and started again a week earlier, yet ChatGPT still had her cat's information; she thought it "should have already been deleted" (Section 4.2). This is a participant's report, not a verified failure.
- Users asked for visibility, accessibility, transparency and control. P4 said that even with memory turned off she "cannot be 100% certain" ChatGPT is not retaining information, and asked for "some sort of actual proof" that memory was removed (Section 4.3.2).
- The authors state it is "unknown whether AI can truly forget, even though the memory feature allows users to delete or clear ChatGPT's memory" (Section 2.1).

## Limits the authors state
One platform (ChatGPT), whose memory feature keeps changing; a one-time study; US Prolific sample of current ChatGPT users; 20 interviewees (Limitations, Section 5.6).

## How it differs from ours
- It collects what users believe and experienced. Participants described a possible deletion failure (P3) and asked for proof, but no one tested the feature. We test it, across six platforms, with planted facts and recall checks.
- It covers ChatGPT's memory only. Our design covers several deletion methods per platform and compares them with each platform's documentation.

## Use in our paper
- This is the closest user-side prior work to ours on memory deletion. Cite it for: (a) users doubt deletion of AI memory and ask for proof, (b) a first-hand account of a possible failure that our recall check could confirm or refute, and (c) the authors' own statement that whether AI can truly forget is unknown.
- It changes Gap 4: user expectations of memory deletion have now been studied qualitatively for ChatGPT memory (20 interviews), so the gap is "never compared with observed behavior", not "never studied". Group 5 note updated to say so.
- Do not describe P3's case as evidence of failure. Describe it as a report.
