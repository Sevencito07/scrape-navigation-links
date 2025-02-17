#!/usr/bin/python
import sys
import json
import requests
import argparse
from bs4 import BeautifulSoup

def results(file):
    content = open(file, 'r').readlines()
    urls = []
    for line in content:
        data = json.loads(line.strip())
        for url in data.get('results', []):
            urls.append(url.get('url', ''))
    return urls

def crawl(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'lxml')
        links = soup.findAll('a', href=True)
        for link in links:
            href = link['href']
            if href and href != '#':
                print(f'[+] {url} : {href}')
    except requests.exceptions.RequestException as e:
        print(f'[-] Error fetching {url}: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="FFUF results file")
    args = parser.parse_args()

    urls = results(args.file)
    for url in urls:
        if url:
            crawl(url)

