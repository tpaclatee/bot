#!/bin/bash

sudo cp edu.ioc-bot.daemon.plist /Library/LaunchAgents/
sudo chown -R root: /Library/LaunchAgents/edu.ioc-bot.daemon.plist
launchctl unload /Library/LaunchAgents/edu.ioc-bot.daemon.plist
launchctl load /Library/LaunchAgents/edu.ioc-bot.daemon.plist
launchctl start /Library/LaunchAgents/edu.ioc-bot.daemon.plistls
launchctl list | grep edu