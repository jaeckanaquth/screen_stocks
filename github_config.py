import os
service_account = str(os.environ['G_SECRETS'])

password = str(os.environ['WP_PASSWORD'])
user = str(os.environ['WP_USER'])
url = str(os.environ['T_NOVEL'])
novel_name = str(os.environ['NOVEL_NAME'])
my_site = f"{os.environ['MY_SITE']}"
translation_site = str(os.environ['T_SITE'])
nu_username = str(os.environ['NU_USER'])
nu_password = str(os.environ['NU_PASSWORD'])
translator = str(os.environ['TRANSLATOR'])
special = ['[', ']', '\\', '\'', '!', '@', '#', '$', '%', '^', '&', '*',
           '{', '}', '"', ':', ';', ',', '<', '>', '.', '?', '<WordPressPost: b\'', 'WordPressPost: ', '\'>', "�"]
tags = [str(os.environ['TAG1'])]
name_edit = novel_name.lower().replace(" ", '-')
novel_link = f"{str(os.environ['NOVEL_LINK'])}{name_edit}/"

