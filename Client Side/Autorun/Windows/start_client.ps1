$pythonScriptPath = "C:\Artefact\Client\main.py"
$pythonExePath = "python"

function ScriptIsRunning {
    $processes = Get-WmiObject Win32_Process -Filter "Name = 'python.exe'"
    $scriptRunning = $false
    foreach ($process in $processes) {
        if ($process.CommandLine -like "*$pythonScriptPath*") {
            $scriptRunning = $true
            break
        }
    }
    return $scriptRunning
}

while ($true) {
    if (-not (ScriptIsRunning)) {
        Start-Process $pythonExePath $pythonScriptPath -WindowStyle Hidden
    }
    Start-Sleep -Seconds 15
}
