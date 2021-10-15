@echo off
set HUBOT_SLACK_TOKEN=xoxb-1502447239939-2576688978260-xXCjemiatbvUbGaIifdF5nel
set HUBOT_GITHUB_TOKEN=
set HUBOT_GITHUB_USER=nayuta-ai

call npm install
SETLOCAL
SET PATH=node_modules\.bin;node_modules\hubot\node_modules\.bin;%PATH%

node_modules\.bin\hubot.cmd --name "myhubot" %* 
