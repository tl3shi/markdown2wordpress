from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.compat import ConfigParser
from wordpress_xmlrpc.methods.users import GetUserInfo
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
        if config == False:
            if line.startswith('---'):
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
                    value = line[line.find(':')+1:]
                    values[key] = value.strip()
                except:
                    printf('config failed! (key, value) = (' + key + ', ' + value + ')');exit()
        else: #config ok
            rawcontent = lines[i:]
            rawfilename = filename + '.raw.md'
            open(rawfilename, 'w').writelines(rawcontent)
            post = WordPressPost()
            post.title = values['title']
            post.slug = values['permalink']
            post.content = pandocTool.md2html(rawfilename)
            post.post_type = values['layout']
            post.post_status = 'publish' if values['published'] == True else 'draft'
            post.comment_status = 'open' #default
            post.pint_status = 'open' #default
            return post

def testConnection():
    client = initClient()
    print client.call(GetUserInfo())

def testNew():
    client = initClient()
    post = WordPressPost()
    post.title = 'My new title'
    post.content = 'This is the body of my new post.'
    print client.call(posts.NewPost(post))

def testUpdate(pid):
    client = initClient()
    post = WordPressPost()
    post.title = 'My new title update 2'
    post.content = 'This is the body of my new post.'
    post.slug= 'helloword'
    post.post_type = 'post'
    post.post_status = 'draft'
    print client.call(posts.EditPost(pid, post))

#testUpdate(2669)
post = parseDocument('test.md')
# post.id = 2659
# post.post_status = 'publish'
client = initClient()
#print client.call(posts.EditPost(2669, testReturnPost() ))
print client.call(posts.EditPost(2669, post))
