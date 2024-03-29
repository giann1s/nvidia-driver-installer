#!/usr/bin/env python3

import os

import sys
import requests
from bs4 import BeautifulSoup

def get_text(text: str, start: str, end: str) -> str:
    """Returns the string found between first "start" and "end" strings."""

    start_idx = text.find(start) + len(start)
    end_idx = text.find(end, start_idx)
    return text[start_idx:end_idx]

def get_filename(url: str) -> str:

    last_slash_pos = 0

    for i, character in enumerate(url):
        if character == "/":
            last_slash_pos = i

    return url[last_slash_pos + 1:]

if "--url" in sys.argv or "--filename" in sys.argv:

    UNIX_DRIVERS = "https://www.nvidia.com/en-us/drivers/unix/"

    result = requests.get(UNIX_DRIVERS)
    page = BeautifulSoup(result.text, "html.parser")
    p_tag = str(page.find(string="Linux x86_64/AMD64/EM64T").parent.parent)
    url = get_text(p_tag, ' Latest Production Branch Version: <a href="', '">')

    result = requests.get(url)
    page = BeautifulSoup(result.text, "html.parser")
    url = f"""https://www.nvidia.com{page.find(id="lnkDwnldBtn").get("href")}"""
    url = get_text(url, 'url=', '&')

    url = f"https://us.download.nvidia.com{url}"

    filename = get_filename(url)

    if "--filename" in sys.argv:
        print(filename)
    if "--url" in sys.argv:
        print(url)
