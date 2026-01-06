import requests
import os
import glob

# --- CONFIGURATIONS ---
# Use 'r' before quotes on Windows (e.g., r'C:\Users\Name\Desktop\Playlists')
SOURCE_FOLDER = r'C:\Path\To\Your\Lists' 
OUTPUT_FILE = 'final_online_list.m3u8'
TIMEOUT = 5 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def validate_iptv():
    unique_channels = {} # Dictionary to avoid duplicates (Name + URL)
    
    # Define the pattern to search for .m3u and .m3u8 files
    search_pattern = os.path.join(SOURCE_FOLDER, "*.m3u*")
    m3u_files = glob.glob(search_pattern)
    
    if not m3u_files:
        print(f"No files found in: {SOURCE_FOLDER}")
        return

    print(f"--- Found {len(m3u_files)} files to process ---")

    for file_path in m3u_files:
        # Ignore the output file if it's in the same folder
        if OUTPUT_FILE in file_path:
            continue
            
        print(f"\nReading: {os.path.basename(file_path)}")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            continue

        metadata_name = ""
        for line in lines:
            line = line.strip()
            
            # Capture the #EXTINF line (channel name and info)
            if line.startswith('#EXTINF'):
                metadata_name = line
            
            # Capture the URL line
            elif line.startswith('http'):
                url = line
                # Create a unique key based on Name + URL
                # This prevents duplicate entries even if they come from different files
                duplicate_key = f"{metadata_name}_{url}"
                
                if duplicate_key not in unique_channels:
                    try:
                        # Perform a HEAD request to check status without downloading the stream
                        response = requests.head(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
                        
                        if response.status_code == 200:
                            print(f"  [ON]  {url}")
                            unique_channels[duplicate_key] = (metadata_name, url)
                        else:
                            print(f"  [OFF] Status {response.status_code}")
                            
                    except Exception:
                        print(f"  [OFF] Timeout/Error")
                else:
                    print(f"  [SKIP] Channel/Link already processed")

    # Save the consolidated results
    final_path = os.path.join(SOURCE_FOLDER, OUTPUT_FILE)
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for name, url in unique_channels.values():
            f.write(f"{name}\n{url}\n")
    
    print(f"\n" + "="*40)
    print(f"PROCESS COMPLETED!")
    print(f"Unique Online Channels: {len(unique_channels)}")
    print(f"Saved to: {final_path}")
    print("="*40)

if __name__ == "__main__":
    validate_iptv()