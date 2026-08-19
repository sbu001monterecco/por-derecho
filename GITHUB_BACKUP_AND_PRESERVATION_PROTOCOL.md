# GitHub Backup and Preservation Protocol

**Repository:** `sbu001monterecco/por-derecho`  
**Adopted:** 19 August 2026  
**Purpose:** continuity, preservation, recoverability and integrity checking of the Por Derecho / Project Sun Rock GitHub estate and its published web presence.

## 1. Preservation objective

GitHub is a publishing and collaboration platform, not the sole archival copy of the project. Material that matters to the project must be capable of being reconstructed independently of continued access to the GitHub account.

The minimum preservation set is therefore:

1. a full Git mirror of every repository owned by the account that is intended to be preserved;
2. a GitHub account-data export retained separately from the Git mirrors;
3. Git LFS objects, where any repository uses Git LFS;
4. a static snapshot of the live GitHub Pages/public website, preserving what a reader could actually see at the snapshot date;
5. an inventory recording what was captured and when;
6. SHA-256 integrity hashes for the resulting archive files; and
7. at least two independent storage copies, with one copy kept outside the normal working environment.

A GitHub “Download ZIP” is useful as a convenience copy but is **not** the archival method because it does not preserve the complete Git history and refs.

## 2. Repository capture standard

For each repository, use a mirror clone:

```powershell
git clone --mirror https://github.com/OWNER/REPOSITORY.git
```

A mirror is the preferred preservation copy because it retains the repository’s Git objects, branches, tags and refs rather than only the currently checked-out files.

For repositories using Git LFS, enter the mirror and fetch all LFS objects:

```powershell
cd REPOSITORY.git
git lfs fetch --all
cd ..
```

The companion script `scripts/backup_github_account.ps1` automates repository discovery and mirror creation for the `sbu001monterecco` account.

## 3. GitHub account-data export

In addition to repository mirrors, periodically request GitHub’s own account-data export from the GitHub account settings and retain the resulting archive unchanged.

The account export is a complementary record. It should not replace repository mirrors, and repository mirrors should not replace the account export.

Record in the inventory:

- date/time the export was requested;
- date/time it was downloaded;
- original filename;
- file size; and
- SHA-256 hash.

Do not edit or repackage the original export before preserving an untouched copy.

## 4. Published-site snapshot

The source repository and the rendered public website are different preservation objects.

For important publication states, preserve a dated static snapshot of the live site at:

`https://sbu001monterecco.github.io/por-derecho/`

Where `wget.exe` or another recursive web-preservation tool is available, capture the site recursively so that HTML, stylesheets, scripts, images and linked internal pages needed to reproduce the public presentation are retained.

At minimum, the snapshot record should state:

- capture date/time and timezone;
- public URL;
- repository commit SHA that was live, if known;
- capture tool and version; and
- any known capture failures or excluded resources.

A rendered-site snapshot is particularly useful when the evidential question is not merely what source files existed, but what the public could actually see at a particular point in time.

## 5. Integrity manifest

After each backup run, compute SHA-256 hashes for the final archive files and write them to a manifest such as:

`SHA256SUMS.txt`

PowerShell example:

```powershell
Get-FileHash .\archive-file.tar.gz -Algorithm SHA256
```

The manifest should itself be copied with the archive set. If an archive is later copied to another drive or cloud location, recompute the hash and compare it with the preserved manifest.

A matching hash demonstrates byte-for-byte identity with the hashed copy. It does not, by itself, prove when a file first existed or establish a complete legal chain of custody.

## 6. Recommended archive structure

```text
GITHUB_ARCHIVE_YYYY-MM-DD_HHMMSSZ/
|
+-- repositories/
|   +-- por-derecho.git/
|   +-- other-repository.git/
|   +-- ...
|
+-- repository-archives/
|   +-- por-derecho.git.tar.gz
|   +-- ...
|
+-- github-account-export/
|   +-- [original GitHub export archive]
|
+-- rendered-website/
|   +-- [static copy of live site]
|
+-- inventory/
|   +-- repositories.csv
|   +-- BACKUP-RUN.txt
|
+-- checksums/
    +-- SHA256SUMS.txt
```

