from django.urls import path
import transaction.views

app_name = 'transaction'

urlpatterns = [
    # 药品管理
    path('drugs/', transaction.views.drug_list, name='drug_list'),  # 药品列表
    path('drugs/create/', transaction.views.drug_create, name='drug_create'),  # 创建药品
    path('drugs/<str:drug_id>/', transaction.views.drug_detail, name='drug_detail'),  # 药品详情
    path('drugs/<str:drug_id>/update/', transaction.views.drug_update, name='drug_update'),  # 更新药品
    # 药品进货管理
    path('purchases/', transaction.views.purchase_list, name='purchase_list'),  # 进货单列表
    path('purchases/create/', transaction.views.purchase_create, name='purchase_create'),  # 创建进货单
    path('purchases/<str:purchase_id>/', transaction.views.purchase_detail, name='purchase_detail'),  # 进货单详情
    path('purchases/<str:purchase_id>/update/', transaction.views.purchase_update, name='purchase_update'),  # 更新进货单
    path('purchases/<str:purchase_id>/approve/', transaction.views.purchase_approve, name='purchase_approve'),  # 审核进货单
    path('purchases/<str:purchase_id>/receive/', transaction.views.purchase_receive, name='purchase_receive'),  # 进货单入库
    path('purchase/approve/<str:purchase_id>/', transaction.views.approve_purchase, name='approve_purchase'),
    path('purchase/reject/<str:purchase_id>/', transaction.views.reject_purchase, name='reject_purchase'),
    # 药品销售管理
    path('sales/', transaction.views.sale_list, name='sale_list'),  # 销售记录列表
    path('sales/create/', transaction.views.sale_create, name='sale_create'),  # 创建销售单
    path('sales/stats/', transaction.views.sale_stats, name='sale_stats'),  # 销售统计
    # 患者用药记录
    path('prescriptions/', transaction.views.prescription_list, name='prescription_list'),  # 用药记录列表
    path('prescriptions/create/', transaction.views.prescription_create, name='prescription_create'),  # 医生录入用药记录
    path('prescriptions/patient/', transaction.views.prescription_patient, name='prescription_patient'),  # 患者查询用药记录
]