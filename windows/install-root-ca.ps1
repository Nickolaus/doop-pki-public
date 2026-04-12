param(
    [ValidateSet("CurrentUser","LocalMachine")]
    [string]$StoreLocation = "CurrentUser"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$CertPath = Join-Path $RepoRoot "certs\\doop-root-ca.crt"

if (-not (Test-Path $CertPath)) {
    throw "Root certificate not found at $CertPath"
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
