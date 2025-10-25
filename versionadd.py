import requests
import urllib.parse
import json

def get_md5(url):
    spl = url.split("/")
    cont = True
    f = ""
    for i in spl:
        if i == "media_ipsw.rar":
            cont = False
        if cont:
            f += f"{i}/"
    f += "checksum_media_ipsw.md5"
    r = requests.get(f)
    if r.status_code != 200:
        return False
    return r.text.split(" ")[0]

def merge_push(old, push):
    for key, value in push.items():
        if key in old and isinstance(push[key], dict) and isinstance(value, dict):
            merge_push(old[key], value)
        else:
            old[key] = value
    return old

def add_push(push):
    with open("beta_versions.json", "r") as f:
        bv = json.load(f)
    nv = merge_push(bv, push)
    with open("beta_versions.json", "w") as f:
        json.dump(nv, f, indent=4)

def automate():
    print("The automate tool was designed solely for https://archive.org/download/Apple_iPod_Firmware URLs!\nIt's unlikely to work with other sources, please input data manually in those cases.")
    device = "iPod" # leftover
    url = input("URL: ")
    o_url = url
    md5 = get_md5(o_url)
    if md5 == False:
        print("Getting MD5 hash failed! Is this an Apple iPod Firmware url?\nPlease input data manually.")
        return False
    spl = url.split("/")
    cont = True
    url = ""
    for i in spl:
        if i == "media_ipsw.rar":
            cont = False
        if cont:
            url += f"{i}/"
    if not url.endswith("/"): # shouldnt happen but better safe than sorry
        url += "/"
    url = urllib.parse.unquote(url)
    url = url.split("/")[-2]
    url = url.split(" ")
    if len(url) >= 7:
        if " ".join([url[0],url[1],url[2]]) == "Apple iPod Touch":
            f_device = device + url[3].replace(".",",")
            push = {}
            push[f_device] = {}
            push[f_device][url[5]] = {}
            f_build = url[6].replace("(","").replace(")","").split(".")[-1]
            push[f_device][url[5]][f_build] = {"url": o_url, "md5": md5}
            print(f"Device: {f_device}\nMajor: {url[5]}\nBuild: {f_build}\nURL: {o_url}\nMD5: {md5}")
            rg = input("Does this look right? (Y/n): ").lower()
            if rg == "y":
                add_push(push)
                print("Done!")
                exit()
        else:
            print(f"ERROR: Expected \"Apple iPod Touch\" but got \"{' '.join([url[0],url[1],url[2]])}\". Is this an Apple iPod Firmware url?\nPlease input data manually.")
            return False
    else:
        print("ERROR: Split into less than 7 items, is this an Apple iPod Firmware url?\nPlease input data manually.")
        return False

do_auto = input("Automate information? (Y/n): ").lower()
if do_auto == "y":
    automate()
device = input("Device (e.g. iPod1,1): ")
major = input("Major (e.g. 3.0): ")
build = input("Build (e.g. 7A280f): ")
url = input("URL: ")
md5 = input("MD5: ")

push = {}
push[device] = {}
push[device][major] = {}
push[device][major][build] = {"url": url, "md5": md5}
rg = input("Is everything correct? (Y/n): ").lower()
if rg == "y":
    add_push(push)
    print("Done!")
exit()
