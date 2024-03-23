$scriptPath = "C:/Artefact/Client/main.py"
$processName = "python"

$running = Get-Process $processName -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $scriptPath }

if (-not $running) {
    Start-Process pythonw.exe -ArgumentList $scriptPath -WindowStyle Hidden
}
