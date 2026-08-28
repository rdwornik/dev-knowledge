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

**Last updated:** 2026-08-26
**Maintained by:** Rob
