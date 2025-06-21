import re
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from core.decorators import role_required
from core.models import User
from hospital.models import Doctor, DrugAdmin, Hospital, Patient
from supply.models import Pharma


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
    pharmas = Pharma.objects.all()
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
            print("用户名不能为空")
        if not re.match(r'^[a-zA-Z0-9_@+-]+$', username):
            print("用户名只能包含字母、数字和@/./+/-/_")
            errors.append("用户名只能包含字母、数字和@/./+/-/_")
        if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            print("请输入有效邮箱")
            errors.append("请输入有效邮箱")
        if not password or len(password) < 8:
            print("密码至少8位")
            errors.append("密码至少8位")
        if password != confirm_password:
            print("两次密码不一致")
            errors.append("两次密码不一致")
        if role not in VALID_ROLES:
            print("无效角色选择")
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
            print("User created:", user)
            
            if role == 'doctor':
                hospital_id = request.POST.get('hospital')
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

            print("User created successfully:", user)
            messages.success(request, "注册成功！请登录")
            return redirect('core:login')
            
        except IntegrityError as e:
            msg = "用户名已存在" if 'username' in str(e).lower() else "邮箱已注册"
            messages.error(request, msg)
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
            print("用户名已存在")
        except (ValueError, Hospital.DoesNotExist) as e:
            messages.error(request, str(e))
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
        except Exception as e:
            messages.error(request, "注册过程中发生错误，请稍后再试")
            if user:  # 检查 user 变量是否已经被赋值
                user.delete()
            print("注册过程中发生错误:", 2)
        
        return render(request, 'register.html', {'hospitals': hospitals, 'roles': dict(User.ROLE_CHOICES), 'pharmas': pharmas})
    
    return render(request, 'register.html', {'hospitals': hospitals, 'roles': dict(User.ROLE_CHOICES), 'pharmas': pharmas})

def logout(request):
    # 执行登出操作
    auth_logout(request)
    messages.success(request, "您已成功登出！")
    return redirect('core:login')

@login_required
@role_required(['system_admin'])
def user_list(request):
    # 获取当前时间相关日期范围
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)

    # 获取筛选参数
    username = request.GET.get('username')
    name = request.GET.get('name')
    role = request.GET.get('role')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-date_joined')  # 默认按注册时间降序

    # 基础查询集
    users = User.objects.all()

    # 应用筛选条件
    if username:
        users = users.filter(username__icontains=username)

    if name:
        # 假设姓名存储在 UserProfile 模型中
        users = users.filter(userprofile__name__icontains=name)

    if role:
        # 假设角色存储在 UserProfile 模型中
        users = users.filter(userprofile__role=role)

    if status:
        if status == 'active':
            users = users.filter(is_active=True)
        elif status == 'inactive':
            users = users.filter(is_active=False)

    if start_date and end_date:
        users = users.filter(date_joined__range=[start_date, end_date])
    elif start_date:
        users = users.filter(date_joined__gte=start_date)
    elif end_date:
        users = users.filter(date_joined__lte=end_date)

    # 排序
    users = users.order_by(ordering)

    # 计算统计数据（基于筛选后的数据集）
    # 本月新增用户数量
    this_month_users = users.filter(
        date_joined__range=[start_of_month, end_of_month]
    )
    user_count = this_month_users.count()

    # 上月新增用户数量
    last_month_users = users.filter(
        date_joined__range=[last_month_start, last_month_end]
    )
    last_user_count = last_month_users.count()

    # 计算用户数量同比增长率
    user_count_growth = 0
    if last_user_count > 0:
        user_count_growth = ((user_count - last_user_count) / last_user_count) * 100

    # 活跃用户数量
    active_users = users.filter(is_active=True).count()

    # 不同角色的用户数量
    role_counts = users.values('role').annotate(count=Count('id'))

    # 分页（每页显示10条记录）
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'user_count': user_count,
        'user_count_growth': round(user_count_growth, 1),
        'active_users': active_users,
        'role_counts': role_counts,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'core/user_list.html', context)

def index(request):
    return render(request, 'index.html', {'user': request.user})

def permission_denied(request, exception=None):
    return render(request, '403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)