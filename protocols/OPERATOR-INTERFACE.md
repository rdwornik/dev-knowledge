---
last_reviewed: 2026-09-08
reconciled_with: handoff-process@7.0.0
status: active
owner: Rob
---

# OPERATOR-INTERFACE — how content actually moves between a seat and this machine

<!-- scope: meta -->

> **What this is.** The four mechanics of the operator's interface, recorded once so a seat stops
> re-deriving them and stops re-explaining them to the next seat. These are capabilities of the
> transport, not preferences: they are the same on every window, and a seat that argues with one
> of them is describing a defect in this file rather than a fact about its own session.
>
> **Why it exists.** The 2026-08-26 handoff census measured 10 of 62 architect supplements
> recording one of these facts as if it were window-specific news, and 4 more recording the
> start-command one on its own. That is judgment-bandwidth spent on a constant. The supplement's
> Q6 is now scoped to changed *intent*; the procedure lives here.
>
> **Where it is read.** The v5 handoff bundle's Operator-facing forms card points here, so an
> incoming seat meets these facts in its own boot rather than by asking.

---

## 1. File exchange goes through the Downloads directory

A file travelling in either direction lands in the operator's prompts directory —
`$env:CLAUDE_PROMPTS_DIR`, and `~/Downloads` when that is unset. A contract dispatched to a lane,
an artifact handed back for review, a census result relayed from a cloud seat: all of them are
files in that directory, named and referred to by filename.

Two consequences a seat can act on directly:

- **A locator a seat is given may be a Downloads path rather than a repo path.** Reading it is a
  read of the operator's disk, which is why work needing it routes LOCAL (`protocols/PLAYBOOK.md`
  Ch8, the boundary test).
- **A file arriving twice arrives as `<name> (1).md`.** The suffixed copy is the newer one, and
  the un-suffixed one is stale — a seat that reads only the plain name reads the previous window.

**FILE EXCHANGE — the transport constant.** The heading above predates the Drive transport and is
kept as written; the constant below is what a seat acts on. Downloads remains the documented
fallback, and nothing else in this section changes.

    prompts dir  : $env:CLAUDE_PROMPTS_DIR (User scope; currently a Google Drive folder
                   synced by Drive for Desktop, which the browser reads/writes via the Drive
                   connector). THE VARIABLE IS THE SOURCE. The folder's location is the
                   operator's and may change without this file changing; a seat that hardcodes
                   a path has substituted a fact it cannot keep current for one it can resolve
    to-cc\       : browser to CC. Contracts, pastes, ARCHITECT-INBOX-<date>-<NNN>.md
    to-browser\  : CC to browser. Delivered artifacts (plain copies, same filename) and inbox
                   copies with a DONE <sha> line per item — the browser's ONLY witness that an
                   item ran
    read rule    : look in the prompts dir first; if the file is not there, ~\Downloads and its
                   to-cc\ / to-browser\ (fallback per FILE, not per variable)
    copy header  : every copy written to to-browser\ starts with one line
                   <!-- COPY OF <repo path>@<sha> - generated, never edited; the repo is the
                   source -->
    session start: every CC session RESOLVES the prompts dir from User scope and prints it on
                   boot (SessionStart hook or /lane-boot line), overriding a differing process
                   value; unset in both scopes prints "CLAUDE_PROMPTS_DIR unset - Downloads
                   fallback" so the fallback is never silent
    inbox naming : ARCHITECT-INBOX-<YYYY-MM-DD>-<NNN>.md, always numbered; items <NNN>-<letter>

**Transport v2 — schema, grammar, retention.** Amends the constant above; the grammar applies from
the NEXT window, and files already in flight stay as they are rather than being renamed mid-use.

    item schema  : every inbox item carries minimal frontmatter -
                   repo: <name> · owner-role: filings|dispatcher|integrator ·
                   files: [footprint] · gate: <none | DECLARE-<item>> · depends: [items]
                   OWNERSHIP AND GATES LIVE IN THE FILE, never in a chat paste. The dispatcher
                   computes disjoint groups from `files:` and boots N FILINGS lanes from them
    naming       : INBOX-<repo>-<YYYY-MM-DD>-<NNN>.md · DECLARE-<item>.md · STATUS-<repo>.md
                   (sections per session; edit only your own) · a delivery keeps its REPO
                   filename and carries the copy header
    retention    : at wrap, FILINGS moves consumed inbox items and delivered artifacts to
                   archive/<window-date>/ and STATUS keeps a one-line pointer, so a fresh
                   window opens on live items only
    ledgers      : STATUS-<repo>.md is the READ SURFACE; the DONE copies are the AUDIT TRAIL.
                   There is no third ledger, and adding one is the failure this clause forbids

