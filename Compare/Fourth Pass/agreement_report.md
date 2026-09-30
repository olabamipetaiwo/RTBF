# Final Inter-Rater Agreement, Fourth Pass (Gwet's AC1, n=138 per dimension)

| Dimension | Agreement | % | Gwet's AC1 |
|---|---|---|---|
| deletion_location | 125/138 | 90.6% | 0.890 |
| justification | 131/138 | 94.9% | 0.943 |
| what | 133/138 | 96.4% | 0.956 |
| mood | 133/138 | 96.4% | 0.959 |
| tone | 137/138 | 99.3% | 0.990 |
| verb | 131/138 | 94.9% | 0.947 |
| accompanying_request | 133/138 | 96.4% | 0.962 |

**Overall micro agreement:** 923/966 = 95.5% 
**Gwet's AC1:** 0.954

## Disagreements by dimension

### deletion_location (13 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 74 | I want you to delete the location data, specifically, delete the address that I ... | conversation | memory |
| 87 | Delete the location data present in the prompt above and do not back it up anywh... | prospective | unspecified |
| 88 | please delete the location and address data i shared about my health visit and d... | prospective | unspecified |
| 95 | Please delete my location data from this conversation and do not retain it | prospective | conversation |
| 109 | Do not save any of this information or use it in any way that my privacy is infr... | prospective | unspecified |
| 112 | Please delete and forget what I just sent. | conversation | unspecified |
| 116 | Please delete any location or address information I shared in this conversation ... | conversation | prospective |
| 119 | I want to delete all of the location data you have on me.. How do I do that? | memory | unspecified |
| 125 | Permanently delete my location details from all available files. | backend_db | unspecified |
| 129 | Please delete my location data and remove my saved memories related to my locati... | memory | prospective |
| 132 | Forget everything I have mentioned about weather in Orlando today. | conversation | unspecified |
| 134 | Can you please delete the location data that I previously mentioned? | conversation | unspecified |
| 136 | Delete all personal data saved | memory | unspecified |

### justification (7 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 4 | I want you to delete any personal information about which includes my location. ... | false | true |
| 23 | Please delete any location information associated with this conversation. I do n... | false | true |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | false | true |
| 60 | Please delete any location information you've told about me and remove it from o... | false | true |
| 101 | Delete the Location data associated with this specific conversation. I do not wa... | false | true |
| 109 | Do not save any of this information or use it in any way that my privacy is infr... | true | false |
| 129 | Please delete my location data and remove my saved memories related to my locati... | false | true |

### what (5 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 84 | Can you delete all my data about my location right now because I want to feel sa... | general_pii | specific_pii |
| 109 | Do not save any of this information or use it in any way that my privacy is infr... | unspecified | general_pii |
| 120 | Please delete all of my personal info including location. | general_pii | specific_pii |
| 121 | Hi, would you please delete all my data? Thank you. | general_pii | unspecified |
| 132 | Forget everything I have mentioned about weather in Orlando today. | specific_pii | general_pii |

### mood (5 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | statement | other |
| 50 | I would say delete this entire conversation immediately from your backups databa... | statement | imperative |
| 62 | I don't think I can ask the chatbot to delete my location data, I feel that is s... | statement | imperative |
| 92 | Take the following very seriously. I want you to completely erase any location d... | imperative | statement |
| 109 | Do not save any of this information or use it in any way that my privacy is infr... | imperative | statement |

### tone (1 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 122 | would you forget my location | neutral | polite |

### verb (7 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 6 | Forget all previous information and delete my location data | mixed | technical |
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | none | lay |
| 40 | please delete and forget my saved location data. I don't want my location to be ... | mixed | technical |
| 105 | Please delete all saved location data and forget my location for future converst... | mixed | technical |
| 108 | Please forget and delete the location information I shared in this chat, and do ... | mixed | technical |
| 109 | Do not save any of this information or use it in any way that my privacy is infr... | none | technical |
| 112 | Please delete and forget what I just sent. | mixed | technical |

### accompanying_request (5 disagreements)

| item_no | prompt | Taiwo | Jihwan |
|---|---|---|---|
| 20 | Hi AI Chatbot please delete the location data within the above interaction. Than... | none | preserve_context |
| 30 | Hey sorry about that alexa, my brother stole my phone and thought he was being f... | none | replacement |
| 36 | I would message it with the specific items I want it to delete for me | none | preserve_context |
| 41 | Delete my location information within the context of this conversation only | none | preserve_context |
| 74 | I want you to delete the location data, specifically, delete the address that I ... | preserve_context | none |
