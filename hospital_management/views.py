from django.shortcuts import render, redirect, HttpResponse
from hospital.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hospital.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                 return redirect('admin_home')
            elif user_type == '2':
                 return redirect('doctor_home')
            elif user_type == '3':
                return redirect('userhome')
            
            
        else:
                messages.error(request,'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Email or Password is not valid')
            return redirect('login')


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request, 'profile.html',context)
@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic:
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except CustomUser.DoesNotExist:
            messages.error(request, "User not found")
        except Exception as e:
            messages.error(request, f"Profile update failed: {str(e)}")
    return render(request, 'profile.html')

@login_required(login_url='/')
def CHANGE_PASSWORD(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    context["data"] = user  # Chỉnh sửa cú pháp sai `context["data"]:data` thành `context["data"] = data`

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        check = user.check_password(current)

        if check:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password changed successfully!')
            login(request, user)  # Đăng nhập lại sau khi thay đổi mật khẩu
            return redirect('profile')  # Redirect về trang profile sau khi thay đổi mật khẩu
        else:
            messages.error(request, 'Current Password is wrong!!!')
            return redirect("change_password")

    return render(request, 'change-password.html', context)