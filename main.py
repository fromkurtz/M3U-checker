import requests
import os
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- CONFIGURATIONS ---
SOURCE_FOLDER = r'C:\Path\To\Your\Lists' 
OUTPUT_FILE = 'final_online_list.m3u8'
TIMEOUT = 5 
MAX_WORKERS = 100  # Number of simultaneous checks. Increase for more speed.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def check_link(name, url):
    """Function to check a single link status."""
    try:
        # We use a short timeout to keep it fast
        response = requests.head(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
        if response.status_code == 200:
            return (name, url, True)
    except:
        pass
    return (name, url, False)

def validate_iptv_fast():
    unique_channels = {} 
    all_tasks = []
    
    search_pattern = os.path.join(SOURCE_FOLDER, "*.m3u*")
    m3u_files = glob.glob(search_pattern)
    
    if not m3u_files:
        print(f"No files found in: {SOURCE_FOLDER}")
        return

    # 1. Parsing files first (Memory efficient)
    print("--- Parsing files and removing local duplicates ---")
    links_to_check = {} # URL: Name

    for file_path in m3u_files:
        if OUTPUT_FILE in file_path: continue
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                name = ""
                for line in f:
                    line = line.strip()
                    if line.startswith('#EXTINF'):
                        name = line
                    elif line.startswith('http'):
                        # Using URL as key to avoid checking the same link twice globally
                        if line not in links_to_check:
                            links_to_check[line] = name
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    total_links = len(links_to_check)
    print(f"Total unique links to verify: {total_links}")

    # 2. Multithreaded Verification
    print(f"--- Starting verification with {MAX_WORKERS} workers ---")
    online_count = 0
    processed_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Schedule the check for each unique link
        future_to_url = {executor.submit(check_link, name, url): url for url, name in links_to_check.items()}
        
        for future in as_completed(future_to_url):
            processed_count += 1
            name, url, is_online = future.result()
            
            if is_online:
                unique_channels[url] = name
                online_count += 1
            
            # Progress update every 100 links
            if processed_count % 100 == 0:
                print(f"Progress: {processed_count}/{total_links} | Online: {online_count}", end='\r')

    # 3. Saving Results
    final_path = os.path.join(SOURCE_FOLDER, OUTPUT_FILE)
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for url, name in unique_channels.items():
            f.write(f"{name}\n{url}\n")
    
    print(f"\n" + "="*40)
    print(f"FINISHED!")
    print(f"Unique Online Channels: {len(unique_channels)}")
    print(f"Saved to: {final_path}")
    print("="*40)

if __name__ == "__main__":
    validate_iptv_fast()