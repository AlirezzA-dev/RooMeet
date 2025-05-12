from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import ManualRegisterForm
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = ManualRegisterForm(request.POST)
        if form.is_valid():
            # ساخت کاربر
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            # ذخیره اطلاعات پروفایل
            profile = user.profile
            profile.mobile = form.cleaned_data['mobile']
            profile.gender = form.cleaned_data['gender']
            profile.save()

            # ورود خودکار پس از ثبت‌نام
            login(request, user)
            return redirect('accounts/dashboard.html')  # مسیر پنل یا چت روم
    else:
        form = ManualRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # اگر بخوای کد امنیتی هم بررسی شه، اینجا باید captcha رو هم بگیری
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('account/dashboard.html')  # یا chatroom یا هرجایی که می‌خوای بفرستی
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."

    return render(request, 'accounts/login.html', {'error': error})