## 7. Storage rule

A completed preservation run should not exist only on the computer used to make it.

Minimum target:

- **Copy A:** local working/archive storage;
- **Copy B:** separate external disk or other physically independent storage; and
- preferably **Copy C:** independent cloud/off-site storage.

For particularly important publication or evidential milestones, preserve a read-only or otherwise immutable copy where practical.

Do not continually overwrite the only historical archive. Use dated snapshots so earlier states remain recoverable.

## 8. When to run the preservation process

Run a full preservation cycle:

- after a major public-site release or evidential publication;
- before any substantial repository restructuring, migration or deletion;
- before changing GitHub account ownership, authentication or hosting arrangements;
- after adding material that would be difficult to reconstruct from another source; and
- periodically even when no major event has occurred.

For a project under active evidential development, a monthly baseline plus milestone-triggered snapshots is the minimum recommended rhythm. More frequent snapshots can be used during periods of rapid publication.

## 9. Verification after every run

A backup is not complete until it has been checked.

Verify:

1. the repository inventory lists every intended repository;
2. every listed repository produced a mirror;
3. mirrors contain refs (`git show-ref` can be used as a basic check);
4. LFS fetch completed where applicable;
5. archive files can be opened/extracted;
6. SHA-256 hashes were generated;
7. a second storage copy was made; and
8. at least one sample repository has been test-restored periodically.

For `por-derecho`, also verify that the preserved site snapshot opens locally and that key public pages/assets are present.

## 10. Restoration principle

The preservation set should allow reconstruction without depending on the original GitHub repository still being available.

A mirror can be restored to another Git remote using normal Git push/mirror operations after the target repository has been created. Do not test restoration by overwriting the live production repository; use an isolated test repository or local clone.

## 11. Limitations and evidential caution

This protocol is designed for operational preservation and integrity verification. It strengthens continuity and later verification but is not a substitute for specialist forensic acquisition, qualified electronic timestamping, notarisation, disclosure preservation obligations, or a formally documented forensic chain of custody where those are required.

For material likely to become important in litigation, regulatory proceedings or criminal investigation, retain the original source material as well as the GitHub publication copy and document provenance separately.

## 12. Deletion-safety rule for ChatGPT work

When a ChatGPT thread produces durable methodology, factual findings, evidential links, case chronology, filing references, scripts, governance decisions or other work that would be costly to reconstruct, the thread should not be treated as deletion-safe until the durable content has been transferred to the repository or another controlled record.

For backup, preservation, deletion-audit and similar continuity threads, **repository transfer alone is not the final handoff**. Before declaring such a thread fully closed or 100% deletion-safe, complete the applicable verification steps, preserve any resulting archive/verification files outside GitHub, and perform the email handoff described below when Gmail is available.

For the thread that generated this protocol, the reusable GitHub-preservation methodology is now captured here and in `scripts/backup_github_account.ps1`; the thread itself is no longer the sole copy of that methodology.

## 13. Email handoff rule for similar threads

For future ChatGPT threads that complete a material backup, preservation cycle, deletion-safety transfer, evidential archive, repository snapshot, restoration test or comparable continuity task, the default closure procedure is:

1. send the user a concise completion email through the connected Gmail account before declaring the thread fully closed, where Gmail is available and the user has asked for or established this handoff practice;
2. send it to the authenticated user (`to: me`) unless a different recipient has been expressly specified;
3. state what was preserved, the date, relevant repository/asset identity, the preserved commit or version where applicable, verification outcome, storage locations and any material limitation;
4. include the final SHA-256 hash or equivalent integrity identifier when one exists;
5. attach the final archive and verification record when attachment size/capability permits; otherwise identify the durable storage location and attach the verification record at minimum;
6. do not claim 100% completion if the email send fails when this handoff is part of the requested closure procedure; record the failure and keep the thread open for remediation; and
7. only after durable transfer, independent-copy verification and the required email handoff may the thread be described as fully deletion-safe.

The purpose of this rule is to ensure that the user receives a human-readable, independently retained closure record outside the ChatGPT conversation itself, rather than relying on the thread as the sole record of completion.
