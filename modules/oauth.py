import discordoauth2
from flask import Flask, request
import config, time, logging
client = discordoauth2.Client(config.client_id, secret=config.client_secret,
redirect="http://localhost:8080/oauth2", bot_token=config.bot_token)
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) 


@app.route("/oauth2")
def oauth2():
    access = client.exchange_code(request.args.get("code"))

    identify = access.fetch_identify()
    while True:
        try:
            access.join_guild(
                guild_id=str(config.guild_id), 
                user_id=identify.get('id'), 
                nick=None, 
            )
            break
        except discordoauth2.exceptions.RateLimited as e:
            time.sleep(e.retry_after)
        except Exception as e:
            break

    return identify, 200
