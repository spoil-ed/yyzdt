from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import Pharma, Supply, Inventory, WarningLog, PharmaGrade, PharmaType, PharmaDrugSupply, City, Drug  # 假设这些模型已定义
from hospital.models import Hospital  # 假设这些模型已定义
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# 模拟数据库数据（实际应用中应从数据库获取）
pharmas_data = [
    {'id': 1, 'name': '国药控股', 'phone': '010-12345678', 'address': '北京市朝阳区', 'description': '大型医药企业'},
    {'id': 2, 'name': '上海医药', 'phone': '021-87654321', 'address': '上海市浦东新区', 'description': '知名药企'},
]

supplies_data = [
    {'batch_code': 'SP2023001', 'drug_name': '阿司匹林', 'pharma_id': 1, 'quantity': 1000, 'price': 10.5, 'status': 'available', 'expiry_date': '2025-12-31', 'created_at': '2023-01-01', 'updated_at': '2023-01-01'},
    {'batch_code': 'SP2023002', 'drug_name': '布洛芬', 'pharma_id': 2, 'quantity': 500, 'price': 15.8, 'status': 'limited', 'expiry_date': '2024-11-15', 'created_at': '2023-01-10', 'updated_at': '2023-01-15'},
]

inventories_data = [
    {'id': 1, 'drug_id': 1, 'drug_name': '阿司匹林', 'hospital_id': 1, 'hospital_name': '北京协和医院', 'quantity': 200, 'warning_threshold': 50, 'status': 'normal'},
    {'id': 2, 'drug_id': 2, 'drug_name': '布洛芬', 'hospital_id': 1, 'hospital_name': '北京协和医院', 'quantity': 30, 'warning_threshold': 50, 'status': 'warning'},
]

warning_logs_data = [
    {'id': 1, 'drug_id': 2, 'drug_name': '布洛芬', 'hospital_id': 1, 'hospital_name': '北京协和医院', 'quantity': 30, 'warning_threshold': 50, 'created_at': '2023-05-10', 'status': 'pending'},
]

@login_required
# 药企管理视图
def pharma_list(request):
    # 实际应用中应从数据库获取：Pharmas.objects.all()
    pharmas = Pharma.objects.all()
    return render(request, 'supply/pharma_list.html', {'pharmas': pharmas})

