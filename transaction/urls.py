from django.urls import path
import transaction.views

app_name = 'transaction'

urlpatterns = [
    # 药品管理
    path('drugs/', transaction.views.drug_list, name='drug_list'),  # 药品列表
    path('drugs/create/', transaction.views.drug_create, name='drug_create'),  # 创建药品
    path('drugs/<str:drug_id>/', transaction.views.drug_detail, name='drug_detail'),  # 药品详情
    path('drugs/<str:drug_id>/update/', transaction.views.drug_update, name='drug_update'),  # 更新药品
    # 药品使用记录
    # 药品进货管理
    path('purchases/', transaction.views.purchase_list, name='purchase_list'),  # 进货单列表
    path('purchases/create/', transaction.views.purchase_create, name='purchase_create'),  # 创建进货单
    path('purchases/store/<str:purchase_id>/', transaction.views.purchase_store, name='store_purchase'),  # 进货单入库
    path('purchase/approve/<str:purchase_id>/', transaction.views.approve_purchase, name='approve_purchase'),
    path('purchase/reject/<str:purchase_id>/', transaction.views.reject_purchase, name='reject_purchase'),
    path('purchase/delete/', transaction.views.purchase_delete, name='purchase_delete'),
    # 药品销售管理
    path('sales/', transaction.views.sale_list, name='sale_list'),  # 销售记录列表
    path('sales/create/', transaction.views.sale_create, name='sale_create'),  # 创建销售单
    path('sales/<str:sale_id>/pay_sale/', transaction.views.pay_sale, name='pay_sale'),  # 销售单详情
    path('sales/<str:sale_id>/take_drug/', transaction.views.take_drug, name='take_drug'),  # 销售单详情
    path('sales/sale_delete/', transaction.views.sale_delete, name='sale_delete'),  # 销售单详情
    # 患者用药记录
    path('drug_use_records/', transaction.views.drug_use_records, name='drug_use_records'),  # 药品使用记录列表
    # 药企供药记录
    path('supply_records/', transaction.views.supply_records, name='supply_records'),  # 药企供药记录列表
]