from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from .models import Purchase, Sale
from hospital.models import DrugAdmin, Hospital, Patient  # 假设DrugAdmin在hospital应用中
from supply.models import Drug, Pharma  # 假设SupplyDrug在supply应用中
from django.contrib.auth.decorators import login_required
# 示例数据
purchase_detail_data = {
    'P2023001': {
        'id': 'P2023001',
        'drug_name': '阿司匹林',
        'specification': '100mg*30片',
        'quantity': 1000,
        'unit_price': 12.0,
        'total_amount': 12000.0,
        'supplier': '健康药业',
        'supplier_contact': '张经理',
        'supplier_phone': '13800138001',
        'date': '2023-05-15',
        'status': '已审核',
        'approve_date': '2023-05-16',
        'approve_by': '王审核员',
        'receive_date': None,
        'receive_by': None,
        'notes': '常规进货，用于补充库存',
        'items': [
            {'drug_id': 'D001', 'name': '阿司匹林', 'specification': '100mg*30片', 'quantity': 1000, 'unit_price': 12.0, 'amount': 12000.0},
        ]
    },
    'P2023002': {
        'id': 'P2023002',
        'drug_name': '布洛芬',
        'specification': '0.3g*20片',
        'quantity': 800,
        'unit_price': 10.0,
        'total_amount': 8000.0,
        'supplier': '康泰制药',
        'supplier_contact': '李经理',
        'supplier_phone': '13900139001',
        'date': '2023-05-16',
        'status': '待审核',
        'approve_date': None,
        'approve_by': None,
        'receive_date': None,
        'receive_by': None,
        'notes': '紧急进货，库存不足',
        'items': [
            {'drug_id': 'D002', 'name': '布洛芬', 'specification': '0.3g*20片', 'quantity': 800, 'unit_price': 10.0, 'amount': 8000.0},
        ]
    },
    'P2023003': {
        'id': 'P2023003',
        'drug_name': '阿莫西林',
        'specification': '0.25g*24粒',
        'quantity': 1500,
        'unit_price': 8.0,
        'total_amount': 12000.0,
        'supplier': '好医生药业',
        'supplier_contact': '赵经理',
        'supplier_phone': '13700137001',
        'date': '2023-05-18',
        'status': '已入库',
        'approve_date': '2023-05-19',
        'approve_by': '王审核员',
        'receive_date': '2023-05-20',
        'receive_by': '李管理员',
        'notes': '季度批量进货，享受折扣',
        'items': [
            {'drug_id': 'D003', 'name': '阿莫西林', 'specification': '0.25g*24粒', 'quantity': 1500, 'unit_price': 8.0, 'amount': 12000.0},
        ]
    }
}

purchase_list_data = [
    {'id': 'P2023001', 'drug_name': '阿司匹林', 'quantity': 1000, 'supplier': '健康药业', 'date': '2023-05-15', 'status': '已审核'},
    {'id': 'P2023002', 'drug_name': '布洛芬', 'quantity': 800, 'supplier': '康泰制药', 'date': '2023-05-16', 'status': '待审核'},
]

sale_list_data = [
    {'id': 'S2023001', 'drug_name': '阿司匹林', 'quantity': 100, 'customer': '中心医院', 'date': '2023-05-20', 'total': 1200},
    {'id': 'S2023002', 'drug_name': '布洛芬', 'quantity': 50, 'customer': '第一人民医院', 'date': '2023-05-21', 'total': 800},
]

prescription_data = [
    {'id': 'R2023001', 'patient': '张三', 'drug_name': '阿莫西林', 'dosage': '500mg', 'frequency': '每日3次', 'doctor': '李医生', 'date': '2023-05-10'},
    {'id': 'R2023002', 'patient': '李四', 'drug_name': '布洛芬', 'dosage': '200mg', 'frequency': '每日2次', 'doctor': '王医生', 'date': '2023-05-12'},
]

@login_required
def drug_list(request):

    return render(request, 'transaction/drug_list.html', {'drugs': Drug.objects.all()})

@login_required
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
def drug_detail(request, drug_id):
    return render(request, 'transaction/drug_detail.html', {'drug': Drug.objects.get(id=drug_id)})

@login_required
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

from django.shortcuts import render
from .models import Purchase
from django.db.models import F, Sum, Count
from django.utils import timezone
from supply.models import Pharma  # 导入药企模型

