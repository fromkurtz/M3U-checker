# IPTV Stream Validator & Merger

This Python script automates the process of checking multiple `.m3u` or `.m3u8` playlist files. It verifies which streaming links are currently online, removes duplicates (based on Name + URL), and merges them into a single consolidated file.

##  Features
* **Automatic Scanning**: Scans an entire folder for playlist files.
* **Smart De-duplication**: Filters out duplicate channels by comparing both the name and the URL.
* **Fast Verification**: Uses HTTP `HEAD` requests to check status without downloading the stream.
* **Clean Output**: Generates a new `#EXTM3U` file containing only working links.

##  Installation
1. **Clone or download** this repository.
2. **Install the required dependencies** using pip:
   ```bash
   pip install -r requirements.txt
 How to Use
Open the script (main.py) and edit the SOURCE_FOLDER variable to point to your folder containing the .m3u8 files:

Python

SOURCE_FOLDER = r'C:\Path\To\Your\Lists'
Run the script:

Bash

python main.py
The script will output a file named final_online_list.m3u8 inside the source folder.

 Configuration
TIMEOUT: Time in seconds to wait for a server response (default is 5s).

HEADERS: Includes a User-Agent to prevent being blocked by streaming servers.

 Disclaimer
This tool is for personal use and management of publicly available or owned stream lists. Ensure you have the right to access the streams you are checking.




### Folder Structure Example
---
To keep things organized, your folder should look like this:

*  **Project_Folder**
    * `main.py` (The script I provided previously)
    * `requirements.txt`
    * `README.md`
    *  **Your_IPTV_Lists** (The folder you point to in `SOURCE_FOLDER`)
        * `list1.m3u8`
        * `list2.m3u8`

Would you like me to add a **logging feature** so the script creates a text file listi