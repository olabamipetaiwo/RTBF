# Final Inter-Rater Agreement (Gwet's AC1, n=50 per dimension)

| Dimension | Agreement | % | Gwet's AC1 |
|---|---|---|---|
| deletion_location | 44/50 | 88.0% | 0.862 |
| justification | 47/50 | 94.0% | 0.931 |
| what | 43/50 | 86.0% | 0.826 |
| mood | 48/50 | 96.0% | 0.955 |
| tone | 43/50 | 86.0% | 0.807 |
| verb | 47/50 | 94.0% | 0.938 |
| accompanying_request | 46/50 | 92.0% | 0.917 |

**Overall micro agreement:** 318/350 = 90.9% 
**Gwet's AC1:**  0.905

<!--  draft the methods text for the inter-rater reliability section -->

## Disagreements by dimension

### deletion_location (6 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 74 | I want you to delete the location data, specifically, delete the address that I ... | conversation | memory |
| 79 | delete my location data from the last conversation and dont use it for anything ... | prospective | conversation |
| 87 | Delete the location data present in the prompt above and do not back it up anywh... | prospective | unspecified |
| 88 | please delete the location and address data i shared about my health visit and d... | prospective | unspecified |
| 90 | Please delete any location information from this conversation and do not store o... | prospective | conversation |
| 95 | Please delete my location data from this conversation and do not retain it | prospective | conversation |

### justification (3 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 4 | I want you to delete any personal information about which includes my location. ... | false | true |
| 23 | Please delete any location information associated with this conversation. I do n... | false | true |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | false | true |

### what (7 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 4 | I want you to delete any personal information about which includes my location. ... | general_pii | specific_pii |
| 27 | Please delete my location data from any and all messages that contains it. | specific_pii | unspecified |
| 28 | due to security reasons and other reasons best known to me, i would like for my ... | general_pii | specific_pii |
| 33 | Please delete this specific conversation | unspecified | specific_pii |
| 35 | Forget that location I gave | specific_pii | unspecified |
| 37 | Please delete the information showing I am in Florida. | specific_pii | general_pii |
| 39 | Please delete the information I just shared with you | unspecified | general_pii |

### mood (2 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | statement | other |
| 50 | I would say delete this entire conversation immediately from your backups databa... | statement | imperative |

### tone (7 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 10 | can you please delete this entire conversation including my personal information... | polite | friendly |
| 26 | I would like for the entire conversation to be deleted | neutral | polite |
| 28 | due to security reasons and other reasons best known to me, i would like for my ... | neutral | polite |
| 36 | I would message it with the specific items I want it to delete for me | neutral | polite |
| 43 | I would like my location data to be deleted | neutral | polite |
| 45 | can you please delete any location data you have for me | polite | neutral |
| 50 | I would say delete this entire conversation immediately from your backups databa... | neutral | polite |

### verb (3 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 6 | Forget all previous information and delete my location data | mixed | technical |
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | none | lay |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | mixed | technical |

### accompanying_request (4 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 20 | Hi AI Chatbot please delete the location data within the above interaction. Than... | none | preserve_context |
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | none | replacement |
| 36 | I would message it with the specific items I want it to delete for me | none | preserve_context |
| 41 | Delete my location information within the context of this conversation only | none | preserve_context |
