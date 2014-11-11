import urllib2, socket
#import pysnap

inputData = []
result = []

def main():
    global result
    
    # +get proxies
    try:
        proxiesFile = open("proxies.txt", "r")
    except BaseException as ex:
        print "No file named 'proxies.txt', error " + str(ex)
        print "\nPress any key to exit"
        # add safe exit
        raw_input()
        exit()

    try:
        inputFile = open("input.txt", "r")
        data = inputFile.read().split("\r\n")
        for item in data:
            item = item.split(":")
            inputData.append({"user":item[0], "pass":item[1]})
        
        #print inputData
    except BaseException as ex:
        print "No file named 'input.txt', error " + str(ex)
        print "\nPress any key to exit"
        # add safe exit
        raw_input()
        exit()
    
    #raw_input()
    
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
    # http prox
    print "\nused proxy =" + prox
    print "user="+auth["user"]+", pass="+auth["pass"]

    num = 0

    # if 



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
        #print 'Error code: ', e.code
        #return e.code
        return True 
    except Exception, detail:
        #print "ERROR:", detail
        return True
    return False




main()
