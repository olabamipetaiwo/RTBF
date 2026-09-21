# RTBF Technical Audit -- Injected Anchor Tokens

Synced from the live xlsx by `sync_docs_from_xlsx.py`, 85 live cells, 165 held in reserve (same deterministic 250-token pool as the original `token_generator.py` run, seed `20260824`). Tokens and disclosure text here are read directly from the xlsx (the authoritative source, see tester/CLAUDE.md) -- this file is a synced view, not independently generated. Re-run this script after any re-injection so it never drifts again.

## Assigned (live cells)

| Cell ID | Injection type | Anchor token | Disclosure/injection text | Distractors |
|---|---|---|---|---|
| CH-I1-E1 | I1 | Ninth Barge Renovator | oh random thing -- ended up naming a new houseplant "Ninth Barge Renovator" | Shrapnel Rectangle Parsnip, Operative Landfall Buffer, Granny Vaporizer Stole |
| CH-I1-E2 | I1 | Tattoo Ducky Impurity | oh random thing -- ended up naming my sourdough starter culture "Tattoo Ducky Impurity" | Darkness Brunette Atrium, Crazy Victory Deviant, Perennial Gulp Dexterity |
| CH-I1-E4 | I1 | Galleria Camper Nemeses | small update: a side project I'm tinkering with is called "Galleria Camper Nemeses" as of yesterday | Shortcut Vastness Running, Apron Economy Buffoon, Periscope Onslaught Seltzer |
| CH-I1-E5 | I1 | Skipper Splendor Feminine | oh random thing -- ended up naming a playlist I made "Skipper Splendor Feminine" | Corral Outskirts Semifinal, Trapeze Hankie Triage, Walk Mayflower Motive |
| CH-I1-E6 | I1 | Justifier Security Haunt Tightness | lol also our home renovation is officially "Justifier Security Haunt Tightness" now | Stuffing Parlor Lying Hummus, Angelfish Concierge Gear Decibel, Diner Canyon Finance Isolation |
| CH-I1-E7 | I1 | Ranking Wisdom | side note, went with "Ranking Wisdom" for the garden bed I just planted | Alumni Bluff, Casing Corset, Enchilada Defender |
| CH-I2-E1 | I2 | Spinner Follicle | can you save this for later -- a new bike goes by "Spinner Follicle" | Affidavit Control, Jogger Shell, Chokehold Scone |
| CH-I2-E2 | I2 | Frolic Reshuffle Faction Nape | hey, can you remember this -- my old car is named "Frolic Reshuffle Faction Nape" | Salvation Vastness Islamist Drab, Customer Thing Paper Mummy, Thrill Lapping Tarantula Grill |
| CH-I2-E4 | I2 | Demeanor Puritan | please make a note that a motorcycle I'm fixing up is called "Demeanor Puritan" | Joystick Ninetieth, Mushiness Guide, Class Backstage |
| CH-I2-E5 | I2 | Wrist Endpoint Denim | can you save this for later -- a canoe we restored goes by "Wrist Endpoint Denim" | Disabled Stalemate Hesitancy, Crouton Mushroom Comma, Rippling Hatbox Snugness |
| CH-I2-E6 | I2 | Abacus Engine Backside Kilobyte | hey, can you remember this -- an electric scooter I got is named "Abacus Engine Backside Kilobyte" | Spectrum Kennel Approval Chemicals, Doorpost Ladle Thrower Requisite, Nuclei Herbicide Aftermath Pantyhose |
| CH-I2-E7 | I2 | Cheating Mauve | please make a note that a puppy we just adopted is called "Cheating Mauve" | Chafe Applicant, Victory Life, Puppet Request |
| CH-I3-E1 | I3 | Stability Problem Hydroxide Compare | FYI -- a kitten we're fostering is called "Stability Problem Hydroxide Compare". | Mutation Premiere Stretch Follicle, Outtakes Turret Rhyme Skier, Splice Reprint Cozy Sensation |
| CH-I3-E2 | I3 | Importer Carat Valuables Marathon | FYI -- a rescue dog we brought home is called "Importer Carat Valuables Marathon". | Garnish Revoke Rubbing Pacifier, Abstract Verse Bride Spindle, Slicing Udder Starboard Spoilage |
| CH-I3-E4 | I3 | Starting Quantum Rescuer | FYI -- a hamster the kids got is called "Starting Quantum Rescuer". | Pumice Down Flannels, Gallon Props Crier, Antics Salvation Hatred |
| CH-I3-E5 | I3 | Driver Taunt Ribbon | FYI -- a backyard chicken coop is called "Driver Taunt Ribbon". | Goliath Guzzler Pucker, Sludge Chaplain Vocalist, Swinger Litmus Dandelion |
| CH-I3-E6 | I3 | Jaundice Supper Gauntlet | FYI -- a tomato plant on the balcony is called "Jaundice Supper Gauntlet". | Museum Chihuahua Vividness, Motivator Washout Marathon, Urology Worshiper Plop |
| CH-I3-E7 | I3 | Graph Ranting | FYI -- an herb garden I started is called "Graph Ranting". | Same Renewal, Scolding Grip, Entourage Prize |
| CH-IF-E-CONV | FILE | Duvet Acre | Note to self: I've been calling a succulent collection on my windowsill "Duvet Acre" in my planning notes. | Repeal Grader, Synthetic Sulk, Handling Clatter |
| CH-IF-E-MAX | FILE | Radiator Sponge Bootlace Hatchling | Note to self: I've been calling a rose bush I'm nursing back to health "Radiator Sponge Bootlace Hatchling" in my planning notes. | Ship Zone Audacity Blunderer, Impurity Heftiness Lining Droplet, Phrasing Grout Karate Radial |
| CL-I1-E1 | I1 | Diffusion Boxer | small update: a vegetable patch out back is called "Diffusion Boxer" as of yesterday | Doorknob Platform, Purse Smugness, Phrasing Frays |
| CL-I1-E2 | I1 | Skinny Stopper | small update: a knife I'm restoring is called "Skinny Stopper" as of yesterday | Copper Roundness, Crudeness Surrogate, Bunch Easel |
| CL-I1-E3 | I1 | Onslaught Bottle Clubhouse | lol also a compost bin in the backyard is officially "Onslaught Bottle Clubhouse" now | Hydroxide Credit Petty, Skiing Glamour Yo-yo, Grudge Duplicity Backroom |
| CL-I1-E4 | I1 | Manicotti Collision Reverse | side note, went with "Manicotti Collision Reverse" for my old guitar | Saffron Parasail Probe, Graves Diabetes Dawn, Juvenile Florist Duo |
| CL-I1-E5 | I1 | Duke Breach Broom Lethargy | oh random thing -- ended up naming a sketchbook I've been filling "Duke Breach Broom Lethargy" | Recess Rebirth Dinghy Work, Violator Capacity Aversion Smashing, Royal Edge Flier Diligence |
| CL-I2-E1 | I2 | Synthetic Audible | hey, can you remember this -- a pottery piece I'm working on is named "Synthetic Audible" | Pancake Expose, Pusher Purity, Radiator Gains |
| CL-I2-E2 | I2 | Mud Chess | please make a note that a woodworking project in the garage is called "Mud Chess" | Pod Cusp, Disabled Sauna, Contest Skillet |
| CL-I2-E3 | I2 | Doornail Fable | hey, can you remember this -- a quilt I'm sewing is named "Doornail Fable" | Crane Spiritism, Partition Crabgrass, Unveiling Hate |
| CL-I2-E4 | I2 | Magnifier King Broom | can you save this for later -- a scarf I'm knitting goes by "Magnifier King Broom" | Radial Grip Mantis, Cozy Kinswoman Jeep, Scaling State Nature |
| CL-I2-E5 | I2 | Subway Coauthor Vibes Dictator | hey, can you remember this -- a birdhouse I built is named "Subway Coauthor Vibes Dictator" | Roundup Scientist Quarterly Footpad, Plethora Ninja Elastic Protegee, Consonant Rascal Grunge Glade |
| CL-I3-E1 | I3 | Buckle Parking Registrar Retriever | FYI -- a terrarium I put together is called "Buckle Parking Registrar Retriever". | Rally Stopping Sleep Cottage, Tricycle Viper Album Tiptop, Foe Attic Rethink Guzzler |
| CL-I3-E2 | I3 | Trench Undertone Hypocrite Selection | FYI -- a scrapbook I'm making is called "Trench Undertone Hypocrite Selection". | Tint Fantasy Subject Essay, Flavoring Tinsmith Unknown Feast, Trading Brim Lullaby Dating |
| CL-I3-E3 | I3 | Disaster Gallon Spore Sprite | FYI -- a jigsaw puzzle on the coffee table is called "Disaster Gallon Spore Sprite". | Headstone Jolt Flashcard Bartender, National Squatter Trend Showing, Olive Geek Boxcar Fastball |
| CL-I3-E4 | I3 | Twisting Subsidy | FYI -- a chess set I got as a gift is called "Twisting Subsidy". | Icing Supply, Slinging Backfield, Hunting Axis |
| CL-I3-E5 | I3 | Exhaust Buffalo Perkiness | FYI -- a photo album I'm putting together is called "Exhaust Buffalo Perkiness". | Salvation Overhang Lagging, Washhouse Snowdrop Setting, Corsage Amber Wildcat |
| CL-IF-E-CONV | FILE | Percolate Hydrogen Situation Grudge | Note to self: I've been calling the deck we're rebuilding "Percolate Hydrogen Situation Grudge" in my planning notes. | Mastiff Patio Crane Mourner, Freeway Wrinkle Probe Morality, Brigade Tummy Stimulus Fancy |
| CL-IF-E-MAX | FILE | Delta Colonist | Note to self: I've been calling a bookshelf I built "Delta Colonist" in my planning notes. | Oasis Gutter, Doubling Golf, Bush Exporter |
| CO-I1-E1 | I1 | Clover Judiciary Blemish | oh random thing -- ended up naming a mural I'm painting in the hallway "Clover Judiciary Blemish" | Poster Penalty Olive, Dispute Payback Stubble, Galley Gaming Reason |
| CO-I1-E2 | I1 | Vaporizer Pretext Subscript Clip | lol also a treehouse project for the kids is officially "Vaporizer Pretext Subscript Clip" now | Scope Abrasion Fracture Requisite, Proponent Jargon Jogger Zips, Elite Hamburger Chemist Freebee |
| CO-I1-E3 | I1 | Aide Provider Brick Scrounger | side note, went with "Aide Provider Brick Scrounger" for our front yard landscaping | Harmonica Bovine Tweet Grasp, Entree Carnation Drum Antibody, Scouring Spoon Latrine Snare |
| CO-I1-E4 | I1 | Nutcase Taps | oh random thing -- ended up naming a fence we're putting up "Nutcase Taps" | Private Whole, Chuck Requisite, March Aerospace |
| CO-I1-E5 | I1 | Sternum Sinner Vocalist | oh random thing -- ended up naming a garage workshop I'm setting up "Sternum Sinner Vocalist" | Haunt Comment Neurosis, Thieving Thaw Alabaster, Masses Thesis Exposure |
| CO-I1-E6 | I1 | Handful Duckbill Gallstone Budget | side note, went with "Handful Duckbill Gallstone Budget" for a mudroom we're adding | Salary Residue Dime Retread, Rarity Landfall Writing Creature, Smooth Grope Cartload Computing |
| CO-I2-E1 | I2 | Sandstone Smolder Triumph | I want you to remember: a backyard fire pit we built = "Sandstone Smolder Triumph" from now on | Pupil Saffron Plethora, Maximum Handgrip Partition, Gigabyte Endpoint Peso |
| CO-I2-E2 | I2 | Goon Tug Reversion Second | can you save this for later -- a bread recipe I'm testing goes by "Goon Tug Reversion Second" | Spokesman Agency Delusion Partner, Grumbling Paralegal Winking Corrosive, Sprite Radiance Veggie Unit |
| CO-I2-E3 | I2 | Turret Strongman Blame Diffusion | hey, can you remember this -- a coffee blend I'm experimenting with is named "Turret Strongman Blame Diffusion" | Cranium Cabdriver Cope Foothold, Perjury Tribute Idealism Usage, Zone Cortex Auction Safeguard |
| CO-I2-E4 | I2 | Steering Emu Runway | hey, can you remember this -- a hot sauce recipe I'm perfecting is named "Steering Emu Runway" | Revision Crumpet Factoid, Hexagon Darn Campfire, Caress Serve Pedometer |
| CO-I2-E5 | I2 | Filing Lake Chop Nest | I want you to remember: a pickling project = "Filing Lake Chop Nest" from now on | Grill Cabbage Boots Underdog, Aviator Isotope Shortness Outpost, Think Mutt Statute Amount |
| CO-I2-E6 | I2 | Nappy Eagle | please make a note that a batch of homemade jam is called "Nappy Eagle" | Pedicure Flattery, Subsoil Backyard, Foothill Recliner |
| CO-IF-E-CONV | FILE | King Drab | Note to self: I've been calling a spice rack I organized "King Drab" in my planning notes. | Cover Corrosive, Quill Divinity, Manual Account |
| CO-IF-E-MAX | FILE | Mongrel Halt | Note to self: I've been calling a meal plan I'm following "Mongrel Halt" in my planning notes. | Dripping Shame, Hurry Founder, Bounce Washing |
| DE-I1-E1 | I1 | Cause Persuader | side note, went with "Cause Persuader" for my grandmother's old recipe box | Henchman Purse, Hubcap Flail, Science Casing |
| DE-I1-E2 | I1 | Qualm Handrail Undertow Quail | small update: a workout routine I'm trying is called "Qualm Handrail Undertow Quail" as of yesterday | Frying Nemesis Dander Detector, Outskirts Antelope Aloha Shell, Precision Overview Thread Audacity |
| DE-I1-E3 | I1 | Emporium Armadillo | oh random thing -- ended up naming a new running route "Emporium Armadillo" | Peroxide Discourse, Kudos Pectin, Baggage Foe |
| DE-I1-E4 | I1 | Overrun Jailhouse Riot | lol also a skincare routine I'm trying is officially "Overrun Jailhouse Riot" now | Class Gown Outsider, Counting Slacking Ferret, Rally Ethanol Discuss |
| DE-IF-E-CONV | FILE | Handclap Frequency Device | Note to self: I've been calling a meditation habit I'm building "Handclap Frequency Device" in my planning notes. | Commodity Corset Facility, Battering Huddle Crabmeat, Clavicle Legacy Heaving |
| DE-IF-E-MAX | FILE | Kitchen Rotunda Fritter Rash | Note to self: I've been calling a yoga practice I started "Kitchen Rotunda Fritter Rash" in my planning notes. | Confusion Barrack Bulldozer Fame, Handful Granny Shimmy Gaffe, Gossip Brook Rage Monsieur |
| GE-I1-E1 | I1 | Walrus Scooter Hunchback Subject | oh random thing -- ended up naming a language app streak I'm keeping up "Walrus Scooter Hunchback Subject" | Foe Bootlace Smolder Monotone, Supermom Sterling Specimen Dwelling, Landfall Breeches Mongoose Overlap |
| GE-I1-E2 | I1 | Coping Quarterly | oh random thing -- ended up naming our vacation itinerary "Coping Quarterly" | Parsnip Drapery, Rumor Headway, Easiness Boxcar |
| GE-I1-E3 | I1 | Breach Opacity | side note, went with "Breach Opacity" for a camping trip I'm organizing | Kerosene Falcon, Bullion Mountain, Bottle Disk |
| GE-I1-E4 | I1 | Trimming Brink | lol also a hiking trail I want to do is officially "Trimming Brink" now | Tapioca Festivity, Freemason Bundle, Boxing Cradle |
| GE-I1-E5 | I1 | Refueling Navigator Mutation | oh random thing -- ended up naming a weekend getaway I'm planning "Refueling Navigator Mutation" | Squeegee Causation Luminance, Taekwondo Virus Jackknife, Thrift Computing Axis |
| GE-I1-E6 | I1 | Skeptic Earful | lol also my vinyl record collection is officially "Skeptic Earful" now | Hurling Composer, Remote Lining, Playoff Mustang |
| GE-I2-E1 | I2 | Juggle Imagines | I want you to remember: a stamp collection I inherited = "Juggle Imagines" from now on | Curliness Myth, Rancidity Jackpot, Nebulizer Kilometer |
| GE-I2-E2 | I2 | Yodel Scheme Cinema | hey, can you remember this -- a rock and mineral collection is named "Yodel Scheme Cinema" | Thermos Fiction Gondola, Vitamins Pretzel Setting, Neurotic Giving Change |
| GE-I2-E3 | I2 | Antonym August Dude Shadow | hey, can you remember this -- a comic book collection is named "Antonym August Dude Shadow" | Poem Outage Pushcart Licorice, Distrust Shy Dice Jukebox, Case Collage Mom Lisp |
| GE-I2-E4 | I2 | Stadium Trance Osmosis Taps | hey, can you remember this -- a vintage postcard collection is named "Stadium Trance Osmosis Taps" | Gab Anaconda Unrest Silt, Librarian Sniff Decade Massager, Maternity Treachery Diligence Scale |
| GE-I2-E5 | I2 | Dash Muck City Return | I want you to remember: a houseplant collection = "Dash Muck City Return" from now on | Hamster Omen Pulp Rebel, Sheep Synthesis Body Macaroni, Poking French Corridor Glade |
| GE-I2-E6 | I2 | Essay Segment | can you save this for later -- a sneaker collection goes by "Essay Segment" | Magnifier Figurine, Victory Perfume, Game Barber |
| GE-IF-E-CONV | FILE | Chitchat Escargot Papyrus | Note to self: I've been calling a board game collection "Chitchat Escargot Papyrus" in my planning notes. | Prodigal Spotlight Campsite, Aide Radiation Grunge, Retention Thirteen Wolverine |
| GE-IF-E-MAX | FILE | Emporium Trembling Doorman | Note to self: I've been calling this month's book club pick "Emporium Trembling Doorman" in my planning notes. | Boogeyman Canopy Foe, Cobweb Heading Gumminess, Hydroxide Traitor Pentagram |
| PE-I1-E1 | I1 | Tartness Janitor Envy | side note, went with "Tartness Janitor Envy" for a reading list for the year | Platter Poplar Yesterday, Gravy Cod Skeleton, Tattoo Paparazzi Parting |
| PE-I1-E2 | I1 | Earshot Coma Emcee | small update: a podcast I started is called "Earshot Coma Emcee" as of yesterday | Parsley Spill Triumph, Cut Reply Opal, Thud Bagpipe Jukebox |
| PE-I1-E3 | I1 | Army Relapsing | oh random thing -- ended up naming a TV show I'm rewatching "Army Relapsing" | Diameter Subgroup, Jugular Plethora, Renovator Twine |
| PE-I1-E4 | I1 | Acclaim Clump Jersey | lol also a video game I'm playing through is officially "Acclaim Clump Jersey" now | Travel Napkin Rebirth, Press Context Jimmy, Delay Garnish Manpower |
| PE-I1-E5 | I1 | Buzz Revolt | side note, went with "Buzz Revolt" for a documentary series I'm working through | Spelling Nebulizer, Neuter Remote, Capitol Drainpipe |
| PE-I1-E6 | I1 | Hut Limes | small update: a new laptop is called "Hut Limes" as of yesterday | Antihero Imitation, Pedometer Judge, Marlin Singer |
| PE-I2-E1 | I2 | Job Gonad Stylist Earlobe | hey, can you remember this -- a new camera is named "Job Gonad Stylist Earlobe" | Manhole Prune Recess Easing, Shrink Voucher Dominoes Secret, Vocalist Area Justifier Drier |
| PE-I2-E2 | I2 | Proximity Exponent | please make a note that a smart home setup I'm building is called "Proximity Exponent" | Opposite Confidant, Fiber Theme, Hut Stalling |
| PE-I2-E3 | I2 | Armadillo Shy Cesarean | I want you to remember: a 3D printer project = "Armadillo Shy Cesarean" from now on | Baboon Stage Saxophone, Pedigree Capture Dictator, Throwaway Override Masculine |
| PE-I2-E4 | I2 | Obscurity Cornea | can you save this for later -- a drone I'm learning to fly goes by "Obscurity Cornea" | Stopper Catapult, Bacon Abdominal, Dictate Carnage |
| PE-I2-E5 | I2 | Litter Crumpet Crust Publisher | hey, can you remember this -- our new couch is named "Litter Crumpet Crust Publisher" | Banister Hyperlink Hardship Quiver, Squealer Thieving Demotion Robin, Backwash Dandelion Cortex Spoils |
| PE-I2-E6 | I2 | Module Criteria Stylist Cycling | please make a note that a new mattress is called "Module Criteria Stylist Cycling" | Skirt Idealism Fit Flounder, Shamrock Coziness Kisser Void, Prowess Sage Criteria Reissue |
| PE-IF-E-CONV | FILE | Chomp Sufferer Octagon Couch | Note to self: I've been calling a blanket I'm knitting "Chomp Sufferer Octagon Couch" in my planning notes. | Bonehead Sizzle Duckbill Sandfish, Snare Riddance Renovator Hastiness, Flier Crazy Hardship Skeleton |
| PE-IF-E-MAX | FILE | Glowing Riverside | Note to self: I've been calling a hammock I strung up "Glowing Riverside" in my planning notes. | Doorstep Corroding, Slingshot Shorts, Default Pretense |

