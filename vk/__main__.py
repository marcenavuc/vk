import os
import json
from typing import Dict, List

import requests
from tqdm import tqdm

from vk.user import User
from vk.cli_parser import parser

VERSION = "5.131"
APP_ID = "7851379"
AUTH_QUERY = 'https://oauth.vk.com/authorize?client_id={}&display=page'\
             '&redirect_uri=https://oauth.vk.com/blank.html&scope=friends'\
             '&response_type=token&v={}'.format(APP_ID, VERSION)
QUERY_TEMPLATE = "https://api.vk.com/method/friends.get?user_id={}" \
                 "&access_token={}&v={}&fields=first_name"

TOKEN = os.environ.get("VK_TOKEN")
if TOKEN is None:
    raise ValueError("You need set environment variable VK_TOKEN with your "
                     "application token")


def send_query(user_id: int) -> Dict:
    query = QUERY_TEMPLATE.format(user_id, TOKEN, VERSION)
    response = requests.get(query)
    return json.loads(response.text)


def find_friends(user_id: int) -> List[User]:
    data = send_query(user_id)
    friends_id = data["response"]["items"]
    friends = []
    for friend_data in tqdm(friends_id):
        user = User.from_dict(friend_data)
        user.count = count_friends(user.id)
        friends.append(user)
    return friends


def count_friends(user_id: int) -> Dict:
    data = send_query(user_id)
    return 0 if "error" in data else data["response"]["count"]


if __name__ == "__main__":
    args = parser.parse_args()
    if args.auth:
        print("Open this link into your browser")
        print(AUTH_QUERY)
        print("And enter your access_token")
        TOKEN = input("Access_token: ")
    friends = find_friends(args.user_id)
    print(*sorted(friends, key=lambda f: f.count, reverse=True), sep="\n")
