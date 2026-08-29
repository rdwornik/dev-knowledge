# [#614] lane-b — P1a re-pointed and EXECUTED, P1b byte-identity confirmed

**Why this file exists:** the frozen contract's done-contract item 2 — *"The P1a boot probe is
re-pointed, then **EXECUTED** against the new `README.md`… A re-point that reads correctly in a
diff and fails at boot is exactly what running it refuses"* — and item 3, the standing guard on
P1b. Both are discharged here by **running**, not by reading a diff.

**Bound at:** `c20d9239` (`docs(614): recreate the root README.md and supersede VISION.md at the
hub`), branch `worktree-lane-b-614-vision-to-readme`. Pre-lane main tip: `902b621b`.

---

## 1. The re-point (one line, `templates/handoff/v5/PROBES.md.tmpl:81`)

The rendered probe row now reads, verbatim:

```
| P1a | Quote, **substring-exact**, the **opening sentence** of `README.md` `## Vision` — *what {{REPO}} is*. (ADR-114, Accepted 2026-08-29: `README.md` supersedes `VISION.md` as the hub's canonical purpose document. In a CHILD repo, whose canonical purpose document is still `VISION.md`, re-bind the path — cross-repo probes are re-bound against target surfaces regardless.) | `README.md` `## Vision` | a paraphrase of "what this is" is not a substring; a summary rounds it off | `grep -A4 '^## Vision' README.md` → the quote must be a substring of the live section |
```

**Why the child-repo caveat rides in the row rather than in a follow-up.** The template renders for
any `{{REPO}}`, and **six of the eight ADR-104 children carry no root `README.md`** (measured
2026-08-29: only `terminal-setup` and `win-tooling` do). A bare re-point would therefore render a
probe that cannot resolve in three-quarters of the fleet. The caveat states the re-bind where a
reader meets the probe; it does not pretend the fleet has migrated.

**Neither rendered copy was touched.** `docs/handoffs/2026-08-28-dev-knowledge-architect/PROBES.md`
and the other 116 bundles are immutable (done-contract item 5) and still name `VISION.md` — which
is correct for an artifact sealed before the ruling.

## 2. P1a EXECUTED against the new `README.md` — output verbatim

```
$ grep -A4 '^## Vision' README.md
## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. Its **doctrine is host-independent**: the
conventions it defines, and the hub-local validators, generators and gates
$ echo $?
0
```

**Verdict: PASS.** The probe resolves, exits 0, and returns a section whose opening sentence —
*"`.dev-knowledge` is a universal LLM-driven development guide and methodology framework."* — is
substring-matchable, which is the whole of what P1a asks. This is the probe *run*, not the diff
read.

## 3. The old target, run as a control — it does not silently keep passing wrongly

```
$ grep -A4 '^## Vision' VISION.md
## Vision

**Canonical text: `README.md` "## Vision".**

`.dev-knowledge` is a universal LLM-driven development guide and methodology framework.
$ echo $?
0
```

**Read this deliberately.** `VISION.md` still resolves, because it is retained with its five-`## H2`
spine — thirteen machine constants and five deploy manifests depend on that. Its `## Vision` body
now **states its own supersession first** and then carries the one mirrored sentence. That sentence
is there for a named reason, recorded in an HTML comment beside it: `gen_handoff._vision_extract`
copies this section into every generated handoff bundle as the browser seat's orienting text, and
until that generator is re-pointed (**lane-a's** `scripts/gen_handoff.py`, tracked as `[#621]`) a
bare pointer here would degrade every new boot. **It is the only mirrored prose in the file**, and
its removal has a named owner rather than being left to be noticed.

## 4. P1b byte-identity (done-contract item 3) — mechanical, not eyeballed

`ARCHITECTURE.md` Ch1's Layer-2 line is under a standing architect guard. Hashed against the
**pre-lane main tip** `902b621b`, not merely against this branch's parent:

```
$ git show 902b621b:ARCHITECTURE.md > /tmp/arch_main.md
$ sed -n '/^## Purpose \[CORE\]/,+6p' /tmp/arch_main.md | sha256sum
ce3c688e7a5b4f0bf94d8643f4c4033b22249f1d26b2e749cf4d45dec558ad7c  -
$ sed -n '/^## Purpose \[CORE\]/,+6p' ARCHITECTURE.md | sha256sum
ce3c688e7a5b4f0bf94d8643f4c4033b22249f1d26b2e749cf4d45dec558ad7c  -

$ sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' /tmp/arch_main.md | sha256sum
7e702f5d09936795e9834ee81a1ebce86d22158640ae351c0013439cb078f78f  -
$ sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' ARCHITECTURE.md | sha256sum
7e702f5d09936795e9834ee81a1ebce86d22158640ae351c0013439cb078f78f  -
```

**Verdict: BYTE-IDENTICAL**, on both the P1b probe's own six-line window and the whole `## Purpose
[CORE]` chapter up to the next H2. The wider hash is deliberate: matching only the six lines the
probe reads would leave the rest of the chapter unproven, and the guard is on the chapter's claim,
not on the probe's window.

The P1b probe command itself, run against the live file:

```
$ sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md
## Purpose [CORE]

`.dev-knowledge` is the universal LLM-driven development guide and methodology
framework for all `Dev/` projects. It is **Layer 2** of the ADR-28 three-layer
ecosystem model — passive storage and governance authority, not an execution
engine. It holds operational protocols, ADRs, intake docs, handoffs, templates, and
```

## 5. Reproduce

```bash
git rev-parse --short HEAD                                  # c20d9239
sed -n '81p' templates/handoff/v5/PROBES.md.tmpl
grep -A4 '^## Vision' README.md ; echo $?
grep -A4 '^## Vision' VISION.md ; echo $?
git show 902b621b:ARCHITECTURE.md > /tmp/arch_main.md
sed -n '/^## Purpose \[CORE\]/,+6p' /tmp/arch_main.md   | sha256sum
sed -n '/^## Purpose \[CORE\]/,+6p' ARCHITECTURE.md     | sha256sum
sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' /tmp/arch_main.md | sha256sum
sed -n '/^## Purpose \[CORE\]/,/^## Codemap/p' ARCHITECTURE.md   | sha256sum
```

**Consumer:** `[#614]`, ADR-114 (AMENDMENT 1), `[#621]`,
`docs/audits/2026-08-29-technical-614-consumer-enumeration.md`.
