param(
    [ValidateSet("CurrentUser","LocalMachine")]
    [string]$StoreLocation = "LocalMachine"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$CertPath = Join-Path $RepoRoot "certs\\doop-root-ca.crt"

if (-not (Test-Path $CertPath)) {
    throw "Root certificate not found at $CertPath"
}

if ($StoreLocation -eq "LocalMachine") {
    $CurrentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $Principal = New-Object Security.Principal.WindowsPrincipal($CurrentIdentity)
    if (-not $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw "LocalMachine\\Root requires an elevated PowerShell session. Re-run as Administrator or use -StoreLocation CurrentUser."
    }
}

$Store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", $StoreLocation)
$Store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)

try {
    $Cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($CertPath)
    $Store.Add($Cert)
}
finally {
    $Store.Close()
}

Write-Host "Installed doop root CA into $StoreLocation\\Root"
