from bs4 import BeautifulSoup
import requests
import redis

REDDIT = "https://www.reddit.com"
PROCESSED_LINKS = []
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def addToList(processedList, value):
    if value not in processedList:
        REDIS.lpush("unprocessedLinks", str(value))
        processedList.append(value)
    return

def getFromList():
    if REDIS.llen("unprocessedlinks") == 0:
        return None
    return str(REDIS.rpop("unprocessedlinks"))

# Open link to redis and check that connection has been made
REDIS = redis.Redis(host='localhost', port=6379, db=0)
def redisCheckConnection(maxRetries):
    try:
        response = rs.client_list()
    except redis.ConnectionError:
        if maxRetries > 0:
            return redisCheckConnection(maxRetries - 1)
        else:
            return False
    return True

while True:
    link = getFromList()
    if link is None:
        break
    
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
                addToList(PROCESSED_LINKS, href)
            else:
                # External
                continue
        elif href.startswith("/"):
            # Internal "good" links
            newLink = REDDIT + href
            addToList(PROCESSED_LINKS, newLink)
        elif "javascript" in href and "void" in href and not "/" in href:
            # Ignore javascript function calls
            continue
        elif href.startswith("#"):
            # Ignore page location links
            continue
        else:
            print(href)

    print(".")
