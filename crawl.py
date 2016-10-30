import re;
import cookielib;
import urllib;
import urllib2;
import optparse;
 
#------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-'*80;

#------------------------------------------------------------------------------
# main function to emulate login baidu
def emulateLoginBaidu():
    printDelimiter();
    # parse input parameters
    parser = optparse.OptionParser();
    parser.add_option("-u","--username",action="store",type="string",default='',dest="username",help="Your Baidu Username");
    parser.add_option("-p","--password",action="store",type="string",default='',dest="password",help="Your Baidu password");
    (options, args) = parser.parse_args();
    # export all options variables, then later variables can be used
    for i in dir(options):
        exec(i + " = options." + i);
    printDelimiter();
    print "[preparation] using cookieJar & HTTPCookieProcessor to automatically handle cookies";

    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
    urllib2.install_opener(opener);
    printDelimiter();

    print "[step1] get cookie";
    mainUrl= "http://www.itjuzi.com/";
    # add a header to pretend this is a request from browser
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url = mainUrl, headers = header)
    resp = urllib2.urlopen(req);
    for index, cookie in enumerate(cj):
        print '[',index, ']',cookie;
    printDelimiter();

    print "[step2] emulate login";
    loginUrl = "https://passport.baidu.com/v2/api/?login";
    postDict = {
        'charset' : "utf-8",
        'username' : username,
        'password' : password,
        'remenber' : 1
    };
'''
    postData = urllib.urlencode(postDict);
    req = urllib2.Request(loginUrl, postData);
        # in most case, to do POST request, the content-type, is application/x-www-form-urlencoded
        req.add_header('Content-Type', "application/x-www-form-urlencoded");
        resp = urllib2.urlopen(req);
        cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID'];
        loginBaiduOK = checkAllCookiesExist(cookiesToCheck, cj);
        if(loginBaiduOK):
            print "+++ Emulate login baidu is OK, ^_^";
        else:
            print "--- Failed to emulate login baidu !"
'''

if __name__=="__main__":
    emulateLoginBaidu();
