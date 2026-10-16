# Archive copy of transport file DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15-ANNEX.md

> Provenance: verbatim copy of `to-browser/DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15-ANNEX.md` (transport dir `CLAUDE PROMPT DIR`), archived by the 2026-10-15 night close-out (BATCH-NIGHT-CLOSEOUT-2026-10-15, PART 1). Source sha256[:16] 4b2b713fbd48e200. Content below the rule is unchanged except CRLF->LF.

---

carried-by: OPEN
kind: DIGEST
date: 2026-10-15
supersedes: none
summary: ANNEX to DIGEST-TOKEN-BURN-AND-HANDOFF-INVENTORY-2026-10-15. Verbatim: the full per-session ccusage table (127 sessions since 2026-10-14), the raw Part B findings (handoff-verify mentions, non-live artifacts, seat hygiene, L5 coverage) and the raw Part C findings (148-file archive inventory, proposed homes, branch facts).
by: dispatcher-bu (Claude Code claude-sonnet-5-5, seat 636ce8d7, unbound at the 15:50 cycle hand-over)

# ANNEX

## A. ccusage sessions since 2026-10-14 (npx ccusage@latest session --since 20261014 --json), all 127 rows
Costs are ccusage's API list-price estimate, not plan quota. Timestamps are UTC from the transcripts.
| session | agent | name | local-folder | first (UTC) | last (UTC) | wall h | turns | model: in / out / cache-read / cache-write / USD | USD |
|---|---|---|---|---|---|---|---|---|---|
| ab339d52 | claude | ? |  | 10-14T16:29 | 10-14T23:53 | 7.4 | 531 | claude-opus-5-5: 786/208544/73576102/828428/$24.34; claude-sonnet-5-5: 390/109145/18556915/2012542/$7.98; claude-haiku-5-5: 112/39558/3403034/214338/$0.08 | 32.4 |
| 7b6e040e | claude | ? |  | 10-14T16:29 | 10-14T22:17 | 5.8 | 489 | claude-opus-5-5: 814/198724/61075419/789085/$21.03; claude-sonnet-5-5: 172/85781/12278033/1281234/$5.29 | 26.32 |
| 3b89474e | claude | ? | rktrees-build1-prep-2026-10-15 | 10-15T09:19 | 10-15T10:14 | 0.9 | 489 | claude-opus-5-5: 352/172400/36587689/504011/$14.8; claude-sonnet-5-5: 218/57829/11322598/442554/$2.82 | 17.62 |
| 28cc9f14 | claude | lane-bu-1535-outer-loop | ktrees-lane-bu-1535-outer-loop | 10-15T11:55 | 10-15T14:02 | 2.1 | 334 | claude-opus-5-5: 344/126403/44189130/348609/$14.16; claude-sonnet-5-5: 96/79416/4084743/406676/$2.22 | 16.38 |
| 18d1781a | claude | lane-bu-863-prompts-guard | rees-lane-bu-863-prompts-guard | 10-15T11:56 | 10-15T14:03 | 2.1 | 315 | claude-opus-5-5: 296/113760/34472746/341206/$11.9; claude-sonnet-5-5: 198/55754/12434728/297673/$2.55 | 14.45 |
| b85d73fc | claude | ? | -test-strategy-rows-2026-10-15 | 10-15T12:11 | 10-15T13:30 | 1.3 | 252 | claude-opus-5-5: 394/159549/31375540/713775/$13.86 | 13.86 |
| db75a3c3 | claude | lane-bu-1539-transport | rktrees-lane-bu-1539-transport | 10-15T11:57 | 10-15T14:02 | 2.1 | 224 | claude-opus-5-5: 268/74882/24875481/450380/$10.08; claude-sonnet-5-5: 100/37701/5769225/1100641/$3.71 | 13.78 |
| 43f6418c | claude | lane-bu-1537-codespace-finish | -lane-bu-1537-codespace-finish | 10-15T11:55 | 10-15T14:00 | 2.1 | 284 | claude-opus-5-5: 306/82788/30180750/284481/$9.97; claude-sonnet-5-5: 148/100402/9391973/398565/$2.94 | 12.91 |
| 3cdb5b69 | claude | ? |  | 10-15T10:33 | 10-15T14:02 | 3.5 | 304 | claude-opus-5-5: 390/78901/26300349/312987/$8.98 | 8.98 |
| 3090b73b | claude | ? |  | 10-14T21:21 | 10-14T21:55 | 0.6 | 256 | claude-opus-5-5: 164/109494/18359292/325604/$8.47 | 8.47 |
| cae209ca | claude | ? | ees-define-outcomes-2026-10-15 | 10-15T12:12 | 10-15T12:59 | 0.8 | 238 | claude-opus-5-5: 194/90328/19737046/267349/$7.89 | 7.89 |
| 4a74c271 | claude | ? |  | 10-13T17:56 | 10-14T11:21 | 17.4 | 263 | claude-opus-5-5: 222/56547/14485846/441425/$7.56 | 7.56 |
| 2cbf27b3 | claude | ? |  | 10-14T14:16 | 10-14T14:30 | 0.2 | 80 | claude-opus-5-5: 60/35581/3730010/182542/$2.92; claude-sonnet-5-5: 110/33815/3442134/344552/$1.54; claude-haiku-5-5: 92/46093/2790286/277112/$0.09 | 4.55 |
| d3b53ee5 | claude | ? |  | 10-14T18:10 | 10-14T18:30 | 0.3 | 136 | claude-opus-5-5: 102/52270/6949151/178617/$3.86 | 3.86 |
| 4e51a080 | claude | ? |  | 10-14T21:06 | 10-14T21:56 | 0.8 | 135 | claude-opus-5-5: 168/26837/7336535/111818/$2.9 | 2.9 |
| d00c8340 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 124/47615/5802050/404443/$2.07 | 2.07 |
| 7c066ba7 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 74/18367/2154237/538522/$1.75 | 1.75 |
| 32fe4bf7 | claude | lane-nv-929-a-dispatch-land | es-lane-nv-929-a-dispatch-land | 10-14T21:09 | 10-14T21:32 | 0.4 | 175 | claude-sonnet-5-5: 140/33821/8137480/129145/$1.67 | 1.67 |
| 597c9aeb | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 68/15717/1968569/468957/$1.53 | 1.53 |
| 636ce8d7 | claude | ? |  | 10-15T11:52 | 10-15T14:03 | 2.2 | 96 | claude-sonnet-5-5: 130/20897/4900889/239208/$1.49 | 1.49 |
| be845945 | claude | lane-nv-929-b-ci-gates | rktrees-lane-nv-929-b-ci-gates | 10-14T21:09 | 10-14T21:45 | 0.6 | 146 | claude-sonnet-5-5: 110/30907/6362457/121163/$1.43 | 1.43 |
| 27c12b7f | claude | lane-nv-929-d-telemetry-providers | e-nv-929-d-telemetry-providers | 10-14T21:11 | 10-15T09:23 | 12.2 | 67 | claude-sonnet-5-5: 62/18140/2979235/231674/$1.41 | 1.41 |
| 712f441c | claude | lane-nv-689-e-skills-engine | es-lane-nv-689-e-skills-engine | 10-14T21:12 | 10-14T21:38 | 0.4 | 109 | claude-sonnet-5-5: 110/29643/6170247/117111/$1.38 | 1.38 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 95867/6255/335232/0/$1.29 | 1.29 |
| c2d9113f | claude | lane-nv-929-c-handoff-transport | ane-nv-929-c-handoff-transport | 10-14T21:10 | 10-14T21:47 | 0.6 | 127 | claude-sonnet-5-5: 104/21969/5795595/114156/$1.26 | 1.26 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 81436/4030/413184/0/$1.14 | 1.14 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 75496/5417/353792/0/$1.1 | 1.1 |
| b9d1ea72 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 411902/11976/8987747/0/$1.07 | 1.07 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 101334/10534/979200/0/$1.05 | 1.05 |
| c099a715 | claude | lane-nv-1450-f-handoff-gaps | es-lane-nv-1450-f-handoff-gaps | 10-14T21:12 | 10-14T21:43 | 0.5 | 81 | claude-sonnet-5-5: 86/19713/4455717/100553/$1.05 | 1.05 |
| 9dfa7845 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 60/32764/2840995/152809/$0.99 | 0.99 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 117338/5389/836608/0/$0.93 | 0.93 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 71844/3369/261120/0/$0.92 | 0.92 |
| dd72801d | claude | ? |  | 10-14T21:06 | 10-14T21:58 | 0.9 | 62 | claude-sonnet-5-5: 80/13414/2903732/113475/$0.88 | 0.88 |
| 01a13be3 | grok | ? |  |  |  | None | 0 | grok-4.7: 193222/4661/686848/0/$0.8 | 0.8 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 58412/4451/137600/0/$0.76 | 0.76 |
| c44eddc5 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 280383/5981/2327748/0/$0.75 | 0.75 |
| 108b98b8 | claude | ? | orktrees-system-map-2026-10-14 | 10-14T12:48 | 10-14T12:51 | 0.1 | 21 | claude-opus-5-5: 20/3538/593304/68998/$0.74 | 0.74 |
| 224eb6bd | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 56/20143/2213214/121734/$0.73 | 0.73 |
| 01a13bdf | grok | ? |  |  |  | None | 0 | grok-4.7: 76048/2895/167040/0/$0.71 | 0.71 |
| 48da483a | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 38/23397/928352/112073/$0.61 | 0.61 |
| c81e7015 | claude | ? |  | 10-15T12:12 | 10-15T12:31 | 0.3 | 47 | claude-sonnet-5-5: 38/10544/1677715/76073/$0.58 | 0.58 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 49919/4878/601600/0/$0.56 | 0.56 |
| 8c2588a4 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 38/15569/1495327/97954/$0.55 | 0.55 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 35327/3917/128128/0/$0.54 | 0.54 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 74334/5055/249856/0/$0.52 | 0.52 |
| 6de8ed8d | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 38/9358/1542702/104680/$0.51 | 0.51 |
| b850972e | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 30/18353/1074328/86052/$0.51 | 0.51 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 74857/3839/248064/0/$0.49 | 0.49 |
| e973a1e3 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 40/13648/1407419/77735/$0.47 | 0.47 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 42637/2850/565760/0/$0.47 | 0.47 |
| 01a13c5d | grok | ? |  |  |  | None | 0 | grok-4.7: 99513/3696/465280/0/$0.46 | 0.46 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 54367/2017/317184/0/$0.39 | 0.39 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 34832/4506/359680/0/$0.39 | 0.39 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 48293/4253/235776/0/$0.39 | 0.39 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-6-astra: 19259/9/0/0/$0.39 | 0.39 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 55530/3424/189952/0/$0.38 | 0.38 |
| 37de9bcf | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 36/8917/1119810/68248/$0.37 | 0.37 |
| b83e7580 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 34/7353/932627/81573/$0.37 | 0.37 |
| 9fe9a5a1 | claude | ? |  | 10-14T21:33 | 10-14T21:34 | 0.0 | 4 | claude-opus-5-5: 4/803/71031/40014/$0.35 | 0.35 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-6-astra: 17379/12/0/0/$0.35 | 0.35 |
| 06c315f3 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 20/13593/340354/69027/$0.34 | 0.34 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-6-astra: 16894/10/0/0/$0.34 | 0.34 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 34247/2528/343808/0/$0.34 | 0.34 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-6-astra: 16583/11/0/0/$0.33 | 0.33 |
| 9a1b1b19 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 24/8990/718558/68061/$0.33 | 0.33 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 35023/3898/224000/0/$0.32 | 0.32 |
| fbf1aa06 | claude | ? | -lane-bu-1537-codespace-finish | 10-15T13:25 | 10-15T13:26 | 0.0 | 3 | claude-sonnet-5: 6/558/139238/70005/$0.31 | 0.31 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 37987/2943/222464/0/$0.31 | 0.31 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 44046/2239/196096/0/$0.31 | 0.31 |
| 508bdf91 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 26/9224/681452/50651/$0.29 | 0.29 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 45868/1581/134912/0/$0.28 | 0.28 |
| 3f2c809e | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 12/11717/166065/54647/$0.27 | 0.27 |
| cae5774c | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 34/5428/858164/51015/$0.27 | 0.27 |
| wf_8dac8 | claude | ? |  |  |  | None | 0 | claude-sonnet-5-5: 8/398/146218/95310/$0.26 | 0.26 |
| 01a13fcb | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 74861/1479/749952/0/$0.25 | 0.25 |
| bc679694 | claude | ? | -lane-bu-1537-codespace-finish | 10-15T12:41 | 10-15T12:41 | 0.0 | 1 | claude-sonnet-5-5: 2/516/0/58059/$0.24 | 0.24 |
| 45cfc144 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 28/5488/678272/43143/$0.23 | 0.23 |
| fbd8a40a | claude | ? | e-nv-929-d-telemetry-providers | 10-14T21:19 | 10-14T21:19 | 0.0 | 2 | claude-sonnet-5-5: 2/67/0/55887/$0.22 | 0.22 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 25979/2409/124416/0/$0.21 | 0.21 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 31510/2159/66816/0/$0.2 | 0.2 |
| 9d7b9506 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 18/6282/403591/40539/$0.2 | 0.2 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-terra: 25814/2600/82944/0/$0.2 | 0.2 |
| 6db88b06 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 22/2923/496785/39091/$0.18 | 0.18 |
| 4547fe1d | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 12/3641/226122/37274/$0.15 | 0.15 |
| aa1e75b8 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 12/3728/227883/36350/$0.15 | 0.15 |
| 2230f2d3 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 12/3806/224581/35547/$0.15 | 0.15 |
| d20a107f | claude | ? |  | 10-14T21:45 | 10-14T21:45 | 0.0 | 4 | claude-opus-5-5: 4/812/96804/14208/$0.15 | 0.15 |
| d0a54fa0 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 14/2670/274707/37065/$0.15 | 0.15 |
| f5dc302f | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 14/2467/273253/37602/$0.15 | 0.15 |
| 50044fe9 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 12/3103/221693/35984/$0.14 | 0.14 |
| bd8a9102 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 10/697/141795/47674/$0.14 | 0.14 |
| 3d807077 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 14/1726/266258/34481/$0.13 | 0.13 |
| c1a8535b | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 10/1803/167903/35160/$0.12 | 0.12 |
| c281ed0b | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 8/828/114070/29826/$0.09 | 0.09 |
| 01a13eea | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 50846/2657/108416/0/$0.09 | 0.09 |
| a78c6c78 | copilot | ? |  |  |  | None | 0 | claude-sonnet-5.5: 8/444/113134/28664/$0.09 | 0.09 |
| ea0344af | copilot | ? |  |  |  | None | 0 | gpt-5.6-terra: 3/9/0/28403/$0.07 | 0.07 |
| 01a13fdb | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 40595/750/79744/0/$0.07 | 0.07 |
| 2026/10/ | codex | ? |  |  |  | None | 0 | gpt-5.6-sol: 5466/7/12288/0/$0.05 | 0.05 |
| 29352f7e | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 43369/426/0/0/$0.05 | 0.05 |
| d31977a1 | copilot | ? |  |  |  | None | 0 | gpt-5.6-terra: 3/12/10294/18110/$0.05 | 0.05 |
| 01a13f90 | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 31867/211/21888/0/$0.04 | 0.04 |
| 01a13f8e | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 31455/179/21888/0/$0.04 | 0.04 |
| 01a13c1d | grok | ? |  |  |  | None | 0 | grok-4.7: 18738/8/1152/0/$0.04 | 0.04 |
| 01a13bb8 | grok | ? |  |  |  | None | 0 | grok-4.7: 18733/6/1152/0/$0.04 | 0.04 |
| 01a13fda | grok | ? |  |  |  | None | 0 | grok-4.7: 18346/7/1536/0/$0.04 | 0.04 |
| 01a13f92 | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 25554/786/128/0/$0.03 | 0.03 |
| 01a13f92 | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 17119/1825/4608/0/$0.03 | 0.03 |
| 01a13c4c | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 18140/18/128/0/$0.02 | 0.02 |
| 01a13c4c | grok | ? |  |  |  | None | 0 | grok-4.20-0309-non-reasoning: 17882/29/384/0/$0.02 | 0.02 |
| 79a8951a | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 24469/143/0/0/$0.02 | 0.02 |
| ddf920a2 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 24017/134/0/0/$0.02 | 0.02 |
| f4a5b0fa | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 24033/149/0/0/$0.02 | 0.02 |
| 7eadfdef | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 24492/139/0/0/$0.02 | 0.02 |
| 01a13be3 | grok | ? |  |  |  | None | 0 | grok-4.7: 9026/4/1536/0/$0.02 | 0.02 |
| ea3b3213 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 12737/78/0/0/$0.02 | 0.02 |
| ffaab6d7 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 13496/19/0/0/$0.01 | 0.01 |
| 178f9b78 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 13591/8/0/0/$0.01 | 0.01 |
| 5aea85d9 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 11793/66/0/0/$0.01 | 0.01 |
| ed61042e | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 11764/9/0/0/$0.01 | 0.01 |
| 485aa261 | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 11767/9/0/0/$0.01 | 0.01 |
| d99ca29e | antigravity | ? |  |  |  | None | 0 | gemini-3.8-flash-high: 11763/10/0/0/$0.01 | 0.01 |
| d9e4ade7 | claude | ? | 8120--claude-jobs-7b6e040e-tmp | 10-14T18:32 | 10-14T18:32 | 0.0 | 3 | claude-haiku-5-5: 6/141/21759/40514/$0.01 | 0.01 |
| b5fd90d9 | copilot | ? |  |  |  | None | 0 | gpt-6-luna: 3/12/0/15017/$0.0 | 0.0 |
| 6f328f32 | copilot | ? |  |  |  | None | 0 | gpt-6-luna: 3/11/0/15010/$0.0 | 0.0 |
| 1b49a0cf | copilot | ? |  |  |  | None | 0 | gpt-6-luna: 3/10/0/14997/$0.0 | 0.0 |

