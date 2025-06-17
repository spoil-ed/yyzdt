from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import Hospital, HospitalType, HospitalGrade, City, Doctor
from .forms import HospitalForm
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# 模拟数据库数据
hospitals = []
doctors = []
drug_admins = []
doctor_hospitals = []

@login_required
def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital/hospital_list.html', {'hospitals': hospitals})

@login_required
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
    grades = HospitalGrade.objects.all()
    types = HospitalType.objects.all()
    cities = City.objects.all()
    
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
def hospital_update(request, pk):
    hospital = Hospital.objects.get(pk=pk)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            messages.success(request, f'医院 {hospital.name} 更新成功')
            return redirect(reverse('hospital:hospital_list'))
        else:
            messages.error(request, '更新医院失败，请检查输入信息')
    else:
        form = HospitalForm(instance=hospital)
    
    grades = HospitalGrade.objects.all()
    types = HospitalType.objects.all()
    cities = City.objects.all()
    
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
        'form': form,
        'grades': GRADE_CHOICES,
        'types': TYPE_CHOICES,
        'cities': CITY_CHOICES,
        'hospital': hospital,
    })

@login_required
def doctor_list(request):
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_create(request):
    if request.method == 'POST':
        # 占位符：处理创建医生的逻辑
        doctor_name = request.POST.get('name')
        doctors.append({'name': doctor_name})
        return redirect(reverse('hospital:doctor_list'))
    return render(request, 'hospital/doctor_create.html')

@login_required
def doctor_update(request, pk):
    if request.method == 'POST':
        # 占位符：处理更新医生的逻辑
        doctor_name = request.POST.get('name')
        doctors[pk]['name'] = doctor_name
        return redirect(reverse('hospital:doctor_list'))
    return render(request, 'hospital/doctor_update.html', {'doctor': doctors[pk]})

@login_required
def drug_admin_list(request):
    return render(request, 'hospital/drug_admin_list.html', {'drug_admins': drug_admins})

@login_required
def drug_admin_create(request):
    if request.method == 'POST':
        # 占位符：处理创建药品管理员的逻辑
        drug_admin_name = request.POST.get('name')
        drug_admins.append({'name': drug_admin_name})
        return redirect(reverse('hospital:drug_admin_list'))
    return render(request, 'hospital/drug_admin_create.html')

@login_required
def drug_admin_update(request, pk):
    if request.method == 'POST':
        # 占位符：处理更新药品管理员的逻辑
        drug_admin_name = request.POST.get('name')
        drug_admins[pk]['name'] = drug_admin_name
        return redirect(reverse('hospital:drug_admin_list'))
    return render(request, 'hospital/drug_admin_update.html', {'drug_admin': drug_admins[pk]})

@login_required
def doctor_hospital_list(request):
    return render(request, 'hospital/doctor_hospital_list.html', {'doctor_hospitals': doctor_hospitals})

@login_required
def doctor_hospital_create(request):
    if request.method == 'POST':
        # 占位符：处理创建医生与医院关系的逻辑
        doctor_id = request.POST.get('doctor_id')
        hospital_id = request.POST.get('hospital_id')
        doctor_hospitals.append({'doctor_id': doctor_id, 'hospital_id': hospital_id})
        return redirect(reverse('hospital:doctor_hospital_list'))
    return render(request, 'hospital/doctor_hospital_create.html')