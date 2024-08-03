$pythonVersion = "3.11.4"
$installDir = "$HOME\AppData\Local\Programs\Python\Python$($pythonVersion.Replace('.', ''))"
$pythonInstallerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
$installerPath = "$HOME\Downloads\python-$pythonVersion-amd64.exe"
function Download-File {
    param (
        [string]$url,
        [string]$outputPath
    )
    Invoke-WebRequest -Uri $url -OutFile $outputPath
}

Write-Host "Downloading Python $pythonVersion..."
Download-File -url $pythonInstallerUrl -outputPath $installerPath
Write-Host "Installing Python $pythonVersion..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=0 TargetDir=$installDir PrependPath=1" -Wait

Write-Host "Verifying Python installation..."
$env:Path += ";$installDir"
python --version

Remove-Item -Path $installerPath

Write-Host "Python $pythonVersion has been installed successfully at $installDir"
