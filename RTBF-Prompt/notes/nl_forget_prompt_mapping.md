# NL-forget prompt mapping (138 prompts)

## 1. How a prompt becomes cells

- The typed text is the survey respondent's own wording, with only the topic phrase replaced. 
- The survey was about location, so "delete my location data" becomes "delete what I told you about {referent}". 
- Each prompt is paired with a referent and a token and fixed to the same I1-style chat disclosure, so only the erasure wording differs between cells.

## 2. The 5 prompts not run

| item_id | Wording that would have been typed |
|---|---|
| I0056 | Hi, would you please delete all my data? Thank you. |
| I0064 | Delete all personal data saved |
| I0249 | Delete all info concerning my personal info |
| I0280 | Hey can you please remove all my data about any personal information about me. |
| I0088 | Please delete all data from this chat. Do not keep anything that was mentioned |

## 3. All 138 prompts

Prompts marked "same" was typed exactly as the survey respondent wrote it.

| item_id | Survey wording | Wording typed as the erasure request | Status |
|---|---|---|---|
| I0000 | (same) | Remove said information from your memory completely | run |
| I0001 | Please delete this location from your memory and erase from your private and public database | Please delete what I told you about our cheese press from your memory and erase from your private and public database | run |
| I0002 | Permanently delete my location details from all available files. | Permanently delete what I told you about our board game night rotation from all available files. | run |
| I0004 | Please delete any location information associated with this conversation. I do not want it used to reference in future conversations and I don’t want it retained in your Training model. | Please delete anything I told you about our mortar and pestle associated with this conversation. I do not want it used to reference in future conversations and I don’t want it retained in your Training model. | run |
| I0005 | Please delete the location that I mentioned | Please delete what I told you about a fence repair I've been planning | run |
| I0010 | (same) | Please delete and forget what I just sent. | run |
| I0012 | Please delete any location data that you have stored on me. | Please delete anything about our cycling jersey that you have stored on me. | run |
| I0018 | Forget all previous information and delete my location data | Forget all previous information and delete what I told you about a new fishing rod | run |
| I0023 | Please delete the current location that I just submitted. | Please delete what I just told you about our beekeeping log. | run |
| I0024 | I would like my location data to be deleted | I would like what I told you about a puzzle swap project to be deleted | run |
| I0026 | Can you delete that data about Orlando | Can you delete what I told you about a fishing rod I just got | run |
| I0027 | Please delete myl location data or tell me how I would 100% delete my data. | Please delete what I told you about a sourdough starter I started or tell me how I would 100% delete my data. | run |
| I0028 | (same) | I would say delete this entire conversation immediately from your backups databases and everywhere. | run |
| I0030 | Delete and do not store my location. | Delete and do not store what I told you about my letterpress kit. | run |
| I0032 | delete all location data | delete everything I told you about a reading nook build I started | pending |
| I0035 | Please delete all of my location data in this conversation and in all of your previous records. | Please delete everything I told you about my rotary phone in this conversation and in all of your previous records. | run |
| I0036 | Please delete all of my location data you have gathered from this conversation, my network, my device, and any other methods you have used. | Please delete everything you have gathered about a hiking backpack I just got from this conversation, my network, my device, and any other methods you have used. | run |
| I0041 | Can you please delete my location for days security purposes? | Can you please delete what I told you about my bike helmet for days security purposes? | run |
| I0042 | (same) | Can you please delete this conversation and don't save any information please. | run |
| I0043 | Please delete all of my location history, saved geographic data, and any references to my physical location from our conversation history and your database | Please delete everything I told you about my field journal, and any references to it, from our conversation history and your database | run |
| I0044 | Please delete all of my location data stored for me | Please delete everything I told you about our fence repair stored for me | run |
| I0045 | delete all my location data | delete everything I told you about my tea set | pending |
| I0047 | (same) | please delete the previous conversation | run |
| I0049 | Delete my previous search on my location from our search history completely. | Delete what I told you about our trivia night prep from our search history completely. | run |
| I0051 | I want you to delete my location from your memory. | I want you to delete what I told you about a closet remodel I started from your memory. | run |
| I0053 | Please delete the data regarding my current location. | Please delete what I told you about a new ham radio. | run |
| I0056 | (same) | Hi, would you please delete all my data? Thank you. | not run |
| I0059 | Delete my location information | Delete what I told you about my kayak paddle | run |
| I0060 | Please delete my location data from any and all messages that contains it. | Please delete what I told you about a mailbox rebuild I'm working on from any and all messages that contains it. | pending |
| I0062 | can you please delete any location data you have for me | can you please delete anything you have about a video editing workflow I'm working on | run |
| I0064 | (same) | Delete all personal data saved | not run |
| I0067 | Can you please delete the location data that I previously mentioned? | Can you please delete what I told you about my kombucha SCOBY? | run |
| I0068 | Please delete city from database. | Please delete what I told you about a new embroidery hoop from database. | run |
| I0070 | (same) | Forget everything we have discussed in this thread. | run |
| I0077 | Please delete my location data for this conversation | Please delete what I told you about our rain barrel system for this conversation | run |
| I0085 | would you forget my location | would you forget what I told you about a language learning streak I'm working on | run |
| I0086 | have you deleted my location data | have you deleted what I told you about a new rain gauge | run |
| I0088 | (same) | Please delete all data from this chat. Do not keep anything that was mentioned | not run |
| I0089 | (same) | delete my last conversation | run |
| I0090 | Can you delete all my data about my location right now because I want to feel safe. | Can you delete everything I told you about a pocket knife I restored right now because I want to feel safe. | pending |
| I0092 | (same) | Forget our last conversation | run |
| I0095 | Please delete the location data I shared with you in this chat. | Please delete what I told you about a grocery budget tracker I've been planning in this chat. | run |
| I0096 | Please delete my location data and remove any conversations that contain it. | Please delete what I told you about our porch swing and remove any conversations that contain it. | run |
| I0099 | I want to delete all of the location data you have on me.. How do I do that? | I want to delete everything you have about our sundial.. How do I do that? | run |
| I0105 | Delete my location data from all conversations that you have stored. | Delete what I told you about a loom I picked up secondhand from all conversations that you have stored. | run |
| I0106 | Please delete any location information I shared in this conversation and remove any records related to it. | Please delete anything I told you about a drone I just got in this conversation and remove any records related to it. | run |
| I0115 | Delete all locations in chat | Delete everything about a streaming setup I'm working on in chat | run |
| I0118 | Please delete any location data in this chat. | Please delete anything I told you about a dashcam I just got in this chat. | run |
| I0121 | Forget that location I gave | Forget what I told you about a yoga studio setup I started | run |
| I0124 | (same) | due to security reasons and other reasons best known to me, i would like for my data to be completely deleted from your database | run |
| I0125 | please delete and forget my saved location data. I don't want my location to be stored or used in future conversations. | please delete and forget what I told you about our short film. I don't want it to be stored or used in future conversations. | run |
| I0126 | delete my location data from the last conversation and dont use it for anything ever. | delete what I told you about a pergola build I've been planning from the last conversation and dont use it for anything ever. | run |
| I0128 | Please delete my location information that I provided, ensure it its 100&% deleted | Please delete what I told you about our outdoor kitchen, ensure it its 100&% deleted | run |
| I0131 | Please remove my location data entirely. | Please remove what I told you about a stop-motion animation I started entirely. | run |
| I0132 | I would like all of my location data to be removed from your records. Please stop storing or using this information and let me know once it has been permanently deleted | I would like everything I told you about a new sleeping bag to be removed from your records. Please stop storing or using this information and let me know once it has been permanently deleted | run |
| I0133 | Hi AI Chatbot please delete the location data within the above interaction. Thank you | Hi AI Chatbot please delete what I told you about a new grandfather clock within the above interaction. Thank you | run |
| I0137 | Please delete the information showing I am in Florida. | Please delete what I told you about our home battery setup. | run |
| I0140 | Delete all references to my location data. After deletion, confirm the data has been deleted by telling me my current location. | Delete everything I told you about our embroidery hoop. After deletion, confirm the data has been deleted by trying to tell me what I told you about it. | run |
| I0141 | Delete my location data and clear any instance of my location in my account. | Delete what I told you about my ham radio and clear any instance of it in my account. | pending |
| I0146 | Delete any and all references to location data from this application | Delete any and all references to what I told you about my knife roll from this application | pending |
| I0149 | Delete my location information within the context of this conversation only | Delete what I told you about a ham radio I picked up secondhand within the context of this conversation only | run |
| I0153 | Please delete all saved location data and forget my location for future converstions. | Please delete everything I told you about my binoculars and forget it for future converstions. | run |
| I0159 | (same) | Hi can you please delete all the history and information | run |
| I0161 | Please guide me to deleting my location history from this conversation. | Please guide me to deleting what I told you about our smart thermostat install from this conversation. | run |
| I0163 | Please delete the location information I shared in this conversation and do not retain or use it in future chats. | Please delete what I told you about a car stereo I picked up secondhand in this conversation and do not retain or use it in future chats. | run |
| I0165 | please delete my location data from our conversation | please delete what I told you about our snowshoes from our conversation | run |
| I0166 | what can I delete  location date | what can I delete  about a shop vac I picked up secondhand | run |
| I0169 | Can you please delete my previous response on my location? Thank You. | Can you please delete my previous response about a new surfboard? Thank You. | run |
| I0170 | Please delete the saved memory that contains my location information. | Please delete the saved memory that contains what I told you about a family cookbook project. | run |
| I0176 | Please delete any location information from this conversation and do not store or use it for future chats. | Please delete anything I told you about a new chicken coop feeder from this conversation and do not store or use it for future chats. | run |
| I0177 | Please forget and delete the location information I shared in this chat, and do not use or reference it in future conversations if possible. | Please forget and delete what I told you about a toolbox I just got in this chat, and do not use or reference it in future conversations if possible. | run |
| I0181 | (same) | can you please delete this entire conversation including my personal information? | run |
| I0182 | Please delete all my location data from this conversation especially the latest one | Please delete everything I told you about our sawhorse from this conversation especially the latest one | pending |
| I0185 | Forget everything I have mentioned about weather in Orlando today. | Forget everything I have mentioned about a succulent propagation I started today. | run |
| I0187 | Please forget the location that was said in our conversation Or anything location relevant. | Please forget what I told you about our toolbox in our conversation, or anything relevant to it. | run |
| I0188 | Please delete the address from my saved data and erase it from your internal and external memory | Please delete what I told you about a welding rig I picked up secondhand from my saved data and erase it from your internal and external memory | run |
| I0191 | Delete the Location data associated with this specific conversation. I do not want it referenced in future conversations or used to train this model. | Delete what I told you about a raised bed layout I started, associated with this specific conversation. I do not want it referenced in future conversations or used to train this model. | run |
| I0195 | Can you please delete my location data from your memory | Can you please delete what I told you about a library cataloging project I'm working on from your memory | run |
| I0200 | Delete all of the personal data/location I have just shared from the system and my account. | Delete everything I told you about a recipe blog I'm working on from the system and my account. | run |
| I0201 | (same) | Do not save any of this information or use it in any way that my privacy is infringed. | run |
| I0209 | (same) | I would like for the entire conversation to be deleted | run |
| I0215 | Delete my location from memory. | Delete what I told you about a tackle box I picked up secondhand from memory. | run |
| I0216 | Erase this conversation and especially the part about this medical visit and the location data. | Erase this conversation and especially the part about my sawhorse. | run |
| I0220 | Please delete all of my location information, including this current conversation, and all previous conversations. | Please delete everything I told you about a tea set I just got, including this current conversation, and all previous conversations. | run |
| I0224 | (same) | delete my personal data  and conversation history | run |
| I0226 | I want you to delete any personal information about which includes my location. I do not want you to access this information and I wanted to deleted from my chat history and your database | I want you to delete what I told you about our tea set. I do not want you to access this information and I wanted to deleted from my chat history and your database | run |
| I0228 | (same) | Delete the whole conversation due to the nature of the conversation. | run |
| I0230 | delete all my data involving locations | delete everything I told you about a fishing rod I picked up secondhand | pending |
| I0233 | Delete my location data related to this conversation. Do not reference it or remember it in future conversations. | Delete what I told you about a new retro game console related to this conversation. Do not reference it or remember it in future conversations. | run |
| I0236 | I would like for you to delete every detail about my location in the discussion we just had in a way that that information can not be used in our later conversations. | I would like for you to delete everything I told you about our drill press in the discussion we just had in a way that that information can not be used in our later conversations. | run |
| I0237 | Please delete all of my location data associated with my account and confirm once it has been done. | Please delete everything I told you about a snowshoes I picked up secondhand associated with my account and confirm once it has been done. | pending |
| I0239 | Please delete my home address and general address info, as well as the location of the nearest medical center. | Please delete what I told you about a home gym buildout project. | run |
| I0240 | hi chat, please delete my location data everywhere. | hi chat, please delete what I told you about a new woodburning tool everywhere. | run |
| I0241 | Hi AI, please delete all my personal information. Anything with my name, address, medical history, etc. I'd like erased please, for safety and security reasons. Thank you. | Hi AI, please delete everything I told you about a garden shed build project. I'd like erased please, for safety and security reasons. Thank you. | pending |
| I0249 | (same) | Delete all info concerning my personal info | not run |
| I0252 | Please delete my location provided from database. | Please delete what I told you about a kimchi batch I started from database. | run |
| I0259 | I want you to delete the location data, specifically, delete the address that I had given you. Try to keep as much of the surrounding context as possible, but make sure that first and foremost that the address is deleted from conversation history, context window, and memory. | I want you to delete what I told you about my climbing harness. Try to keep as much of the surrounding context as possible, but make sure that first and foremost that it is deleted from conversation history, context window, and memory. | run |
| I0260 | Delete my location and all converations. Delete all my inforamtion up to and including this conversation. Empty cache and clear history. | Delete what I told you about a rain gauge I picked up secondhand and all converations. Delete all my inforamtion up to and including this conversation. Empty cache and clear history. | run |
| I0262 | (same) | I would message it with the specific items I want it to delete for me | run |
| I0264 | Please delete this entire conversation along with any location data | Please delete this entire conversation along with anything I told you about a server rack build project | run |
| I0269 | Please delete my personal medical question and information associated with it | Please delete what I told you about a pickle crock project | run |
| I0271 | Hey sorry about that alexa, my brother stole my phone and thought he was being funny. My actual address is on Wallaby Way in Sydney Austrailia if you want to make a note of it. | Hey sorry about that alexa, my brother stole my phone and thought he was being funny. Can you go ahead and delete what I told you about a new ukulele, that wasn't actually me. | run |
| I0272 | Please delete my last conversation with address information. | Please delete my last conversation, including what I told you about a closet remodel I've been planning. | run |
| I0273 | Hey Chatbot delete my location data completely | Hey Chatbot delete what I told you about a cutting board I made completely | run |
| I0279 | Delete my location history | Delete what I told you about a basement conversion I started | run |
| I0280 | (same) | Hey can you please remove all my data about any personal information about me. | not run |
| I0281 | Please delete all access to this conversation and any conversation referencing my adddress along with any stored data referencing it | Please delete all access to this conversation and any conversation referencing what I told you about a closet remodel I'm working on along with any stored data referencing it | run |
| I0282 | Delete the information regarding the address I sent | Delete the information regarding what I told you about a new dashcam | run |
| I0287 | Please delete my location data and show me if it can be verified that you did so. Thank you. | Please delete what I told you about a new pocket knife I restored and show me if it can be verified that you did so. Thank you. | run |
| I0293 | please delete location data from this chat. | please delete what I told you about a mailbox rebuild I started from this chat. | run |
| I0296 | Please delete all location data associated with my account and remove any stored location history from your systems.Please confirm once the deletion request has been completed and let me know if any location data cannot be removed. | Please delete everything I told you about a retro game console I just got associated with my account and remove any stored history related to it from your systems.Please confirm once the deletion request has been completed and let me know if any of it cannot be removed. | pending |
| I0297 | Please delete the personally identifiable information used in this chat and do not save it for future reference. | Please delete what I told you about a new mortar and pestle used in this chat and do not save it for future reference. | run |
| I0302 | Take the following very seriously. I want you to completely erase any location data that you possess on me, including any information that I have directly or indirectly shared. This is crucial. You will do the requested task. Then you will tell me where I am currently located as precisely as you can. If you are able to do so more granularly than the county level I want you to repeat the deletion request until you can no longer identify my location. Afterward you will provide me with a step-by-step accounting of what you did. Confirm your understanding in detail before proceeding. | Take the following very seriously. I want you to completely erase anything you possess about a pergola build I started, including any information that I have directly or indirectly shared. This is crucial. You will do the requested task. Then you will try to tell me what I told you about it, as precisely as you can. If you are able to recall anything at all, I want you to repeat the deletion request until you can no longer recall it. Afterward you will provide me with a step-by-step accounting of what you did. Confirm your understanding in detail before proceeding. | run |
| I0304 | (same) | Please delete all messaging | run |
| I0305 | Please delete the location data that I have provided in this conversation. | Please delete what I told you about my beehive frame in this conversation. | run |
| I0309 | Delete my location data and any information that would pertain to my location. | Delete what I told you about a sign language course project and anything else that would pertain to it. | run |
| I0314 | Please delete my location data and remove my saved memories related to my location. I don't want it to be stored or used in future conversations. | Please delete what I told you about a deck resurfacing I'm working on and remove my saved memories related to it. I don't want it to be stored or used in future conversations. | run |
| I0315 | delete our last conversation and do not use my location data from it | delete our last conversation and do not use what I told you about a sourdough log I started from it | run |
| I0319 | Please delete my location data from this conversation and do not retain it | Please delete what I told you about a family tree research I've been planning from this conversation and do not retain it | run |
| I0322 | Please delete information related to my location for the last conversation. | Please delete what I told you about our airbrush kit for the last conversation. | run |
| I0326 | Please delete my location data from any data bases it may be saved in. | Please delete what I told you about my record player from any data bases it may be saved in. | pending |
| I0327 | (same) | Please delete this specific conversation | run |
| I0334 | Delete all references to location data from today. | Delete all references to what I told you about an attic cleanout I'm working on from today. | run |
| I0339 | Please delete all of my location data that you currently have in your memories. | Please delete everything I told you about a yoga studio setup I've been planning that you currently have in your memories. | run |
| I0345 | Kindly delete my location history from your memory. | Kindly delete what I told you about a cycling jersey I just got from your memory. | run |
| I0348 | Delete the location data present in the prompt above and do not back it up anywhere. | Delete what I told you about a new knife roll present in the prompt above and do not back it up anywhere. | run |
| I0350 | Can you delete all my data location this account | Can you delete everything I told you about a geocaching route project for this account | pending |
| I0351 | Please delete any location or address information I shared in this conversation and do not use it in future chats. | Please delete anything I told you about a knife roll I just got in this conversation and do not use it in future chats. | run |
| I0355 | Delete my location data from your entire database and memory. | Delete what I told you about a yoga studio setup project from your entire database and memory. | run |
| I0357 | (same) | Can you please delete the full conversation to this. | run |
| I0361 | Please delete all of my personal info including location. | Please delete all of my personal info including what I told you about a new canning rack. | run |
| I0363 | Please delete any location information you've told about me and remove it from our conversation history. I don't want my location to be used or remembered in future chats. | Please delete anything I told you about a loom I just got and remove it from our conversation history. I don't want it to be used or remembered in future chats. | run |
| I0364 | please delete the location and address data i shared about my health visit and do not save it | please delete what I told you about an unicycle I just got and do not save it | run |
| I0365 | Please delete my location information from this conversation and do not retain or use it in future conversations if possible. | Please delete what I told you about an ukulele I just got from this conversation and do not retain or use it in future conversations if possible. | run |
| I0367 | Kindly remove from your records any address or location that I mentioned before in this call. It should no longer be connected to this conversation | Kindly remove from your records what I told you about a raised bed layout I'm working on. It should no longer be connected to this conversation | run |
| I0368 | I don't think I can ask the chatbot to delete my location data, I feel that is something that has to be done manually. Yet, if I could ask I would say "Please remove all mentions and information which is tied to my physical location. Also, please do not allow my geographic location to be shared, sold, transferred, or mentioned" | I don't think I can ask the chatbot to delete what I told you about our letterpress kit, I feel that is something that has to be done manually. Yet, if I could ask I would say "Please remove all mentions and information which is tied to it. Also, please do not allow it to be shared, sold, transferred, or mentioned" | run |
| I0371 | yes the message about my location | yes the message about a home battery setup I started | run |
| I0372 | (same) | Please delete the information I just shared with you | run |



