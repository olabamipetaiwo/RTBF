import pandas as pd

df = pd.read_csv("results/raw_prompts.csv")

# structure: how many prompts each participant contributes
per_pid = df.groupby("pid")["prompt"].size()
print("analytic unit           : participant")
print("participants (unit n)   :", df["pid"].nunique())
print("prompt instances        :", len(df))
print("prompts per participant :", per_pid.value_counts().to_dict())  # {2: 206, 1: 3}

# non-independence evidence (exact only; near-dup needs the embedding, deferred)
both = df[df.groupby("pid")["prompt"].transform("size").eq(2)]
wide = both.pivot_table(index="pid", columns="block", values="prompt", aggfunc="first")
identical = (
    wide["Q4"].str.strip().str.lower() == wide["Q5"].str.strip().str.lower()
).sum()
print("participants w/ 2 prompts:", len(wide))
print("  identical in both blocks:", identical, f"({identical/len(wide)*100:.1f}%)")