@login_required
def purchase_list(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    
    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)
    
    # 本月进货单数量（已审核）
    this_month_orders = Purchase.objects.filter(
        create_time__range=[start_of_month, end_of_month],
        status='已审核'
    )
    order_count = this_month_orders.count()
    
    # 上月进货单数量
    last_month_orders = Purchase.objects.filter(
        create_time__range=[last_month_start, last_month_end],
        status='已审核'
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
    
    # 上月进货金额
    last_month_amount = last_month_orders.aggregate(Sum('price'))['price__sum'] or 0
    
    # 计算进货金额同比增长率
    amount_growth = 0
    if last_month_amount > 0:
        amount_growth = ((this_month_amount - last_month_amount) / last_month_amount) * 100
    
    # 待审核订单数量
    pending_orders = Purchase.objects.filter(status='待审核').count()
    
    # 供应商数量（从采购记录中统计不同药企数量）
    total_suppliers = Purchase.objects.values('pharma').annotate(Count('pharma')).count()
    
    # 本月新增供应商（假设Pharma模型有updated_at字段）
    new_suppliers_this_month = Pharma.objects.filter(
        updated_at__range=[start_of_month, end_of_month]
    ).count()
    
    # 获取所有采购记录（按创建时间降序排列）
    purchases = Purchase.objects.all().order_by('-create_time')

    context = {
        'purchases': purchases,
        'order_count': order_count,
        'order_count_growth': round(order_count_growth, 1),
        'this_month_amount': this_month_amount,
        'amount_growth': round(amount_growth, 1),
        'pending_orders': pending_orders,
        'total_suppliers': total_suppliers,
        'new_suppliers_this_month': new_suppliers_this_month,
    }

    return render(request, 'transaction/purchase_list.html', context)

@login_required
def purchase_create(request):
    if request.method == 'POST':
        # 获取表单数据
        purchase_id = request.POST.get('purchase_id')
        drug_id = request.POST.get('drug')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        status = request.POST.get('status')
        print(status)
        admin_id = request.POST.get('admin')
        pharma_id = request.POST.get('pharma')  # 新增药企字段
        hospital_id = request.POST.get('hospital')  # 新增医院字段
        create_time = request.POST.get('purchase_date')  # 新增进货日期字段

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
                create_time=create_time or datetime.now(),
                status=status,
            )
            
            messages.success(request, f'进货单 {purchase_id} 创建成功')
            return redirect(reverse('transaction:purchase_list'))
        except Drug.DoesNotExist:
            error_message = '选择的药品不存在'
            messages.error(request, error_message)
            print(error_message)
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
            print(error_message)
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
            print(error_message)
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
def purchase_update(request, purchase_id):
    purchase = next((p for p in purchase_list_data if p['id'] == purchase_id), None)
    if request.method == 'POST':
        messages.success(request, '进货单更新成功')
        return redirect('transaction:purchase_list')
    return render(request, 'transaction/purchase_form.html', {'action': '更新', 'purchase': purchase})

@login_required
def purchase_approve(request, purchase_id):
    purchase = next((p for p in purchase_list_data if p['id'] == purchase_id), None)
    if purchase:
        purchase['status'] = '已审核'
        messages.success(request, '进货单审核成功')
    return redirect('transaction:purchase_list')

from django.utils import timezone
from django.db.models import Sum