*Why ownership belongs in the file.* A chat paste is not addressable: two sessions given
overlapping work by two pastes cannot detect the overlap, and the first evidence is a merge
conflict or a doubled filing. `files:` makes the footprint checkable BEFORE dispatch, which is the
same property the contract-freeze coupling scan (candidate (f)) wants one layer down.

*Folder rename, PENDING and sequenced.* `CLAUDE PROMPT DIR` becomes `claude-exchange` — no spaces,
lowercase, and it says what it carries. It is ONE operator act (rename in Drive, then
`SetEnvironmentVariable(..., "User")`), and it is deliberately ordered AFTER the User-scope
resolution hook lands, because until then a rename would break every seat holding an inherited
literal path. `to-cc/` and `to-browser/` keep their names; they are direction-named and correct.

Two clauses above exist because a specific failure happened, and they are cheap only until they
are skipped. A seat that inherits `CLAUDE_PROMPTS_DIR` from a shell predating the setting resolves
it to Downloads, finds `to-cc\` present but EMPTY, and reads that as "nothing filed" rather than as
a misresolved variable — the fallback directory EXISTING is what makes the failure silent, which is
what the session-start echo removes. And the `DONE <sha>` line is the browser's only witness: a
seat that finishes an item without writing it has, from the browser's side, not done the item.

**The copy header and byte-identity.** Prepending the header means a delivered copy is not
byte-identical to its blob. That is deliberate and it is the later ruling: the copy is an envelope
carrying a repo path and a SHA, so identity stays PROVABLE (compare the body below the header
against `git show <sha>:<path>`) while the file itself says what it is a copy of. A copy that does
not name its source is the stale-delivery failure waiting to happen.

**Transport v2.1 — the filename grammar, one table.** Extends the `naming` line above with the
shapes the 2026-09-06 night window actually used (inbox 028 criterion G). One grammar covers every
transport file, so a reader identifies a file's kind, its author and its direction from the name
alone. `<seat>` is a session name (`filings`, `integrator`), `<date>` is `YYYY-MM-DD`.

| Shape | What it carries | Written by | Home |
|---|---|---|---|
| `STATUS-<seat>.md` | a seat's running findings, kept current while it works | that seat | `to-browser/` |
| `SESSION-<seat>.md` | that seat's close-out account, written on stop | that seat | `to-browser/` |
| `QUESTION-<seat>.md` | a question raised without stopping, under night autonomy | that seat | `to-browser/` |
| `ANSWER-<seat>.md` | the reply to one | browser | `to-cc/` |
| `AMEND-<batch>-<NNN>.md` | an additive clarification to a live batch contract | browser | `to-cc/` |
| `ADDENDUM-<lane>-<tag>.md` | a change scoped to a single lane's contract | browser | `to-cc/` |
| `RATIFICATION-<date>.md` | the sitting's decision list, one row per item | filings | `to-browser/` |
| `UNOWNED-<date>.md` | unowned items enumerated, owner left unproposed | filings | `to-browser/` |
| `RETRO-<date>.md` | a window's retrospective | browser | `to-cc/` |
| `LEDGER-<repo>.md` | the operator's read surface, overwritten each batch and wrap | browser | `to-browser/` |
| `INBOX-<repo>-<date>-<NNN>.md` | one numbered architect item | browser | `to-cc/` |
| `DECLARE-<item>.md` | an operator ruling that gates an item | browser | `to-cc/` |
| `BATCH-<date>-<name>-CONTRACTS.md` | one batch's lane contracts | browser | `to-cc/` |

Every browser artifact — retrospectives, plans, contracts — travels on this transport rather than
through Downloads, and `retention` above moves the consumed ones to `archive/<window-date>/` at
wrap. `/handoff-verify` P8 checks a bundle's transport section against this table.

## 2. Inline chat paste of large content arrives empty — so uploads are `.md` files

Pasting a large body of text into the browser chat inline is unreliable: it can arrive truncated,
and past a size it arrives as an empty frame with no error. The transport gives no signal that it
degraded, so the reader's assumption that it arrived whole is where the cost lands
(`protocols/PLAYBOOK.md` Ch8, "Paste-vs-file transport").

**The working form is a `.md` file upload.** Anything longer than a short message travels as a
file rather than as pasted text. Two cheap discriminators when something did arrive by paste: the
artifact's own tail, and its closing fence. A paste that ends mid-sentence ended mid-transport.

The one deliberate exception is `PASTE_THIS.md`, which is assembled precisely so that a single
paste carries a whole bundle — and it ships a terminal `=== END OF PASTE ===` sentinel so a
truncated one is visible on sight.

**Rule 1 (inbox 029) — a browser decision exists only as a file.** A ruling spoken in chat
and not written to `to-cc/` has no addressable existence: no seat can cite it, and no gate can
resolve it.

**The chat is the cost, not the transport (inbox 030).** Measured 2026-09-06: an outgoing browser
chat spent roughly **30% of a usage window in 20 minutes of short answers**. The cause is not the
Drive transport — it is a five-day chat whose every turn re-processes its whole history, by then
30+ pasted session outputs of 10-20 KB and about 30 uploaded files, on the most expensive model.
**A Drive read is cheap and one-shot; a pasted transcript is permanent and is re-billed on every
later turn.** So the transport stays and the chat changes, along these lines:

| Line | Shape |
|---|---|
| Window | one sitting — a single milestone (ratification / GO / packet) or about 40 turns, then wrap. The bundle and transport make a wrap cheap by design; `turns per window` is a scorecard line |
| CC output | read from the transport — `STATUS-*`, `LEDGER-<repo>`, `QUESTION-*`, close packets — on "check". A pasted session log counts as a browser-seat defect (form-probe predicate #5) |
| File size | `STATUS-*` at or under 5 KB with a "now" section on top; history rotates to `archive/` at each batch close; a census reaches the browser as a summary of 40 lines or fewer |
| Seats | ONE chat per window, model switched per act (`DECLARE-BROWSER-TOPOLOGY-2026-09-06`). Routine acts — checks, relays, FREEZE, LEDGER refresh — run on the default model; when an act enters the ruling class the chat emits a fixed switch line naming the cost and the files it will read, one Fable turn happens, and the operator switches back. A second parallel chat buys nothing: the cost is context LENGTH, not chat count |
| Relaying | questions as files plus the LEDGER (inboxes 020 and 028-B) remove the operator's relaying once ratified |
| Order (inbox 033) | **Think, then gather, then act** — a fixed three-step order, stated before acting rather than reconstructed after it. **(1) PLAN** — what should be done and why, in a few lines, before any tool call, read or paste. **(2) INFORMATION** — what to gather, how, by whom, and at what model/effort, with the switch named aloud (`ROUTINE — Opus is enough` / `RULING AHEAD — Fable (est. ~N k tokens: <files>)`); gathering — reads, scans, digests — is Opus-class work at low effort, while conclusions and rulings are Fable-class at higher effort. **(3) ACT** — only after (1) and (2) are stated, and only what they stated. The operator's driving pattern is what makes the order cheap: he asks on Fable at LOW effort what the next act should be, the browser answers with (1)+(2), and he raises effort for the execution of what was already planned. **Form probe:** a browser turn that starts a read > 10 KB, a file write, or a paste block without (1)+(2) stated earlier in the same window **for that act** = defect. Carried into the v7.1 floor as item seven (#68/#76) |

## 3. Every session ships its exact start command

A session handed to the operator without the literal line that starts it does not get started.
The line is copied, not composed: its single source is `protocols/PLAYBOOK.md` Ch8, "The dispatch
table — the SOLE literal-command site", and a v5 bundle's forms card renders that line at
generation time rather than carrying a copy of it.

This applies to a lane contract, a dispatched brief, and a handover that expects a new seat to
open. Where the substrate is anything other than a local lane, the verb changes and Ch8's table
carries the substrate-named form.

## 4. Reports travel as files, not as chat text

A report, a census result, an audit or a review artifact is delivered as a file — into the repo
where it belongs in-tree, or into the Downloads directory where the destination is another seat.
A report pasted into chat is unciteable a window later, and it is subject to §2's silent
truncation on the way in.

The in-tree homes are the ones the taxonomy already defines (`docs/audits/`, `docs/decisions/`,
`docs/intake/`); a file with no in-tree home travels through Downloads and is named for its
subject and date.

**Standing delivery rule — candidate (n), filed not ratified.** A session that finishes a
deliverable copies it to `to-browser\` as its last act before it stops: an artifact that exists
only in-tree has not reached the seat that asked for it, and "it is committed" is not delivery.
The copy is a generated one under §1's `source` clause. Landing this as a habit is what the
candidate declines to do — the mechanism belongs in `/lane-integrate` and the close-packet step,
so the copy happens whether or not a session remembers it.

---

## 5. The browser role file is INSTALLED ONCE, not re-pasted (v6.3.0)

**The one-time act.** Install the contents of **`protocols/HANDOFF_BOOT.md`** as the browser
project's own **project instructions**. Once per browser project — not once per session, and not
once per handoff. That file *is* the seat's operating role.

**Why it is a one-time act and not a paste.** Through HANDOFF_PROCESS v6.2.0 the assembler inlined
the whole role file into every `PASTE_THIS.md`: ~17 KB of identical role text re-transmitted on
every single handoff, to an actor that can simply hold it. The browser project instruction field is
exactly the residency this repeated transmission was substituting for.

**What each paste carries instead — the ROLE PIN.** Every assembled `PASTE_THIS.md` now opens with
three lines: the role file's name, the live `handoff-process` version, its `sha256`, and a standing
refusal line —

> *If your project instructions do not carry this contract at this version+sha, say so before
> answering.*

**What the operator does with a refusal.** A seat reporting a mismatch is the mechanism WORKING, not
a failure to route around: re-install the current `protocols/HANDOFF_BOOT.md` into the project
instructions and re-paste. Residency without that refusal degrades silently the moment the resident
copy drifts, and a silently-stale role is strictly worse than a heavy paste — which is why the pin
carries teeth rather than merely announcing a version.

**The requirement did not change, only the mechanism.** `HANDOFF_PROCESS` still requires that the
role **reach** the browser; §"Browser-role delivery" now names residency + pin as the satisfying
mechanism. Nothing about the anti-bluff contract or the probe teeth depends on the role travelling
in the paste body.

---

## 6. The architect seat is ONE fleet-wide Project — "Dev — Architect Seat" (LIVE)

**Landed state as of 2026-08-28**, recorded as what exists rather than as a proposal. One
claude.ai Project hosts every architect window across every repo in the fleet; §5's install act is
performed against this Project.

- **Project knowledge holds exactly ONE file** — `protocols/HANDOFF_BOOT.md`. The reason is the
  RAG threshold: past a certain knowledge size a Project stops carrying its knowledge inline and
  falls back to retrieval, and a *retrieved* role is one the seat may or may not be shown on any
  given turn. Holding the knowledge to a single file keeps the role resident, which is the property
  §5's version-refusal pin depends on to have teeth.
- **Project instructions hold the pointer plus the version-refusal rule** — the three-line ROLE PIN
  of §5 and its refusal sentence, and nothing further. Instructions that restate the role would
  reintroduce the second copy this arrangement removes.
- **Per-repo projects were rejected, on measurement.** One Project per repo means N copies of the
  same role drifting apart independently — the version-drift disease already measured in this
  corpus, arriving by a new route. One seat, one role, one place it lives.

The scope of this entry is residency. What the role file *says* is `HANDOFF_BOOT.md`'s own content;
what obliges it to reach the browser at all is `HANDOFF_PROCESS.md`.

## 7. Operator-action steps end with a copy-ready block

OPERATOR ACTION STEPS: every step that requires the operator's action ends with a copy-ready
block — the exact shell command(s) or the exact CC paste — never a description of what will
happen. A description where a block belongs is an interface defect.

This generalises §3 from the start command to every step the operator is expected to run. The
failure is the same one: a described action is handed to the operator where a runnable one
belongs, and the gap between them is closed by the operator retyping it, or not at all.

---

## Scope, and what this file is not

This file records the **transport**. It rules nothing about content, routing, or authority:

- Which substrate a piece of work runs on → `protocols/PLAYBOOK.md` Ch8, the boundary test.
- The literal command for each substrate → Ch8's dispatch table, the sole site.
- What a handoff bundle contains and how it is verified → `protocols/HANDOFF_PROCESS.md`.
- What an outgoing architect owes the next seat → the same spec's supplement section.

A fact here that turns out to be wrong is a correction to this file, made once — rather than a
paragraph in the next window's supplement.

---

**Last updated:** 2026-09-06
**Maintained by:** Rob
