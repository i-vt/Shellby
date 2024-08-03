$localInstallerPath = "C:\path\to\your\python-installer.exe"  # Change this to the path where you saved the installer
$pythonVersion = "3.11.4"
$installDir = "$HOME\AppData\Local\Programs\Python\Python$($pythonVersion.Replace('.', ''))"

if (Test-Path $localInstallerPath) {
    Write-Host "Installing Python from local installer: $localInstallerPath"

    Start-Process -FilePath $localInstallerPath -ArgumentList "/quiet InstallAllUsers=0 TargetDir=$installDir PrependPath=1" -Wait

    Write-Host "Verifying Python installation..."
    $env:Path += ";$installDir"
    python --version

    Write-Host "Python $pythonVersion has been installed successfully at $installDir"
} else {
    Write-Host "Installer not found at $localInstallerPath. Please check the path and try again."
}
