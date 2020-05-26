# Automated bot <br />  

Object of this bot demonstrate functionalities of Social Network API according to defined rules.<br />  

**Requirements and used technologies:**<br /> 
1. **requests**<br />
2. **redis**- for storing tokens during bot activity<br />
3. **secrets** - for generating random passwords<br />
4. **configparser** - for parsing data from config files<br />

## Basic Features:
1. Bot are reading rules from config file ```bot.ini```:<br />

Example config:<br />

```[bot config]```<br />
```number_of_users=4```<br />
```max_posts_per_user=10```<br />
```max_likes_per_user=3```<br />

```[users list]```<br />
```user_list=users.txt```<br />

2. According to example config and ```users.txt``` file, Bot will sign up for each user (no mre then ```number_of_users``` parameter).
3. Create random number of posts (no more then ```max_posts_per_user``` parameter)
4. After all posts will be created, Bot will get total amount of posts (list) and using parameter ```max_likes_per_user``` will randomly like posts from list.


