from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from var_dump import var_dump

from InstagramAPI import InstagramAPI

from .models import User, InstagramAccount, InstagramTag, InstagramAccountSetting
from .forms import InstagramAccountForm, UserSignupForm, InstagramTagForm, InstagramAccountSettingForm
# Create your views here.


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'web/index.html', context)

def signup(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        user_signup_form = UserSignupForm(request.POST)
        if user_creation_form.is_valid() and user_signup_form.is_valid():
            base_user = user_creation_form.save()
            user = user_signup_form.save(commit=False)
            user.base_user = base_user
            user.save()
            username = user_creation_form.cleaned_data.get('username')
            raw_password = user_creation_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        user_creation_form = UserCreationForm()
        user_signup_form = UserSignupForm()
    return render(request, 'registration/signup.html', {
        'user_creation_form': user_creation_form,
        'user_signup_form': user_signup_form
    })


@login_required
def profile(request):
    form = InstagramAccountForm()
    if request.method == 'POST':
        form = InstagramAccountForm(request.POST)
        if form.is_valid():
            instagram_account = InstagramAccount.objects.filter(user__base_user=request.user,
                                                                username=request.POST['username'])
            if not instagram_account:
                user = User.objects.get(base_user=request.user)
                instagram_account = InstagramAccount(user=user,
                                                     username=form.cleaned_data['username'],
                                                     password=form.cleaned_data['password'],
                                                     is_active=form.cleaned_data['is_active'])
                instagram_account.save()

                instagram_account_settings = InstagramAccountSetting(instagram_account=instagram_account)
                instagram_account_settings.save()
            else:
                form.add_error('username', 'Current username is exist!')
    account_list = InstagramAccount.objects.filter(user__base_user=request.user)
    return render(request, 'profile/instagram_account.html', {'form': form, 'account_list': account_list})


@login_required
def add_instagram_account(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # var_dump(instagram_account.count)
    # exit()
    # api = InstagramAPI("nearpay.ir", "719235692Max")
    #
    # if api.login():
    #     api.follow(286424719)
    #
    # print(api.username_id)
    return ""


@login_required
def edit_instagram_account(request, instagram_account_id):
    try:
        instagram_account = InstagramAccount.objects.get(user__base_user=request.user, id=instagram_account_id)
    except InstagramAccount.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        instagram_account_setting_form = InstagramAccountSettingForm(request.POST,
                                                                     initial={'instagram_account': instagram_account})
        if instagram_account_setting_form.is_valid():
            instagram_account_setting = instagram_account_setting_form.save(commit=False)
            instagram_account_setting.instagram_account = instagram_account
            instagram_account_setting_form.save()
    else:
        instagram_account_setting, created = \
            InstagramAccountSetting.objects.get_or_create(instagram_account=instagram_account)

        instagram_account_setting_form = InstagramAccountSettingForm(instance=instagram_account_setting)

    tag_list = InstagramTag.objects.filter(instagram_account=instagram_account)
    instagram_tag_form = InstagramTagForm()

    return render(request, 'profile/edit_instagram_account.html', {
        'instagram_account': instagram_account,
        'tag_list': tag_list,
        'instagram_tag_form': instagram_tag_form,
        'instagram_account_setting_form': instagram_account_setting_form
    })


@login_required
def add_tag(request, instagram_account_id):
    tag_form = InstagramTagForm(request.POST)
    if tag_form.is_valid():
        try:
            instagram_account = InstagramAccount.objects.get(user__base_user=request.user, id=instagram_account_id)
        except InstagramAccount.DoesNotExist:
            raise Http404

        instagram_tag = InstagramTag.objects.filter(instagram_account=instagram_account, tag=tag_form.cleaned_data['tag'])
        if not instagram_tag:
            var_dump(tag_form.cleaned_data)
            InstagramTag.objects.create(instagram_account=instagram_account,
                                        tag=tag_form.cleaned_data['tag'],
                                        is_active=tag_form.cleaned_data['is_active'])

    return redirect(edit_instagram_account, instagram_account_id=instagram_account_id)


@login_required
def delete_instagram_account(request, instagram_account_id):
    try:
        instagram_account = InstagramAccount.objects.get(user__base_user=request.user, id=instagram_account_id)
        instagram_account.delete()
    except InstagramAccount.DoesNotExist:
        raise Http404
    return redirect(profile)
