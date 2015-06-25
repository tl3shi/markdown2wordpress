from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.compat import ConfigParser
import pandocTool

def initClient():
    config = ConfigParser()
    with open('wp-config.cfg', 'r') as f:
        config.readfp(f)
    xmlrpc_url = config.get('wordpress', 'url')
    username = config.get('wordpress', 'username')
    userid = config.get('wordpress', 'userid')
    return Client(xmlrpc_url, username, config.get('wordpress', 'password'))

def parseDocument(filename):
    lines = open(filename, 'r').readlines()
    values = {'title':'', 'permalink':'', 'layout':'post', 'tags':'', 'categories':'default', 'published':False}
    start = False
    config = False
    for i in range(len(lines)):
        line = lines[i]
        if !config:
            if line.starts('---'):
                if (start == False):
                    start = True
                else: # end
                    if (values['title'] == '' or values['permalink'] == ''):
                        printf('title and permalink should not be null'); exit()
                    else:# config ok 
                        config = True
            else:
                try:
                    key = line[:line.find(':')]
                    value = line[line.find(':'):]
                    values[key] = value
                except:
                    printf('config failed! (key, value) = (' + key + ', ' + value + ')');exit()
        else: #config ok
            rawcontent = lines[i:]
            rawfilename = filename + '.raw'
            open(rawfilename, 'w').writelines(rawcontent)
            post = WordPressPost()
            post.title = values['title']
            post.link = values['permalink']
            post.content = pandocTool.md2html(rawfilename)
            post.post_type = values['layout']
            post.post_status = values['published'] ? 'publish' : ''
            return post

client = initClient()
#post.id = client.call(posts.NewPost(post))
post.id = 2659
client.call(posts.EditPost(post.id, post))

# post.post_status = 'publish'
print client.call(posts.EditPost(post.id, post))
print post.id

