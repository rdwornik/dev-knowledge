# .devcontainer/Dockerfile — [#554] the reachability repair. Measured 2026-08-19, not anticipated.
#
# WHAT IS BROKEN AND WHERE. The pinned base image below ships an apt source for the yarn Debian
# repository whose signing key is no longer in the image keyring. Any `apt-get update` inside a
# container built from it therefore ends:
#
#   W: GPG error: https://dl.yarnpkg.com/debian stable InRelease: The following signatures
#      couldn't be verified because the public key is not available: NO_PUBKEY 62D54FD4003F6525
#   E: The repository 'https://dl.yarnpkg.com/debian stable InRelease' is not signed.
#
# and returns NON-ZERO. That single upstream defect is what walled D1, in two places at once:
#   * Codespaces' own on-demand SSH installer (`/workspaces/.codespaces/.persistedshare/
#     installSSH.sh`, line 125 `if ! aptSudoIf "update"; then`) aborts, so `gh codespace ssh`
#     AND `gh codespace logs` both refuse with "failed to start SSH server" — the codespace comes
#     up Available and is reachable only from a browser;
#   * every devcontainer FEATURE install aborts the same way (witnessed: the sshd feature exited
#     100, `docker buildx build` failed, and Codespaces silently replaced the container with an
#     alpine RECOVERY container in which uv, the venv and the full clone are simply absent —
#     the provisioning that `provision.sh` asserts had never run, and nothing said so).
#
# WHY THE REPAIR LIVES HERE AND NOT IN provision.sh. Features and the SSH installer both run
# BEFORE `postCreateCommand`, so a repair inside provision.sh would land after the damage. It also
# keeps provision.sh's stated design intact: that script talks to nothing but git, curl and uv.
#
# WHY NOT A DIFFERENT TAG. Checked against the live MCR tag list on 2026-08-19: the `1-3.12` line
# offers only `bookworm` and `bullseye`, so there is no newer Debian base to move to.
#
# PORTABILITY is unchanged — `devcontainer up` on a VPS builds this same Dockerfile.

ARG BASE_IMAGE=mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
FROM ${BASE_IMAGE}

# Drop any apt source pointing at the unsigned yarn repo, then PROVE apt is healthy: the second
# `apt-get update` is the assert, and a non-zero exit fails the build loudly instead of handing a
# lane a container whose ssh server can never be installed.
RUN set -eux; \
    grep -rl 'dl\.yarnpkg\.com' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null \
      | xargs -r rm -f; \
    apt-get update; \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------------------------
# uv, AT THE ADR-106 PIN, BAKED INTO THE IMAGE. Measured 2026-08-26, not anticipated.
#
# WHAT WAS BROKEN. Smoke 5 (`docs/audits/2026-08-26-verification-batch-1-close-packet.md` §11,
# defect 2) found `uv` absent from `~/.local/bin`, `/usr/local/bin` AND PATH in a live codespace,
# so the delivered contract's `uv run --locked ...` exited 127. Every hub gate is `uv run --locked`
# by ADR-106, so **no hub gate could execute on this substrate at all** — the vacuous-gate failure
# this whole devcontainer was built to refuse, arriving by absence rather than by a wrong version.
#
# WHY provision.sh LEG L1 IS NOT ENOUGH, which is the whole point of the repair. L1 installs uv
# into `${HOME}/.local/bin` at PROVISION time. Two failure modes survive that, both witnessed in
# this tree: a container that came up from a stale prebuilt image or from Codespaces' alpine
# RECOVERY container never ran provisioning and therefore carries no uv at any path; and a
# non-login `gh codespace ssh` exec does not carry `~/.local/bin` on PATH even when provisioning
# DID run. Baking the binary into the image closes both — `/bin` is on the default PATH for every
# user and every shell, and it is populated before any feature, SSH installer or lifecycle script
# runs, i.e. before anything that has historically failed here.
#
# THE MECHANISM IS THE DOCUMENTED ONE, quoted rather than invented. docs.astral.sh/uv, "Installing
# uv in Docker", gives the distroless-copy form as its first method:
#     "COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/"
# and on versions: "it is best practice to pin to a specific uv version", shown as
#     "COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/"
# The line below is that form with the repo's own pin substituted. The tag's existence was checked
# live against the ghcr manifest API on 2026-08-26 (HTTP 200) rather than assumed from the version
# string — a tag that does not exist fails the build, and this file's own history is a record of
# assuming a registry.
#
# THE RESTATED PIN IS DELIBERATE, AND IT IS THE ONE RESTATEMENT A LIVE ASSERT CATCHES.
# `devcontainer.json`'s single-source-of-pins rule holds because `provision.sh` READS each pin from
# its home; a Dockerfile cannot — the build context is `.devcontainer/` and `pyproject.toml` is not
# in it. Widening `build.context` to the repo root ("a value of `\"..\"` would allow you to reference
# content in sibling directories", containers.dev JSON reference) would put every tracked file in
# the image's cache key and rebuild the image on every commit — precisely the prebuild churn step 2
# of this row is trying to bound. So the token is restated here, and the drift is NOT silent:
# `provision.sh` leg L1 compares the resolved `uv --version` against `pyproject.toml [tool.uv]
# required-version` on every create AND every start, reinstalls on mismatch, and DIES if the result
# still disagrees. Bumping the pin in pyproject.toml without bumping the tag below therefore costs
# one re-install per container — never a wrong uv, and never a vacuous gate.
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

# PROVE it, in the same shape as the apt assert above: a build that produced no runnable uv fails
# HERE, loudly, instead of handing a lane a container in which every gate exits 127 and nothing
# says why. This is the assert whose absence smoke 5 measured.
RUN set -eux; \
    uv --version; \
    uvx --version
