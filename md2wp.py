# coding=utf8
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts, media, taxonomies
from wordpress_xmlrpc.compat import ConfigParser, xmlrpc_client
from wordpress_xmlrpc.methods.users import GetUserInfo
import pandocTool
import mimetypes
import re
import os, sys, getopt

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
    values = {'title':'', 'permalink':'', 'layout':'post', 'tags':'', 'categories':'default', 'published': 'false'}
    start = False
    config = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if config == False:
            if line == '---':
                if (start == False):
                    start = True
                else: # end
                    if (values['title'] == '' or values['permalink'] == ''):
                        printf('title and permalink should not be null!\n'); exit()
                    else:# config ok 
                        config = True
            else:
                try:
                    key = line[:line.find(':')]
                    value = line[line.find(':')+1:]
                    values[key] = value.strip()
                except:
                    printf('config failed! (key, value) = (' + key + ', ' + value + ')\n');exit()
        else: #config ok
            while len(lines[i]) <= 1: #filter first blank lines
                i+=1
            rawcontent = parseMedia(lines[i:])
            rawfilename = filename[:-3] + '.raw.id-'
            open(rawfilename, 'w').writelines(rawcontent)
            post = WordPressPost()
            post.title = values['title']
            post.slug = values['permalink']
            post.content = pandocTool.md2html(rawfilename)
            post.post_type = values['layout']
            post.post_status = 'publish' if values['published'].lower() == 'true' else 'draft'
            post.comment_status = 'open' #default
            post.pint_status = 'open' #default
            post.terms_names = {}
            #values['tags'] = values['tags'].replace('，', ',') compatible with jekyll, use blank
            #values['categories'] = values['categories'].replace('，', ',')
            if len(values['tags']) > 0:
                post.terms_names['post_tag'] = [ tag.strip() for tag in values['tags'].split() if len(tag) > 0] 
            if len(values['categories']) > 0:
                post.terms_names['category'] = [ cate.strip() for cate in values['categories'].split() if len(cate) > 0] 
            return post

def newPost(filename):
    post = parseDocument(filename)
    client = initClient()
    post.id = client.call(posts.NewPost(post))
    oldRawFilename = filename[:-3] + '.raw.id-'
    newRawFilename = filename[:-3] + '.raw.id-' + str(post.id)
    os.rename(oldRawFilename, newRawFilename)
    return post.id > 0

def editPost(filename, post_id):
    post = parseDocument(filename)
    client = initClient()
    oldRawFilename = filename[:-3] + '.raw.id-'
    newRawFilename = filename[:-3] + '.raw.id-' + str(post_id)
    os.rename(oldRawFilename, newRawFilename)
    return client.call(posts.EditPost(post_id, post))

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

def testEdit():
    #testUpdate(2669)
    post = parseDocument('posts/binding-domain-to-plugin-of-mobile-theme.md')
    # post.id = 2659
    # post.post_status = 'publish'
    client = initClient()
    #print client.call(posts.EditPost(2669, testReturnPost() ))
    print client.call(posts.EditPost(2659, post))

def help():
    print 'useage:\n' + 'md2wp.py' + ' -f <postfilename> -o <operation>' + '\t or'
    print               'md2wp.py' + ' --file=<postfilename> --operation=<operation>'

def main(argv):
    filename = ''
    operation = ''
    try:
        opts, args = getopt.getopt(argv[1:], 'hf:o:', ['help', 'file=', 'operation='])
        if len(opts) < 2 :
            help()
            exit()
    except getopt.GetoptError:
        help()
        exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            exit()
        elif opt in ('-f', '--file'):
            filename = arg
        elif opt in ('-o', '--operation'):
            operation = arg
    if not os.path.exists(filename):
        print 'make sure the input file exists! ' + filename
        exit()
    if operation not in ('new', 'update'):
        print 'The operation "' + operation + '" not supported, current support operations are: "new", "update" !'
        exit()
    
    (postdir, basefilename) = os.path.split(filename)
    rawFilename = ''
    for f in os.listdir(postdir):
        if f.startswith(basefilename[:-3]) and len(f) > len(basefilename)+len('.raw.id-')-3:
            rawFilename = postdir + os.path.sep + f
            break
    
    if operation == 'new':
        if rawFilename != '':
            print 'The post with same filename has exsisted, make sure the operation is "new" or "update" ? ' + filename
            exit()
        if newPost(filename):
            print 'Post new successfully !\n'
        else:
            print 'Post failed !\n'
    elif operation == 'update':
        if rawFilename == '':
            print 'make sure the corresponding rawfile exists! \n'
            exit()
        post_id = rawFilename[rawFilename.find('.raw.id-')+len('.raw.id-'):]
        if not post_id.isdigit():
            print 'make sure the corresponding rawfile exists! \n'
            exit()
        if editPost(filename, post_id):
            print 'Update successfully !\n'
        else:
            print 'Update failed !\n'
        
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'command error! try ' + sys.argv[0] + ' -help\n'
        exit()
    main(sys.argv)
