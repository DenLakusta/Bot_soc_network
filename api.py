import random
import requests
import logging
import secrets
import string


logging.basicConfig(filename='bot.log', datefmt="%Y-%m-%d-%H-%M-%S",
                    level=logging.DEBUG)
class Bot:

    def __init__(self, api_url, number_of_users, max_posts_per_user, user_file_path):
        self.api_url = api_url
        self.number_of_users = number_of_users
        self.user_file_path = user_file_path
        self.max_posts_per_user = max_posts_per_user
        self.random_str_generator = string.ascii_letters + string.digits


    """Parse file with users email for signup metgod"""

    def parse_users(self):
        if self.user_file_path:
            with open(self.user_file_path, 'r') as f:
                email_list = f.read().splitlines()
        return email_list

    """Create new user using email list from config and get jwt token"""

    def signup(self, email):
        if email:
            url = f'{self.api_url}users/signup/'
            username = email.split('@')[0]
            password = ''.join(secrets.choice(self.random_str_generator) for i in range(20))
            try:
                r = requests.post(url, {'username': username, 'password': password, 'email': email})
                print(r.text)
            except requests.exceptions.RequestException as e:
                logging.exception('Not successful - %s' % str(e))
                raise SystemExit(e)
            if r.status_code == 201:
                access_t = r.json().get('tokens').get('access')
                return username,password,access_t
            elif r.json()['username'][0] == 'Email already exists.':
                logging.info('Not successful - %s' % r.json())
                return None
            else:
                logging.info('Response - %s' % r.json())
        logging.info('Not successful - all fields are required for registration.')
        return


    """Create post using recieved jwt token of user"""

    def post_create(self, access_token):
        url = f'{self.api_url}posts/post/create/'
        for post in range(random.randint(1, self.max_posts_per_user)):
            r = requests.post(url,
                              {'title': ''.join(secrets.choice(self.random_str_generator) for i in range(40)),
                               'body': ''.join(secrets.choice(self.random_str_generator) for i in range(100))},
                              headers={
                                  'Authorization': f'JWT {access_token}'})
            user_id = r.json().get('user_id')
            if r.status_code == 201:
                logging.info('Post created by user id - %s' % user_id)
            logging.info('Response - %s' % r.json())
        return None


    """get a list of all existing posts for like_posts method"""

    def get_all_post(self):
        url = f'{self.api_url}posts/posts/'
        r = requests.get(url)
        posts = []
        if r.status_code == 200:
            for post in r.json():
                post_id = post.get('id')
                posts.append(post_id)
        return posts


    """like posts from the posts list"""

    def like_posts(self, post_id, access_token):
        url = f'{self.api_url}likes/like/{post_id}/'
        r = requests.get(url, {'id': post_id}, headers={
            'Authorization': f'JWT {access_token}'})
        if r.status_code == 200:
            print(r)
        return None

