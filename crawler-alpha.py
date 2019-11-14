from bs4 import BeautifulSoup
import requests
from time import time

REDDIT = "https://www.reddit.com"
LINKS = ["https://www.reddit.com"]
EXTERNAL_LINKS = []
PROCESSED_LINKS = []
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
PAGES_PROCESSED = 0


def addToList(currentList, processedList, value):
    if value not in processedList:
        currentList.append(value)
    return

while LINKS:
    t0 = time()
    link = LINKS.pop(0)

    try:
        r = requests.get(link, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        LINKS.append(link)
        continue

    PROCESSED_LINKS.append(link)
    
    t = r.text
    s = BeautifulSoup(t, "html.parser")
    a_list = s.find_all("a", href=True)
    a_formatted = []
    for a in a_list:
        href = a["href"]
        if href.startswith("http"):
            # Full URL Links
            if "reddit.com" in href:
                # Internal
                addToList(LINKS, PROCESSED_LINKS, href)
            else:
                # External
                addToList(EXTERNAL_LINKS, PROCESSED_LINKS, href)
        elif href.startswith("/"):
            # Internal "good" links
            newLink = REDDIT + href
            addToList(LINKS, PROCESSED_LINKS, newLink)
        elif "javascript" in href and "void" in href and not "/" in href:
            # Ignore javascript function calls
            continue
        elif href.startswith("#"):
            # Ignore page location links
            continue
        else:
            print(href)

    t1 = time()
    diff = t1 - t0
    PAGES_PROCESSED = PAGES_PROCESSED + 1
            
    print(str(PAGES_PROCESSED) + ": " + str(len(LINKS)) + " | " + str(diff) + " seconds")
