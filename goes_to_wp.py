from datetime import datetime, timedelta
import glob
if glob.glob("config.py"):
    import config
else:
    import github_config as config
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc import WordPressPost

client = Client(config.my_site, config.user, config.password)

def posting(header, content):
    # print(heading)
    # heading = 'test'
    post = WordPressPost()
    post.title = header
    post.terms_names = {
        'post_tag': ["code", "python"],
        'category': ["stock codes"],
    }
    post.content = content
    post.mime_type = "text/html"
    post.id = client.call(posts.NewPost(post))
    post.date = datetime.now() + timedelta(days=7)
    post.post_status = 'publish'
    client.call(posts.EditPost(post.id, post))
    print(post, post.id)
    return post.id