@login_required
def pharma_create(request):
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
        business = request.POST.getlist('business[]')
        phone = request.POST.get('phone')
        # 验证必要字段
        if not name or not address or not contact:
            error_message = '药企名称、地址和联系电话是必填项'
            messages.error(request, error_message)
            return render(request, 'supply/pharma_create.html', {'error': error_message})

        try:
            # grade = PharmaGrade.objects.get(id=grade_id) if grade_id else None
            # type_obj = PharmaType.objects.get(id=type_id) if type_id else None
            # city = City.objects.get(id=city_id) if city_id else None

            # 创建药企实例
            pharma = Pharma.objects.create(
                name=name,
                phone=phone,
                address=address,
                description=description,
                status='待审核',  # 默认状态
                founded=None,  # 成立日期可以留空
                contact=contact,
                email=email,
                updated_at=None,  # 更新时间可以留空
                # business=', '.join(business)  # 保存业务范围
            )
            

            messages.success(request, f'药企 {name} 创建成功')
            return redirect(reverse('supply:pharma_list'))
        except Exception as e:
            error_message = f'创建药企失败: {str(e)}'
            messages.error(request, error_message)
            return render(request, 'supply/pharma_create.html', {'error': error_message})

    # 获取下拉菜单选项
    # grades = PharmaGrade.objects.all()
    # types = PharmaType.objects.all()
    # cities = City.objects.all()

    GRADE_CHOICES = [
        {'id': 1, 'name': 'AAA级（优秀）'},
        {'id': 2, 'name': 'AA级（良好）'},
        {'id': 3, 'name': 'A级（一般）'},
        {'id': 4, 'name': 'B级（较差）'},
        {'id': 5, 'name': 'C级（差）'}
    ]
    
    TYPE_CHOICES = [
        {'id': 1, 'name': '化学制药企业'},
        {'id': 2, 'name': '生物制药企业'},
        {'id': 3, 'name': '中药制药企业'},
        {'id': 4, 'name': '医药研发外包企业'},
        {'id': 5, 'name': '医药流通企业'},
        {'id': 6, 'name': '医疗器械生产企业'},
        {'id': 7, 'name': '保健品生产企业'}
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

    return render(request, 'supply/pharma_create.html', {
        'grades': GRADE_CHOICES,
        'types': TYPE_CHOICES,
        'cities': CITY_CHOICES,
    })

@login_required
def pharma_update(request, pk):
    pharma = get_object_or_404(Pharma, id=pk)
    
    if not pharma:
        return HttpResponse("药企不存在", status=404)
    
    if request.method == 'POST':
        # 实际应用中应更新数据库记录
        pharma['name'] = request.POST.get('name')
        pharma['phone'] = request.POST.get('phone')
        pharma['address'] = request.POST.get('address')
        pharma['description'] = request.POST.get('description')
        return redirect(reverse('supply:pharma_list'))
    
    return render(request, 'supply/pharma_update.html', {'pharma': pharma})

@login_required
def pharma_detail(request, pk):
    """药企详情视图"""
    pharma = get_object_or_404(Pharma, pk=pk)
    # 获取药企药品供货记录
    # pharma_supplies = pharma.supply_set.all()
    # 获取药企药品库存记录
    # pharma_inventories = pharma.inventory_set.all()
    return render(request, 'supply/pharma_detail.html', {
        'pharma': pharma,
        # 'pharma_supplies': pharma_supplies,
        # 'pharma_inventories': pharma_inventories
    })

@login_required
# 供货管理视图
def supply_list(request):
    # 实际应用中应从数据库获取：Supply.objects.all()
    supplies = supplies_data
    
    # 处理搜索过滤
    drug_name = request.GET.get('drug_name')
    pharma_id = request.GET.get('pharma')
    status = request.GET.get('status')
    
    if drug_name:
        supplies = [s for s in supplies if drug_name.lower() in s['drug_name'].lower()]
    if pharma_id:
        supplies = [s for s in supplies if str(s['pharma_id']) == pharma_id]
    if status:
        supplies = [s for s in supplies if s['status'] == status]
    
    return render(request, 'supply/supply_list.html', {'supplies': supplies, 'pharmas': pharmas_data})

@login_required
def supply_create(request):
    if request.method == 'POST':
        # 实际应用中应保存到数据库
        new_supply = {
            'batch_code': request.POST.get('batch_code'),
            'drug_name': request.POST.get('drug_name'),
            'pharma_id': int(request.POST.get('pharma')),
            'quantity': int(request.POST.get('quantity')),
            'price': float(request.POST.get('price')),
            'status': request.POST.get('status'),
            'expiry_date': request.POST.get('expiry_date'),
            'created_at': '2023-01-01',  # 实际应用中应使用当前时间
            'updated_at': '2023-01-01',  # 实际应用中应使用当前时间
            'description': request.POST.get('description')
        }
        supplies_data.append(new_supply)
        return redirect(reverse('supply:supply_list'))
    
    return render(request, 'supply/supply_create.html', {'pharmas': pharmas_data})

@login_required
def supply_detail(request, batch_code):
    # 实际应用中应从数据库获取：supply = get_object_or_404(Supply, batch_code=batch_code)
    supply = next((s for s in supplies_data if s['batch_code'] == batch_code), None)
    
    if not supply:
        return HttpResponse("供货记录不存在", status=404)
    
    # 获取药企信息
    pharma = next((p for p in pharmas_data if p['id'] == supply['pharma_id']), None)
    supply['pharma'] = pharma
    
    return render(request, 'supply/supply_detail.html', {'supply': supply})

@login_required
def pharma_drug_supply(request):
    pharma_data = None
    return render(request, 'supply/pharma_drug_supply.html', {'pharmas': pharmas_data})

@login_required
def pharma_drug_supply_create(request):
    # 获取所有药企和药品数据，用于表单选择
    pharmas = Pharma.objects.all()
    drugs = Drug.objects.all()
    
    if request.method == 'POST':
        # 处理表单提交
        pharma_id = request.POST.get('pharma')
        drug_id = request.POST.get('drug')
        start_date = request.POST.get('supply_start_date')
        end_date = request.POST.get('supply_end_date')
        is_primary = request.POST.get('is_primary_supplier') == 'on'
        cert_number = request.POST.get('certification_number')
        remark = request.POST.get('remark')
        
        # 验证必填字段
        errors = []
        if not pharma_id:
            errors.append('请选择药企')
        if not drug_id:
            errors.append('请选择药品')
        if not start_date:
            errors.append('请选择供应开始日期')
        
        # 检查药企-药品组合是否已存在
        if pharma_id and drug_id:
            if PharmaDrugSupply.objects.filter(pharma_id=pharma_id, drug_id=drug_id).exists():
                errors.append('该药企与药品的供应关系已存在')
        
        # 验证日期逻辑
        if start_date and end_date:
            try:
                if timezone.datetime.strptime(start_date, '%Y-%m-%d').date() > timezone.datetime.strptime(end_date, '%Y-%m-%d').date():
                    errors.append('供应开始日期不能晚于结束日期')
            except ValueError:
                errors.append('日期格式不正确')
        
        if errors:
            # 显示错误信息
            for error in errors:
                messages.error(request, error)
            return render(request, 'supply/pharma_drug_supply_create.html', {
                'pharmas': pharmas,
                'drugs': drugs,
                'form_data': request.POST  # 返回已填写的数据
            })
        
        # 创建新的供应关系
        try:
            supply = PharmaDrugSupply.objects.create(
                pharma_id=pharma_id,
                drug_id=drug_id,
                supply_start_date=start_date,
                supply_end_date=end_date or None,
                is_primary_supplier=is_primary,
                certification_number=cert_number,
                remark=remark
            )
            messages.success(request, f'成功创建 {supply} 的供应关系')
            return redirect('supply:pharma_drug_supply_list')  # 重定向到供应关系列表
        except Exception as e:
            messages.error(request, f'创建供应关系失败: {str(e)}')
    
    return render(request, 'supply/pharma_drug_supply_create.html', {
        'pharmas': pharmas,
        'drugs': drugs
    })

from django.db.models import Count, Sum, F, Q
from django.shortcuts import render
from .models import Inventory
from transaction.models import Purchase

@login_required
def inventory_list(request):
    # 获取用户选择的医院 ID
    selected_hospital_id = request.GET.get('hospital')

    if selected_hospital_id :
        # 如果用户选择了某个医院，筛选该医院的库存数据
        hospital = Hospital.objects.get(id=selected_hospital_id)
        inventory_list = Inventory.objects.filter(hospital=hospital)
    else:
        # 如果用户选择了“所有医院”，显示所有库存数据
        inventory_list = Inventory.objects.all()

    # 计算总药品数（总库存记录数）
    total_drugs = inventory_list.count()

    # 计算低库存药品数
    low_stock_drugs = inventory_list.filter(current_quantity__lt=F('warning_threshold')).count()

    # 计算库存预警比例
    low_stock_percentage = (low_stock_drugs / total_drugs * 100) if total_drugs > 0 else 0

    # 计算本月入库金额
    current_month = timezone.now().month
    current_year = timezone.now().year
    if selected_hospital_id:
        # 如果选择了特定医院，计算该医院本月入库金额
        total_incoming = Purchase.objects.filter(
            create_time__month=current_month,
            create_time__year=current_year,
            hospital=hospital
        ).annotate(
            total_price=F('quantity') * F('price')
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    else:
        # 如果选择所有医院，计算所有医院本月入库金额
        total_incoming = Purchase.objects.filter(
            create_time__month=current_month,
            create_time__year=current_year
        ).annotate(
            total_price=F('quantity') * F('price')
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    hospitals = Hospital.objects.all()

    return render(request, 'supply/inventory_list.html', {
        'inventory_list': inventory_list,
        'total_drugs': total_drugs,
        'low_stock_drugs': low_stock_drugs,
        'low_stock_percentage': low_stock_percentage,
        'total_incoming': total_incoming,
        'hospitals': hospitals,
        'selected_hospital': selected_hospital_id,
    })

@login_required
def inventory_update(request, drug_id, hospital_id):
    # 实际应用中应从数据库获取：inventory = get_object_or_404(Inventory, drug_id=drug_id, hospital_id=hospital_id)
    inventory = next((i for i in inventories_data if i['drug_id'] == drug_id and i['hospital_id'] == hospital_id), None)
    
    if not inventory:
        return HttpResponse("库存记录不存在", status=404)
    
    if request.method == 'POST':
        # 实际应用中应更新数据库记录
        inventory['warning_threshold'] = int(request.POST.get('warning_threshold'))
        # 根据库存数量和阈值更新状态
        if inventory['quantity'] < inventory['warning_threshold']:
            inventory['status'] = 'warning'
        else:
            inventory['status'] = 'normal'
        
        # 如果触发预警，添加预警记录
        if inventory['status'] == 'warning':
            new_warning = {
                'id': len(warning_logs_data) + 1,
                'drug_id': drug_id,
                'drug_name': inventory['drug_name'],
                'hospital_id': hospital_id,
                'hospital_name': inventory['hospital_name'],
                'quantity': inventory['quantity'],
                'warning_threshold': inventory['warning_threshold'],
                'created_at': '2023-05-10',  # 实际应用中应使用当前时间
                'status': 'pending'
            }
            warning_logs_data.append(new_warning)
        
        return redirect(reverse('supply:inventory_list'))
    
    return render(request, 'supply/inventory_update.html', {'inventory': inventory})

@login_required
# 预警日志视图
def warning_log_list(request):
    # 实际应用中应从数据库获取：WarningLog.objects.all()
    warning_logs = warning_logs_data
    return render(request, 'supply/warning_log_list.html', {'warning_logs': warning_logs})

