import os, sys, json, re
import requests
import datetime
from common import process_new_file
from configloader import config

from pprint import pprint

# https://api.j-novel.club/api/users/590f6374c3f8137f46a648aa?filter={%22include%22:[%22accessTokens%22,%22credentials%22,%22identities%22,{%22ownedBooks%22:%22serie%22},%22readParts%22,%22roles%22,%22subscriptions%22]}

authtoken = None
userid = None
username = None

def login():
    global authtoken, userid, username
    if authtoken:
        return True

    data = request("/Users/login?include=user", data={"email": config["JNC_EMAIL"], "password": config["JNC_PASSWORD"]}, usePost=True)
    #pprint(data)
    try:
        authtoken = data["id"]
        userid = data["userId"]
        username = data["user"]["username"]
        return True
    except:
        print("Invalid response when trying to login")
        return False

def request(url, data=None, usePost=False, requireAuth=False, verbose=True):
    global authtoken
    try:
        if requireAuth:
            res = login()
            if not res: return None

        headers = None
        if authtoken:
            #print "USING authtoken:", authtoken
            headers={"Authorization": authtoken}

        #print url, data

        if usePost:
            r = requests.post(config["JNC_API_ENDPOINT"]+url, data=data, headers=headers, timeout=10)
        else:
            r = requests.get(config["JNC_API_ENDPOINT"]+url, data=data, headers=headers, timeout=10)
        
        #print r.text
        json = r.json()

        if "error" in json:
            if verbose:
                print("Error making request to JNC API:")
                try: print  ("   %s" % json["error"]["message"])
                except: pass
                print ("   ", url)
                print ("   ", data)
            return None
        return json
    except KeyboardInterrupt:
        raise
    except Exception as ex:
        if verbose:
            print("Error making request to JNC API:")
            print("   ", "Error:", ex)
            print("   ", url)
            print("   ", data)
        return None


def getAvailableVolumes():
    global userid
    datafilter = {
        "include": [
            {"ownedBooks": "serie"}
        ]
    }
    data = {
        "filter": json.dumps(datafilter)
    }
    login()
    return request("/users/%s" % userid, data=data, requireAuth=True)

def getDownloadUrlForBook(bookid):
    global authtoken, userid, username
    return "%s/volumes/%s/getpremiumebook?userId=%s&userName=%s&access_token=%s" % (
        config["JNC_API_ENDPOINT"],
        bookid,
        userid,
        username,
        authtoken
    )

def isDateIsoStringBeforeNow(dstr):
    now = datetime.datetime.now()
    then = datetime.datetime.strptime(dstr, "%Y-%m-%dT%H:%M:%S.%fZ")
    return now > then


def titleToFilename(title):
    x = re.sub(r'[^\d\w]+', '-', title.lower())
    x = re.sub(r'\-+', '-', x)
    return x

def getNewBooksAvailableToDownload():
    data = getAvailableVolumes()
    newbookstodl = []
    for book in data['ownedBooks']:

        fn = "%s.epub" % titleToFilename(book['title'])
        fullfn = os.path.join(config["JNC_OUTPUT_DIR"], fn)
        available = isDateIsoStringBeforeNow(book['publishingDate'])
        downloaded = os.path.exists(fullfn)

        #print()
        #print("%s (%s)" % (book['title'], book['id']))
        #print("Is available: %s" % (str(available)) )
        #print("File exists: %s (%s)" % (str(downloaded), fn))
        #print("Download URL: %s" % getDownloadUrlForBook(book['id']))

        if available and not downloaded:
            newbookstodl.append(book)
    
    return newbookstodl



def process():
    books = getNewBooksAvailableToDownload()
    if len(books) == 0:
        print("No new books available")
        return
    
    for book in books:

        fn = "%s.epub" % titleToFilename(book['title'])
        fullfn = os.path.join(config["JNC_OUTPUT_DIR"], fn)
        available = isDateIsoStringBeforeNow(book['publishingDate'])
        downloaded = os.path.exists(fullfn)
        url = getDownloadUrlForBook(book['id'])

        #print("%s (%s)" % (book['title'], book['id']))
        #print("Is available: %s" % (str(available)) )
        #print("File exists: %s (%s)" % (str(downloaded), fn))
        #continue

        try:
            print("Found new book %s" % book['title'])
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            with open(fullfn, 'wb') as file:
                file.write(r.content)
            print("Downloaded %s", book['title'])
            process_new_file(fullfn, "JNC")
        except Exception as e:
            if os.path.exists(fullfn):
                os.unlink(fullfn)
            print("An error ocurred: %s" % str(e))


if __name__ == "__main__":
    process()
