from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from hospital.models import Hospital
from supply.decorators import role_required
from .models import Drug, Inventory, Pharma, PharmaDrugSupply

@login_required
@role_required(['system_admin'])
# 药企管理视图
def pharma_list(request):
    pharmas = Pharma.objects.all()
    return render(request, 'supply/pharma_list.html', {'pharmas': pharmas})

@login_required
@role_required(['system_admin'])
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
@role_required(['system_admin'])
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
@role_required(['system_admin'])
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
@role_required(['system_admin', 'pharma_admin'])
def pharma_drug_supply(request):
    # 获取当前用户
    user = request.user
    
    # 筛选条件处理
    pharma_id = request.GET.get('pharma')
    drug_id = request.GET.get('drug')
    is_primary_supplier = request.GET.get('is_primary_supplier')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-create_time')
    
    # 获取所有供应关系
    queryset = PharmaDrugSupply.objects.select_related('pharma', 'drug').all()
    
    # 筛选：根据药企
    if pharma_id:
        queryset = queryset.filter(pharma_id=pharma_id)
    
    # 筛选：根据药品
    if drug_id:
        queryset = queryset.filter(drug_id=drug_id)
    
    # 筛选：根据是否为主要供应商
    if is_primary_supplier in ['True', 'False']:
        queryset = queryset.filter(is_primary_supplier=(is_primary_supplier == 'True'))
    
    # 筛选：根据供应开始日期范围
    if start_date and end_date:
        queryset = queryset.filter(supply_start_date__range=[start_date, end_date])
    elif start_date:
        queryset = queryset.filter(supply_start_date__gte=start_date)
    elif end_date:
        queryset = queryset.filter(supply_start_date__lte=end_date)
    
    # 排序
    queryset = queryset.order_by(ordering)
    
    
    # 分页处理
    paginator = Paginator(queryset, 10)  # 每页显示10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取药企和药品列表，用于筛选下拉框
    pharma_list = Pharma.objects.all()
    drug_list = Drug.objects.all()
    
    # 准备上下文数据
    context = {
        'pharma_drug_supplies': page_obj,
        'pharma_list': pharma_list,
        'drug_list': drug_list,
        # 'current_supply_count': current_supply_count,
        # 'primary_supplier_count': primary_supplier_count,
        # 'upcoming_expiry_count': upcoming_expiry_count,
        # 'today_new_count': today_new_count,
        'request': request  # 用于在模板中访问GET参数
    }
    
    return render(request, 'supply/pharma_drug_supply.html', context)


@require_POST
@role_required(['system_admin', 'pharma_admin'])
def pharma_drug_supply_delete(request, pk):
    """删除药企药品供应关系"""
    try:
        # 获取要删除的供应关系对象
        supply = get_object_or_404(PharmaDrugSupply, id=pk)
        
        # 执行删除操作
        supply.delete()
        
        # 返回成功响应
        return JsonResponse({
            'success': True,
            'message': '供应关系已成功删除'
        })
    except Exception as e:
        # 返回错误响应
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@role_required(['system_admin', 'pharma_admin'])
def pharma_drug_supply_create(request):
    if request.method == 'POST':
        # 获取表单数据
        pharma_id = request.POST.get('pharma')
        drug_id = request.POST.get('drug')
        supply_start_date = request.POST.get('supply_start_date')
        supply_end_date = request.POST.get('supply_end_date')
        is_primary_supplier = request.POST.get('is_primary_supplier') == 'on'
        certification_number = request.POST.get('certification_number')
        remark = request.POST.get('remark')

        try:
            # 获取药企和药品实例
            pharma = Pharma.objects.get(id=pharma_id)
            drug = Drug.objects.get(id=drug_id)

            # 创建新的药企药品供应关系实例
            supply = PharmaDrugSupply(
                pharma=pharma,
                drug=drug,
                supply_start_date=supply_start_date,
                supply_end_date=supply_end_date or None,
                is_primary_supplier=is_primary_supplier,
                certification_number=certification_number or None,
                remark=remark or None
            )

            # 保存实例
            supply.save()

            # 显示成功消息
            messages.success(request, '药企药品供应关系创建成功！')

            # 重定向到供应列表页面（你可以根据实际情况修改重定向的 URL）
            return redirect('supply:pharma_drug_supply')

        except (Pharma.DoesNotExist, Drug.DoesNotExist):
            # 显示错误消息
            messages.error(request, '药企或药品不存在，请重新选择。')
        except Exception as e:
            # 显示其他错误消息
            messages.error(request, f'创建失败：{str(e)}')

    # 获取药企和药品列表，用于表单下拉框
    pharma_list = Pharma.objects.all()
    drug_list = Drug.objects.all()

    # 渲染创建页面
    return render(request, 'supply/pharma_drug_supply_create.html', {
        'pharma_list': pharma_list,
        'drug_list': drug_list
    })


