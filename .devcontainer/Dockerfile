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
