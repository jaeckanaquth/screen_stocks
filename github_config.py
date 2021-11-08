import os
service_account = str(os.environ['G_SECRETS'])
my_site = f"{os.environ['MY_SITE']}"
password = str(os.environ['WP_PASSWORD'])
user = str(os.environ['WP_USER'])
head = str(os.environ['HEAD'])
count = int(os.environ['COUNT'])
imgurl = "http://www.outdoor-photos.com/shuffle/"
