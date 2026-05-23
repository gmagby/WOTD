$Action = New-ScheduledTaskAction -Execute 'python.exe' -Argument 'daily_update.py' -WorkingDirectory (Get-Location).Path
$Trigger = New-ScheduledTaskTrigger -Daily -At 3:00am
# Use the current user to run the task
$Principal = New-ScheduledTaskPrincipal -UserId (whoami) -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$TaskName = "WOTD_DailyUpdate"
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings

Write-Host "Scheduled task '$TaskName' registered successfully to run daily at 3:00 AM CST."
