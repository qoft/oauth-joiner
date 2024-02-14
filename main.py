import config, os
import httpx, threading, time
from modules import oauth
from concurrent.futures import ThreadPoolExecutor

print("Getting discord build number...")
try:
    build_num = int(httpx.get("https://raw.githubusercontent.com/EffeDiscord/discord-api/main/fetch").json()['client_build_number'])
except Exception as e:
    build_num = 179882



class Token:
    def __init__(self, token: str, bot_id: int):
        self.token = token
        self.bot_id = bot_id
        
        self.location = None
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": token,
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc5ODgyLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMDMwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
        }   # hard coded x-super-properties i know 
    
    def _do_oauth(self) -> str:        
        request = httpx.post(
                f"https://discord.com/api/v9/oauth2/authorize",
                headers=self.headers,
                params={
                    "client_id": str(self.bot_id),
                    "response_type":"code",
                    "redirect_uri": "http://localhost:8080/oauth2",
                    "scope":"identify guilds.join",
                },
                json={"permissions":"0","authorize":True}
            )
        if request.status_code != 200:
            return None
        
        return request.json()["location"]
    
    def _request_location(self):
        if self.location is None:
            return
        req = httpx.get(self.location)
        if req.status_code != 200:
            self.location = None
            self._request_location()
        self.username = req.json()["username"]
        self.discriminator = req.json()["discriminator"]
        print(f"Joined {self.username}#{self.discriminator}!")

    def start(self):
        self.location = self._do_oauth()
        self._request_location()

class Joiner:

    def start():
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/tokens.txt"):
            print("tokens.txt not found!")
            open("data/tokens.txt", "w").close()
            return
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
            
        threading.Thread(target=oauth.app.run, kwargs={"host": "localhost", "port": 8080}, daemon=True).start()
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            for token in tokens:
                executor.submit(Token(token, config.client_id).start)
                time.sleep(0.5) # discord ratelimits oauth hard 💀
        
    
if __name__ == "__main__":
    Joiner.start()

    