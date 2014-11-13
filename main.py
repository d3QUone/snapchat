import urllib2, socket, urllib
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
            inputData.append({
                "user":item[0].replace("\n", "").replace("\r\n", ""), 
                "pass":item[1].replace("\n", "").replace("\r\n", "")
                }) 
        inputFile.close()
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
        for item in settings:
            if item.find("image:") != -1:
                image = item.replace(" ", "")
            if item.find("threads:") != -1:
                threads = item.replace(" ", "")
        image = image.split("image:")[1]
        threads = int(threads.split("threads:")[1])
        #print "image =", image
        #print "threads =", threads
        settingsFile.close()
    except BaseException as ex:
        print "No file named 'settings.txt', error " + str(ex)
        print "\nPress any key to exit"
        raw_input()
        exit()

    form = image.split("/")
    form = form[len(form)-1].split(".")[1]
    #print form
    urllib.urlretrieve(image, filename="file." + form)
    print "image is ready for upload"

    # all code below is for every thread. above - once in main thread


    #upload this to every account

    #save media_id, send to every friend
        

    #print "\nPress any key to continue"
    #raw_input()
    #print ""
    
    # +parse proxies 
    i = 0 
    for line in proxiesFile:
        proxy = line.replace("\n", "")

        # +check if ok
        if not is_bad_proxy(proxy):
            print "+ " + proxy
            for auth in inputData:
                # check if auth is not in results (error or not, dont process twice)
                
                if process(proxy, auth) == 0:
                    #mean that proxy is banned ?
                    #
                    result.append(auth["user"]+":"+auth["pass"] + " #error")
                    #break
                else:
                    result.append(auth["user"]+":"+auth["pass"] + " #well")
                    
            
        else:
            print "- " + proxy


        #---for early tests
        i += 1
        if i > 5:
            break
        #---for early tests

    #save results
    print "\n---Results---"
    for line in result: print line


def process(prox, auth):
    global result
    print "user "+auth["user"]+" pass "+auth["pass"]
    num = 0 #successfully processed 
    prox = {"http": "http://"+prox, "https": "https://"+prox}

    #work with Snapchat here
    try:
        s = Snapchat()
        s.proxies = prox
        login = s.login(auth["user"], auth["pass"])
        #print "login =", login
        #print "friends ", login['friends']
        print "num friends = ", len(login["friends"]), ", names below:"
        for friend in login["friends"]:
            print friend["name"]

        #if login['friends'] == 'friends':
            #means error in pass / anything else
            #return 0

        # upload pic for curr account

        # send to all 'friends'

        # make uploading module - snapTo(friendName, friendID)

        print "\n-------------------"
        return 1
        # save here "user #<num>"
    except Exception as ex:
        print str(ex)
        print "\n-------------------"
        return 0
        # save here "user #error"


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



main()
