import logging
from random import sample
import api
import configparser
import redis

"""create redis storage to save session tokens for user activity"""
r = redis.Redis(host='localhost', port=6379, db=0)

"""Create user parser"""
config = configparser.ConfigParser()
config.read('bot.ini')

"""parse user config"""
number_of_users = int(config.get('bot config', 'number_of_users'))
max_posts_per_user = int(config.get('bot config', 'max_posts_per_user'))
max_likes_per_user = int(config.get('bot config', 'max_likes_per_user'))
users_list_file = config.get('users list', 'user_list')


"""create api parser"""
api_config = configparser.ConfigParser()
api_config.read('api.ini')
"""parse api config"""
api_url = api_config.get('API', 'api_url')


logging.basicConfig(filename='bot.log', datefmt="%Y-%m-%d-%H-%M-%S",
                    level=logging.DEBUG)

def main():
    bot = api.Bot(
        api_url,
        number_of_users,
        max_posts_per_user,
        users_list_file)
    # parse emails to get user name from it
    emails = bot.parse_users()
    for email in sample(emails, number_of_users):
        # get access token for next activity
        credentials = bot.signup(email)
        if credentials:
            access_t = credentials[2]
            r.mset({credentials[0]: credentials[2]})
            if access_t:
                # create post
                bot.post_create(access_t)
    # get all post list to randomly like it
    posts = bot.get_all_post()
    #for each user saved in redis storage, like post according to max_likes_per_user
    for key in r.keys():
        user_access_t = r.get(key).decode('utf-8')
        for post in sample(posts, max_likes_per_user):
            bot.like_posts(post, user_access_t)
            print(f'Post with ID %s liked' % post)
            r.delete(key)


if __name__ == '__main__':
    main()