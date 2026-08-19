<#
.SYNOPSIS
Creates a dated preservation copy of repositories owned by a GitHub account.

.DESCRIPTION
For each repository returned by `gh repo list`, this script creates a Git mirror,
fetches Git LFS objects when Git LFS is available, creates a compressed archive,
and records SHA-256 hashes. It also creates an inventory and placeholders for the
GitHub account-data export and rendered-site snapshot.

This is an operational preservation tool, not a substitute for specialist forensic
acquisition or a formal legal chain-of-custody process.
#>

[CmdletBinding()]
param(
    [string]$Owner = "sbu001monterecco",
    [string]$DestinationRoot = (Join-Path (Get-Location) "GitHub-Archive"),
    [string]$PublicSiteUrl = "https://sbu001monterecco.github.io/por-derecho/"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found in PATH."
    }
}

Require-Command "git"
Require-Command "gh"

# Confirm GitHub CLI authentication before beginning.
& gh auth status | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login' and retry."
}

# Configure git to reuse GitHub CLI authentication for HTTPS clones.
& gh auth setup-git
if ($LASTEXITCODE -ne 0) {
    throw "Unable to configure Git authentication through GitHub CLI."
}

$timestamp = [DateTime]::UtcNow.ToString("yyyy-MM-dd_HHmmss'Z'")
$archiveRoot = Join-Path $DestinationRoot "GITHUB_ARCHIVE_$timestamp"
$repositoriesDir = Join-Path $archiveRoot "repositories"
$repositoryArchivesDir = Join-Path $archiveRoot "repository-archives"
$accountExportDir = Join-Path $archiveRoot "github-account-export"
$renderedSiteDir = Join-Path $archiveRoot "rendered-website"
$inventoryDir = Join-Path $archiveRoot "inventory"
$checksumsDir = Join-Path $archiveRoot "checksums"

@(
    $archiveRoot,
    $repositoriesDir,
    $repositoryArchivesDir,
    $accountExportDir,
    $renderedSiteDir,
    $inventoryDir,
    $checksumsDir
) | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }

$repoJson = & gh repo list $Owner --limit 1000 --json name,nameWithOwner,url,visibility,isPrivate,isArchived
if ($LASTEXITCODE -ne 0) {
    throw "Unable to enumerate repositories for '$Owner'."
}

$repos = @($repoJson | ConvertFrom-Json)
if ($repos.Count -eq 0) {
    throw "No repositories were returned for '$Owner'."
}

$repos |
    Select-Object name, nameWithOwner, url, visibility, isPrivate, isArchived |
    Export-Csv -Path (Join-Path $inventoryDir "repositories.csv") -NoTypeInformation -Encoding UTF8

$hasLfs = $false
try {
    & git lfs version *> $null
    if ($LASTEXITCODE -eq 0) { $hasLfs = $true }
} catch {
    $hasLfs = $false
}

$hasTar = $null -ne (Get-Command "tar.exe" -ErrorAction SilentlyContinue)
$hashRecords = New-Object System.Collections.Generic.List[object]
$failures = New-Object System.Collections.Generic.List[string]

foreach ($repo in $repos) {
    $fullName = [string]$repo.nameWithOwner
    $repoName = [string]$repo.name
    $mirrorDir = Join-Path $repositoriesDir "$repoName.git"

    Write-Host "Preserving $fullName ..."

    try {
        & git clone --mirror "https://github.com/$fullName.git" $mirrorDir
        if ($LASTEXITCODE -ne 0) {
            throw "git clone --mirror failed with exit code $LASTEXITCODE"
        }

        if ($hasLfs) {
            & git -C $mirrorDir lfs fetch --all
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "Git LFS fetch returned exit code $LASTEXITCODE for $fullName. Review this repository manually."
                $failures.Add("LFS fetch warning: $fullName")
            }
        }

        & git -C $mirrorDir show-ref *> $null
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "No refs verified for $fullName. Review this mirror manually."
            $failures.Add("Ref verification warning: $fullName")
        }

        if ($hasTar) {
            $archivePath = Join-Path $repositoryArchivesDir "$repoName.git.tar.gz"
            & tar.exe -czf $archivePath -C $repositoriesDir "$repoName.git"
            if ($LASTEXITCODE -ne 0) {
                throw "tar archive creation failed with exit code $LASTEXITCODE"
            }

            $hash = Get-FileHash -Path $archivePath -Algorithm SHA256
            $hashRecords.Add([pscustomobject]@{
                SHA256 = $hash.Hash.ToLowerInvariant()
                File = (Split-Path $archivePath -Leaf)
            })
        } else {
            Write-Warning "tar.exe was not found. Mirror preserved, but no .tar.gz archive was created for $fullName."
            $failures.Add("Archive not created (tar.exe unavailable): $fullName")
        }
    } catch {
        $message = "Repository failure: $fullName - $($_.Exception.Message)"
        Write-Warning $message
        $failures.Add($message)
    }
}

