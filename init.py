import re
import os
import argparse
import urllib.request
import json
import webbrowser

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_mod_id(value):
    if value.isdigit() and len(str(value)):
        return value
    # Searches for the Mod ID in the URL
    match = re.search(r'/mods/(\d+)', value)
    return match.group(1) if match else None

def get_mod_name(mod_id):
    url = f"https://api.gamebanana.com/Core/Item/Data?itemtype=Mod&itemid={mod_id}&fields=name"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode()
    return json.loads(data)  # returns mod name string

def get_file_size(url):
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            size = resp.getheader('Content-Length')
            return int(size) if size else None
    except:
        return None

def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]+', '_', name)

def download_file(url, dest_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp, open(dest_path, 'wb') as out_file:
        out_file.write(resp.read())

def download_mod(mod_id, location):
    if not mod_id:
        print("Null Mod ID")
    try:
        mod_name = get_mod_name(mod_id)
        dl_url = f"https://gamebanana.com/dl/{mod_id}"
        size = get_file_size(dl_url)
        size_mb = size / (1024*1024) if size else None
        size_str = f"{size_mb:.2f} MB" if size_mb else "Unknown size"

        filename = f"{mod_name}.zip"
        filename = sanitize_filename(filename)
        dest_path = os.path.join(location, filename)

        print(f"Downloading '{mod_name}' ({size_str}) from {dl_url} ...")
        download_file(dl_url, dest_path)
        print(f"Downloaded and saved as '{dest_path}'")

    except Exception as e:
        print(f"Error downloading mod ID {mod_id}: {e}")

def help():
    clear_screen()
    print("GameBanana Download Manager v0.1")
    print("Made by thefakeryker")
    print("\nThis software is not affliated/sponsered by GameBanana or its associates")
    print("\nType code to view this project on GitHub, press Enter to exit\n\n")
    
    line = input("> ").strip()
    if line == "code":
        webbrowser.open("https://github.com/thefakeryker/gb-dl/")

    clear_screen()
    exit()
    

def terminal(location):
    clear_screen()
    print("GameBanana Download Manager v0.1")
    print("Paste GameBanana mod URLs or IDs (https://gamebanana.com/mods/XXXXXX or XXXXXX).")
    print("Type 'done' when finished.\n")

    mod_ids = []
    while True:
        line = input("> ").strip()
        # Commands
        if line.lower() == 'done':
            break
        if line.lower() == 'help':
            help()
        if line.lower() == 'exit':
            return
        mod_id = extract_mod_id(line)
        if mod_id:
            mod_ids.append(mod_id)
        else:
            print("Unknown Command or Invalid Mod ID")

    if not mod_ids:
        print("No valid mod IDs provided, exiting.")
        return

    for mod_id in mod_ids:
        download_mod(mod_id, location)

def main():
    clear_screen()
    parser = argparse.ArgumentParser(description="GameBanana Download Manager v0.1")
    parser.add_argument('-l', '--location', type=str, default='.', help='Download folder (default: current directory)')
    parser.add_argument('-d', '--download', type=str, help='Download single mod by ID or full URL')
    args = parser.parse_args()

    location = args.location
    if not os.path.isdir(location):
        print(f"Download location '{location}' does not exist. Creating it.")
        os.makedirs(location, exist_ok=True)

    if args.download:
        downloads = str.split(args.download, " ")
        for download_id in downloads:
            mod_id = extract_mod_id(download_id)
            download_mod(mod_id, location)
    else:
        terminal(location)

if __name__ == "__main__":
    main()
