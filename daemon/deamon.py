from datetime import datetime
from httplib import HTTPConnection, HTTPException
from time import sleep
from xml.etree import ElementTree
from functools import total_ordering

import json,sys,socket
import urllib2

@total_ordering
class Post(object):
    def __init__(self, post_id, time, ua, user, msg):
        self.post_id=post_id
        self.time=time
        self.ua=ua
        self.user=user
        self.msg=msg
        
    def __lt__(self,other):
        return self.post_id < other.post_id
            
    def __eq__(self,other):
        return self.post_id == other.post_id
    
class PostEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,Post):
            return dict(post_id=o.post_id, time=o.time, ua=o.ua, user=o.user, msg=o.msg)
        elif isinstance(o,datetime):
            return o.isoformat()
        else:
            super(PostEncoder, self).default(o)

last_id = -1
headers = dict(ContentType = "application/json; charset=utf-8")
http = HTTPConnection("localhost:8000")
post_list = []

while True:
    backend = urllib2.urlopen("http://euromussels.eu/?q=tribune.xml&last_id=%d"%last_id)
    #backend = urllib2.urlopen("http://linuxfr.org/board/index.xml")
    xml_string = backend.read()
    tree = ElementTree.fromstring(xml_string)
    
    

    for child in tree :
        id_post = int(child.get("id"))
    
        if id_post > last_id:
            t = child.get("time")
            timestamp = datetime.strptime(t,"%Y%m%d%H%M%S")
            user_agent = child.find("info").text
            if user_agent == None:
                        user_agent = ""
            msg = child.find("message").text
            login = child.find("login").text
            post_list.append(Post(id_post, timestamp, user_agent,login,msg))
            
    if post_list:
        last_id = max(post_list).post_id
      #  print "last id: %d"%(last_id)
        post_json = dict(tribune="euromussels", posts=post_list)
        json_str = json.dumps(post_json,cls=PostEncoder)
        print json_str
        try:
            http.request("POST", "/post", json_str, headers)
            resp = http.getresponse()
            resp_body = resp.read()
            if resp.status == 500:
                f = open("/tmp/error.html","w")
                f.write(resp_body)
                f.close()
                print "500\n"
            else:
                print "%d: %s\n"%(resp.status, resp_body)
                post_list = []
        except (HTTPException, socket.error) as e:
            print "Error: " + unicode(e)
            http = HTTPConnection("localhost:8000")
        sys.stdout.flush()
    sleep(10)