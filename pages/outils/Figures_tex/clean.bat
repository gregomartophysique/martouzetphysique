@echo off
for /r %%x in (*.aux) do (
    DEL %%x
)
for /r %%x in (*.log) do (
    DEL %%x
)
for /r %%x in (*.out) do (
    DEL %%x
)
for /r %%x in (*.synctex.gz) do (
    DEL %%x
)
pause