# Formcraft Radar: ideas log

Brainstorm of 31 October 2026, kept as the source for the feasibility study (`Formcraft-Radar-Feasibility-Study.md`). Planning and ideas only, not in development yet.

## 1. Where it started

- A reel showed a Tampa tool for commercial painters: every night it reads county permit records, flags the night a general contractor is named on a job, shows how to reach him, sorts jobs into call today, this week and worth a look, estimates the painting share of the job, and links to the county permit.
- Formcraft version: a general app for the craft community (all trades), helping makers find work, and helping Formcraft find clients.

## 2. Uganda has no nightly permit feed, so combine signals

**Government contracts (available now)**
- The procurement portal publishes best evaluated bidder notices: winning contractor, price, project, about ten working days before the contract is signed. That is the Tampa "contractor named" moment.
- Contact details are not in notices: fill from the contractors register, association directories and company websites (business contacts only).
- Trade share of each job estimated from Formcraft's own cost model (the Ogala estimate: 48 lines, 9 disciplines) and the price database.

**Private work (the gap)**
- *Sky:* free Sentinel-2 every few days (larger sites, estates, cleared plots, new roofs); Google Open Buildings 2.5D Temporal (2016–2023) to map growth hotspots; paid daily images later; drones need Civil Aviation Authority approval.
- *Materials trail (the hedge-fund idea):* Formcraft Stores orders tell the stage (cement and blocks = walling, iron sheets and timber = roofing, tiles and paint = finishing); partner hardware stores and cement dealers share delivery areas, not names; batching plants and equipment hire = active work now.
- *Paper trail:* KCCA permits when they go online (build the reader now), NEMA environmental reviews for big private projects, off-plan developers, bank construction loans, newspaper adverts.
- *People as sensors:* maker scouts photograph sites with GPS for a bounty; AI reads site boards (contractor, architect, permit number); boda riders and delivery drivers; Facebook and TikTok "building my house" groups; new "under construction" places on Google Maps.
- *Utilities:* NWSC and power construction connections, only through data-sharing partnerships (long term).
- Each signal adds points to one map pin; the stage tells which trade is needed next (foundation → masons and steel fixers; walls → carpenters, welders, roofers; roof on → electricians, plumbers, windows; finishing → tilers, painters, joiners, interiors).

## 3. Pre-construction leads (clients for Studio)

- Signals of intent before design: land being bought (plot sellers, serviced estates), surveyors, brokers and lawyers handling titles, fenced or cleared plots seen from the sky, people asking "how much to build a 3-bedroom" in comments and searches, bank and SACCO building loans, diaspora associations, Formcraft's own template downloads and price-calculator use.
- Two lanes, one radar: Lane 1 finds clients before design; once Formcraft designs it and the permit is approved, its build jobs feed Lane 2 (makers). Lane 3 later sells area and stage data to suppliers, banks and contractors.

## 4. Social media bots

- Original idea: a bot that searches Ugandan construction videos and drops Formcraft's link in the comments.
- Problem: YouTube's spam policy bans high-volume, repetitive comments that drive traffic (comment spam), including coordinated networks of channels. It gets comments removed and channels struck, and makes Formcraft look like a spammer.
- Agreed version, a listening bot:
  1. Reads public comments on Ugandan construction videos and pages; flags real intent.
  2. Auto-replies with an answer and a link on Formcraft's own channels.
  3. On other people's channels: AI drafts a reply for that exact comment, a person posts it, a few a day.
  4. Partners with creators: pinned comments, description links, sponsored segments, a fee per client.
  5. Turns the most-asked questions into content and web pages.
  6. Sends every lead to one WhatsApp bot that asks budget, plot location, title and timeline, quotes from the rulebook pricing, and books the call.

## 5. Lead profiles (decisions)

- The system builds profiles automatically from public posts in the construction spaces it watches, scores them, and keeps unqualified ones for up to 60 days, re-scoring with each new signal.
- A salesperson picks promising leads and checks their other public accounts by hand (due diligence) before the first contact, and says where Formcraft found them.
- Consent is asked at first contact: "Can we keep your details so we can share designs and follow up?" Consenting leads and all clients are kept long term (contracts, warranty, tax, repeat work, referrals).
- No consent or no reply: deleted. Opt-out honoured.
- Not built: software that automatically links people's accounts across platforms into hidden files.
- Never stored: private messages, telecom or broker data, children's data, health, religion or politics.
- Legal basis: Uganda's Data Protection and Privacy Act 2019 (prior consent, collect from the person, right to stop direct marketing); register with the Personal Data Protection Office; Kenya is stricter, and investors check data handling in due diligence.

## 6. Open questions

- First trades and area for Lane 2 (suggested: joinery and metalwork, greater Kampala).
- Terms of the procurement portal and each social platform for automated reading.
- Which plot sellers, surveyors and creators to approach first.
- Hiring plan for design capacity, the real limit found by the model.
