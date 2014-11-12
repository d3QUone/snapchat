import urllib2, socket
import requests
from snapi import Snapchat

inputData = []
result = []

# start new thread with a pack of users
def main():
    global result
    
    # +get proxies
    try:
        proxiesFile = open("proxies.txt", "r")
    except BaseException as ex:
        print "No file named 'proxies.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    try:
        inputFile = open("input.txt", "r")
        data = inputFile.read().split("\r\n")
        for item in data:
            item = item.split(":")
            inputData.append({"user":item[0].split("@")[0], "pass":item[1]})
    except BaseException as ex:
        print "No file named 'input.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    image = ""
    threads = ""
    try:
        settingsFile = open("settings.txt", "r")
        settings = settingsFile.read().split("\n")
        #print settings
        for item in settings:
            if item.find("image:") != -1:
                image = item.replace(" ", "")
            if item.find("threads:") != -1:
                threads = item.replace(" ", "")
        image = image.split("image:")[1]
        threads = int(threads.split("threads:")[1])
        #print "image =", image
        #print "threads =", threads
    except BaseException as ex:
        print "No file named 'settings.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    #print "\nPress any key to continue"
    #raw_input()
    #print ""
    
    i = 0
    # +parse proxies 
    for line in proxiesFile:
        proxy = line.replace("\n", "")

        # +check if ok
        if not is_bad_proxy(proxy):
            print "+ " + proxy
            for auth in inputData:
                process(proxy, auth)
            
        else:
            print "- " + proxy


        #---for tests only
        i += 1
        if i > 5:
            break

    #save results


def process(prox, auth):
    global result
    print "user="+auth["user"]+", pass="+auth["pass"]

    num = 0
    prox = {"http": "http://"+prox}
    print "proxies =", prox

    #login here
    #try:
    s = Snapchat()
    s.proxies = prox
    s.login(auth["user"], auth["pass"])

    friendlist = s.get_friends()
    print friendlist
    #except Exception as ex:
        #print "error user " + str(ex)

    #get list of friends


def is_bad_proxy(pip):
    socket.setdefaulttimeout(10)
    try:        
        proxy_handler = urllib2.ProxyHandler({'http': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req=urllib2.Request('http://www.google.com')  # change the url address here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:        
        return True 
    except Exception, detail:
        return True
    return False



main()
