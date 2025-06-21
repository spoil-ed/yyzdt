from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from hospital.models import Doctor, DrugAdmin, Hospital, Patient
from supply.models import Drug, Pharma
from transaction.decorators import role_required
from .models import Purchase, Sale

@login_required
@role_required(['system_admin', 'pharma_admin'])
def supply_records(request):
    # 获取当前时间相关日期范围
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    
    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)
    
    # 获取筛选参数
    hospital_id = request.GET.get('hospital')
    purchase_id = request.GET.get('purchase_id')
    drug_name = request.GET.get('drug_name')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-create_time')  # 默认按创建时间降序
    
    # 基础查询集（使用select_related减少数据库查询）
    supplies = Purchase.objects.select_related('hospital', 'drug')
    
    # 应用筛选条件
    if hospital_id:
        supplies = supplies.filter(hospital_id=hospital_id)
    
    if purchase_id:
        supplies = supplies.filter(purchase_id__icontains=purchase_id)
    
    if drug_name:
        supplies = supplies.filter(drug__name__icontains=drug_name)
    
    if status:
        # 转换为中文状态
        status_mapping = {
            'pending': '待审核',
            'approved': '已审核',
            'received': '已入库',
            'rejected': '已拒绝',
        }
        if status in status_mapping:
            supplies = supplies.filter(status=status_mapping[status])
    
    if start_date and end_date:
        supplies = supplies.filter(create_time__range=[start_date, end_date])
    elif start_date:
        supplies = supplies.filter(create_time__gte=start_date)
    elif end_date:
        supplies = supplies.filter(create_time__lte=end_date)
    
    # 月度供货数据（最近12个月）
    monthly_supplies = supplies.annotate(month=TruncMonth('create_time')).values('month').annotate(
        amount=Sum(F('quantity') * F('price'))
    ).order_by('month')[:12]

    # 按医院分组的供货数据，累积所有日期的总金额
    supplies_by_hospital = Purchase.objects.values('hospital__name').annotate(
        amount=Sum(F('quantity') * F('price'))
    )

    # 排序
    supplies = supplies.order_by(ordering)
    
    # 计算统计数据（基于筛选后的数据集）
    # 本月供货单数量
    this_month_supplies = supplies.filter(
        create_time__range=[start_of_month, end_of_month]
    )
    supply_count = this_month_supplies.count()
    
    # 上月供货单数量
    last_month_supplies = supplies.filter(
        create_time__range=[last_month_start, last_month_end]
    )
    last_supply_count = last_month_supplies.count()
    
    # 计算供货单数量同比增长率
    supply_count_growth = 0
    if last_supply_count > 0:
        supply_count_growth = ((supply_count - last_supply_count) / last_supply_count) * 100
    
    # 本月供货金额
    this_month_amount = this_month_supplies.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 上月供货金额
    last_month_amount = last_month_supplies.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 计算供货金额同比增长率
    amount_growth = 0
    if last_month_amount > 0:
        amount_growth = ((this_month_amount - last_month_amount) / last_month_amount) * 100
    
    # 待审核订单数量
    pending_orders = Purchase.objects.filter(status='待审核').count()
    
    # 合作医院数量
    total_hospitals = Purchase.objects.values('hospital').annotate(Count('hospital')).count()
    
    # 本月新增医院（假设Hospital模型有founded字段）
    new_hospitals_this_month = Hospital.objects.filter(
        founded__range=[start_of_month, end_of_month]
    ).count()

    # 分页（每页显示10条记录）
    paginator = Paginator(supplies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取医院列表，用于筛选下拉框
    hospitals = Hospital.objects.all()
    
    context = {
        'supplies': page_obj,
        'hospitals': hospitals,
        'supply_count': supply_count,
        'supply_count_growth': round(supply_count_growth, 1),
        'this_month_amount': this_month_amount,
        'amount_growth': round(amount_growth, 1),
        'pending_orders': pending_orders,
        'total_hospitals': total_hospitals,
        'new_hospitals_this_month': new_hospitals_this_month,
        'monthly_supplies': monthly_supplies,
        'supplies_by_hospital': supplies_by_hospital,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'transaction/supply_records.html', context)


@login_required
@role_required(['system_admin', 'patient'])
def drug_use_records(request):
    # 获取筛选参数
    name = request.GET.get('name', '')
    drug_name = request.GET.get('drug_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    ordering = request.GET.get('ordering', '-create_time')  # 默认按最新用药时间排序
    patient_name = request.user.name
    
    # 构建查询集
    medication_records = Sale.objects.all()
    
    # 应用筛选条件
    if drug_name:
        medication_records = medication_records.filter(drug__name__icontains=drug_name)
    
    if start_date and end_date:
        medication_records = medication_records.filter(
            create_time__range=[start_date, end_date]
        )
    
    if patient_name:
        medication_records = medication_records.filter(
            patient__name__icontains=patient_name
        )

    # 应用排序
    if ordering in ['create_time', '-create_time']:
        medication_records = medication_records.order_by(ordering)
    
    # 准备上下文数据
    context = {
        'medication_records': medication_records,
        'request': request  # 将request对象传递给模板，用于保留筛选参数
    }
    
    return render(request, 'transaction/drug_use_records.html', context)

@login_required
@role_required(['system_admin', 'drug_admin'])
def drug_list(request):
    # 获取筛选参数
    approval_number = request.GET.get('approval_number')
    drug = request.GET.get('drug_name')
    status = request.GET.get('status')

    # 基础查询集
    drugs = Drug.objects.all()

    # 应用筛选条件
    if approval_number:
        drugs = drugs.filter(approval_number__icontains=approval_number)
    if drug:
        drugs = drugs.filter(name__icontains=drug)
    if status:
        drugs = drugs.filter(status=status)


    # 分页（每页显示10条记录）
    paginator = Paginator(drugs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'drugs': page_obj,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'transaction/drug_list.html', context)

@login_required
@role_required(['system_admin', 'drug_admin'])
def drug_create(request):
    if request.method == 'POST':
        # 处理表单提交
        name = request.POST.get('name')
        spec = request.POST.get('specification')
        category = request.POST.get('category')
        expiration = request.POST.get('expiration')
        manufacturer = request.POST.get('manufacturer')
        approval_number = request.POST.get('approval_number')
        
        # 验证必填字段
        if not name:
            messages.error(request, '药品名称为必填项')
            return render(request, 'transaction/drug_create.html', {'action': '创建'})
        
        # 创建药品实例
        try:
            drug = Drug.objects.create(
                name=name,
                spec=spec,
                category=category,
                expiration=expiration or None,  # 处理空日期
                manufacturer=manufacturer,
                approval_number=approval_number or None,  # 处理空批准文号
            )
            messages.success(request, f'药品 {drug.name} 创建成功')
            return redirect('transaction:drug_list')  # 重定向到药品列表页
        except Exception as e:
            messages.error(request, f'创建药品失败: {str(e)}')
    
    # 首次加载或表单验证失败时显示表单
    return render(request, 'transaction/drug_create.html', {'action': '创建'})

@login_required
@role_required(['system_admin', 'drug_admin'])
def drug_detail(request, drug_id):
    return render(request, 'transaction/drug_detail.html', {'drug': Drug.objects.get(id=drug_id)})

@login_required
@role_required(['system_admin', 'drug_admin'])
def drug_update(request, drug_id):
    """更新药品信息的简化视图函数"""
    drug = get_object_or_404(Drug, id=drug_id)
    
    if request.method == 'POST':
        # 提取表单数据
        name = request.POST.get('name')
        spec = request.POST.get('specification')
        category = request.POST.get('category')
        expiration = request.POST.get('expiration')
        manufacturer = request.POST.get('manufacturer')
        approval_number = request.POST.get('approval_number')
        
        # 验证必填字段
        if not name:
            messages.error(request, '药品名称为必填项')
            return render(request, 'transaction/drug_update.html', {'drug': drug})
        
        # 更新药品数据
        try:
            drug.name = name
            drug.spec = spec or None
            drug.category = category or None
            drug.expiration = expiration or None
            drug.manufacturer = manufacturer or None
            drug.approval_number = approval_number or None
            drug.save()
            
            messages.success(request, f'药品 "{drug.name}" 更新成功！')
            return redirect('transaction:drug_list')  # 重定向到列表页
            
        except Exception as e:
            messages.error(request, f'更新失败: {str(e)}')
            return render(request, 'transaction/drug_update.html', {'drug': drug})
    
    # 首次加载时显示表单
    return render(request, 'transaction/drug_update.html', {'drug': drug})

@login_required
@role_required(['system_admin', 'drug_admin'])
def purchase_list(request):
    # 获取当前时间相关日期范围
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    
    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)
    if request.user.role == 'drug_admin':
        drug_admin = DrugAdmin.objects.get(user=request.user)
        hospital_id = drug_admin.hospital.id
    # 获取筛选参数
    hospital_id = request.GET.get('hospital')
    purchase_id = request.GET.get('purchase_id')
    drug_name = request.GET.get('drug_name')
    supplier_id = request.GET.get('supplier')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-create_time')  # 默认按创建时间降序
    
    # 基础查询集（使用select_related减少数据库查询）
    purchases = Purchase.objects.select_related('hospital', 'drug', 'pharma')
    
    # 应用筛选条件
    if hospital_id:
        purchases = purchases.filter(hospital_id=hospital_id)
    
    if purchase_id:
        purchases = purchases.filter(purchase_id__icontains=purchase_id)
    
    if drug_name:
        purchases = purchases.filter(drug__name__icontains=drug_name)
    
    if supplier_id:
        purchases = purchases.filter(pharma_id=supplier_id)
    
    if status:
        purchases = purchases.filter(status=status)
    
    if start_date and end_date:
        purchases = purchases.filter(create_time__range=[start_date, end_date])
    elif start_date:
        purchases = purchases.filter(create_time__gte=start_date)
    elif end_date:
        purchases = purchases.filter(create_time__lte=end_date)
    
    # 月度进货数据（最近12个月）
    monthly_purchases = purchases.annotate(month=TruncMonth('create_time')).values('month').annotate(
        amount=Sum(F('quantity') * F('price'))
    ).order_by('month')[:12]

    # 按医院分组的进货数据，累积所有日期的总金额
    purchases_by_hospital = Purchase.objects.values('hospital__name').annotate(
        amount=Sum(F('quantity') * F('price'))
    )

    # 排序
    purchases = purchases.order_by(ordering)
    
    # 计算统计数据（基于筛选后的数据集）
    # 本月进货单数量（已审核）
    this_month_orders = purchases.filter(
        create_time__range=[start_of_month, end_of_month],
        status__in=['已审核', '已入库']  # 假设已入库的订单也算在内
    )
    order_count = this_month_orders.count()
    
    # 上月进货单数量
    last_month_orders = purchases.filter(
        create_time__range=[last_month_start, last_month_end],
        status__in=['已审核', '已入库']  # 假设已入库的订单也算在内
    )
    last_order_count = last_month_orders.count()
    
    # 计算进货单数量同比增长率
    order_count_growth = 0
    if last_order_count > 0:
        order_count_growth = ((order_count - last_order_count) / last_order_count) * 100
    
    # 本月进货金额（已审核订单）
    this_month_amount = this_month_orders.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 上月进货金额
    last_month_amount = last_month_orders.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 计算进货金额同比增长率
    amount_growth = 0
    if last_month_amount > 0:
        amount_growth = ((this_month_amount - last_month_amount) / last_month_amount) * 100
    
    # 待审核订单数量（基于所有数据，不应用筛选）
    pending_orders = Purchase.objects.filter(status='待审核').count()
    
    # 供应商数量（从所有采购记录中统计不同药企数量）
    total_suppliers = Purchase.objects.values('pharma').annotate(Count('pharma')).count()
    
    # 本月新增供应商（假设Pharma模型有updated_at字段）
    new_suppliers_this_month = Pharma.objects.filter(
        updated_at__range=[start_of_month, end_of_month]
    ).count()

    # 分页（每页显示10条记录）
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取医院和药企列表，用于筛选下拉框
    if request.user.role == 'drug_admin':
        drug_admin = DrugAdmin.objects.get(user=request.user)
        hospital = drug_admin.hospital
        hospitals = [hospital]
    else:
        hospitals = Hospital.objects.all()
    pharmas = Pharma.objects.all()
    
    context = {
        'purchases': page_obj,
        'hospitals': hospitals,
        'pharmas': pharmas,
        'order_count': order_count,
        'order_count_growth': round(order_count_growth, 1),
        'this_month_amount': this_month_amount,
        'amount_growth': round(amount_growth, 1),
        'pending_orders': pending_orders,
        'total_suppliers': total_suppliers,
        'new_suppliers_this_month': new_suppliers_this_month,
        'monthly_purchases': monthly_purchases,
        'purchases_by_hospital': purchases_by_hospital,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'transaction/purchase_list.html', context)

@login_required
@role_required(['system_admin', 'drug_admin'])
def purchase_create(request):
    if request.method == 'POST':
        # 获取表单数据
        purchase_id = request.POST.get('purchase_id')
        drug_id = request.POST.get('drug')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        status = request.POST.get('status')
        admin_id = request.POST.get('admin')
        pharma_id = request.POST.get('pharma')  # 新增药企字段
        hospital_id = request.POST.get('hospital')  # 新增医院字段
        purchase_date_str = request.POST.get('purchase_date')  # 新增进货日期字段
        
        if purchase_date_str:
            # 将字符串转换为日期对象
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d')
            
            # 获取当前时间的时分秒
            now = timezone.now()
            current_time = now.time()
            
            # 组合日期和当前时分秒
            create_time = datetime.combine(purchase_date, current_time)
            
            # 若使用时区，需将时间转换为带时区的datetime对象
            create_time = timezone.make_aware(create_time, timezone=now.tzinfo)
        else:
            # 未选择日期时，使用当前完整时间
            create_time = timezone.now()

        # 获取下拉菜单选项
        drugs = Drug.objects.all()
        admins = DrugAdmin.objects.all()
        hospitals = Hospital.objects.all()
        # 状态选项
        STATUS_CHOICES = [
            ('pending', '待审核'),
            ('approved', '已审核'),
            ('stored', '已入库'),
            ('rejected', '已拒绝'),
        ]

        # 验证必要字段
        if not purchase_id or not drug_id or not quantity or not price or not admin_id:
            error_message = '进货单号、药品、数量、价格和管理员是必填项'
            messages.error(request, error_message)
            return render(request, 'transaction/purchase_create.html', {'error': error_message})

        try:
            # 获取关联对象
            drug = Drug.objects.get(id=drug_id)
            admin = DrugAdmin.objects.get(id=admin_id)
            pharma = Pharma.objects.get(id=pharma_id)
            hospital = Hospital.objects.get(id=hospital_id)
            # 创建进货记录实例
            purchase = Purchase.objects.create(
                purchase_id=purchase_id,
                hospital=hospital,
                drug=drug,
                pharma=pharma,
                quantity=quantity,
                price=price,
                admin=admin,
                create_time=create_time,
                status=status,
            )
            
            messages.success(request, f'进货单 {purchase_id} 创建成功')
            return redirect(reverse('transaction:purchase_list'))
        except Drug.DoesNotExist:
            error_message = '选择的药品不存在'
            messages.error(request, error_message)
            return render(request, 'transaction/purchase_create.html', {
                'drugs': drugs,
                'admins': admins,
                'hospitals': hospitals,
                'status_choices': STATUS_CHOICES,
                'pharma_list': Pharma.objects.all(),
                'error': error_message,
            })
        except DrugAdmin.DoesNotExist:
            error_message = '选择的药品管理员不存在'
            messages.error(request, error_message)
            return render(request, 'transaction/purchase_create.html', {
                'drugs': drugs,
                'admins': admins,
                'hospitals': hospitals,
                'status_choices': STATUS_CHOICES,
                'pharma_list': Pharma.objects.all(),
                'error': error_message,
            })
        except Exception as e:
            error_message = f'创建进货单失败: {str(e)}'
            messages.error(request, error_message)
            return render(request, 'transaction/purchase_create.html', {
                'drugs': drugs,
                'admins': admins,
                'hospitals': hospitals,
                'status_choices': STATUS_CHOICES,
                'pharma_list': Pharma.objects.all(),
                'error': error_message,
            })
    # 获取下拉菜单选项
    drugs = Drug.objects.all()
    admins = DrugAdmin.objects.all()
    hospitals = Hospital.objects.all()
    
    # 状态选项
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已审核'),
        ('stored', '已入库'),
        ('rejected', '已拒绝'),
    ]
    
    return render(request, 'transaction/purchase_create.html', {
        'drugs': drugs,
        'admins': admins,
        'hospitals': hospitals,
        'status_choices': STATUS_CHOICES,
        'pharma_list': Pharma.objects.all(),
    })

