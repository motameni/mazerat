from __future__ import absolute_import, unicode_literals
import os
from celery import task


@task
def check():
    os.path.abspath("..")
    from site.web.models import InstagramAccount
    accounts = InstagramAccount.objects.all()
    usernames = [account.username for account in accounts]
    print(usernames)

    # instagram_accounts = InstagramAccount.objects.get()
    # for instagram_account in instagram_accounts:
    #     print(instagram_account.is_active)

