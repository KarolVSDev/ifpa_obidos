$exclude = @("venv", "bot_covid.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot_covid.zip" -Force