@echo off
setlocal enabledelayedexpansion

rem 遍历当前文件夹及其子文件夹下所有的 .po 文件
for /r %%i in (*.po) do (
    rem 获取 .po 文件所在的文件夹路径
    set "po_folder=%%~dpi"
    
    rem 获取 .po 文件名（不包含路径和扩展名）
    set "po_file=%%i"
    for %%F in ("!po_file!") do (
        set "filename=%%~nxF"
    )

    rem 获取文件名（不包含扩展名）
    set "name=!filename:.po=!"

    rem 编译为 .mo 文件，并放置在 .po 文件所在的文件夹中
    msgfmt -o "!po_folder!!name!.mo" "!po_file!"
)
