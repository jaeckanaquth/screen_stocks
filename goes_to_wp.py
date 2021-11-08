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
from wordpress_xmlrpc import WordPressPage

client = Client(config.my_site, config.user, config.password)

def posting(content):
    # print(heading)
    post = WordPressPost()
    post.title = "Stocks of the Day"
    post.terms_names = {
        'post_tag': ["code", "python"],
        'category': ["stock codes"],
    }
    post.content = content
    post.mime_type = "text/html"
    post.id = client.call(posts.NewPost(post))
    post.post_status = 'publish'
    client.call(posts.EditPost(post.id, post))
    print(post, post.id)
    return post.id


def uploadImage(novel_img, img_data):
    data = {
        'name': novel_img,
        'type': 'image/jpeg',
    }
    data['bits'] = xmlrpc_client.Binary(img_data)
    response = client.call(media.UploadFile(data))
    attachment_id = response['id']
    return attachment_id


def attachment_img(attachment_id):
    # print(heading)
    page = WordPressPage()
    page.title = "Intraday Stocks"
    page.thumbnail = attachment_id
    page.post_status = 'publish'
    page.id = 1586
    client.call(posts.EditPost(page.id, page))
    print(page, page.id)
    return page.id
