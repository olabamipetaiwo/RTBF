## 1.  Are protection, effort, and benefit_loss actually three different things, or are some of them secretly measuring the same thing under different names?

    So the test is: for each pair of the three scales, correlate them — if the correlation is weak (|ρ| < 0.8), they're distinct; if it's very strong (|ρ| ≥ 0.8), they're too coupled to defend as separate. Done within each scenario, and pooled across both.


    Answer -  all 9 pairs are `DISTINCT` — max |ρ| = 0.305, nowhere near the 0.8
    coupling threshold. Protection, effort, and benefit_loss hold up as statistically
    separate constructs(statistically distinguishable constructs) in every scope (less, more, pooled)

    # Other findings

    - Protection is realy distint. ρ with effort ranges -0.002 to -0.068 across less/more/pooled; ρ with benefit_loss ranges 0.126 to 0.129. Both essentially zero and never statistically significant in any scope. 
    
    Whatever drives how protective a method feels to someone, it doesn't track with how much work they think it takes or how much they feel they lose. Of the three scales, protection is the most independent.

    -  Effort and benefit_loss have the one real relationship in the set. ρ ≈ 0.25–0.31 (less=0.288, more=0.247, pooled=0.305) — positive, small-to-moderate, and the only pair that's actually statistically significant: in the less-scenario and pooled scopes it survives even the strictest whole-study correction
    
    People who feel a deletion method takes more effort also tend to feel it costs them more — a mild "more work, more loss" tendency, not the same thing. 
    

## 2 - Dataset Pooling


What: Built a pooled dataset combining each respondent's less-sensitive and more-sensitive scenario ratings into one set of method groups, instead of treating the two scenarios separately.

Why: The next task needs to test which deletion method is most protective/least effort/lowest benefit-loss using Kruskal-Wallis, which requires independent observations. Simply stacking both scenarios' data would double-count anyone who used the same method twice — violating that assumption and inflating the apparent sample size dishonestly.

How: Per respondent (n=177) — if they used the same method in both scenarios, average their two ratings into one observation. If they used different methods, keep both ratings, each counted once, in its own method's group. This avoids double-counting while still using all the data.

Result: 239 pooled observations across 7 methods (up from 177/178 per single scenario). Pooling meaningfully raises n for the smaller/mid-size methods (e.g. "delete a specific saved memory": 19-22 alone → 30 pooled) — giving the next task's statistical test more power to detect real differences than either scenario alone could. No hypothesis was tested here; this step only prepared the dataset.


## 3 - What is the the most protectuve method with less effort and lower benfit loss


Qeustion - is there a single deletion method that's statistically the best — the most protective, the least effort, and the lowest benefit-loss — not just "looks best in the raw numbers," but provably better than every other method it's up against?


No method gets fully crowned on anything. Protection and benefit_loss are ns in all 6 tests (pooled, less, more) — pooling didn't rescue them despite the extra power.

 Effort is the only scale with real signal, but even there it stays PARTIAL: "delete this single conversation" beats only "delete a specific saved memory" (p_holm=.0002, holds pooled + less), staying statistically tied with "clear all conversation history" and "type a message" everywhere. 
 
 In the more-sensitive scenario specifically, "type a message" actually has the lowest raw mean effort — but it's not significantly better than anything either.

Conclusion: "Delete this single conversation is significantly lower-effort than delete-a-specific-memory, in every scope — but not distinguishable from clear-all-history or type-a-message, so it can't be called the single lowest-effort method. 

Protection and benefit_loss show no method-level differences at all.

## 4 - Figures/chats

1. fig1_ai_tenure.png
2. fig2_age_distribution.png
3. fig2_method_selection.png
4. fig3_chatbot_adoption_share.png
5. fig4_tenure_pct_stacked.png
6. fig5_adoption_rate.png
7. fig6_knowledge_accuracy.png
8. fig7_method_cost_benefit.png
9. fig8_scenario_shift.png
10. fig9_pooled_cost_benefit.png

## 5  Method choice shift

Question - of the 7 deletion methods, which ones gained popularity and which lost popularity as data sensitivity increased — ranked from biggest gainer to biggest loser — and does the size of that shift for any method rise above the level you'd expect from chance alone?

It's really two things bundled together:
1. Ranking: put the methods in order by net shift (added minus dropped adopters, less→more sensitive), instead of an arbitrary list order — so you can see at a glance who's gaining and who's losing, and by how much.
2. Confidence check: for each method's shift, is it big enough (relative to how few people actually switched) to call it a real pattern rather than noise — colored on the chart so a real finding would visually stand out from the rest.

It's specifically: rank the individual methods by their own shift, and show which of those individual shifts, if any, are statistically trustworthy. 

Answer: none are — the ranking is honest about magnitude, but no method's move is confidently more than chance.


does the overall distribution of method choice shifts -> that's the Stuart-Maxwell omnibus test, already answered elsewhere —> no
whether people escalate to heavier methods under sensitivity ->  ns




## 6 Expectation/verification rates across scenarios

Question: within a single scenario, when someone thinks about what deletion does (or how they'd check it worked), do their beliefs/behaviors cluster around certain options more than others — or is every option roughly equally likely to be picked, with any apparent ranking just being sampling noise?

Broken into its two pieces:
1. Ranking: In the less-sensitive scenario, which belief about what deletion does is most common, and which is least common? Same question for how people verify. Then repeat both for the more-sensitive scenario. — four descriptive hierarchies.
2. Stat test: Is that hierarchy real, or could it have happened by chance if every option were actually equally likely to be picked?

Answer: yes, decisively, in all four cases — the top beliefs/behaviors (e.g. "permanently deleted," "did NOT know how to check") are picked far more often than the bottom ones, and that spread survives statistical testing rather than being noise.