@login_required
def sale_list(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
    
    # 计算上月同期范围
    last_month_start = (start_of_month - timezone.timedelta(days=1)).replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(seconds=1)
    
    # 本月销售数据
    this_month_sales = Sale.objects.filter(create_time__range=[start_of_month, end_of_month])
    total_sales_this_month = this_month_sales.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 上月销售数据
    last_month_sales = Sale.objects.filter(create_time__range=[last_month_start, last_month_end])
    total_sales_last_month = last_month_sales.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    
    # 计算销售总额增长率
    sales_growth_rate = 0
    if total_sales_last_month > 0:
        sales_growth_rate = ((total_sales_this_month - total_sales_last_month) / total_sales_last_month) * 100
    
    # 统计每种药品的总销量
    drug_sales = Sale.objects.values('drug').annotate(total_quantity=Sum('quantity'))
    
    # 畅销药品（销量>100）
    popular_drug_count = drug_sales.filter(total_quantity__gt=100).count()
    
    # 滞销药品（销量<10）
    unpopular_drug_count = drug_sales.filter(total_quantity__lt=10).count()
    
    # 销售订单数量及增长率
    sale_order_count = this_month_sales.count()
    sale_order_count_last_month = last_month_sales.count()
    
    order_count_growth_rate = 0
    if sale_order_count_last_month > 0:
        order_count_growth_rate = ((sale_order_count - sale_order_count_last_month) / sale_order_count_last_month) * 100
    
    # 畅销药品数量增长率
    # 先获取上月畅销药品数量
    last_month_drug_sales = last_month_sales.values('drug').annotate(total_quantity=Sum('quantity'))
    last_month_popular_drug_count = last_month_drug_sales.filter(total_quantity__gt=100).count()
    
    popular_drug_growth_rate = 0
    if last_month_popular_drug_count > 0:
        popular_drug_growth_rate = ((popular_drug_count - last_month_popular_drug_count) / last_month_popular_drug_count) * 100
    
    # 滞销药品数量增长率
    last_month_unpopular_drug_count = last_month_drug_sales.filter(total_quantity__lt=10).count()
    
    unpopular_drug_growth_rate = 0
    if last_month_unpopular_drug_count > 0:
        unpopular_drug_growth_rate = ((unpopular_drug_count - last_month_unpopular_drug_count) / last_month_unpopular_drug_count) * 100
    
    context = {
        'sales': this_month_sales,
        'total_sales_this_month': total_sales_this_month,
        'popular_drug_count': popular_drug_count,
        'unpopular_drug_count': unpopular_drug_count,
        'sale_order_count': sale_order_count,
        'sales_growth_rate': round(sales_growth_rate, 1),
        'order_count_growth_rate': round(order_count_growth_rate, 1),
        'popular_drug_growth_rate': round(popular_drug_growth_rate, 1),
        'unpopular_drug_growth_rate': round(unpopular_drug_growth_rate, 1),
    }
    
    return render(request, 'transaction/sale_list.html', context)

@login_required
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
        create_time = request.POST.get('sale_date')  # 新增销售日期字段

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
                create_time=create_time or datetime.now(),
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
def sale_stats(request):
    # 模拟销售统计数据
    stats = {
        'total_sales': 125000,
        'top_drugs': [
            {'name': '阿司匹林', 'quantity': 1500, 'amount': 30000},
            {'name': '布洛芬', 'quantity': 1200, 'amount': 24000},
            {'name': '阿莫西林', 'quantity': 1000, 'amount': 20000},
        ],
        'monthly_trend': [
            {'month': '1月', 'amount': 15000},
            {'month': '2月', 'amount': 18000},
            {'month': '3月', 'amount': 22000},
            {'month': '4月', 'amount': 25000},
            {'month': '5月', 'amount': 28000},
        ]
    }
    return render(request, 'transaction/sale_stats.html', {'stats': stats})

@login_required
def prescription_list(request):
    return render(request, 'transaction/prescription_list.html', {'prescriptions': prescription_data})

@login_required
def prescription_create(request):
    if request.method == 'POST':
        messages.success(request, '用药记录创建成功')
        return redirect('transaction:prescription_list')
    return render(request, 'transaction/prescription_form.html', {'action': '创建'})

@login_required
def prescription_patient(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        filtered_prescriptions = [p for p in prescription_data if p['patient'] == patient_name]
        return render(request, 'transaction/prescription_patient.html', 
                     {'prescriptions': filtered_prescriptions, 'patient_name': patient_name})
    return render(request, 'transaction/prescription_patient.html')

@login_required
# 补充进货单详情视图
def purchase_detail(request, purchase_id):
    purchase = purchase_detail_data.get(purchase_id)
    if not purchase:
        messages.error(request, '进货单不存在')
        return redirect('transaction:purchase_list')
    
    # 模拟操作权限（实际项目中应使用权限系统）
    can_approve = purchase['status'] == '待审核'
    can_receive = purchase['status'] == '已审核'
    
    return render(request, 'transaction/purchase_detail.html', {
        'purchase': purchase,
        'can_approve': can_approve,
        'can_receive': can_receive
    })

@login_required
# 补充进货单入库视图
def purchase_receive(request, purchase_id):
    purchase = purchase_detail_data.get(purchase_id)
    if not purchase:
        messages.error(request, '进货单不存在')
        return redirect('transaction:purchase_list')
    
    if purchase['status'] != '已审核':
        messages.error(request, '只有已审核的进货单才能入库')
        return redirect('transaction:purchase_detail', purchase_id=purchase_id)
    
    if request.method == 'POST':
        # 模拟入库操作
        purchase['status'] = '已入库'
        purchase['receive_date'] = datetime.now().strftime('%Y-%m-%d')
        purchase['receive_by'] = request.user.username if request.user.is_authenticated else '系统'
        
        # 更新库存（模拟）
        for item in purchase['items']:
            drug = next((d for d in inventory_data if d['id'] == item['drug_id']), None)
            if drug:
                drug['quantity'] += item['quantity']
                # 更新库存状态
                if drug['quantity'] >= drug['alert_quantity'] and drug['quantity'] > 0:
                    drug['status'] = '正常'
        
        messages.success(request, '进货单已成功入库，库存已更新')
        return redirect('transaction:purchase_detail', purchase_id=purchase_id)
    
    return render(request, 'transaction/purchase_receive.html', {'purchase': purchase})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # 仅用于开发测试，生产环境建议使用 CSRF 保护
def approve_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, purchase_id=purchase_id)
        if purchase.status == '待审核' or purchase.status == '已拒绝':
            purchase.status = '已审核'
            purchase.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '订单状态不是待审核'})
    return JsonResponse({'success': False, 'error': '无效请求'})

@csrf_exempt  # 仅用于开发，生产环境移除
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