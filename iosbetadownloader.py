import urllib.request
import ssl
import time
import json
import hashlib
import math
import os

import requests
from progress_bar import InitBar

print("""iOS Beta Downloader
Fork of turlum25's "iosbeta-downloader\"""")

r = requests.get("https://raw.githubusercontent.com/loanfrauder/ios-beta-downloader/refs/heads/main/beta_versions.json")
if r.status_code != 200:
    print("Couldn't fetch device versions. Are you connected to the internet?")
    r.raise_for_status()
data = r.json()

print("Got device versions.")

print("\nSupported devices:\n")


def verify(file, md5):
    progress = InitBar(file)
    progress(0)
    chunks = math.ceil(os.path.getsize(file) / 4096)
    h = hashlib.md5()
    with open(file, 'rb') as f:
        c = 0
        while True:
            progress((c / chunks) * 100)
            c += 1
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    del progress
    if h.hexdigest() == md5:
        return True
    else:
        return False

def main():
    for device in data:
        print(device)

    print("---")

    awaiting_valid_input = True

    while awaiting_valid_input:
        try:
            device = input("Enter a model identifier (e.g. iPod1,1) > ")

            if device in data:
                print(f"Available versions for {device}:")
                for major_version in data[device]:
                    print(f"- {major_version}")
                    for build in data[device][major_version]:
                        print(f"  - {build}")
                print("")
                awaiting_valid_input = False
            else:
                print("Not a supported device, try again. Ctrl+C to exit.")
        except KeyboardInterrupt:
            exit()
        except Exception as exception:
            raise exception

    awaiting_valid_input = True

    while awaiting_valid_input:
        try:
            raw_ios_input = input("Enter a version (example: 2.0 5A240d) > ")
            ios_input = raw_ios_input.split(" ") # TODO  !!!!!!!!!
            if len(ios_input) != 2:
                print("Couldn't find that iOS version, are you sure you typed it correctly? Ctrl+C to exit.")
            elif ios_input[0] not in data[device]:
                print("Couldn't find that iOS version, are you sure the device supports it? Ctrl+C to exit.")
            elif ios_input[1] not in data[device][ios_input[0]]:
                print("Couldn't find that iOS version, are you sure the device supports it? Ctrl+C to exit.")
            else:
                awaiting_valid_input = False
        except KeyboardInterrupt:
            exit()
        except Exception as exception:
            raise exception
            
    url = data[device][ios_input[0]][ios_input[1]]["url"]
    print("Downloading IPSW")
    progress = InitBar("Download")
    progress(0)
    fn = urllib.request.urlretrieve(url, url.split('/')[-1]) # need to switch to something with a meaningful speed increase
    fn = fn[0]
    progress(100)
    del progress
    print("Verifying IPSW")
    v = verify(fn, data[device][ios_input[0]][ios_input[1]]["md5"])
    if not v:
        print("IPSW hash does not match! Deleting file...")
        if os.path.isfile(fn):
            os.remove(fn)
        print("Try downloading again.")
    else:
        print("Done!")
    
if __name__ == "__main__":
    main()
