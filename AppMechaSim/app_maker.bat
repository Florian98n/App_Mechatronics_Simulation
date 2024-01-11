@echo off

pyinstaller --onefile --noconsole --add-data "images/;images" --distpath . --name AppMechatronicsSimulation main.py && rmdir /s /q build && del /q AppMechatronicsSimulation.spec