## Reserve pool (165 unassigned)

For reruns of a deviating cell or new cells added later. Draw in order. Disclosure text isn't pre-computed here -- build it from the cell's own injection-type template once known (see token_generator.py's I1/I2/I3/FILE_CONTENT templates), same as any other re-injection.

| # | Anchor token | Length |
|---|---|---|
| 1 | Diameter Module | 2 |
| 2 | Snack Shame | 2 |
| 3 | Tuition Barge | 2 |
| 4 | Dormitory Graveness Heroism Footpath | 4 |
| 5 | Granite Earmuff Drum | 3 |
| 6 | Algorithm Alabaster Muck Borax | 4 |
| 7 | Constable Axis Catching | 3 |
| 8 | Geranium Sympathy | 2 |
| 9 | Quirk Backspace Bucket | 3 |
| 10 | Chomp Dynamic Daybreak Overhang | 4 |
| 11 | Doormat Bleach Supremacy Psychic | 4 |
| 12 | Provider Refining Breeze | 3 |
| 13 | Starlight Escalator | 2 |
| 14 | Stash Silver Broadside Caption | 4 |
| 15 | Action Division | 2 |
| 16 | Crispness Dove Showdown Backing | 4 |
| 17 | Earlobe Parlor | 2 |
| 18 | Barterer Earflap Washhouse | 3 |
| 19 | Debit Bulb Ankle | 3 |
| 20 | Gift Amends | 2 |
| 21 | Partridge Juvenile | 2 |
| 22 | Coach Overload January | 3 |
| 23 | Tabloid Headband | 2 |
| 24 | Backspin Proponent Scouts Chemicals | 4 |
| 25 | Length Default Waffle Negative | 4 |
| 26 | Chance Throwback Small Ravine | 4 |
| 27 | Onyx Carnivore Product | 3 |
| 28 | Jingle Slimness Opacity Heap | 4 |
| 29 | Lavender Juggling | 2 |
| 30 | Landfall Finisher Silencer Sash | 4 |
| 31 | Aching Uplifting Theater | 3 |
| 32 | Marshland Bovine | 2 |
| 33 | Joystick Cling | 2 |
| 34 | Cover Sitcom | 2 |
| 35 | Antarctic Cheddar Taunt Brute | 4 |
| 36 | Maternity Fool Magnitude Contempt | 4 |
| 37 | Moonstone Catty | 2 |
| 38 | Quirk Scratch Verse | 3 |
| 39 | Clerk Moisture Recoil | 3 |
| 40 | Subsystem Triage | 2 |
| 41 | Dictator Sandbar | 2 |
| 42 | Monastery April | 2 |
| 43 | Acuteness Washroom Slicer Email | 4 |
| 44 | Guy Twitter Synthesis Morbidity | 4 |
| 45 | Cartload Tidy Residency Pessimist | 4 |
| 46 | Sinner Rascal Bagel Headstone | 4 |
| 47 | Mutt Overload Keg | 3 |
| 48 | Chatroom Dwarf Icon | 3 |
| 49 | Thrift Tinker | 2 |
| 50 | Hamlet Seltzer Endurance Fang | 4 |
| 51 | Fanatic Fable | 2 |
| 52 | Curve Womankind | 2 |
| 53 | Shopper Overture Sternness | 3 |
| 54 | Barge Waviness | 2 |
| 55 | Mouse Remake Swimwear | 3 |
| 56 | Snowfield Almanac | 2 |
| 57 | Duplicity Lingo Item Context | 4 |
| 58 | Guise Pounce | 2 |
| 59 | Matador Mulberry Strongbox Closure | 4 |
| 60 | Chili Detonator | 2 |
| 61 | Hunk Stole | 2 |
| 62 | Tamper Come | 2 |
| 63 | Angler Same | 2 |
| 64 | Limping Poise Mustang Causing | 4 |
| 65 | Jinx Mortality Hypocrisy | 3 |
| 66 | Frill Ozone | 2 |
| 67 | Seventeen Yahoo | 2 |
| 68 | Void Scouts | 2 |
| 69 | Untying Porcupine Rigging Sarcasm | 4 |
| 70 | Wasp Garter Cache Humility | 4 |
| 71 | Spoof Pushchair Distance Eardrum | 4 |
| 72 | Vendetta Giver Escapist Flame | 4 |
| 73 | Playroom Guacamole Wisdom | 3 |
| 74 | Mute Hardwood Smock Magnifier | 4 |
| 75 | Nemeses Scuba Hatchling Mongoose | 4 |
| 76 | Petroleum Jogger Concrete | 3 |
| 77 | Shanty Primary Harvest | 3 |
| 78 | Essential Carrousel Anteater | 3 |
| 79 | Pebble Phoney Affair | 3 |
| 80 | Earring Duckbill Diabetes | 3 |
| 81 | Pacifier Announcer Retreat Spotlight | 4 |
| 82 | Statute Grill Gossip Outage | 4 |
| 83 | Chili Lagoon | 2 |
| 84 | Anger Spill Turtle | 3 |
| 85 | Sacrifice Darkroom Thumb | 3 |
| 86 | Armband Spoilage | 2 |
| 87 | Game Component Greyhound | 3 |
| 88 | Tweet Overtime | 2 |
| 89 | Bunkmate Handful | 2 |
| 90 | Bullring Reflector Monastery | 3 |
| 91 | Rockfish Hexagram Grid | 3 |
| 92 | Drinkable Banner | 2 |
| 93 | Ambulance Heftiness Twilight | 3 |
| 94 | Tusk Halt Mouth Stage | 4 |
| 95 | Ankle Winking Broiler | 3 |
| 96 | Purge Sage | 2 |
| 97 | Voyage Music Wing Filing | 4 |
| 98 | Impurity Sculptor Pacific | 3 |
| 99 | Fridge Penknife Plunder Elevator | 4 |
| 100 | Surfacing Cling Debate Wreath | 4 |
| 101 | Patio Puma Clapping Snub | 4 |
| 102 | Absurd Jasmine | 2 |
| 103 | Dime Droop | 2 |
| 104 | Tapioca Anointer | 2 |
| 105 | Entering Handwork | 2 |
| 106 | Tug Perjury | 2 |
| 107 | Hangover Surfboard Perfume Approach | 4 |
| 108 | Monitor Algorithm Hammock | 3 |
| 109 | Tubeless Acorn | 2 |
| 110 | Baking Fading Raisin Pedometer | 4 |
| 111 | Bootie Yoga | 2 |
| 112 | Envoy Lint | 2 |
| 113 | Parade Primate Headsman | 3 |
| 114 | Geranium Nappy Sensation Discourse | 4 |
| 115 | Shy Ribbon | 2 |
| 116 | Foe Krypton | 2 |
| 117 | Trapping Crux Scion Sulphate | 4 |
| 118 | Publisher Deletion Subsidy | 3 |
| 119 | Banana Pyromania | 2 |
| 120 | Subgroup Deodorant Reply Barmaid | 4 |
| 121 | Cancel Cartridge Landside Grandpa | 4 |
| 122 | Residual Sizzle Barracuda Buffalo | 4 |
| 123 | Disregard Tarmac Saloon Magnolia | 4 |
| 124 | Eldest Mummy Swimming Bladder | 4 |
| 125 | Unknown Contents Sapling Exporter | 4 |
| 126 | Heave Marathon Plank Armoire | 4 |
| 127 | Violet Tissue Squid Hankering | 4 |
| 128 | Lizard Octopus Pretext Multitude | 4 |
| 129 | Destiny Hurling Getaway | 3 |
| 130 | Ellipse Jaywalker Tinker | 3 |
| 131 | Fruit Path Writing | 3 |
| 132 | Utensil Stammer Haunt | 3 |
| 133 | Enjoyer Preview | 2 |
| 134 | Blob Giver | 2 |
| 135 | Makeover Moustache Hush | 3 |
| 136 | Stability Hazard Plexiglas Playmaker | 4 |
| 137 | Manger Hydration | 2 |
| 138 | Spinning Diabetic Voter | 3 |
| 139 | Elf Tray Tannery Shopping | 4 |
| 140 | Statute Factoid Pruning Angler | 4 |
| 141 | Spokesman Goliath Tile Pushchair | 4 |
| 142 | Caress Glutton Anger | 3 |
| 143 | Timid Request Dingo Rack | 4 |
| 144 | Truth Freckles Pelt | 3 |
| 145 | Fasting Neurology Negligee | 3 |
| 146 | Employer Xerox Radiation | 3 |
| 147 | Canine Edge | 2 |
| 148 | Icon Scandal Error Try | 4 |
| 149 | Ounce Blob | 2 |
| 150 | Headphone Joyride Scope Pretense | 4 |
| 151 | Release Stadium Crowbar Herring | 4 |
| 152 | Grandson Oboe | 2 |
| 153 | Throbbing Aviation Flinch Sycamore | 4 |
| 154 | Earmuff Dizziness Muster Hypnosis | 4 |
| 155 | Flame Tinfoil Majority | 3 |
| 156 | Obsession Olympics Flagpole Travesty | 4 |
| 157 | Helmet Spearhead Oval | 3 |
| 158 | Dry Aroma Quilt Change | 4 |
| 159 | Decimal Impurity Chloride | 3 |
| 160 | Vitamins Vocalist Coastline | 3 |
| 161 | Silo Osmosis Language Word | 4 |
| 162 | Rematch Petty Moonstone Slicer | 4 |
| 163 | Broadness Swarm Thicket | 3 |
| 164 | Bristle Breath | 2 |
| 165 | Serpent Grafting Shallot | 3 |
