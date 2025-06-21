from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import Hospital #, HospitalType, HospitalGrade, City, Doctor
# from .forms import HospitalForm
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from hospital.decorators import role_required

# 模拟数据库数据
hospitals = []
doctors = []
drug_admins = []
doctor_hospitals = []

@login_required
@role_required(['system_admin'])
def hospital_list(request):
    # 获取筛选参数
    address = request.GET.get('address')
    name = request.GET.get('hospital_name')
    status = request.GET.get('status')

    # 基础查询集
    hospitals = Hospital.objects.all()

    if address:
        hospitals = hospitals.filter(address__icontains=address)
    if name:
        hospitals = hospitals.filter(name__icontains=name)
    if status:
        hospitals = hospitals.filter(status=status)

    # 分页（每页显示10条记录）
    if status:
        hospitals = hospitals.filter(status=status)

    # 分页（每页显示10条记录）
    paginator = Paginator(hospitals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'hospitals': page_obj,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'hospital/hospital_list.html', context)

@login_required
@role_required(['system_admin'])
def hospital_create(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        grade_id = request.POST.get('grade')
        type_id = request.POST.get('type')
        city_id = request.POST.get('city')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        description = request.POST.get('description')
        founded = request.POST.get('founded')
        
        # 验证必要字段
        if not name or not address or not contact:
            error_message = '医院名称、地址和联系电话是必填项'
            messages.error(request, error_message)
            return render(request, 'hospital/hospital_create.html', {'error': error_message})
        
        # 创建医院实例
        try:
            # grade = HospitalGrade.objects.get(id=grade_id) if grade_id else None
            # type_obj = HospitalType.objects.get(id=type_id) if type_id else None
            # city = City.objects.get(id=city_id) if city_id else None
            
            hospital = Hospital.objects.create(
                name=name,
                # grade=grade,
                # type=type_obj,
                # city=city,
                address=address,
                contact=contact,
                email=email,
                description=description,
                founded=founded
            )
            messages.success(request, f'医院 {name} 创建成功')
            return redirect(reverse('hospital:hospital_list'))
        except Exception as e:
            error_message = f'创建医院失败: {str(e)}'
            messages.error(request, error_message)
            return render(request, 'hospital/hospital_create.html', {'error': error_message})
    
    # 获取下拉菜单选项
    # grades = HospitalGrade.objects.all()
    # types = HospitalType.objects.all()
    # cities = City.objects.all()
    
    GRADE_CHOICES = [
        {'id': 1, 'name': '三级甲等'},
        {'id': 2, 'name': '三级乙等'},
        {'id': 3, 'name': '二级甲等'},
        {'id': 4, 'name': '二级乙等'},
        {'id': 5, 'name': '一级医院'},
        {'id': 6, 'name': '未定级'},
    ]
    
    TYPE_CHOICES = [
        {'id': 1, 'name': '综合医院'},
        {'id': 2, 'name': '专科医院'},
        {'id': 3, 'name': '中医医院'},
        {'id': 4, 'name': '中西医结合医院'},
        {'id': 5, 'name': '民族医院'},
        {'id': 6, 'name': '康复医院'},
        {'id': 7, 'name': '妇幼保健院'},
    ]
    
    CITY_CHOICES = [
        {'id': 1, 'name': '北京市'},
        {'id': 2, 'name': '上海市'},
        {'id': 3, 'name': '广州市'},
        {'id': 4, 'name': '深圳市'},
        {'id': 5, 'name': '杭州市'},
        {'id': 6, 'name': '南京市'},
        {'id': 7, 'name': '武汉市'},
        {'id': 8, 'name': '成都市'},
        {'id': 9, 'name': '重庆市'},
        {'id': 10, 'name': '西安市'},
    ]


    return render(request, 'hospital/hospital_create.html', {
        'grades': GRADE_CHOICES,
        'types': TYPE_CHOICES,
        'cities': CITY_CHOICES,
    })

@login_required
@role_required(['system_admin'])
def hospital_detail(request, pk):
    """医院详情视图"""
    hospital = get_object_or_404(Hospital, pk=pk)
    # 获取医院药品库存统计
    # hospital_inventories = hospital.inventory_set.all()
    # 获取合作药企
    # partner_pharmas = hospital.pharmas.all()
    
    return render(request, 'hospital/hospital_detail.html', {
        'hospital': hospital,
        # 'hospital_inventories': hospital_inventories,
        # 'partner_pharmas': partner_pharmas
    })

@login_required
@role_required(['system_admin'])
def hospital_update(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        grade_id = request.POST.get('grade')
        type_id = request.POST.get('type')
        city_id = request.POST.get('city')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        description = request.POST.get('description')
        founded = request.POST.get('founded')
        
        # 验证必要字段
        if not name or not address or not contact:
            error_message = '医院名称、地址和联系电话是必填项'
            messages.error(request, error_message)
            return render(request, 'hospital/hospital_update.html', {
                'hospital': hospital,
                'error': error_message
            })
        
        # 更新医院实例
        try:
            # 获取外键关联对象
            # grade = HospitalGrade.objects.get(id=grade_id) if grade_id else None
            # type_obj = HospitalType.objects.get(id=type_id) if type_id else None
            # city = City.objects.get(id=city_id) if city_id else None
            
            # 更新医院对象字段
            hospital.name = name
            # hospital.grade = grade
            # hospital.type = type_obj
            # hospital.city = city
            hospital.address = address
            hospital.contact = contact
            hospital.email = email
            hospital.description = description
            hospital.founded = founded
            
            # 保存更新
            hospital.save()
            
            messages.success(request, f'医院 {name} 更新成功')
            return redirect(reverse('hospital:hospital_list'))
        except Exception as e:
            error_message = f'更新医院失败: {str(e)}'
            messages.error(request, error_message)
            return render(request, 'hospital/hospital_update.html', {
                'hospital': hospital,
                'error': error_message
            })
    
    # 准备下拉菜单选项
    GRADE_CHOICES = [
        {'id': 1, 'name': '三级甲等'},
        {'id': 2, 'name': '三级乙等'},
        {'id': 3, 'name': '二级甲等'},
        {'id': 4, 'name': '二级乙等'},
        {'id': 5, 'name': '一级医院'},
        {'id': 6, 'name': '未定级'},
    ]
    
    TYPE_CHOICES = [
        {'id': 1, 'name': '综合医院'},
        {'id': 2, 'name': '专科医院'},
        {'id': 3, 'name': '中医医院'},
        {'id': 4, 'name': '中西医结合医院'},
        {'id': 5, 'name': '民族医院'},
        {'id': 6, 'name': '康复医院'},
        {'id': 7, 'name': '妇幼保健院'},
    ]
    
    CITY_CHOICES = [
        {'id': 1, 'name': '北京市'},
        {'id': 2, 'name': '上海市'},
        {'id': 3, 'name': '广州市'},
        {'id': 4, 'name': '深圳市'},
        {'id': 5, 'name': '杭州市'},
        {'id': 6, 'name': '南京市'},
        {'id': 7, 'name': '武汉市'},
        {'id': 8, 'name': '成都市'},
        {'id': 9, 'name': '重庆市'},
        {'id': 10, 'name': '西安市'},
    ]

    return render(request, 'hospital/hospital_update.html', {
        'grades': GRADE_CHOICES,
        'types': TYPE_CHOICES,
        'cities': CITY_CHOICES,
        'hospital': hospital,
    })
