# Lane AB-828 closure census

Frozen source: `DIGEST-2026-09-16-closure-candidates.md` (sha256 `c21d7e8f9470429dcf3d66d4a288332d7cccdc21e517f5178854cf6a9df8acee`).
The digest was rehashed before work. Table 1's 25 permitted rows were re-witnessed and closed with the proving SHAs below; Table 2 was not touched.

## Premises and filings

- `[#752]` is closed only after filing the transcript-read and receipt legs, including the untested `--permission-mode` leg, as `[#828]` (aa-12 / `e17c6200`).
- `[#613]` is CLOSE-PRE on its recorded witness. Its live-table test is RED at this tip (`codex` versus `sol`); that separate defect is `[#829]`.
- The digest instrument defect is filed as `[#830]`: witness frontmatter/schema backfill and a Q2 mode for `propose_row_closures.py`. No implementation was made in this lane.
- FPG-1 answers the reference half of the census. No existing organ answers last-touched dates; that gap is carried in `[#828]` rather than adding another task row.

## Table 1 closures

| Row | Proving SHA | Witness / caveat |
|---:|---|---|
| 740 | `f903a24` | dispatch conformance test |
| 742 | `dfe72365` | actions verdict unreadable-job tests |
| 743 | `ed93586f` | root-file seat-refusal test |
| 744 | `8bc3ea98` | incomplete receipt median tests |
| 750 | `d91603a8` | merge receipt completeness tests |
| 751 | `2e5c31bc` | lane cost rate/token/report tests |
| 752 | `a9aa67a6` | dispatch and receipt routing tests; --permission-mode gap filed [#828] |
| 765 | `bfd55534` | quality requirements hook and tests; duplicate [#782] floor caveat |
| 780 | `5f270cd9` | lane z-11 comparison matrix and dispositions |
| 784 | `73789d49` | lane z-10 M04 packet |
| 785 | `ad03c361` | provider bench logs and tests; gemini unreachable, agy unpriced |
| 470 | `2812cd9d` | cp1252 check-summary test |
| 587 | `e806376e` | journal anchor byte-identity test |
| 591 | `8e832523` | substrate refusal/override tests |
| 592 | `dd76e2b8` | dispatch drift tests |
| 596 | `f8ae0f6d` | proof-layer planted-guard test |
| 597 | `6a4740ab` | all-checks tier declaration test |
| 600 | `b14306bc` | handoff probe boundedness/era tests |
| 601 | `b043b9e1` | supplement-folded check and tests |
| 605 | `79d5707b` | consumer-root resolution tests |
| 608 | `c52c5daa` | journal tiling/shared predicate tests |
| 613 | `09fd7a00` | L0 routing agreement test; live-table RED filed [#829] |
| 626 | `07e3adcb` | bucketed proposal discovery tests |
| 643 | `d30d1187` | handoff preflight/assembly refusal tests |
| 653 | `e73d4b84` | fleet-shape spec version/changelog/reconciliation |

## Table 2 awaiting operator

| Row | Digest evidence | Disposition |
|---:|---|---|
| 303 | `3c9418cc` | seed_runbook.py deleted; operator retirement decision |
| 369 | `3c9418cc` | boundary_headers.py deleted; operator retirement decision |
| 383 | `5f9489c1` | desired_state_report.py deleted; re-scope or retire |
| 604 | `3c9418cc` | validate_onboarding_rulings.py deleted; re-scope or retire |
| 617 | `c9ea3b07` | gen_trend_dashboard.py deleted; re-scope or retire |

## Age-and-abandonment census

Last-touched is read from the row file's latest git commit. Referenced-by is the persisted FPG-1 consumer count; FPG-1 is the organ used for that half. The last-touched half has no existing organ answer and is therefore marked `unanswered -- [#828]`.

| Row | Last touched | Referenced by | Organ |
|---:|---|---:|---|
| 112 | `45ff9a74|2026-08-29` | 27 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 130 | `8cb96a17|2026-08-29` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 145 | `45ff9a74|2026-08-29` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 146 | `45ff9a74|2026-08-29` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 170 | `2ae7bf39|2026-08-12` | 20 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 171 | `45ff9a74|2026-08-29` | 43 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 185 | `5c8a9d6d|2026-07-28` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 210 | `18b2214c|2026-08-16` | 23 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 241 | `412506fb|2026-09-14` | 31 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 242 | `7bf20766|2026-08-27` | 43 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 267 | `45ff9a74|2026-08-29` | 26 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 271 | `a83d4e5a|2026-08-28` | 28 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 274 | `aba76527|2026-08-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 277 | `45ff9a74|2026-08-29` | 26 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 293 | `7bf20766|2026-08-27` | 42 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 298 | `ee01a2c1|2026-08-29` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 334 | `5c8a9d6d|2026-07-28` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 340 | `5c8a9d6d|2026-07-28` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 341 | `8b04b6f1|2026-08-13` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 342 | `5c8a9d6d|2026-07-28` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 343 | `5c8a9d6d|2026-07-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 345 | `5c8a9d6d|2026-07-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 347 | `8b04b6f1|2026-08-13` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 351 | `0bacab02|2026-08-16` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 354 | `5c8a9d6d|2026-07-28` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 357 | `9ca3c8f3|2026-08-13` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 359 | `2ae7bf39|2026-08-12` | 35 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 361 | `9f89ce3e|2026-08-18` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 362 | `ca49020a|2026-08-13` | 35 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 365 | `5c8a9d6d|2026-07-28` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 369 | `52d230cc|2026-08-13` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 371 | `ca49020a|2026-08-13` | 24 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 383 | `52d230cc|2026-08-13` | 51 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 385 | `7bf20766|2026-08-27` | 29 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 387 | `05fb0f37|2026-08-15` | 27 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 388 | `ae55ff8b|2026-07-28` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 389 | `992891c4|2026-08-13` | 24 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 390 | `52d230cc|2026-08-13` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 392 | `5c8a9d6d|2026-07-28` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 393 | `0bacab02|2026-08-16` | 27 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 400 | `9ce96be8|2026-07-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 401 | `5c8a9d6d|2026-07-28` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 402 | `5c8a9d6d|2026-07-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 403 | `5c8a9d6d|2026-07-28` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 404 | `5c8a9d6d|2026-07-28` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 405 | `5c8a9d6d|2026-07-28` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 413 | `7bf20766|2026-08-27` | 20 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 414 | `6f06c8a5|2026-08-13` | 20 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 418 | `6f06c8a5|2026-08-13` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 419 | `7bf20766|2026-08-27` | 35 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 420 | `45ff9a74|2026-08-29` | 24 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 422 | `27ec8bc5|2026-07-30` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 426 | `353149ab|2026-08-22` | 49 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 427 | `5c8a9d6d|2026-07-28` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 428 | `59df6478|2026-08-18` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 430 | `41c040b4|2026-08-15` | 37 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 431 | `5c8a9d6d|2026-07-28` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 438 | `6602e841|2026-08-16` | 20 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 440 | `104a04f6|2026-07-28` | 20 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 442 | `9ce96be8|2026-07-28` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 445 | `99aceb54|2026-07-29` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 447 | `645822ba|2026-07-30` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 448 | `6ae2acb0|2026-07-30` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 451 | `6bfa544f|2026-07-30` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 454 | `584ab835|2026-07-31` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 457 | `fce8b5b0|2026-08-18` | 40 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 477 | `d2ba06ca|2026-08-03` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 478 | `d2ba06ca|2026-08-03` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 485 | `aad1a235|2026-08-04` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 487 | `41c040b4|2026-08-15` | 33 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 493 | `ae531acf|2026-08-13` | 21 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 496 | `4ca1ca23|2026-08-05` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 497 | `23518240|2026-08-05` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 500 | `23518240|2026-08-05` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 506 | `ae531acf|2026-08-13` | 29 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 509 | `e351b685|2026-08-07` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 510 | `05fb0f37|2026-08-15` | 30 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 511 | `05fb0f37|2026-08-15` | 40 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 514 | `fce8b5b0|2026-08-18` | 34 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 518 | `a4882b78|2026-08-09` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 519 | `5f17b771|2026-08-09` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 520 | `5f17b771|2026-08-09` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 522 | `05fb0f37|2026-08-15` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 523 | `59df6478|2026-08-18` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 526 | `2588d07d|2026-08-14` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 528 | `412506fb|2026-09-14` | 128 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 531 | `98f4bbd4|2026-08-18` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 533 | `45ff9a74|2026-08-29` | 47 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 534 | `b099f3ff|2026-08-19` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 535 | `ee01a2c1|2026-08-29` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 538 | `606e9b11|2026-08-17` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 540 | `fce8b5b0|2026-08-18` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 541 | `45ff9a74|2026-08-29` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 542 | `4836512f|2026-08-17` | 9 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 546 | `77e3147f|2026-08-17` | 9 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 547 | `523411de|2026-08-17` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 548 | `7bf20766|2026-08-27` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 550 | `59df6478|2026-08-18` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 551 | `98f4bbd4|2026-08-18` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 552 | `412506fb|2026-09-14` | 25 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 553 | `98f4bbd4|2026-08-18` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 554 | `f0681233|2026-09-15` | 29 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 555 | `45ff9a74|2026-08-29` | 24 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 559 | `7bf20766|2026-08-27` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 560 | `8f428e21|2026-08-19` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 561 | `45ff9a74|2026-08-29` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 564 | `b6e2044b|2026-08-20` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 567 | `b6e2044b|2026-08-20` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 568 | `b6e2044b|2026-08-20` | 12 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 570 | `80af6da8|2026-08-22` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 571 | `80af6da8|2026-08-22` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 572 | `92caed40|2026-08-22` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 573 | `92caed40|2026-08-22` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 574 | `92caed40|2026-08-22` | 8 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 575 | `92caed40|2026-08-22` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 576 | `92caed40|2026-08-22` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 578 | `b45e4146|2026-08-23` | 28 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 579 | `7bf20766|2026-08-27` | 15 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 580 | `9058308f|2026-08-26` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 581 | `9058308f|2026-08-26` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 582 | `9058308f|2026-08-26` | 18 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 583 | `9058308f|2026-08-26` | 9 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 585 | `9058308f|2026-08-26` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 586 | `9058308f|2026-08-26` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 588 | `dd2f78d9|2026-08-26` | 9 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 589 | `6b256fb9|2026-09-01` | 43 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 590 | `dd2f78d9|2026-08-26` | 61 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 593 | `dd2f78d9|2026-08-26` | 9 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 594 | `7bf20766|2026-08-27` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 595 | `dd2f78d9|2026-08-26` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 598 | `dd2f78d9|2026-08-26` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 599 | `d6c77aca|2026-08-26` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 602 | `d6c77aca|2026-08-26` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 603 | `d6c77aca|2026-08-26` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 604 | `d6c77aca|2026-08-26` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 606 | `d6c77aca|2026-08-26` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 607 | `914dc4aa|2026-08-28` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 609 | `dadda5fc|2026-09-06` | 8 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 610 | `412506fb|2026-09-14` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 611 | `dadda5fc|2026-09-06` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 612 | `20ec03fc|2026-08-28` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 615 | `3a4066eb|2026-09-01` | 25 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 616 | `49a3f854|2026-08-29` | 13 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 617 | `6ab764fc|2026-09-16` | 19 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 618 | `7f01e51a|2026-08-29` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 619 | `08029542|2026-08-31` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 620 | `3c83e377|2026-08-29` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 621 | `3c83e377|2026-08-29` | 22 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 622 | `3c83e377|2026-08-29` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 623 | `86bed827|2026-08-29` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 624 | `08029542|2026-08-31` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 625 | `fbe70097|2026-08-31` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 627 | `412506fb|2026-09-14` | 32 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 628 | `412506fb|2026-09-14` | 41 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 629 | `dadda5fc|2026-09-06` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 631 | `412506fb|2026-09-14` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 632 | `cd80ed66|2026-09-01` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 633 | `33a5c867|2026-09-01` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 634 | `b9db30f7|2026-09-05` | 8 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 637 | `301f2266|2026-09-08` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 639 | `301f2266|2026-09-08` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 640 | `301f2266|2026-09-08` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 641 | `289b4c8f|2026-09-08` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 642 | `77259f5d|2026-09-08` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 644 | `ff798a1a|2026-09-09` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 645 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 646 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 647 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 648 | `ff798a1a|2026-09-09` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 649 | `ff798a1a|2026-09-09` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 650 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 651 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 652 | `ff798a1a|2026-09-09` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 654 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 655 | `ff798a1a|2026-09-09` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 656 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 657 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 658 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 659 | `ff798a1a|2026-09-09` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 660 | `ff798a1a|2026-09-09` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 661 | `ff798a1a|2026-09-09` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 662 | `ff798a1a|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 663 | `ff798a1a|2026-09-09` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 664 | `7e7ff1a4|2026-09-11` | 44 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 665 | `412506fb|2026-09-14` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 666 | `0d00f631|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 667 | `412506fb|2026-09-14` | 8 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 668 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 669 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 670 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 671 | `8869eb23|2026-09-09` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 672 | `412506fb|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 673 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 674 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 675 | `412506fb|2026-09-14` | 30 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 676 | `412506fb|2026-09-14` | 17 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 677 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 678 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 679 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 680 | `412506fb|2026-09-14` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 681 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 682 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 685 | `412506fb|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 686 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 687 | `412506fb|2026-09-14` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 689 | `412506fb|2026-09-14` | 16 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 690 | `412506fb|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 691 | `412506fb|2026-09-14` | 10 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 693 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 694 | `412506fb|2026-09-14` | 11 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 695 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 696 | `412506fb|2026-09-14` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 697 | `83fd57c3|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 698 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 699 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 700 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 701 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 702 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 703 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 704 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 705 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 706 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 707 | `412506fb|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 715 | `412506fb|2026-09-14` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 719 | `412506fb|2026-09-14` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 720 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 721 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 722 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 723 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 724 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 725 | `cbcecb88|2026-09-11` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 726 | `cbcecb88|2026-09-11` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 728 | `cbcecb88|2026-09-11` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 729 | `cbcecb88|2026-09-11` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 730 | `86a4cbe0|2026-09-11` | 8 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 731 | `5d233b0e|2026-09-16` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 732 | `86a4cbe0|2026-09-11` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 733 | `86a4cbe0|2026-09-11` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 734 | `86a4cbe0|2026-09-11` | 14 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 735 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 736 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 737 | `412506fb|2026-09-14` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 738 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 739 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 741 | `412506fb|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 745 | `e0761575|2026-09-13` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 746 | `a7edeecf|2026-09-15` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 747 | `412506fb|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 748 | `bebd002f|2026-09-13` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 749 | `bebd002f|2026-09-13` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 753 | `dceb82e9|2026-09-14` | 6 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 754 | `5d233b0e|2026-09-16` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 755 | `530dbecf|2026-09-15` | 7 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 757 | `223353b7|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 758 | `223353b7|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 759 | `223353b7|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 760 | `223353b7|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 761 | `af0a2bc7|2026-09-14` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 762 | `bd8f5a9d|2026-09-14` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 763 | `6572c1b1|2026-09-15` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 764 | `6572c1b1|2026-09-15` | 5 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 766 | `b0539f12|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 767 | `b0539f12|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 768 | `b0539f12|2026-09-15` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 769 | `b0539f12|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 770 | `b0539f12|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 771 | `b0539f12|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 772 | `b0539f12|2026-09-15` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 781 | `0ca3a02b|2026-09-15` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 783 | `0ca3a02b|2026-09-15` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 786 | `779763e8|2026-09-15` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 787 | `83fd57c3|2026-09-15` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 788 | `6e9b7a4f|2026-09-15` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 789 | `279caaff|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 791 | `279caaff|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 792 | `766bf2f2|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 793 | `0d00f631|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 800 | `279caaff|2026-09-16` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 801 | `279caaff|2026-09-16` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 802 | `279caaff|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 803 | `279caaff|2026-09-16` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 804 | `0d00f631|2026-09-16` | 4 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 805 | `0d00f631|2026-09-16` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 806 | `0d00f631|2026-09-16` | 1 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 807 | `5d233b0e|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 808 | `d0fe3865|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 809 | `d0fe3865|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 810 | `d0fe3865|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 823 | `6ab764fc|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 824 | `6ab764fc|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 825 | `6ab764fc|2026-09-16` | 2 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 826 | `6ab764fc|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 827 | `d89b836a|2026-09-16` | 3 FPG-1 consumers | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 828 | `working tree (new row)` | 1 FPG-1 consumer | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 829 | `working tree (new row)` | 1 FPG-1 consumer | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |
| 830 | `working tree (new row)` | 1 FPG-1 consumer | `git log` (no organ) / FPG-1 refs; last-touch gap -> [#828] |

## Verification

- `uv run --locked python scripts/gen_task_tree.py --check`: PASS.
- `uv run --locked pytest tests/test_gen_task_tree.py tests/test_validate_backlog.py -x --tb=short`: PASS (167 passed).
- `uv run --locked python scripts/graph_queries.py orphan-census`: PASS.
- `uv run --locked python scripts/graph_queries.py process-list`: PASS (167 processes; 134 triggered; 33 not).
- `uv run --locked python scripts/decision_coverage.py metrics`: 112 accepted / 11 executing / 96 done.
- `uv run --locked ruff check ...`: PASS; `validate_backlog.py`: PASS (348 tasks, 2 pre-existing warnings).
- Targeted dispatch/receipt/quality witnesses: PASS (309 passed). Broader census witness selection: 358 passed, 5 skipped; one handoff probe was skipped because the host lacks `sed` (environmental, not a code assertion).
- `tests/test_routing_agreement.py::test_the_live_table_is_well_formed`: RED as frozen and filed as [#829], not counted green.
- `worktree_import_proof.py`: NOT-APPLICABLE (hub declares no importable package).

Filing-to-closing ratio: 3 distinct required filings (`[#828]`, `[#829]`, `[#830]`) / 25 closures. Census last-touch gap is carried by `[#828]`.