@login_required
@role_required(['system_admin', 'drug_admin'])
def inventory_list(request):
    # 获取当前时间相关日期范围
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)

    # 获取筛选参数
    hospital_id = request.GET.get('hospital')
    drug_name = request.GET.get('drug_name')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-last_updated')  # 默认按更新时间降序

    # 基础查询集（使用select_related减少数据库查询）
    inventories = Inventory.objects.select_related('hospital', 'drug')

    # 应用筛选条件
    if hospital_id:
        inventories = inventories.filter(hospital_id=hospital_id)

    if drug_name:
        inventories = inventories.filter(drug__name__icontains=drug_name)

    if status:
        if status == '充足':
            inventories = inventories.filter(current_quantity__gte=F('warning_threshold'))
        elif status == '低库存':
            inventories = inventories.filter(
                current_quantity__lt=F('warning_threshold'),
                current_quantity__gt=0
            )
        elif status == '缺货':
            inventories = inventories.filter(current_quantity__lte=0)

    if start_date and end_date:
        inventories = inventories.filter(last_updated__range=[start_date, end_date])
    elif start_date:
        inventories = inventories.filter(last_updated__gte=start_date)
    elif end_date:
        inventories = inventories.filter(last_updated__lte=end_date)

    # 排序
    inventories = inventories.order_by(ordering)

    # 计算统计数据（基于筛选后的数据集）
    # 本月库存总量
    this_month_inventory = inventories.filter(
        last_updated__range=[start_of_month, end_of_month]
    )
    total_inventory_this_month = this_month_inventory.aggregate(
        total=Sum('current_quantity')
    )['total'] or 0

    # 上月库存总量
    last_month_inventory = inventories.filter(
        last_updated__range=[last_month_start, last_month_end]
    )
    total_inventory_last_month = last_month_inventory.aggregate(
        total=Sum('current_quantity')
    )['total'] or 0

    # 计算库存总量同比增长率
    inventory_growth = 0
    if total_inventory_last_month > 0:
        inventory_growth = ((total_inventory_this_month - total_inventory_last_month) / total_inventory_last_month) * 100

    # 库存预警数量
    low_stock_inventories = inventories.filter(current_quantity__lte=F('warning_threshold'))
    low_stock_count = low_stock_inventories.count()

    # 库存预警比例
    total_count = inventories.count()
    low_stock_percentage = 0
    if total_count > 0:
        low_stock_percentage = (low_stock_count / total_count) * 100

    # 分页（每页显示10条记录）
    paginator = Paginator(inventories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取医院列表，用于筛选下拉框
    hospitals = Hospital.objects.all()

    context = {
        'inventories': page_obj,
        'hospitals': hospitals,
        'total_inventory_this_month': total_inventory_this_month,
        'inventory_growth': round(inventory_growth, 1),
        'low_stock_count': low_stock_count,
        'low_stock_percentage': round(low_stock_percentage, 1),
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'supply/inventory_list.html', context)


