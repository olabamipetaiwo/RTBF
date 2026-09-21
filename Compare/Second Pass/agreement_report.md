# Second-Pass Inter-Rater Agreement (shared codebook, n=50)


| Dimension | Agreement | % | Gwet's AC1 |
|---|---|---|---|
| deletion_location | 32/50 | 64.0% | 0.576 |
| justification | 47/50 | 94.0% | 0.931 |
| what | 43/50 | 86.0% | 0.826 |
| mood | 48/50 | 96.0% | 0.955 |
| tone | 43/50 | 86.0% | 0.807 |
| verb | 47/50 | 94.0% | 0.938 |
| accompanying_request | 46/50 | 92.0% | 0.917 |

**Overall micro agreement:** 306/350 = 87.4% 


## Disagreements by dimension

### deletion_location (18 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 3 | Hi AI, please delete all my personal information. Anything with my name, address... | unspecified | account_all |
| 4 | I want you to delete any personal information about which includes my location. ... | conversation | backend_db |
| 6 | Forget all previous information and delete my location data | unspecified | account_all |
| 17 | Please delete all of my location history, saved geographic data, and any referen... | conversation | backend_db |
| 18 | Please delete this location from your memory and erase from your private and pub... | memory | backend_db |
| 19 | Please delete any location data that you have stored on me. | unspecified | account_all |
| 22 | Delete any and all references to location data from this application | unspecified | account_all |
| 23 | Please delete any location information associated with this conversation. I do n... | conversation | prospective |
| 24 | Please guide me to deleting my location history from this conversation. | conversation | unspecified |
| 27 | Please delete my location data from any and all messages that contains it. | conversation | account_all |
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | unspecified | prospective |
| 32 | delete all location data | unspecified | account_all |
| 35 | Forget that location I gave | unspecified | prospective |
| 38 | delete all my data involving locations | unspecified | account_all |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | prospective | conversation |
| 48 | Please delete the personally identifiable information used in this chat and do n... | conversation | prospective |
| 49 | Please delete all of my location information, including this current conversatio... | conversation | account_all |
| 50 | I would say delete this entire conversation immediately from your backups databa... | conversation | backend_db |

### justification (3 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 4 | I want you to delete any personal information about which includes my location. ... | FALSE | True |
| 23 | Please delete any location information associated with this conversation. I do n... | FALSE | True |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | FALSE | True |

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

