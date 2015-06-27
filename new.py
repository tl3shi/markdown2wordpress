# coding=utf8
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts, media, taxonomies
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

def parseMedia(lines):
    config = readConfig()
    resourcePrefix = config.get('resource', 'picGithubPrefix')
    reImg = r'!\[[^\\\\]*\]\(\./[^\\\\]*\)'
    reFile= r'\(\.\/[^\\\\]*\)'
    content = []
    for line in lines:
        matches = re.findall(reImg, line)
        for pic in matches:
            filename = re.findall(reFile, pic)[0]
            line = line.replace(filename, '(' + resourcePrefix + filename[2:-1] + ')')
        content.append(line)
    return content

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
            rawcontent = parseMedia(lines[i:])
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
            post.terms_names = {}
            values['tags'] = values['tags'].replace('，', ',')
            values['categories'] = values['categories'].replace('，', ',')
            if len(values['tags']) > 0:
                post.terms_names['post_tag'] = [ tag.strip() for tag in values['tags'].split(',') if len(tag) > 0] 
            if len(values['categories']) > 0:
                post.terms_names['category'] = [ cate.strip() for cate in values['categories'].split(',') if len(cate) > 0] 
            return post

def uploadFile(client, filename):
    data = {}
    data['type'] = mimetypes.guess_type(filename)[0] 
    data['name'] = filename
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    resp = client.call(media.UploadFile(data))
    return resp

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

def testTerm(client):
    categories = client.call(taxonomies.GetTerms('category'))
    #decode may have problem when chinese
    print categories

#testUpdate(2669)
post = parseDocument('posts/binding-domain-to-plugin-of-mobile-theme.md')
# post.id = 2659
# post.post_status = 'publish'
client = initClient()
#print client.call(posts.EditPost(2669, testReturnPost() ))
print client.call(posts.EditPost(2659, post))
