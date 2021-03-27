#!/bin/bash
cp /Users/cmann/PycharmProjects/iocBot/deployed/prod/bot.db ../bot.prod.db
rm -rf /Users/cmann/PycharmProjects/iocBot/deployed/prod/
rsync -av --progress /Users/cmann/PycharmProjects/iocBot/ /Users/cmann/PycharmProjects/iocBot/deployed/prod --exclude deployed
cp ../bot.prod.db /Users/cmann/PycharmProjects/iocBot/deployed/prod/bot.db
cp ../.env.prod /Users/cmann/PycharmProjects/iocBot/deployed/prod/.env
rm /Users/cmann/PycharmProjects/iocBot/deployed/prod/bot.prod.db
rm /Users/cmann/PycharmProjects/iocBot/deployed/prod/bot.unit.db
rm /Users/cmann/PycharmProjects/iocBot/bot.prod.db
./schedule.sh