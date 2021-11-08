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

def posting(content, attachment_id):
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
    post.thumbnail = attachment_id
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
