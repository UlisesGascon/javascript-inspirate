# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib

def change_text(text):
    return text.encode('utf-8', 'ignore')

developers_md = ""

developers = ["AriyaHidayat", "BrendanEich", "DotProto", "John_Papa", "MatiasArriola", "PascalPrecht", "SachaGreif", "SimoAhava", "addyosmani", "alexnavasardyan", "amasad", "brianleroux", "codepo8", "codylindley", "codingcarlos", "davidwalshblog", "dejan_dimic", "dshaw", "ducntq", "elijahmanor", "erikthedev_", "firede", "garu_rj", "gavrisimo", "gibson042", "greybax", "idangazit", "jamsyoung", "jdalton", "jeresig", "jfroffice", "kahliltweets", "kentcdodds", "kom_256", "l0ckys", "ladyleet", "leobetosouza", "marcotrulla", "marocchino", "mathias", "mihaipaun", "nataliemac", "nicksalloum_", "okuryu", "os_weekends", "ossreleasefeed", "paul_irish", "rauschma", "rem", "remotesynth", "rmurphey", "roebuk", "rwaldron", "stephanlindauer", "tomdale", "trevnorris", "umaar", "wecodesign", "yotamofek", "_ericelliott", "slicknet"]

for developer in developers:
    
    url = "https://twitter.com/" + developer
    request = urllib.urlopen(url)
    
    print "status code: " + str(request.getcode())
    if request.getcode() == 200:
        request = request.read()
        soup = BeautifulSoup(request, "html5lib")
        print "url: " + url
        
        name = soup.findAll("a", { "class" : "ProfileHeaderCard-nameLink"})
        bio = soup.findAll("p", { "class" : "ProfileHeaderCard-bio"})
    
        if name and bio:
            name = name[0].text.encode('utf-8')
            bio = bio[0].text.encode('utf-8')
            
            print "current: " + name
            print "bio: " + bio
        
            developers_md += "- **["+ name +"]("+url+")**\n\n"
            developers_md += "\t@"+ developer+ ": *"+ bio +"*\n\n"
            print "-------------------------------------"

text_file = open("developers.md", "w")
text_file.write(developers_md)
text_file.close()