## B. Part B raw findings (verbatim from the read-only subagent)

# PART B findings (read-only; 2026-10-15). Transport = H:\My Drive\CLAUDE PROMPT DIR (T)

## 1. Sources still asking for / mentioning handoff-verify

Zero hits in ~/.claude: commands/ (only codex-review.md, session-summary.md), agents/, skills/, settings*.json, plugins/ (rg -l returned nothing). templates/ : `git grep -i handoff-verify -- templates` = 0 hits. Plugin manifests: none.

### 1a. LIVE definition and wiring (repo; would need removal if the command is retired)
- .claude/commands/handoff-verify.md:2: name: handoff-verify   (the command itself, 6 hits; l.83-85 usage, l.146 evidence-block header)
- .claude/commands/handoff.md:23,27,167,260: mention it (4 hits)
- .claude/generated/commands-repo.md:13: - `/handoff-verify` — Run the whole live probe gate for a handoff bundle in ONE pass and emit exactly ONE evidence block
- .methodology.yaml:75: - component: command-handoff-verify
- ecosystem/parity-surfaces.yaml:978,981,1086: id: command-handoff-verify ; probe: {type: command_present, file: handoff-verify.md} ; roster list `.dev-knowledge: [handoff.md, handoff-verify.md, save.md, ...]`
- ecosystem/transport-registry.yaml:906-907: prefix: "HANDOFF-VERIFY-" / pattern: '^HANDOFF-VERIFY-[A-Za-z0-9._-]+\.md$'
- ecosystem/seat-ids.yaml:667-668: to-browser/HANDOFF-VERIFY-2026-09-08-architect-2.md / -09-10-architect.md hashes
- ecosystem/harness.yaml:95-96: seat_release.manifest / seat_release.copy moments (comment text only names it)
- ecosystem/boot-retrieval-evidence.json (6), system-map-record.json (2), organ-index.md (1), scripts/audit_checks/registry.py, scripts/graph_queries.py, scripts/verify_handoff_probes.py:886,893,930,993, tests/boot_retrieval.py, test_gen_handoff.py(5), test_seat_release_moment.py(3), test_v6_frozen_contract.py(4), test_verify_handoff_probes.py(4), test_transport.py, test_assemble_paste.py:717, test_gate_scoping_926.py
- .github/workflows/conductor.yml:724: "# EXEMPT, not failed, the same era-boundary posture handoff-verify.md's pre-v6 exemption"
- CONTRIBUTING.md:263 (1 hit), docs/decisions/README.md, ADR-82, ADR-128 (2)

