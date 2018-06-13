from django.contrib import messages, auth
from django.contrib.auth import authenticate, hashers
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View, TemplateView

from apps.myuser.forms import LoginForm, RegisterForm
from apps.myuser.models import UserProfile, EmailValiRecord
from custmethods.send_email import SendEmail


class CustomBackend(ModelBackend):
    """
    自定义用户登录验证：支持用户名或邮箱登录。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class HomePageView(TemplateView):
    """
    基于通用类视图的首页(首次登陆)
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['flag'] = None
        return context


class IndexView(TemplateView):
    """
    基于通用类视图的首页(重定向后)
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['username'] = username
        context['succ_msg'] = succ_msg
        return context


class LoginView(View):
    """
    基于通用类视图的登录验证
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        global username, succ_msg

        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get('username', None)
            password = form_data.cleaned_data.get('password', None)

            userobj = authenticate(username=username, password=password)
            if userobj is not None:
                if userobj.is_active:
                    auth.login(request, userobj)
                    succ_msg = '欢迎，登录成功！'
                    request.session['username'] = username
                    request.session['succ_msg'] = succ_msg
                    return redirect(reverse('index'), username=username, succ_msg=succ_msg)
                else:
                    messages.error(request, '用户名未激活！')
                    return render(request, 'login.html', locals())
            else:
                messages.error(request, '用户名或密码不正确！')
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', context={'form_data': form_data})


class LogoutView(View):
    """
    退出
    """

    def get(self, request):
        auth.logout(request)
        return redirect(reverse('home'))


class RegisterView(View):
    """
    注册用户
    """

    def get(self, request):
        reg_form = RegisterForm()
        return render(request, template_name='register.html', context={'reg_form': reg_form})

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            email = reg_form.cleaned_data.get('email', '')
            if UserProfile.objects.filter(email=email):
                messages.error(request, '用户名已存在！')
                return render(request, 'register.html', {'reg_form': reg_form})
            password = reg_form.cleaned_data.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = hashers.make_password(password=password)  # 没有加盐
            user_profile.is_active = 0      # 还未邮箱验证，所以设为未激活0

            # 发送注册邮件
            send_email = SendEmail(email, send_type='register')
            send_status = send_email.send_acti_email()
            if send_status:
                user_profile.save()
                reg_msg = 'OK！邮件已发送，请登录您的邮箱按提示激活。。'
                return render(request, 'register.html', {'send_status': send_status, 'reg_msg': reg_msg})
            else:
                return render(request, 'register.html', {'reg_form': reg_form})
        else:
            return render(request, 'register.html', {'reg_form': reg_form})


class ActivateView(View):
    """
    邮箱验证
    """

    def get(self, request, activate_reg_code):
        email_vali = EmailValiRecord.objects.filter(code=activate_reg_code).last()
        if email_vali:
            email = email_vali.email
            user = UserProfile.objects.get(email=email)
            user.is_active = 1
            user.save()

            return HttpResponse('<h1>✔激活成功☞<a href="http://127.0.0.1:8000/user/login" %}">返回登录页面</a></h1>')
        else:
            return HttpResponse('<h1>✘激活失败</h1>')



# ******************************************************************************************* #


# def index(request):
#     """
#     首页视图
#     :param request:
#     :return:
#     """
#     username = request.session.get('username', None)
#     succ_msg = request.session.get('succ_msg', None)
#     return render(request, 'index.html', context={'username': username, 'succ_msg': succ_msg})
#
#
# def user_login(request):
#     """
#     用户登录视图
#     :param request:
#     :return:
#     """
#     global username, succ_msg
#
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         userobj = authenticate(username=username, password=password)
#         if userobj is not None:
#             login(request, userobj)
#             succ_msg = '欢迎，登录成功！'
#             request.session['username'] = username
#             request.session['succ_msg'] = succ_msg
#             return redirect(reverse('index'), username=username, succ_msg=succ_msg)
#         else:
#             messages.error(request, '用户名或密码不正确！')
#             return render(request, 'login.html', locals())
#
#     elif request.method == 'GET':
#         return render(request, 'login.html')
