- **Define bot**
  * See https://pypi.org/project/webexteamsbot/
  * Define bot and put token in ```.env```

- **Build**
  * ```pip install -r requirements.txt```  

- **Create your DEV webex bot**
  * Go [here](https://developer.webex.com/docs/bots) and click create a bot button
    * Enter UMD email and login to CAS, click create bot again
    * _Bot Name_: IOCBot DEV LDAPID    (where LDAPID is your LDAP ID)
    * _Bot Username_: IOCBotDEVLDAPID
    * _Icon_: Choose your favorite
  * Put token in keyring as ```webex_token``` (see config passwords)
  
- **Create your webex rooms**
  * Manually create 2 rooms in webex teams and add your IOCBot to the rooms
    * IOC Bot DEV LDAPID
    * IOC Bot DEV LDAPID Debug
  
- **Config passwords**
  *
  * ```keyring set iocbotdev webex_token```
  * ```keyring set iocbotdev dt_bearer_token```
  * ```keyring set iocbotdev dt_api_token```
  * ```keyring set iocbotdev nagios_pass```
  

- **Dynatrace integration**
  * Setup [custom integration](https://kbl44849.live.dynatrace.com/#settings/integration/notification/integrationtypeoverview)
  * Webhook URL ```https://cmann.ngrok.io/dynatraceProblem```
  * Authentication / Security
    * Click Add HTTP header button and add an authorization header ```authorization : Bearer tokenXYZ```
    * Where ```Bearer ``` is a string followed by a random token you generate and replace ```tokenXYZ```
    * Place the token in your ```.env``` file as ```DYNATRACE_BEARER_TOKEN = tokenXYZ```
  * Payload
  ```json
    {
    "State":"{State}",
    "PID" : "{PID}",
    "ProblemID":"{ProblemID}",
    "ProblemTitle":"{ProblemTitle}",
    "ProblemDetailsText":"{ProblemDetailsText}",
    "ProblemDetailsMarkdown":"{ProblemDetailsMarkdown}",
    "ProblemURL": "{ProblemURL}",
    "ImpactedEntities":{ImpactedEntities},
    "ImpactedEntity":"{ImpactedEntity}",
    "ProblemDetailsJSON":{ProblemDetailsJSON},
    "ProblemSeverity":"{ProblemSeverity}",
    "Tags": "{Tags}"
    }
  ```
  
- **Get room IDs**
  * Once bot is running and ports are open
  * In each room ask bot for room ID with ```@IOCBotLDAP /room```

- **Endpoint URL the cisco will call**
  * Use ngrok to setup a development tunnel so the webhook works. You can also open a port on your home firewall instead.
    * ```ngrok http 5000``` (free)
    * ```ngrok http -region=us -hostname=cmann.ngrok.io 5000``` (with account)
    * Take URL returned by ngrok and place in ```.env``` under key ```TEAMS_BOT_URL =```
    * Leave ngrok running in a terminal so the tunnel stays open and bot can receive commands
    
 
- **Test it is working with Curl**
  * You can call it from the command line with Curl using
  ```shell
  curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"username":"xyz","password":"xyz"}' \
    curl https://cmann.ngrok.io/webhooks
  ```

- **Room ID**
    * Get the room ID by asking the bot ```@IOCbot /room``` and put it in ```.env ```
    * This is the room the bot will post messages from Dynatrace etc to


- **Deploy separate prod copy on local PC**
  * See README-deploy.md
  
- **TODO: Run in production**
  * Do not use development flask to run in prod
  * Set ```env=prod``` in ```.env``` to launch with waitress
  * Need to look into waitress
  * Need SSL cert
  * Front with NGINX or Apache