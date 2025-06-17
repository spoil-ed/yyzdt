from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db import IntegrityError
from core.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from hospital.models import Hospital, DrugAdmin, Patient, Doctor
import re

def login(request):


    # 如果用户已经登录，重定向到仪表盘页面
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        # 获取表单中的用户名和密码
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username='shenjingbing')
            print("User exists:", user)
        except User.DoesNotExist:
            print("User does not exist")

        errors = []
        # 检查用户名和密码是否为空
        if not username:
            errors.append("用户名不能为空")
        if not password:
            errors.append("密码不能为空")

        if errors:
            # 如果有错误信息，将错误信息添加到消息框架中
            for err in errors:
                messages.error(request, err)
            return render(request, 'login.html')

        # 验证用户信息
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                # 如果用户存在且账户激活，进行登录操作
                auth_login(request, user)
                messages.success(request, "登录成功！")
                return redirect('core:index')
            else:
                # 如果用户账户未激活，显示错误信息
                messages.error(request, "账户未激活，请联系管理员。")
        else:
            # 如果用户信息验证失败，显示错误信息
            print("用户名或密码错误")
            messages.error(request, "用户名或密码错误，请重试。")

    # 处理 GET 请求，渲染登录页面
    return render(request, 'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    VALID_ROLES = dict(User.ROLE_CHOICES).keys()
    hospitals = Hospital.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        name = request.POST.get('name').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'patient')
        
        errors = []
        if not username:
            errors.append("用户名不能为空")
        if not re.match(r'^[a-zA-Z0-9_@+-]+$', username):
            errors.append("用户名只能包含字母、数字和@/./+/-/_")
        if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append("请输入有效邮箱")
        if not password or len(password) < 8:
            errors.append("密码至少8位")
        if password != confirm_password:
            errors.append("两次密码不一致")
        if role not in VALID_ROLES:
            errors.append("无效角色选择")
        
        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'register.html', {'hospitals': hospitals, 'roles': dict(User.ROLE_CHOICES)})
            
        user = None  # 初始化 user 变量
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                role=role
            )
            
            if role == 'doctor':
                hospital_id = request.POST.get('doctor_hospital')
                title = request.POST.get('title')
                contact = request.POST.get('doctor_contact')
                
                if not hospital_id:
                    raise ValueError("医生必须选择医院")
                
                hospital = get_object_or_404(Hospital, id=hospital_id)
                
                Doctor.objects.create(
                    user=user,
                    hospital=hospital,
                    title=title,
                    contact=contact
                )

            elif role == 'drug_admin':
                hospital_id = request.POST.get('admin_hospital')
                employee_id = request.POST.get('admin_id')

                if not hospital_id or not employee_id:
                    raise ValueError("药品管理员必须选择医院和员工编号")
                
                hospital = get_object_or_404(Hospital, id=hospital_id)
                DrugAdmin.objects.create(
                    user=user,
                    name=name,
                    hospital=hospital,
                    employee_id=employee_id,
                )

            elif role == 'patient':
                gender = request.POST.get('gender')
                birth_date = request.POST.get('birth_date')
                contact = request.POST.get('patient_contact')
                address = request.POST.get('patient_address')
                
                if not gender:
                    raise ValueError("患者必须选择性别")
                
                gender_value = 'M' if gender == 'male' else 'F'
                Patient.objects.create(
                    user=user,
                    name=name,
                    gender=gender_value,
                    birth=birth_date,
                    contact=contact,
                    address=address
                )
            
            messages.success(request, "注册成功！请登录")
            return redirect('core:login')
            
        except IntegrityError as e:
            msg = "用户名已存在" if 'username' in str(e).lower() else "邮箱已注册"
            messages.error(request, msg)
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
        except (ValueError, Hospital.DoesNotExist) as e:
            messages.error(request, str(e))
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
        except Exception as e:
            print(e)
            messages.error(request, "注册过程中发生错误，请稍后再试")
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
        
        return render(request, 'register.html', {'hospitals': hospitals, 'roles': dict(User.ROLE_CHOICES)})
    
    return render(request, 'register.html', {'hospitals': hospitals, 'roles': dict(User.ROLE_CHOICES)})

def logout(request):
    # 执行登出操作
    auth_logout(request)
    messages.success(request, "您已成功登出！")
    return redirect('core:login')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

def user_create(request):
    return HttpResponse("User create page")

def user_update(request, pk):
    return HttpResponse(f"User update page for user {pk}")

def user_detail(request, pk):
    return HttpResponse(f"User detail page for user {pk}")

def index(request):
    return render(request, 'index.html', {'user': request.user})

def government_data(request):
    return HttpResponse("Government data page")

def government_report(request):
    return HttpResponse("Personal data page")