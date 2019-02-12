from __future__ import absolute_import, unicode_literals
import os
import psutil
import sys
import signal
from celery import task
import subprocess
from multiprocessing import Process, freeze_support
from .instabotpy.src.instabot import InstaBot


try:
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mazeratsite.settings")
    django.setup()
except:
    pass
    # from django.core.wsgi import get_wsgi_application
    # application = get_wsgi_application()

# sys.path.append('..')
# from web.models import InstagramAccount


def make_insta_bot(instagram_account):
    # return 0
    return InstaBot(
        login=instagram_account.username,  # Enter username (lowercase). Do not enter email!
        password=instagram_account.password,
        like_per_day=1000,
        comments_per_day=0,
        tag_list=["follow4follow", "f4f", "cute", "l:212999109"],
        tag_blacklist=["rain", "thunderstorm"],
        user_blacklist={},
        max_like_for_one_tag=50,
        follow_per_day=300,
        follow_time=1 * 60 * 60,
        unfollow_per_day=300,
        unlike_per_day=0,
        time_till_unlike=3 * 24 * 60 * 60,  # 3 days
        unfollow_break_min=15,
        unfollow_break_max=30,
        user_max_follow=0,
        # session_file=False, # Set to False to disable persistent session, or specify custom session_file (ie ='myusername.session')
        user_min_follow=0,
        log_mod=0,
        proxy="",
        # List of list of words, each of which will be used to generate comment
        # For example: "This shot feels wow!"
        comment_list=[
            ["this", "the", "your"],
            ["photo", "picture", "pic", "shot"],
            ["is", "looks", "is 👉", "is really"],
            [
                "great",
                "super",
                "good",
                "very good",
                "good",
                "wow",
                "WOW",
                "cool",
                "GREAT",
                "magnificent",
                "magical",
                "very cool",
                "stylish",
                "beautiful",
                "so beautiful",
                "so stylish",
                "so professional",
                "lovely",
                "so lovely",
                "very lovely",
                "glorious",
                "so glorious",
                "very glorious",
                "adorable",
                "excellent",
                "amazing",
            ],
            [".", "🙌", "... 👏", "!", "! 😍", "😎"],
        ],
        # Use unwanted_username_list to block usernames containing a string
        # Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
        # 'free_followers' will be blocked because it contains 'free'
        unwanted_username_list=[
            "second",
            "stuff",
            "art",
            "project",
            "love",
            "life",
            "food",
            "blog",
            "free",
            "keren",
            "photo",
            "graphy",
            "indo",
            "travel",
            "art",
            "shop",
            "store",
            "sex",
            "toko",
            "jual",
            "online",
            "murah",
            "jam",
            "kaos",
            "case",
            "baju",
            "fashion",
            "corp",
            "tas",
            "butik",
            "grosir",
            "karpet",
            "sosis",
            "salon",
            "skin",
            "care",
            "cloth",
            "tech",
            "rental",
            "kamera",
            "beauty",
            "express",
            "kredit",
            "collection",
            "impor",
            "preloved",
            "follow",
            "follower",
            "gain",
            ".id",
            "_id",
            "bags",
        ],
        unfollow_whitelist=["example_user_1", "example_user_2"],
        # Enable the following to schedule the bot. Uses 24H
        # end_at_h = 23, # Hour you want the bot to stop
        # end_at_h = 30, # Minute you want the bot stop, in this example 23:30
        # start_at_h = 9, # Hour you want the bot to start
        # start_at_m = 10, # Minute you want the bot to start, in this example 9:10 (am).
    )


def save_process_id(instagram_account, pid):
    sys.path.append('..')
    from web.models import InstagramAccountSetting
    instagram_account_setting, created = InstagramAccountSetting.objects.get_or_create(instagram_account=instagram_account)
    instagram_account_setting.process_id = pid
    instagram_account_setting.save()


def get_process_id(instagram_account):
    sys.path.append('..')
    from web.models import InstagramAccountSetting
    instagram_account_setting, created = InstagramAccountSetting.objects\
        .get_or_create(instagram_account=instagram_account)
    return instagram_account_setting.process_id


def exist_process_id(pid):
    return psutil.pid_exists(pid)


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        print("Windows error: %s", OSError)


class Account:
    def __init__(self, instagram_account):
        self.instagram_account = instagram_account
        pid = get_process_id(instagram_account)
        if instagram_account.is_active:
            if pid == 0 or not exist_process_id(pid):
                self.start()
                print('"'+instagram_account.username+'": process is started.')
            else:
                print('"' + instagram_account.username + '": process is already exist.')
        else:
            if pid != 0 and exist_process_id(pid):
                self.stop()
                print('"' + self.instagram_account.username + '": process is stopped.')

    def start(self):
        process = Process(target=self.run, args=())
        process.daemon = True
        process.start()
        # process.join()
        save_process_id(self.instagram_account, process.pid)

    def stop(self):
        pid = get_process_id(self.instagram_account)
        kill_process(pid)
        save_process_id(self.instagram_account, 0)

    def run(self):
        bot = make_insta_bot(self.instagram_account)
        while True:
            bot.new_auto_mod()
            if not self.instagram_account.is_active:
                self.stop()
                return


@task
def change_status_of_bots():
    sys.path.append('..')
    from web.models import InstagramAccount
    accounts = InstagramAccount.objects.all()
    print([account.username for account in accounts])
    for instagram_account in accounts:
        # pass
        Account(instagram_account)

    print("instabot status changed.")

