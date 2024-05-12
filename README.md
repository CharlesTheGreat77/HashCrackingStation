# HashCrackingStation

Crack hashes in the cli with crackstation.com fast and efficiently without the need to go through captchas!

# Prerequisites
```
apt install ffmpeg
pip3 install -r requirements.txt
playwright install
```

# Usage
```
usage: python3 crackstation.py --hash <hash> [hash.txt]

Hash Cracker using CrackingStation.com

options:
  -h, --help   show this help message and exit
  --hash HASH  specify hash to crack [single hash or file]
```
- If specifying file, hashes must be split by line


# Proxy option
One can specify a proxy to use in the core/browser.py file on line 15