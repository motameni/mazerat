from django import forms
from .models import \
    User,\
    InstagramAccount,\
    InstagramTag,\
    InstagramFavoriteAccount,\
    InstagramAccountSetting


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mobile']


class InstagramAccountForm(forms.ModelForm):
    class Meta:
        model = InstagramAccount
        fields = ['username', 'password', 'is_active']


class InstagramAccountSettingForm(forms.ModelForm):
    class Meta:
        model = InstagramAccountSetting
        fields = [
            'start_at_h',
            'start_at_m',
            'end_at_h',
            'end_at_m',
            'like_per_day',
            'media_min_like',
            'media_max_like',
            'follow_per_day',
            'follow_time',
            'user_min_follow',
            'user_max_follow',
            'follow_time_enabled',
            'unfollow_per_day',
            'unfollow_recent_feed',
            'unlike_per_day',
            'time_till_unlike',
            'comment_list',
            'tag_list',
            'user_blacklist',
            'max_like_for_one_tag',
            'unfollow_break_min',
            'unfollow_break_max'
        ]


class InstagramTagForm(forms.ModelForm):
    class Meta:
        model = InstagramTag
        fields = ['tag', 'is_active']
        help_texts = {
            'tag': 'Favorite tag you want to attract it\'s people',
        }


class InstagramFavoriteAccountForm(forms.ModelForm):
    class Meta:
        model = InstagramFavoriteAccount
        fields = ['username', 'is_active']
