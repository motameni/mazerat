from django.db import models
from django.contrib.auth.models import User as BaseUser

# Create your models here.


class User(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    mobile = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.email

    def is_mobile_valid(self):
        return self.mobile == self.mobile


class InstagramAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    username_id = models.CharField(max_length=100, null=True)
    uuid = models.CharField(max_length=100, null=True)
    rank_token = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=200, null=True)
    is_logged_in = models.BooleanField(default=False)

    def get_instagram_account_setting(self):
        instagram_account_setting, created = InstagramAccountSetting.objects.get_or_create(instagram_account=self)
        return instagram_account_setting


class InstagramFavoriteAccount(models.Model):
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class InstagramFollowedAccount(models.Model):
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    is_followed = models.BooleanField()
    is_following = models.BooleanField()
    is_public = models.BooleanField()


class InstagramTag(models.Model):
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


class InstagramAccountSetting(models.Model):
    instagram_account = models.OneToOneField(InstagramAccount, on_delete=models.CASCADE, primary_key=True)
    start_at_h = models.IntegerField(default=9)
    start_at_m = models.IntegerField(default=0)
    end_at_h = models.IntegerField(default=23)
    end_at_m = models.IntegerField(default=59)
    like_per_day = models.IntegerField(default=1000)
    media_min_like = models.IntegerField(default=0)
    media_max_like = models.IntegerField(default=0)
    follow_per_day = models.IntegerField(default=0)
    follow_time = models.IntegerField(default=5 * 60 * 60)
    user_min_follow = models.IntegerField(default=0)
    user_max_follow = models.IntegerField(default=0)
    follow_time_enabled = models.BooleanField(default=True)
    unfollow_per_day = models.IntegerField(default=0)
    unfollow_recent_feed = models.BooleanField(default=True)
    unlike_per_day = models.IntegerField(default=0)
    time_till_unlike = models.IntegerField(default=3 * 24 * 60 * 60)
    comments_per_day = models.IntegerField(default=0)
    comment_list = models.CharField(max_length=5000, default="[['like']]")
    tag_list = models.CharField(max_length=2000, default="['f4f']")
    tag_blacklist = models.CharField(max_length=2000, default="[]")
    user_blacklist = models.CharField(max_length=2000, default="{}")
    max_like_for_one_tag = models.IntegerField(default=5)
    unfollow_break_min = models.IntegerField(default=15)
    unfollow_break_max = models.IntegerField(default=30)

    process_id = models.IntegerField(default=0)


