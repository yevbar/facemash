import json
from lxml import html
import os
import pprint
import requests
from time import sleep
import twitter

def read_through_list_file():
    my_session = requests.session()
    page = None

    with open("page.html", "r") as f:
        content = f.read()
        page = html.fromstring(content.encode("ascii", "ignore"))

    lines = page.xpath('//div[@id="m_-6350649862926397860gmail-grid-body"]/div/div[1]/div[1]')
    names = [line.text.strip() for line in lines]

    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                      consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                      access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
                      access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    vc_homies = {}
    with open("result.txt", "r") as f:
        content = f.read()
        vc_homies = json.loads(content)

    for name in names:
        if name in vc_homies:
            continue

        try:
            results = api.GetUsersSearch(term=name)
        except:
            continue

        if len(results) == 0:
            continue

        first_result = results[0]
        vc_homies[name] = first_result.AsDict()
        sleep(0.25)

    with open("result.txt", "w") as f:
        f.write(json.dumps(vc_homies))

def without_normal(s):
    return s[:s.index("_normal")] + s[s.index("_normal")+7:]

my_obj = {}
with open("result.txt", "r") as f:
    content = f.read()
    my_obj = json.loads(content)

for user in my_obj:
    pprint.pprint(my_obj[user], width=1)
    """
    user_obj = my_obj[user]
    for key in user_obj:
        if "url" in key and "_normal" in user_obj[key]:
            user_obj[key] = without_normal(user_obj[key])

    my_obj[user] = user_obj
    """

"""
with open("result.txt", "w") as f:
    f.write(json.dumps(my_obj))
"""
