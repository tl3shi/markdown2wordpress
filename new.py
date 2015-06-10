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

client = initClient()
post = WordPressPost()
post.title = 'My post2'
post.content = pandocTool.md2html('test.md')
#post.id = client.call(posts.NewPost(post))
post.id = 2659
client.call(posts.EditPost(post.id, post))

# post.post_status = 'publish'
print client.call(posts.EditPost(post.id, post))
print post.id

