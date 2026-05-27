@echo off
cd /d "%~dp0"

setlocal enabledelayedexpansion

set "classpath=."
for %%f in (lib\*.jar) do (
    set "classpath=!classpath!;%%f"
)


java -cp "!classpath!" Main

endlocal
@REM pause