@login_required
@role_required(['system_admin', 'drug_admin'])
def sale_list(request):
    # 获取当前时间相关日期范围
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)

    if request.user.role == 'drug_admin':
        drug_admin = DrugAdmin.objects.get(user=request.user)
        hospital_id = drug_admin.hospital.id
    # 获取筛选参数
    hospital_id = request.GET.get('hospital')
    sale_id = request.GET.get('sale_id')
    drug_name = request.GET.get('drug_name')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    ordering = request.GET.get('ordering', '-create_time')  # 默认按创建时间降序

    # 基础查询集（使用select_related减少数据库查询）
    sales = Sale.objects.select_related('hospital', 'drug')

    # 应用筛选条件
    if hospital_id:
        try:
            sales = sales.filter(hospital_id=int(hospital_id))
        except ValueError:
            pass
    if sale_id:
        sales = sales.filter(sale_id__icontains=sale_id)
    if drug_name:
        sales = sales.filter(drug__name__icontains=drug_name)
    if status:
        sales = sales.filter(status=status)
    if start_date and end_date:
        try:
            sales = sales.filter(create_time__range=[start_date, end_date])
        except ValueError:
            pass
    elif start_date:
        try:
            sales = sales.filter(create_time__gte=start_date)
        except ValueError:
            pass
    elif end_date:
        try:
            sales = sales.filter(create_time__lte=end_date)
        except ValueError:
            pass

    # 月度销售数据（最近12个月）
    monthly_sales = sales.annotate(month=TruncMonth('create_time')).values('month').annotate(
        amount=Sum(F('quantity') * F('price'))
    ).order_by('month')[:12]

    # 按医院分组的销售数据
    sales_by_hospital = sales.values('hospital__name').annotate(
        amount=Sum(F('quantity') * F('price'))
    )
    
    # 排序
    sales = sales.order_by(ordering)

    def get_sales_in_range(start, end):
        return sales.filter(
            create_time__range=[start, end],
            status__in=['已支付', '已取药']
        )

    this_month_sales = get_sales_in_range(start_of_month, end_of_month)
    last_month_sales = get_sales_in_range(last_month_start, last_month_end)

    # 计算销售总额
    def calculate_total_sales(sales_queryset):
        return sales_queryset.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

    total_sales_this_month = calculate_total_sales(this_month_sales)
    total_sales_last_month = calculate_total_sales(last_month_sales)

    # 计算销售总额增长率
    sales_growth_rate = 0
    if total_sales_last_month > 0:
        sales_growth_rate = ((total_sales_this_month - total_sales_last_month) / total_sales_last_month) * 100

    # 统计每种药品的总销量
    def calculate_drug_sales(sales_queryset):
        return sales_queryset.values('drug').annotate(total_quantity=Sum('quantity'))

    drug_sales = calculate_drug_sales(sales)
    last_month_drug_sales = calculate_drug_sales(last_month_sales)

    # 畅销药品（销量>100）
    popular_drug_count = drug_sales.filter(total_quantity__gt=100).count()
    last_month_popular_drug_count = last_month_drug_sales.filter(total_quantity__gt=100).count()

    # 滞销药品（销量<10）
    unpopular_drug_count = drug_sales.filter(total_quantity__lt=10).count()
    last_month_unpopular_drug_count = last_month_drug_sales.filter(total_quantity__lt=10).count()

    # 销售订单数量及增长率
    sale_order_count = this_month_sales.count()
    sale_order_count_last_month = last_month_sales.count()

    def calculate_growth_rate(current, previous):
        if previous > 0:
            return ((current - previous) / previous) * 100
        return 0

    order_count_growth_rate = calculate_growth_rate(sale_order_count, sale_order_count_last_month)
    popular_drug_growth_rate = calculate_growth_rate(popular_drug_count, last_month_popular_drug_count)
    unpopular_drug_growth_rate = calculate_growth_rate(unpopular_drug_count, last_month_unpopular_drug_count)

    # 分页（每页显示10条记录）
    paginator = Paginator(sales, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取医院列表，用于筛选下拉框
    if request.user.role == 'drug_admin':
        drug_admin = DrugAdmin.objects.get(user=request.user)
        hospital = drug_admin.hospital
        hospitals = [hospital]
    else:
        hospitals = Hospital.objects.all()

    context = {
        'sales': page_obj,
        'hospitals': hospitals,
        'total_sales_this_month': total_sales_this_month,
        'popular_drug_count': popular_drug_count,
        'unpopular_drug_count': unpopular_drug_count,
        'sale_order_count': sale_order_count,
        'sales_growth_rate': round(sales_growth_rate, 1),
        'order_count_growth_rate': round(order_count_growth_rate, 1),
        'popular_drug_growth_rate': round(popular_drug_growth_rate, 1),
        'unpopular_drug_growth_rate': round(unpopular_drug_growth_rate, 1),
        'monthly_sales': monthly_sales,
        'sales_by_hospital': sales_by_hospital,
        'filters': request.GET.dict(),  # 传递筛选参数用于模板
    }

    return render(request, 'transaction/sale_list.html', context)

@login_required
@role_required(['system_admin', 'drug_admin'])
def sale_create(request):
    if request.method == 'POST':
        # 获取表单数据
        sale_id = request.POST.get('sale_id')
        drug_id = request.POST.get('drug')
        hospital_id = request.POST.get('hospital')
        patient_id = request.POST.get('patient')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        status = request.POST.get('status')
        admin_id = request.POST.get('admin')
        sale_date_str = request.POST.get('sale_date')  # 新增销售日期字段
        
        if sale_date_str:
            # 将字符串转换为日期对象
            sale_date = datetime.strptime(sale_date_str, '%Y-%m-%d')
            
            # 获取当前时间的时分秒
            now = timezone.now()
            current_time = now.time()
            
            # 组合日期和当前时分秒
            create_time = datetime.combine(sale_date, current_time)
            
            # 若使用时区，需将时间转换为带时区的datetime对象
            create_time = timezone.make_aware(create_time, timezone=now.tzinfo)
        else:
            # 未选择日期时，使用当前完整时间
            create_time = timezone.now()

        # 验证必要字段
        if not sale_id or not drug_id or not hospital_id or not patient_id or not quantity or not price or not admin_id:
            error_message = '销售编号、药品、医院、患者、数量、价格和管理员是必填项'
            messages.error(request, error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})

        try:
            # 获取关联对象
            drug = Drug.objects.get(id=drug_id)
            hospital = Hospital.objects.get(id=hospital_id)
            patient = Patient.objects.get(id=patient_id)
            admin = DrugAdmin.objects.get(id=admin_id)

            # 创建销售记录实例
            sale = Sale.objects.create(
                sale_id=sale_id,
                drug=drug,
                hospital=hospital,
                patient=patient,
                quantity=quantity,
                price=price,
                status=status,
                create_time=create_time,
                admin=admin,
            )

            messages.success(request, f'销售单 {sale_id} 创建成功')
            return redirect(reverse('transaction:sale_list'))

        except Drug.DoesNotExist:
            error_message = '选择的药品不存在'
            messages.error(request, error_message)
            print(error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})
        except Hospital.DoesNotExist:
            error_message = '选择的医院不存在'
            messages.error(request, error_message)
            print(error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})
        except Patient.DoesNotExist:
            error_message = '选择的患者不存在'
            messages.error(request, error_message)
            print(error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})
        except DrugAdmin.DoesNotExist:
            error_message = '选择的药品管理员不存在'
            messages.error(request, error_message)
            print(error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})
        except Exception as e:
            error_message = f'创建销售单失败: {str(e)}'
            messages.error(request, error_message)
            print(error_message)
            return render(request, 'transaction/sale_create.html', {'error': error_message})

    # 获取下拉菜单选项
    drugs = Drug.objects.all()
    patients = Patient.objects.all()
    hospitals = Hospital.objects.all()
    admins = DrugAdmin.objects.all()

    # 状态选项
    STATUS_CHOICES = [
        ('待审核', '待审核'),
        ('已审核', '已审核'),
        ('已完成', '已完成'),
        ('已取消', '已取消'),
    ]

    return render(request, 'transaction/sale_create.html', {
        'action': '创建',
        'drugs': drugs,
        'patients': patients,
        'hospitals': hospitals,
        'admins': admins,
        'status_choices': STATUS_CHOICES,
    })