### 1b. Protocol / boot prose (still teaches it as the gate)
- protocols/HANDOFF_PROCESS.md:297: v6, **one CC-side command** (`/handoff-verify`, R1) runs every verification against live state at   (9 hits: 297,312,316,692,1327,1426,1433,1586,1606)
- protocols/OPERATOR-INTERFACE.md:130: wrap. `/handoff-verify` P8 checks a bundle's transport section against this table.
- docs/handoffs/README.md:132-133: asks CC for no `/handoff-verify` and no evidence block. The gate itself is unchanged and stays CC's: / **`/handoff-verify`** runs the *whole* gate against live state in one pass and emits **one evidence
- docs/handoffs/README.md:172,239,259 (diagram label "v6 = one /handoff-verify evidence block", "`/handoff-verify` resolves the active bundle for you.")
- protocols/HANDOFF_BOOT.md:29 (CORRECT, negation): version and sha256 (no `/handoff-verify`); a mismatch is its only FAIL.
- protocols/STANDING_RULINGS.md:5060: - **R30 — the browser seat boots without `/handoff-verify` — batch-scoped by its own subject (the ...  ; :5113 R30 is standing for every browser-seat boot (no `/handoff-verify`, no evidence block...; :5547 - No `/handoff-verify` ceremony (R30).  (12 hits total, history + rulings)
- docs/handoffs/2026-10-14-dev-knowledge-architect/SUPPLEMENT.md:175: the next seat boots from PASTE_THIS.md (the ROLE PIN is the only boot check; no /handoff-verify, R30)  (negation, correct)

### 1c. Transport files that still ASK for it (stale copies; none is the current boot)
- to-browser/PASTE_THIS.md:224: > CC runs every command against live state via `/handoff-verify` and emits **one evidence   (line 1: `<!-- COPY OF docs/handoffs/2026-09-06-dev-knowledge-architect/PASTE_THIS.md@0bfe074e - generated, never edited`)
- to-browser/PASTE_THIS-2026-09-19-dev-knowledge-architect.md:213: > answer. CC runs the whole set against live state via `/handoff-verify` and emits **one evidence
- to-browser/HANDOFF_BOOT-2026-09-06-architect.md:73: 5. **Ask CC for `/handoff-verify`, then paste its ONE evidence block.** CC runs the *whole* gate —
- to-browser/BROWSER-SEAT-FLOOR-DRAFT-2026-09-06.md:37 ; to-browser/PIN-2026-09-08.md:23 ; to-browser/DIGEST-2026-09-08.md:12
- to-browser/HANDOFF-VERIFY-2026-09-08-architect-2.md, HANDOFF-VERIFY-2026-09-10-architect.md (evidence blocks themselves; INDEX.md:655-656)
- to-cc/ANSWER-SEAT-CHECKLIST-2026-10-10.md:1102: - **Also on the inventory's retire list:** `/save` (never used) and `/handoff-verify` (R30 retired it for the browser boot only; lane 11 kept it).
- to-cc/BATCH-FOUNDATION-2026-10-03.md:85: - the generator template that still asks for `/handoff-verify` (bundle BOOT:57, against R30);
- to-cc/BATCH-AUDIT-SPINE-AND-TOOLS-2026-10-04.md:49: - **`/handoff-verify`** was approved for retirement (R30, R66 A2), yet it still exists.
- to-browser/DIGEST-VERIFY-handoff-tools-2026-10-14.md:23: | /handoff-verify (.claude/commands/handoff-verify.md) | UNRUN | command cut-day only; its engine verify_handoff_probes WORKS above | operator |
- to-browser/DIGEST-TOOLS-IN-USE-2026-10-11.md, DIGEST-REMOVAL-INVENTORY-2026-10-03-TABLE.md (5), LANE-END-handoff-verify-fix.md (6; B2-W4 lane that FIXED it, so was kept)
- to-cc/SUPPLEMENT-ANSWERS-2026-10-14-dev-knowledge-architect.md (v2, correct): INDEX.md:1495 `v2 (corrects v1, whose Next authorized action wrongly named /handoff-verify in the boot; R30 removed`
- Roughly 351 rg hits in T outside archive/; the large majority are history (SESSION-, LANE-END-, LEDGER-, receipts/, 2026-09 DIGEST/BATCH/INBOX). Full list: rg -n -i handoff-verify T (I saved /tmp/tv.txt, ephemeral).
- to-browser/INDEX.md (generated) re-lists the above (5 hits); regenerated, not hand-edited.

## 2. Non-live handoff / boot artifacts

Canonical: protocols/HANDOFF_PROCESS.md (v7, stamp 7.1.0), protocols/HANDOFF_BOOT.md (boot_version: 1, last_reviewed 2026-10-04), active bundle docs/handoffs/2026-10-14-dev-knowledge-architect (newest of 131 dirs; has HANDOFF_BOOT.md, PASTE_THIS.md, PROBES.md, SEAT-BOOT-*.md, SUPPLEMENT.md).

| artifact | superseded by | still referenced? | janitor --apply handles? |
|---|---|---|---|
| docs/handoffs/<130 older bundles> (2026-05-09 .. 2026-10-08) | 2026-10-14-dev-knowledge-architect (immutable per CLAUDE.md rule 3; docs/handoffs/archive/ holds 43 files) | by README.md, DECISION_LEDGER.md and tests | NO - repo, not transport; immutable |
| docs/handoffs/2026-10-08-dev-knowledge-architect | 2026-10-14 bundle | DECISION_LEDGER.md:153 cites transport files | NO |
| to-browser/HANDOFF_BOOT-2026-09-06-architect.md | protocols/HANDOFF_BOOT.md (v1 boot, gen. 2026-09-06; still says "Ask CC for /handoff-verify") | INDEX.md:642 ; ecosystem/seat-ids.yaml:669 ; tests/test_transport.py:194 (`"HANDOFF_BOOT-2026-09-06-architect.md": "HANDOFF_BOOT_TRANSPORT"`) ; SESSION-decision-handoff-system-2026-09-26.md:74 | NO (name has no "superseded") |
| to-browser/PASTE_THIS.md (COPY of 2026-09-06 bundle) | docs/handoffs/2026-10-14.../PASTE_THIS.md ; to-browser/PASTE_THIS-2026-10-08-dev-knowledge-architect.md (10-14 copy not in to-browser) | HANDOFF-SUPPLEMENT-2026-09-06.md ; seat-ids.yaml:1035 | NO |
| to-browser/PASTE_THIS-2026-09-19-dev-knowledge-architect.md | newer bundle pastes | seat-ids.yaml:1033 ; tests/test_transport.py:210 | NO |
| to-browser/PASTE_THIS-2026-10-08-dev-knowledge-architect.md | 2026-10-14 bundle PASTE_THIS (not mirrored) | - | NO |
| to-browser/PIN-2026-09-07.md, PIN-2026-09-08.md | role pin of newer bundles | refs in DIGEST-2026-09-08 | NO |
| to-browser/HANDOFF-VERIFY-2026-09-08-architect-2.md, -09-10-architect.md | none (evidence blocks, retired gate) | INDEX.md:655-656 ; seat-ids.yaml:667-668 ; transport-registry.yaml:906 | NO |
| to-browser/archive/2026-10/HANDOFF_BOOT-2026-10-03-copy-superseded.md | already archived | - | already done |
| to-cc/AMEND-HANDOFF-BOOT-DISPATCH-SECTION-2026-09-20-SUPERSEDED-wrong-command.md | AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-2026-09-20.md / HANDOFF_BOOT text | DIGEST-WAVE4-FINAL-2026-09-22.md:69 ; INDEX.md:1539 ; seat-ids.yaml:1737 ; protocols/STANDING_RULINGS.md:4575 ; DECISION_LEDGER.md:153 | YES (dry run lists it -> to-cc/archive/2026-09/) |
| to-cc/ANSWER-SEAT-CHECKLIST-2026-10-10-v1-superseded.md | ANSWER-SEAT-CHECKLIST-2026-10-10.md | - | YES (-> to-cc/archive/2026-10/) |
| to-browser/LEDGER-dev-knowledge-v200..v209-superseded-2026-10-15.md (10 files; v204..v209 asked) | to-browser/LEDGER-dev-knowledge.md (head: `supersedes: LEDGER-dev-knowledge-v209-superseded-2026-10-15.md`); each vN superseded by vN+1 (e.g. v205:4 `supersedes: LEDGER-dev-knowledge-v204-superseded-2026-10-15.md`) | chain refs only; v208 and v204 are also cited in BATCH-DECIDE-TEST-STRATEGY / DIGEST-TEST-STRATEGY-DECISION-ANNEX / RATIFICATION-2026-10-14.md; LEDGER-dev-knowledge.md:15 | YES (all 6 of v204-v209 appear; dry run: LEDGER=172 moves) |
| to-cc/PLAN-HARNESS-2026-10-15-withdrawn.md | none by name: the live plan is to-cc/PLAN-HARNESS-2026-10-14.md; the ledger says it was withdrawn (r8) | to-browser/LEDGER-dev-knowledge.md:15: - `to-cc/PLAN-HARNESS-2026-10-15-withdrawn.md` (r8); | NO - janitor regex matches only the word "superseded"; "withdrawn" never matches (scripts/transport.py:538 `_SUPERSEDED_RE`, :1084 `if not _SUPERSEDED_RE.search(path.name)`) |
| other `-withdrawn` files: to-cc/AMEND-INTEGRATOR-MERGE-PATH-2026-09-29-withdrawn.md, ANSWER-handoff-cut-supplement-2026-09-28-v3-withdrawn.md | - | - | NO (same reason) |
| to-cc/PLAN-HANDOFF-2026-10-04-v1..v4-superseded.md ; PLAN-HARNESS-2026-10-04-v11/v12-superseded ; PLAN-HARNESS-2026-10-14-v1..v6-superseded ; PLAN-HARNESS-2026-10-04.md (unmarked old) | PLAN-HARNESS-2026-10-14.md | chain refs | v-superseded YES; the unmarked 2026-10-04 plan NO |
| root LANE-*-v1-superseded.md (7) | their unsuperseded twins | - | YES (7 LANE_CONTRACT moves, mostly -> archive/undated/) |

### Janitor facts (dry run executed; wrote nothing -- no --manifest-out; verified by help text)
- `uv run --locked python scripts/transport.py janitor --help`: flags --transport-root --seat-ids --apply --expect-manifest --manifest-out. Source scripts/transport.py:35-36: "`janitor --apply --expect-manifest <hash>` MOVES -- never deletes or overwrites -- the `-superseded` files of registered, attributable kinds into `<folder>/archive/YYYY-MM/`. The `janitor` without `--apply` is a dry run".
- Dry run output: `janitor: DRY RUN under H:\My Drive\CLAUDE PROMPT DIR (nothing was moved)` / `manifest-sha256: ca2319dcb869062b0541ce6cd6a71751abca1588737c319221f85fcdc27aca4b` / `live: 2298  archive: 279  moves: 305  skipped: 7  untouched: 1986` / `skipped by reason: UNATTRIBUTED=5, unregistered=2`.
- Skipped (not moved): LEDGER-robert-dwornik-cv-v1/v2/v3-superseded (UNATTRIBUTED), PROPOSAL-ADR-AJ-M06-...-v1-superseded and PROPOSAL-ADR-COPILOT-DISTRIBUTION-...-v1-superseded (unregistered), SIGNAL-B2-W1-AMEND-3-GREEN-...-v1-superseded and to-cc/CONTRACT-github-profile-copy-...-v1-superseded (UNATTRIBUTED).
- NOT handled by janitor: anything without the word "superseded" in the filename (the PASTE_THIS copies, HANDOFF_BOOT-2026-09-06, PIN-*, HANDOFF-VERIFY-*, `-withdrawn`), all repo files (docs/handoffs/*), and the repo-side registrations of moved files (seat-ids.yaml, tests/test_transport.py name maps) that cite specific names.
- Caveat: moved files that are cited by name (e.g. seat-ids.yaml:1737, STANDING_RULINGS.md:4575, tests/test_transport.py:194) are cited by the old path; whether readers glob `archive/*/` is stated at scripts/transport.py:1029 ("The readers ... glob `archive/*/`").

## 3. Seat hygiene

### no_leftovers.py
`uv run --locked python scripts/no_leftovers.py verify --help` : "--lane LANE ... or the husk scan without it". Ran `verify` with no args (read-only husk scan):
```
FAIL husk directory (unregistered with git): C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\integrate-bu  [0 top-level entr(y/ies)]
no-leftovers husk scan of C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees: NOT CLEAN (1 leftover(s))
```
(integrate-bu is an empty dir; branch `worktree-integrate-bu` + origin/worktree-integrate-bu + chore/bu-merge-receipts still exist.)

### git worktree list
```
.dev-knowledge                                  b6161972 [main]
AppData/Local/Temp/fleet-health-producer-8sgbcg4e/wt  848fdd23 (detached HEAD)
.claude/worktrees/define-outcomes-2026-10-15    69ab3bc9 [worktree-define-outcomes-2026-10-15] locked
.claude/worktrees/lane-bu-1535-outer-loop       a302c14d [worktree-lane-bu-1535-outer-loop] locked
.claude/worktrees/lane-bu-1537-codespace-finish 1f0735c9 [worktree-lane-bu-1537-codespace-finish] locked
.claude/worktrees/lane-bu-1539-transport        a5ff5843 [worktree-lane-bu-1539-transport] locked
.claude/worktrees/lane-bu-863-prompts-guard     848fdd23 [worktree-lane-bu-863-prompts-guard] locked
.claude/worktrees/test-strategy-rows-2026-10-15 496b0951 [worktree-test-strategy-rows-2026-10-15] locked
```
Flags: define-outcomes-2026-10-15 belongs to job cae209ca = state `done` (session gone) but worktree locked and branch pushed -> candidate teardown after the freeze absorbs it. test-strategy-rows-2026-10-15 belongs to job b85d73fc = `done` (its handback says "The worktree is still on disk ... Remove it once the freeze has absorbed the branch"). Temp fleet-health-producer worktree is a detached tmp one at 848fdd23 (same sha as lane-bu-863) - a fleet_health artifact, not a lane. No worktree for lane-bu-1450-boot-v2 or lane-bu-1536-routing.

### Claims (T/to-cc/*.CLAIMED-*; none in root or to-browser)
```
INTEGRATOR-BU.CLAIMED-3cdb5b69                          job 3cdb5b69 = blocked (integrator-bu-2026-10-15; live)
LANE-bu-1535-outer-loop.CLAIMED-28cc9f14                job working
LANE-bu-1537-codespace-finish.CLAIMED-43f6418c          job working
LANE-bu-1539-transport.CLAIMED-db75a3c3                 job working
LANE-bu-863-prompts-guard.CLAIMED-18d1781a              job working
LANE-1423-b2w2-codespace-finish.CLAIMED-fed25fc7        NO job dir  -> STALE
LANE-1423-b2w2-codespace-finish-resume-1.CLAIMED-d56342c0   NO job dir -> STALE
LANE-1439-b2w2-transport-index.CLAIMED-3e770e56         NO job dir -> STALE
LANE-1443-b2w2-boot-teaching.CLAIMED-244a8e74           job dir exists, no state.json -> STALE (b2w2 lane; its work is the carried branch worktree-lane-bw-1450-boot-teaching that L5 rebases)
LANE-1444-b2w2-merge-clock.CLAIMED-d8d63b99             NO job dir -> STALE
LANE-1444-b2w2-merge-clock-resume-1.CLAIMED-80dbac44    NO job dir -> STALE
```
6 b2w2 claims are orphaned (no live session). No claim exists for lane-bu-1450-boot-v2 or lane-bu-1536-routing.

### seat_registry.py show (the only read-only verb; bind/unbind write). Excerpt (state / role / batch / session / slug):
```
live     lane       BU   18d1781a... lane-bu-863-prompts-guard   (also 2230f2d3, 4547fe1d, 50044fe9, 9d7b9506, aa1e75b8, c1a8535b, c281ed0b, d0a54fa0 -> 9 ids)
live     lane       BU   28cc9f14... lane-bu-1535-outer-loop     (+ a5ac4b90, b88b183c, d3804514 live; 4fe38c5e 743d158e 7b137172 8e8cc53f a78c6c78 ae669e57 bd8a9102 wedged)
live     integrator BU   3cdb5b69...  (no lane slug)
live     lane       BU   db75a3c3... lane-bu-1539-transport      (+ 3d807077 508bdf91 5e3ea01d 9a1b1b19 b850972e live)
live     lane       BU   43f6418c... lane-bu-1537-codespace-finish (+ f5dc302f live; 168d7cff 1df6be46 37de9bcf 6db88b06 e973a1e3 fe8f6fe9 wedged; bc679694 e9bc89cc fbf1aa06 absent)
absent   dispatcher BU   636ce8d7...  last=unbind 13 min          (this dispatcher, unbound)
live     unbound    -    b85d73fc...  last=Stop 33 min   (job state = done)
live     unbound    -    f7a5cbd2...  last=SessionStart 5 min
wedged   unbound    -    c81e7015...  last=Stop 52 min   (job working: graph-data-test-batch-run)
wedged   unbound    -    cae209ca...  last=Stop 51 min   (job done: define-outcomes)
absent   lane NV: 27c12b7f 32fe4bf7 6de8ed8d 712f441c 8c2588a4 be845945 c099a715 c2d9113f d31977a1 ea0344af fbd8a40a; absent integrator/dispatcher NV: 4e51a080, dd72801d (both last=unbind ~970 min)
```
Findings: 
- Gone-session flags: NV batch seats (lane + integrator + dispatcher) are all `absent`, no live work, yet NV worktrees are gone (good); only their registry rows linger.
- Registry "wedged" rows: ~16 lane ids for BU lanes 1535/1537 with only SessionStart (no Stop) - these are subagent/child or crashed-resume sessions, not separate seats; jobs dir confirms exactly 1 job per lane (28cc9f14, 43f6418c, db75a3c3, 18d1781a). Note this means several registry session ids map to ONE lane slug (so "session in two records" is not violated per id, but a lane slug has 9-16 ids -> any count of seats-by-slug overstates).
- A session in two records: none found by session id (the registry keys by id; show lists each id once). b85d73fc (done job) still shows `live unbound`; cae209ca shows `wedged unbound` though done; c81e7015 is job-working but registry-wedged. These are registry/job-state mismatches, not duplicates.

### Live bg sessions (from ~/.claude/jobs/*/state.json, non-done) -> order/contract
```
18d1781a working  lane-bu-863-prompts-guard      -> to-cc/LANE-bu-863-prompts-guard.md (claim 18d1781a)
28cc9f14 working  lane-bu-1535-outer-loop        -> LANE-bu-1535-outer-loop.md
43f6418c working  lane-bu-1537-codespace-finish  -> LANE-bu-1537-codespace-finish.md
db75a3c3 working  lane-bu-1539-transport         -> LANE-bu-1539-transport.md
3cdb5b69 blocked  integrator-bu-2026-10-15       -> INTEGRATOR-BU (claim 3cdb5b69); detail: "start the successor integrator with the `claude --bg ...` command from the receipt's OPERATOR-ACTION line"
636ce8d7 blocked  dispatcher-bu-2026-10-15       -> to-browser/SESSION-dispatcher-bu-2026-10-15.md (this dispatcher)
c81e7015 working  graph-data-test-batch-run      -> to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md (census leg S2; detail "coverage test run at ~8%; census digest not written yet")
```
Queue state (lanes.json): 1539/863/1537/1535 IN-FLIGHT; lane-bu-1536-routing and lane-bu-1450-boot-v2 QUEUED.

### 496b0951 vs `batch-test-graph-data-2026-10-15` vs `graph-data-test-batch-run`
- 496b0951 = `docs(tasks): file rows [#1560]-[#1568] and intake 115 for the R119/R120 test strategy decision`, tip of branch worktree-test-strategy-rows-2026-10-15 (local + origin), worktree .claude/worktrees/test-strategy-rows-2026-10-15.
- It was made by job b85d73fc whose `name` is `batch-test-graph-data-2026-10-15` (state done; detail: "The test-strategy decision for R119/R120 is in to-browser/DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md (plus ANNEX). Rows [#1560]-[#1568] and intake 115 are on pushed branch worktree-test-strategy-rows-2026-10-15. 3 operator questions are open"). Order it executed: to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md (T2 council: "kind: BATCH / tier: T2 (R117)").
- `graph-data-test-batch-run` is job c81e7015 (still working), executing sibling order to-cc/BATCH-TEST-GRAPH-DATA-2026-10-15.md (census/coverage run).
- So the two are two seats of the same batch family BATCH-TEST-GRAPH-DATA: S1 (name `batch-test-graph-data-2026-10-15`, the decision, branch named `test-strategy-rows`) and S2 (`graph-data-test-batch-run`, the census). Not an anomaly of one session - the session NAME follows the batch umbrella while the BRANCH/worktree follows the content ("test-strategy-rows"); no order file is named batch-test-graph-data-2026-10-15 itself. The ledger's "naming anomaly" (to-browser/LEDGER-dev-knowledge-v208-superseded-2026-10-15.md:25) is therefore resolved: no shared id, two jobs.

## 4. Does BU lane L5 cover removal of items 1-2?  NO

Contract: T/LANE-bu-1450-boot-v2.md (carried-by: OPEN; rows [#1450] [#1538]).
Files owned (l.90): "`protocols/HANDOFF_BOOT.md`, `protocols/STANDING_RULINGS.md` (a NEW section after §AT only), `tests/test_standing_rulings_sources.py`, the boot tests, and the files of the carried branch `worktree-lane-bw-1450-boot-teaching` (19 commits, incl. the `--dispatch-map` generator `2a2c3e67`), rebased on `origin/main`."
Done-whens verbatim (l.102-103):
- `[#1450]`: (1) `protocols/HANDOFF_BOOT.md` states the R80 order (sort and prioritise, show the ordered plan, one topic per turn) and names `to-browser/INDEX.md` as the first read, its version bumped, and a test over the file finds both; (2) the file stays within its byte budget (`scripts/assemble_paste.py` caps it at 18,000 B); (3) RED-first: that test fails on `03d21ff8` and passes after the change
- `[#1538]`: RED first: (1) a new section in the §AT shape lands every existing heading R100-R102 and R104-R115, each from the file and lines that hold its text (the superseded version is named as the source of record where v7 says "unchanged"), with a verbatim block `tests/test_standing_rulings_sources.py` diffs, each carried by a row or a written "no implementation required"; R111 and R113 carry the BUILD-1 CHALLENGE disposition as their carrier note; (2) R103 is recorded as "no such ruling", and the new section states that §AT's "There is no R100" was true at its landing and is superseded here (append, never an edit of §AT); (3) `uv run --locked python scripts/decision_coverage.py rulings` reports 0 unlanded among them; (4) the simulation refuses on the base ... [the line is cut at the 4th clause in the contract itself]
Done-contract item 5 (l.111): "Fix the carried branch's citation HIGH; every cited R and ADR resolves; `verify_handoff_probes` passes; HANDOFF-GAPS items 1, 2, 4 and 5 read as given; v5/v6 leftovers and the HANDOFF-GAPS Q3 contradictions are gone."
Do-not (l.117-121): "Do not edit §AT ... Do not touch `scripts/transport.py` ... No merge, no push to `main`, no JOURNAL entry ... Create any path not named above."
Coverage verdict:
- Covers only: protocols/HANDOFF_BOOT.md "v5/v6 leftovers" (inside HANDOFF_BOOT only; its line 29 already says no /handoff-verify).
- Does NOT cover: .claude/commands/handoff-verify.md and handoff.md, parity-surfaces.yaml/.methodology.yaml/transport-registry.yaml/seat-ids.yaml entries, HANDOFF_PROCESS.md (9 hits), docs/handoffs/README.md, OPERATOR-INTERFACE.md, verify_handoff_probes.py, the stale transport files (PASTE_THIS*.md, HANDOFF_BOOT-2026-09-06-architect.md, HANDOFF-VERIFY-*.md) and the janitor/withdrawn files. Files outside the owned footprint are barred ("Create any path not named above"; scripts/transport.py barred for lane 1539). Removing the command itself is a separate row (retirement was "approved for retirement (R30, R66 A2)" per BATCH-AUDIT-SPINE-AND-TOOLS-2026-10-04.md:49 but "lane 11 kept it"; ANSWER-SEAT-CHECKLIST-2026-10-10.md:1102 still lists it on the retire list).

Is L5 launched? NO.
- queue.log final line (C:\Users\1028120\.claude\jobs\636ce8d7\tmp\queue.log): `[queue] watch ended after 50 poll(s): fired 4, held-failed 0, routed-codespace 0, of 6; DEADLINE -- still pending: lane-bu-1536-routing, lane-bu-1450-boot-v2`
- lanes.json: lane-bu-1450-boot-v2 state QUEUED (receipt `to-browser/SESSION-dispatcher-bu-2026-10-15.md`)
- No worktree `lane-bu-1450-boot-v2`, no branch, no `LANE-bu-1450-boot-v2.CLAIMED-*` in to-cc, no job. Gate in contract l.78: "**Starts after `lane-bu-1539-transport` is merged.**" - `git branch --merged main` does not list worktree-lane-bu-1539-transport (tip a5ff5843 "feat(transport): architect inbox (query --since)... [#1539] [#1454]" is unmerged; job db75a3c3 still `working`). Queue watcher already hit its DEADLINE, so it is not polling any more; L5 will not self-start.


## C. Part C raw findings (verbatim from the read-only subagent)

# Part C findings (2026-10-15, read-only)

Method: filesystem LastWriteTime/CreationTime >= 2026-10-14 00:00 under H:\My Drive\CLAUDE PROMPT DIR\{to-browser,to-cc}: 148 files. HOME test = a tracked file with the SAME BASENAME on origin/main (`git ls-tree -r`) -> found for ZERO of the 148. Second test = `git grep -F <stem>` on origin/main and the 4 branches that carry 10-14..15 records (CITED = named inside a repo file; a citation is NOT a home).

## 1. Inventory (sizes bytes; mtime local)

Legend: HOME = tracked copy by that name. CITED-IN = repo files that quote the name. All "-vN-superseded" files listed as groups; every one has HOME NONE.

### to-browser/ (CC -> browser)
| name | kind | size | mtime | HOME | CITED-IN (main) |
|---|---|---|---|---|---|
| ANSWER-outgoing-seat-interview-2026-10-14.md | other (ANSWER) | 9635 | 10-14 13:34 | NONE | none |
| ANSWER-session-plan-tech-architect-45-2026-10-14.md | other (ANSWER) | 7250 | 10-14 15:02 | NONE | none |
| QUESTION-outgoing-seat-interview-2026-10-14.md | other (QUESTION) | 4871 | 10-14 19:02 | NONE | none |
| QUESTION-session-plan-tech-architect-45-2026-10-14.md | other | 2395 | 10-14 19:02 | NONE | none |
| SUPPLEMENT-QUESTIONS-2026-10-14-dev-knowledge-architect.md | other | 4144 | 10-14 00:15 | NONE | none |
| DIGEST-BUILD1-CHALLENGE-EVAL1-2026-10-15.md | DIGEST | 16778 | 10-15 12:10 | NONE | none |
| DIGEST-BUILD1-CHALLENGE-EVAL2-2026-10-15.md | DIGEST | 9339 | 10-15 12:10 | NONE | none |
| DIGEST-BUILD1-CHALLENGE-M2-R113-2026-10-15.md | DIGEST | 4315 | 10-15 12:10 | NONE | tasks/1536-provider-routing-follows-r104-copilot-first-priced-5-5-models.md |
| DIGEST-BUILD1-CHALLENGE-M3-R114-2026-10-15.md | DIGEST | 4983 | 10-15 12:10 | NONE | tasks/1535-the-outer-loop-runs-in-code-the-689-loop-step-and-adr-130.md |
| DIGEST-BUILD1-CHALLENGE-M4-RUNNER-2026-10-15.md | DIGEST | 2238 | 10-15 12:10 | NONE | none |
| DIGEST-BUILD1-CHALLENGE-M5-L6-2026-10-15.md | DIGEST | 3524 | 10-15 12:10 | NONE | tasks/1539-the-architect-reads-an-inbox-and-request-status-is-derived.md |
| DIGEST-BUILD1-CHALLENGE-RESPONSES-2026-10-15.md | DIGEST | 11805 | 10-15 12:10 | NONE | none |
| DIGEST-BUILD1-DESIGN-RECHECK-2026-10-15.md | DIGEST | 3945 | 10-15 12:13 | NONE | none |
| DIGEST-BUILD1-READY-2026-10-15.md | DIGEST | 7676 | 10-15 12:13 | NONE | JOURNAL.md; docs/audits/2026-10-15-technical-batch-bu-manifest.md; docs/intake/2026-10-15-tech-build1-owed-rows.md |
| DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md | DIGEST | 15356 | 10-14 23:53 | NONE | tasks/1535-...; tasks/1538-rulings-r100-r115-land-in-standing-rulings-by-id.md |
| DIGEST-DESIGN-OUTER-LOOP-2026-10-15-checker.md | DIGEST | 8689 | 10-14 23:54 | NONE | none |
| DIGEST-HANDOFF-GAPS-2026-10-14.md | DIGEST | 6260 | 10-14 23:42 | NONE | none |
| DIGEST-HANDOVER-ANSWERS-2026-10-14.md | DIGEST | 17429 | 10-14 19:17 | NONE | none |
| DIGEST-HOW-WORK-RUNS-2026-10-14.md | DIGEST | 6026 | 10-15 01:52 | NONE | none |
| DIGEST-NIGHT-READY-2026-10-14.md | DIGEST | 4866 | 10-14 20:29 | NONE | none |
| DIGEST-OPERATOR-ASKS-REGISTER-2026-10-14.md (+v1..v4-superseded: 9844/10572/14465/18174) | DIGEST | 24144 | 10-14 18:36 | NONE | none |
| DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md | DIGEST | 12276 | 10-15 14:56 | NONE on main | on branch worktree-define-outcomes-2026-10-15: docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md + tasks/1551..1555 cite it |
| DIGEST-OUTER-LOOP-RESEARCH-2026-10-14.md (+v1-superseded 12635) | DIGEST | 12930 | 10-14 19:16 | NONE | none |
| DIGEST-PHASE0-2026-10-14.md | DIGEST | 13339 | 10-14 16:29 | NONE | none |
| DIGEST-TEST-EXECUTION-MAP-2026-10-15.md | DIGEST | 4418 | 10-15 13:47 | NONE | none |
| DIGEST-TEST-STRATEGY-DECISION-2026-10-15.md | DIGEST | 10630 | 10-15 14:56 | NONE on main | branch worktree-test-strategy-rows-2026-10-15: docs/intake/2026-10-15-tech-test-strategy-rows.md + tasks/1560 cite it |
| DIGEST-TEST-STRATEGY-DECISION-2026-10-15-ANNEX.md | DIGEST | 41221 | 10-15 14:57 | NONE | none |
| DIGEST-VERIFIED-HARNESS-MAP-2026-10-15.md | DIGEST | 14706 | 10-14 23:51 | NONE | none |
| DIGEST-VERIFY-{ci,commands-skills,dispatch,handoff-tools,hooks-gates,land,providers,spine-engine,telemetry,transport}-2026-10-14.md (10 files, 3.4-6.1 KB each) | DIGEST | ~46 KB total | 10-14 23:31-23:45 | NONE | none |
| INDEX.md | other (generated index) | 375536 | 10-14 23:46 | NONE (basename); name appears inside other files only | n/a |
| LANE-END-codespace-finish-2026-10-14.md | LANE | 12312 | 10-14 23:57 | NONE | JOURNAL.md on branches worktree-codespace-sample/-finish (not main) |
| LANE-END-green-main-2026-10-14.md | LANE | 10063 | 10-15 01:52 | NONE | JOURNAL.md (main) |
| LANE-END-lane-nv-{1450-f-handoff-gaps,689-e-skills-engine,929-a-dispatch-land,929-b-ci-gates,929-c-handoff-transport,929-d-telemetry-providers}.md (6, ~3.1 KB) | LANE | ~19 KB | 10-14 23:32-23:46 | NONE | none |
| LEDGER-dev-knowledge.md (+v185..v209-superseded, 25 files, 2.1-5.3 KB) | LEDGER | 3253 (cur) | 10-15 15:49 | NONE (basename); name cited in JOURNAL.md + two docs/audits/2026-09-0{8,9}-*lane-v-000-seat-templates-ledger* | n/a |
| RATIFICATION-2026-10-14.md (+v1..v8-superseded) | other (RATIFICATION) | 5443 | 10-15 13:55 | NONE (basename) | JOURNAL.md; docs/handoffs/2026-10-14-dev-knowledge-architect/HANDOFF_BOOT.md; .../PASTE_THIS.md; tasks/1536,1537,1538; tests/test_handoff_restamp.py |
| SESSION-b2w4-finish.md | SESSION | 49384 | 10-14 00:05 | NONE | docs/audits/2026-10-12-technical-batch-bw-close-packet.md |
| SESSION-{design-outer-loop-2026-10-14, dispatcher-bu-2026-10-15, dispatcher-nv-2026-10-14, integrator-bu-2026-10-15, integrator-nv-2026-10-14, lane-nv-1450-f-handoff-gaps, lane-nv-689-e-skills-engine, lane-nv-929-a/b/c/d}.md (11) | SESSION | 1.2-8.3 KB | 10-14 23:32 .. 10-15 15:54 | NONE | none |
| STATE-BATCH-NV.md, STATE-bu-2026-10-15.json, STATE-bu-2026-10-15-dispatcher.json, STATE-nv-2026-10-14.json, STATE-nv-2026-10-14-dispatcher.json | STATE | 355-2315 | 10-14 23:46 .. 10-15 15:54 | NONE | none |

### to-cc/ (browser -> CC)
| name | kind | size | mtime | HOME | CITED-IN (main) |
|---|---|---|---|---|---|
| AMEND-BATCH-BUILD1-PREP-2026-10-15.md (+v1..v4-superseded) | BATCH/amend | 8147 | 10-15 11:21 | NONE | docs/audits/2026-10-15-technical-batch-bu-manifest.md; tasks/1539; tasks/1540 |
| BATCH-BU-COMMON-2026-10-15.md | BATCH | 6793 | 10-15 11:57 | NONE | docs/audits/2026-10-15-technical-batch-bu-manifest.md |
| BATCH-BUILD1-PREP-2026-10-15.md | BATCH | 8451 | 10-15 10:58 | NONE | manifest; docs/intake/2026-10-15-tech-build1-owed-rows.md; tasks/1535 |
| BATCH-CODESPACE-FINISH-2026-10-14.md | BATCH | 4932 | 10-14 18:27 | NONE | tasks/1537-the-codespace-lane-path-finishes-and-agy-signs-in-by-a-link.md |
| BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md | BATCH | 4489 | 10-15 13:55 | NONE on main | branch test-strategy-rows: docs/intake/2026-10-15-tech-test-strategy-rows.md, tasks/1560-1568 |
| BATCH-DEFINE-OUTCOMES-2026-10-15.md | BATCH | 5268 | 10-15 14:01 | NONE on main | branch define-outcomes: intake 112 + tasks/1551-1555 |
| BATCH-TEST-GRAPH-DATA-2026-10-15.md | BATCH | 3452 | 10-15 14:00 | NONE | none |
| BATCH-DESIGN-OUTER-LOOP-2026-10-14.md (+v1-superseded) | BATCH | 8211 | 10-14 23:19 | NONE | none |
| BATCH-GREEN-MAIN-PILOT-2026-10-14.md (+v1-superseded) | BATCH | 6787 | 10-14 18:20 | NONE | JOURNAL.md; docs/intake/2026-10-15-tech-ci-verdict-step-window-overlap.md; ...map-refresh-closed-loop.md |
| BATCH-NIGHT-PREP-2026-10-14.md (+v1..v3-superseded) | BATCH | 8059 | 10-14 20:08 | NONE | none |
| BATCH-NV-COMMON-2026-10-14.md (+v1-superseded) | BATCH | 6967 | 10-14 23:00 | NONE | none |
| BATCH-PHASE0-EVIDENCE-2026-10-14.md (+v1-superseded) | BATCH | 8511 | 10-14 15:44 | NONE | none |
| BATCH-VERIFY-BOOT-2026-10-14-superseded.md | BATCH | 5043 | 10-14 15:06 | NONE | none |
| DISPATCHER-BU-2026-10-15.md | other (dispatcher) | 5117 | 10-15 11:57 | NONE | JOURNAL.md; BU manifest |
| INTEGRATOR-BU-2026-10-15.md | other (integrator) | 6862 | 10-15 11:57 | NONE | JOURNAL.md; BU manifest |
| DISPATCHER-NV-2026-10-14.md, INTEGRATOR-NV-2026-10-14.md | other | 4576 / 5981 | 10-14 20:27 | NONE | none |
| INTEGRATOR-BU.CLAIMED-3cdb5b69; LANE-bu-1535-outer-loop.CLAIMED-28cc9f14; LANE-bu-1537-codespace-finish.CLAIMED-43f6418c; LANE-bu-1539-transport.CLAIMED-db75a3c3; LANE-bu-863-prompts-guard.CLAIMED-18d1781a | STATE (claim markers) | 111 each | 10-15 12:33..13:57 | NONE (runtime markers) | none |
| LANE-codespace-sample-2026-10-14.md | LANE | 2378 | 10-14 19:08 | NONE (run record landed on branch as docs/audits file, see s.3) | none |
| PLAN-HARNESS-2026-10-14.md (+v1..v6-superseded) | PLAN | 5473 | 10-15 12:41 | NONE | docs/audits/2026-10-15-technical-batch-bu-manifest.md |
| PLAN-HARNESS-2026-10-15-withdrawn.md | PLAN | 5962 | 10-15 15:49 | NONE | none |
| SUPPLEMENT-ANSWERS-2026-10-14-dev-knowledge-architect.md (+v1-superseded) | other | 9022 | 10-14 12:41 | NONE | none |

Tallies: DIGEST 38 files (incl. 5 superseded), LEDGER 26, RATIFICATION 9, SESSION 12, LANE-END 7, STATE 5, PLAN 8, BATCH ~20, AMEND 5, other remainder.
Note: no unmerged branch carries any of these basenames either (ls-tree/grep on define-outcomes, test-strategy-rows, codespace-sample, codespace-finish: only citations).

## 2. Proposed repo home for NONE decision/analysis records (from governance only)

Rules found (verbatim):
- origin/main:protocols/STANDING_RULINGS.md:3664: "Everything written to `to-browser/` is a GENERATED copy: the repo stays the single source, and a copy there is a copy, never an authority."  (ruling (m))
- origin/main:protocols/STANDING_RULINGS.md:3705: "**(n) STANDING DELIVERY RULE - a deliverable is copied to `to-browser/` as a session's last act**" (direction is repo -> to-browser; the repo copy is expected to exist first)
- origin/main:protocols/OPERATOR-INTERFACE.md:123: "| `LEDGER-<repo>.md` | the operator's read surface, overwritten each batch and wrap | browser | `to-browser/` |"  -> LEDGER/STATUS are transport-only surfaces; "exactly two ledgers exist" (STANDING_RULINGS ruling (m) v2 amendment).
- origin/main:protocols/OPERATOR-INTERFACE.md:114-115: STATUS-<seat> / SESSION-<seat> homes are `to-browser/`; :120 RATIFICATION-<date> home `to-browser/`; :129 "`retention` above moves the consumed ones to `archive/<window-date>/` at wrap".
- origin/main:protocols/OPERATOR-INTERFACE.md:128-129: "Every browser artifact - retrospectives, plans, contracts - travels on this transport rather than through Downloads".
- origin/main:protocols/STANDING_RULINGS.md:4592: "Every architect ruling and operator ratification that `to-browser/DIGEST-HANDOFF-READINESS-2026-09-23.md` ..." and :4758 "Every item of `to-browser/RATIFICATION-2026-09-24.md` ..." and :4828/:4867/:4906 "Landed by `lane-...`" -> precedent: rulings land as an entry in protocols/STANDING_RULINGS.md citing the to-browser file by name; the transport file itself is NOT copied into the repo.
- origin/main:ecosystem/fleet-shape-spec.yaml:374-385: `audit_class_enum:` = technical, functional, qa, census, verification, ecosystem-audit, conformance-nightly-digest, changelog-review, codex, fresh-eyes, incident-evidence. (`DIGEST` is NOT a class; "conformance-nightly-digest" is only the recurring-report family.)
- origin/main:docs/decisions/ADR-101-hermetization.md:64: "**Rule B (audit grammar).** An added `docs/audits/*.md` whose name fails `<date>-<class>-<slug>` with `<class>` whole-token matched against the CLOSED enum ... -> **BLOCK**."
- origin/main:docs/decisions/ADR-101-hermetization.md:63: "**Rule A (top-level seal).** ... a new Tier-2 `docs/<genre>/` folder -> **BLOCK**." (so no new docs/digests/ folder)
- origin/main:docs/intake/README.md:144: "**Intake doc = WHAT/WHY** - problem, scenarios, requirements, ex-ante acceptance" (docs/intake/ = requirements spine, not analysis archive).

Proposals:
| to-browser/to-cc file | proposed home | basis |
|---|---|---|
| DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md | already cited by intake 112 (`docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md`) on branch worktree-define-outcomes-2026-10-15 - the in-repo consumer exists; verbatim copy: `docs/audits/<date>-<class>-<slug>.md`, class technical (enum :375) | ADR-101 Rule B + fleet-shape-spec :374 |
| DIGEST-TEST-STRATEGY-DECISION-2026-10-15 (+ANNEX) | same: cited by intake 115 on branch worktree-test-strategy-rows-2026-10-15; decision record -> STANDING_RULINGS entry citing it (precedent :4592/:4885 R11 -> ADR-127 "in-repo record of the decision itself") ; analysis body -> `docs/audits/2026-10-15-technical-<slug>.md` | STANDING_RULINGS precedent + ADR-101 Rule B |
| DIGEST-BUILD1-* (EVAL1/2, CHALLENGE-*, DESIGN-RECHECK, READY), DIGEST-DESIGN-OUTER-LOOP-*, DIGEST-VERIFIED-HARNESS-MAP, DIGEST-VERIFY-* (10), DIGEST-HANDOFF-GAPS, DIGEST-HANDOVER-ANSWERS, DIGEST-HOW-WORK-RUNS, DIGEST-NIGHT-READY, DIGEST-OPERATOR-ASKS-REGISTER, DIGEST-OUTER-LOOP-RESEARCH, DIGEST-PHASE0, DIGEST-TEST-EXECUTION-MAP | if kept in repo: `docs/audits/<date>-<class>-<slug>.md` with class from the closed enum (technical / verification / census fit by name); no rule says a DIGEST-* MUST be copied in. Several are already cited by name from tracked files (tasks/1535, 1536, 1538, 1539, JOURNAL.md, BU manifest) i.e. cited as external transport files | ADR-101 Rule B only; "no rule found" that mandates archiving DIGEST-* transport files |
| PLAN-HARNESS-2026-10-14 / 10-15-withdrawn, BATCH-*, AMEND-*, DISPATCHER/INTEGRATOR-* (to-cc) | no rule found for a repo copy. Precedent: OPERATOR-INTERFACE.md:118 AMEND/:126 BATCH have home `to-cc/` (transport only); BU manifest already cites them by name (docs/audits/2026-10-15-technical-batch-bu-manifest.md). Landed contracts for lanes go under `prompts/*` (ADR-101 home allowlist, line ~238 "SANCTIONED_TIER1_DIRS += `prompts`") | OPERATOR-INTERFACE.md:118,126; ADR-101 |
| RATIFICATION-2026-10-14.md | decisions land in protocols/STANDING_RULINGS.md ("Landed by `lane-...`" pattern :4828/:4867/:4906); open row: tasks/1538-rulings-r100-r115-land-in-standing-rulings-by-id.md (on main) is the filed vehicle | STANDING_RULINGS.md + row 1538 |
| LEDGER-*, SESSION-*, STATE-*, LANE-END-*, QUESTION/ANSWER, INDEX.md, *.CLAIMED-* | no repo home intended: transport-only surfaces per OPERATOR-INTERFACE.md:114-125 and STANDING_RULINGS.md:3664; retention = `archive/<window-date>/` under the prompts dir (OPERATOR-INTERFACE.md:129). NOTE: JOURNAL.md is the repo-side narrative (cites LANE-END-green-main, LEDGER, RATIFICATION) | rules above |

Caveat: ruling (m) says the to-browser copy is generated FROM the repo; for the DIGEST-* files the reverse happened (no repo source). I found no rule that says what to do in that case - "no rule found".

## 3. Pushed branches not merged into origin/main (after `git fetch origin`)
Last main commit touching JOURNAL.md: `7437920e docs(journal): 2026-10-15 (c) batch BU (BUILD-1) frozen`. None of the branches below touches JOURNAL.md except the two codespace ones noted.

| branch | ahead/behind main | commits | files | what is visible about landing |
|---|---|---|---|---|
| origin/worktree-define-outcomes-2026-10-15 @ 69ab3bc9 | 1 / 0 | `docs(tasks): file [#1551]-[#1555] + intake 112` | 10 files, +119/-8: BACKLOG.md, docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md, docs/intake/README.md, docs/intake/manifest.json, tasks/1551..1555, tasks/manifest.json | Commit body HAS `kill-candidates: none -- ...` (flush-left). No JOURNAL.md entry/anchor in diff. 0 behind -> fast-forwardable base; main requires --no-ff merge. Missing: JOURNAL anchor (block-unanchored-push is the pre-push rule per CLAUDE.md s.9). [#id] close tags not needed (rows added, not closed). |
| origin/worktree-test-strategy-rows-2026-10-15 @ 496b0951 | 1 / 0 | `docs(tasks): file rows [#1560]-[#1568] and intake 115` | 14 files, +190/-8: docs/intake/manifest.json, intake 115 md, tasks/1560..1568, tasks/manifest.json (+README/BACKLOG not seen in tail of stat) | Commit body HAS `kill-candidates: [#1383] -- ...`. No JOURNAL change. 0 behind. Missing: JOURNAL anchor; --no-ff merge. NOTE both branches add disjoint intake ids (112, 115) but both edit tasks/manifest.json and docs/intake/manifest.json -> second merge will likely conflict (generated files; MEMORY: "generated-file-merge-conflict-is-regenerated-not-refused"). I did not test-merge. |
| origin/chore/bu-merge-receipts @ 5a208874 | 1 / 0 | `chore(receipts): close the merge receipt for build1-prep (b6161972...)` | logs/MERGE-RECEIPTS.jsonl +1 | single-line receipt; no JOURNAL, no kill-candidates (not adding an id). |
| origin/worktree-codespace-sample-2026-10-14 (tip b7787edb) | 51 / 0 | 51 commits incl. lane-bu-1537-codespace-finish work (agy sign-in, schema token, EXIT trap) + `docs(codespace-sample): the Codespace sample lane run record` + audits-index regen | 25 files +6486/-229: scripts/dispatch.py (+1058), tests/*, JOURNAL.md, audit record | Carries JOURNAL.md change. Is a superset chain of worktree-lane-bu-1537-codespace-finish (same 98f5a8d6/d42a6ce6 commits). Needs lane-integrate (full suite once at integration per AGENTS.md), --no-ff. |
| origin/worktree-lane-bu-1537-codespace-finish (tip 1f0735c9) | 51 / 0 | 51 (fix/test RED/chore pins; last: agy-signin-start one-Enter) | 23 files +6536/-228 | No JOURNAL.md in diff -> JOURNAL anchor missing; lane of batch BU row [#1537]; 0 behind. |
| origin/worktree-codespace-finish-2026-10-14 (tip f7cc1ef6) | 43 / 30 | 43; last `docs(journal): 2026-10-14 (b) BATCH-CODESPACE-FINISH -- REFUSE after round 2` | 22 files +5362/-218 | Journal entry says REFUSE; 30 commits behind main. Predecessor carried into lane-bu-1537 (commit dccc2c03 "carry worktree-codespace-finish-2026-10-14 @ f7cc1ef6"). Likely superseded by the two above. |
| origin/worktree-integrate-bw (tip 0d3f7433, 2026-10-13) | 1 / 34 | receipt close for b2-w4-close | 1 file +1 | stale, no 10-14/15 content. |
| origin/worktree-lane-bw-1450-boot-teaching (2026-10-13) | 19 / 93 | boot v2 five F4 pointers, R95 D1 citation check [#1450] | 17 files +1955/-105 | Older than window; 93 behind. |
| origin/worktree-lane-bw-1374-lane-controller (2026-10-13) | 13 / 93 | lane-controller copilot/Windows fixes | 7 files +991/-30 | Older than window; 93 behind. |
| origin/worktree-b2w2-codespace-finish (2026-10-10) | 43 / 217 | parity-run records | 20 files | Old, 217 behind. |
| origin/automation/fleet-audit | 114 / 9345 | routine baselines 10-14, 10-15 | - | `git diff origin/main...` fatal: "no merge base" (unrelated history); routine branch, not a landing candidate. |

Branches carrying 2026-10-14..15 rows/records: define-outcomes, test-strategy-rows, chore/bu-merge-receipts, codespace-sample, lane-bu-1537-codespace-finish, codespace-finish-2026-10-14, automation/fleet-audit.