$checksumPath = Join-Path $checksumsDir "SHA256SUMS.txt"
$hashRecords |
    Sort-Object File |
    ForEach-Object { "$($_.SHA256)  $($_.File)" } |
    Set-Content -Path $checksumPath -Encoding UTF8

@"
GitHub account-data export
==========================

Request the account-data export from GitHub account settings after this backup run.
Place the ORIGINAL downloaded archive in this directory without editing or repackaging it.
Then calculate its SHA-256 hash, for example:

    Get-FileHash .\<github-export-file> -Algorithm SHA256

Record the request date, download date, original filename, file size and SHA-256 hash.
"@ | Set-Content -Path (Join-Path $accountExportDir "PLACE_GITHUB_EXPORT_HERE.txt") -Encoding UTF8

$siteSnapshotStatus = "Not attempted"
$wget = Get-Command "wget.exe" -ErrorAction SilentlyContinue
if ($null -ne $wget) {
    Write-Host "Capturing rendered website $PublicSiteUrl ..."
    & $wget.Source --mirror --convert-links --adjust-extension --page-requisites --no-parent --directory-prefix=$renderedSiteDir $PublicSiteUrl
    if ($LASTEXITCODE -eq 0) {
        $siteSnapshotStatus = "Captured with wget.exe"
    } else {
        $siteSnapshotStatus = "wget.exe returned exit code $LASTEXITCODE - manual review required"
        $failures.Add("Rendered-site snapshot warning: wget.exe exit code $LASTEXITCODE")
    }
} else {
    $siteSnapshotStatus = "wget.exe unavailable - rendered-site snapshot not captured automatically"
    @"
Rendered-site snapshot not captured automatically.

Install a recursive web-preservation tool such as GNU Wget and rerun, or capture the
site separately. Preserve the public URL, capture time, tool/version and any errors.

Target URL:
$PublicSiteUrl
"@ | Set-Content -Path (Join-Path $renderedSiteDir "SITE_SNAPSHOT_NOT_CAPTURED.txt") -Encoding UTF8
}

$gitVersion = (& git --version) -join " "
$ghVersion = (& gh --version | Select-Object -First 1) -join " "
$lfsVersion = if ($hasLfs) { (& git lfs version) -join " " } else { "Git LFS not available" }

$runRecord = @"
POR DERECHO / PROJECT SUN ROCK - GITHUB PRESERVATION RUN
=======================================================
UTC timestamp: $timestamp
Owner: $Owner
Public site: $PublicSiteUrl
Repository count returned: $($repos.Count)
Git: $gitVersion
GitHub CLI: $ghVersion
Git LFS: $lfsVersion
Rendered-site status: $siteSnapshotStatus
Archive root: $archiveRoot

Repository failures/warnings: $($failures.Count)
$($failures -join [Environment]::NewLine)

NEXT STEPS
----------
1. Place the untouched GitHub account-data export in github-account-export/.
2. Hash that export and record the result.
3. Review any failures/warnings above.
4. Copy the completed archive to at least one independent storage location.
5. Recompute hashes on copied archive files and compare with checksums/SHA256SUMS.txt.
6. Periodically test-restoring a sample mirror in an isolated location.
"@

$runRecord | Set-Content -Path (Join-Path $inventoryDir "BACKUP-RUN.txt") -Encoding UTF8

Write-Host ""
Write-Host "Preservation run complete."
Write-Host "Archive: $archiveRoot"
Write-Host "Repositories enumerated: $($repos.Count)"
Write-Host "Warnings/failures: $($failures.Count)"
Write-Host "Do not leave this as the only copy; copy the archive to independent storage."