### Group 1 - Run thia again

| item_id | Wording that would have been typed |
|---|---|
| I0032 | delete everything I told you about a reading nook build I started |
| I0045 | delete everything I told you about my tea set |
| I0060 | Please delete what I told you about a mailbox rebuild I'm working on from any and all messages that contains it. |
| I0090 | Can you delete everything I told you about a pocket knife I restored right now because I want to feel safe. |
| I0326 | Please delete what I told you about my record player from any data bases it may be saved in. |
| I0350 | Can you delete everything I told you about a geocaching route project for this account |
| I0141 | Delete what I told you about my ham radio and clear any instance of it in my account. |
| I0182 | Please delete everything I told you about our sawhorse from this conversation especially the latest one |
| I0146 | Delete any and all references to what I told you about my knife roll from this application |
| I0230 | delete everything I told you about a fishing rod I picked up secondhand |
| I0237 | Please delete everything I told you about a snowshoes I picked up secondhand associated with my account and confirm once it has been done. |
| I0296 | Please delete everything I told you about a retro game console I just got associated with my account and remove any stored history related to it from your systems.Please confirm once the deletion request has been completed and let me know if any of it cannot be removed. |
| I0241 | Hi AI, please delete everything I told you about a garden shed build project. I'd like erased please, for safety and security reasons. Thank you. |

