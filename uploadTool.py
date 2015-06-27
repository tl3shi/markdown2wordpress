#coding utf-8
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import ConfigParser, xmlrpc_client
from wordpress_xmlrpc.methods.users import GetUserInfo
import pandocTool
import mimetypes
import re

def readConfig():
    config = ConfigParser()
    with open('wp-config.cfg', 'r') as f:
        config.readfp(f)
    return config

def initClient():
    config = readConfig()
    xmlrpc_url = config.get('wordpress', 'url')
    username = config.get('wordpress', 'username')
    userid = config.get('wordpress', 'userid')
    return Client(xmlrpc_url, username, config.get('wordpress', 'password'))

def uploadFile(client, filename): # failed
    data = {}
    data['type'] = mimetypes.guess_type(filename)[0]
    data['name'] = filename
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    resp = client.call(media.UploadFile(data))
    return resp

#tanglei:markdown2wordpress TangLei$ python uploadTool.py
#{'url': 'http://www.tanglei.name/wp-content/uploads/2015/06/postsbinding-domain-to-plugin-of-mobile-themem.tanglei.name_.preview.png', 'type': 'image/png', 'id': '2683', 'file': 'postsbinding-domain-to-plugin-of-mobile-themem.tanglei.name_.preview.png'}
#tanglei:markdown2wordpress TangLei$ python uploadTool.py
#{'url': 'http://www.tanglei.name/wp-content/uploads/2015/06/postsbinding-domain-to-plugin-of-mobile-themem.tanglei.name_.preview1.png', 'type': 'image/png', 'id': '2684', 'file': 'postsbinding-domain-to-plugin-of-mobile-themem.tanglei.name_.preview.png'}

# post.id = 2659
client = initClient()
print uploadFile(client, './posts/binding-domain-to-plugin-of-mobile-theme/m.tanglei.name.preview.png')