@login_required
@role_required(['system_admin', 'drug_admin'])
def purchase_store(request, purchase_id):
    purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
    # 这里添加入库逻辑，比如更新进货单状态为已入库
    purchase.status = '已入库'
    purchase.save()
    return redirect('transaction:purchase_list')  # 重定向到进货单列表页面

def approve_purchase(request, purchase_id):
    if request.method == 'POST':
        try:
            purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
            if purchase.status == '待审核' or purchase.status == '已拒绝' or purchase.status == '已入库':
                purchase.status = '已审核'
                purchase.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '订单状态不是待审核'})
        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': '未知错误'}, status=500)

    return JsonResponse({'success': False, 'error': '无效请求'})

def reject_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
        if purchase.status == '待审核' or purchase.status == '已审核':
            purchase.status = '已拒绝'
            purchase.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '订单状态不是待审核'})
    return JsonResponse({'success': False, 'error': '无效请求'})

@csrf_protect  # 使用Django的CSRF保护，而非csrf_exempt
def store_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
        if purchase.status == '已审核':
            purchase.status = '已入库'
            purchase.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '订单未审核'})
    return JsonResponse({'success': False, 'error': '无效请求'})

def purchase_delete(request):
    purchase_id = request.GET.get('purchase_id')
    try:
        purchase = Purchase.objects.get(purchase_id=purchase_id)
        purchase.delete()
        return JsonResponse({'success': True, 'message': '进货单删除成功'})
    except Purchase.DoesNotExist:
        return JsonResponse({'success': False, 'message': '进货单不存在'})
    except ValueError as e:
        print(f"ValueError")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def pay_sale(request, sale_id):
    try:
        sale = Sale.objects.get(sale_id=sale_id)
        if sale.status == '待支付':
            sale.status = '已支付'
            sale.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '该销售单状态不是待支付，无法进行支付操作。'})
    except Sale.DoesNotExist:
        return JsonResponse({'success': False, 'error': '未找到该销售单。'})

@csrf_exempt
def take_drug(request, sale_id):
    try:
        sale = Sale.objects.get(sale_id=sale_id)
        if sale.status == '已支付':
            sale.status = '已取药'
            sale.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '该销售单状态不是已支付，无法进行取药操作。'})
    except Sale.DoesNotExist:
        return JsonResponse({'success': False, 'error': '未找到该销售单。'})
    except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': '未知错误'}, status=500)
    
def sale_delete(request):
    sale_id = request.GET.get('sale_id')
    try:
        sale = Sale.objects.get(sale_id=sale_id)
        sale.delete()
        return JsonResponse({'success': True, 'message': '销售单删除成功'})
    except Sale.DoesNotExist:
        return JsonResponse({'success': False, 'message': '销售单不存在'})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})