import re;
import time;
import sys;
import cookielib;
import urllib;
import urllib2;
import optparse;
from bs4 import BeautifulSoup;
 
#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;

#------------------------------------------------------------------------------
# get the comments of each project according to the given url parameter
def getComment(url):
    crawlUrl = url
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url = crawlUrl, headers = header)
    resp = urllib2.urlopen(req);
    soup = BeautifulSoup(resp.read());
    comment = soup.find(name = 'div', attrs = {'class' : 'main'}).find(name = 'div', attrs = {'class' : 'block'}).find(name='div', attrs = False).findAll(name = 'p')
    commentStr = ""
    for i in comment:
        commentStr = commentStr + i.get_text()
    return commentStr

#------------------------------------------------------------------------------
# main function to emulate login baidu
def mainFunc(url):
    # [preparation] using cookieJar & HTTPCookieProcessor to automatically handle cookies
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
    urllib2.install_opener(opener);

    # [step1] get cookie
    mainUrl= "http://www.itjuzi.com/";
    # add a header to pretend this is a request from browser
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url = mainUrl, headers = header)
    resp = urllib2.urlopen(req);

    # [step2] emulate login
    loginUrl = "https://www.itjuzi.com/user/login";
    postDict = {
        'identity' : "f22123@126.com",
        'password' : "Fzxdtc945288",
        'remember' : 1
    };
    postData = urllib.urlencode(postDict);
    req = urllib2.Request(loginUrl, postData, header);
    resp = urllib2.urlopen(req);
    
    # [step3] crawl
    crawlUrl = url
    req = urllib2.Request(url = crawlUrl, headers = header)
    resp = urllib2.urlopen(req);

#[step4] extract needed info with beautifulsoup
    soup = BeautifulSoup(resp.read())
#company = soup.find(name = 'span', attrs={'class' : 'title'}).get_text().strip()
    company = soup.find(name = 'span', attrs={'class' : 'title'}).get_text().strip()
    invecaseTable = soup.find(attrs={"class" : "list-invecase limited-itemnum haslogin needfilter"});
    invecase = invecaseTable.findAll(name = 'tr');
    for i in range(0, len(invecase)):
        item = invecase[i].findAll(name = 'td')
        date = item[0].get_text().strip()
        year = re.split('\.', date)[0]
        month = re.split('\.', date)[1]
        localYear = time.localtime()[0] # year of local system
        localMonth = time.localtime()[1] # month of local system
        if int(year) < int(localYear) or int(month) < int(localMonth):
            continue
        proj = invecase[i].find(name = 'td', attrs = {'class' : 'title'})
        projUrl = proj.find(name = 'a', href = True)['href']
        comment = getComment(projUrl);
        sys.stdout.write(company + '\t' + date)
        for j in range(1, len(item)):
            itemTxt = item[j].get_text().strip()
            sys.stdout.write('\t' + itemTxt)
        sys.stdout.write('\t' + comment + '\n');

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for line in sys.stdin.readlines():
        mainFunc(line);
