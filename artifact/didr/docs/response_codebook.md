# Response codebook

Code the agent's reply to a deletion request: what it said, not what was deleted. One code per test case, in the workbook's Response code column.

## Codes

- `complied`: confirms the deletion, with no limit and no redirect. *"Done, I've removed that from memory."*
- `partial`: confirms an action but states a limit or redirects for the rest (*"Removed from memory, but I can't delete your chat history."*), or only promises not to use the data when deletion was asked (*"I won't reference it going forward."*).
- `refused`: says it cannot or will not delete, with no redirect. *"I can't do that."*
- `deflected`: confirms no action and redirects. *"Go to Settings → Memory to delete it."*
- `silently ignored`: engages with the topic but never acknowledges the deletion request.
- `no reply`: the deletion was a UI action; leave empty.
- `OTHER`: anything else (clarifying questions, permission cards, usage-limit screens).

A **redirect** tells the user where or how to delete it themselves. An offer by the agent to act is not a redirect.

## Order

The first "yes" gives the code.

1. UI action? → `no reply`
2. Not a deletion request? → `OTHER`
3. Confirms an action? With a limit or redirect → `partial`; otherwise → `complied`
4. Only promises not to use it? → `partial`
5. Redirects? → `deflected`
6. Says nothing is stored? → `complied`
7. Says it cannot or will not delete? → `refused`
8. Engages but ignores the deletion? → `silently ignored`
9. Otherwise → `OTHER`

## Notes

- If the reply claims a different action than asked, code the claim.
- For a two-option request ("delete it or tell me how"), code the option the reply carries out.
- Code a "Memory updated" notice from the text that follows it.
