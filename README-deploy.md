- **Deploy copy on mac**
  * In ```osx``` directory run ```./deploy``` to copy files to `./deployed` directory
    * Deploy will run ```./schedule.sh``` to use launchd to schedule at startup
    * Note: In .plist file we need to specify path to python venv to find libraries
  * Logs will write to ```./deployed/prod/stderr.log``` and ```stdout.log```
  * In PyCharm, right click on ```deployed``` directory and mark as excluded so it isn't indexed
  
- **ngrok prod**
  * See project https://github.com/cmann50/ngrok
  * See local folder readme /Users/cmann/PycharmProjects/ngrok