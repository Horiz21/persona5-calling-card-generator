@echo off

:PROMPT
SET /P ANSWER=Choose mode: Python Package[P] / Avalonia Publish[A] / Full Release[R] (default):
if /i {%ANSWER%}=={} goto :RELEASE
if /i {%ANSWER%}=={A} goto :AVALONIA
if /i {%ANSWER%}=={P} goto :PYTHON
if /i {%ANSWER%}=={R} goto :RELEASE
goto :PROMPT

:PYTHON
echo Executing Python Package mode...
call conda activate p5ccg311
cd ./Python/
pyinstaller --clean --distpath ../Assets/Binary cli.spec
cd ..
goto :EOF

:AVALONIA
echo Executing Avalonia Publish mode...
dotnet publish -c Release -r win-x64 --self-contained
goto :EOF

:RELEASE
echo Executing Full Release mode...
call conda activate p5ccg311
cd ./Python/
pyinstaller --clean --distpath ../Assets/Binary cli.spec
cd ..
dotnet publish -c Release -r win-x64 --self-contained
goto :EOF
