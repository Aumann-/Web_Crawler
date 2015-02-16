#python web crawler
#when run, crawler will ask for a starting URL and will crawl and catalog all links with a delay between each. Crawler will terminate are crawling a set number of links
#BUGS:      1. Crawler will only catalog the first links on each page *FIXED* - In get_all_links proc, return statement was indented to be part of loop, so it would always return after finding one link
#           2. Crawler will continue to crawl links it has already cataloged if it returns to it.*Fixed*
#           3. Crawler would break on some recursive links due to check_links procedure *FIXED* - fixed by removing procedure and casting list to set and back to list
#           3. Casting to set and back to list sorted links so program was crawling in wrong order

#TODO
#           1. Move caluclation for toprint to its own procedure *DONE*
import urllib, time, datetime

def get_page(url):
    try:
        #print 'Success'
        return urllib.urlopen(url).read()
    except:
        #print 'Fail'
        return ''

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        #print 'No Links Found'
        #wait = input("@>")
        return '0',-1
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    c = 0
    while True:
        url,endpos = get_next_target(page)
        if endpos == -1:
            #print 'get_all_links break'
            break
        else:
            print 'Got: ' + url
            links.append(url)
            page = page[endpos:]
    c = len(links)
    return links, c

#procedure to remove url from tocrawl if it has already been crawled
def check_crawled(tocrawl, crawled, dups):
    f_tocrawl = []
    s_tocrawl = set()
    for i in tocrawl:
            if i in crawled: #if link already crawled, add to duplicate file and remove from tocrawl
                print 'Removing (Already Crawled): ' + i
                dups.write(i + '\n')
                tocrawl.remove(i)
            elif i not in s_tocrawl:
                f_tocrawl.append(i)
                s_tocrawl.add(i)
    return f_tocrawl

def get_toprint(counters):
    check = 0
    toprint = ''
    for i in counters[0]:
        if counters[0][check] == ' ': #once a space is found, entire number has been found
            break
        toprint = toprint + counters[0][check]
        check = check + 1
    return toprint
    

def crawl_web(seed):
    tocrawl = [seed]
    print 'Origin: ' + seed
    crawled = [] #holds links that have been crawled
    links = [] #temporarily holds links return from get_all_links proc
    counters = [] #holds tier lines
    count = 1 #keeps track of number of links crawled to determine when to temrinate
    c = 0 #temp holds how many links were returned from get_all_links
    printed = 0 #holds how many links have been printed from last tier line
    temp = 0
    toprint = '' #holds how many links to print til next tier line
    check_flag = True #used for creating toprint
    textfile = file('links.txt','wt') #file to hold links crawled
    dups = file('duplicates.txt','wt') #file to hold duplicate links before removal
    while tocrawl:
        page = tocrawl.pop(0)
        if page not in crawled:
            print 'Crawling: ' + page
            links, c = get_all_links(get_page(page))
            #only add amount to counters if links found are greater than 0
            if (c > 0):
                counters.append(str(c) + ' from ' + page)
            tocrawl = tocrawl + links
            #tocrawl = check_crawled(tocrawl, crawled, dups)
            crawled.append(page)
            textfile.write(page + '\n')
            printed = printed + 1
            #precaution in case a 0 from amount is in counters
            if (len(counters) > 0 and int(counters[0][0]) == 0):
                counters.pop(0)
            #this block is to get the proper number of links to count to
            #before printing the next tier line
            if (check_flag == True and len(counters) > 0):
                toprint = get_toprint(counters)
                check_flag = False
                temp = counters[0]
                counters.pop(0)
            #//////
            #if at the origin, print its tier line
            if (page == seed):
                #temp = counters[0]
                #counters.pop(0)
                textfile.write('\n' + temp + '\n\n')
                printed = 0
            #if it has printed the appropriate amount of links from last tier line
            #print next tier line
            elif (printed == int(toprint)):
                temp = counters[0]
                textfile.write('\n' + temp + '\n\n')
                printed = 0
                toprint = ''
                check_flag = True
            print 'Sleeping'
            time.sleep(10) #wait for x seconds between links
            count = count + 1
        else: #if current link is already in crawled list
            print 'Already Crawled: ' + page
            printed = printed + 1
            count = count + 1
            if (len(counters) > 0 and int(counters[0][0]) == 0):
                counters.pop(0)
            #this block is to get the proper number of links to count to
            #before printing the next tier line
            if (check_flag == True and len(counters) > 0):
                toprint = get_toprint(counters)
                check_flag = False
                counters.pop(0)
            #
            dups.write(page + '\n') #write link to duplicates file
            #if it has printed the appropriate amount of links from last tier line
            #print next tier line
            if (printed == int(toprint)):
                temp = counters[0]
                textfile.write('\n' + temp + '\n\n')
                printed = 0
                toprint = ''
                check_flag = True
        #Ask every x links to quit
        if count % 360 == 0:
            print datetime.datetime.now().time()
            print 'Stop?'
            com = input('@>')
            if com == 'y':
                print 'Done'
                break
    textfile.close()
    dups.close()
    return tocrawl

print "Enter URL"
myurl = input("@")
links = crawl_web(myurl)
#print all links found but not crawled to second file
textf = file('tocrawl.txt','wt')
for i in links:
    textf.write(i + '\n')
textf.close()
raw_input('Ready to Quit ')
