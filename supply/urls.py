from django.urls import path
import supply.views

app_name = 'supply'

urlpatterns = [
    # 药品供应管理
    path('pharmas/', supply.views.pharma_list, name='pharma_list'),  # 药企列表
    path('pharmas/create/', supply.views.pharma_create, name='pharma_create'),  # 创建药企
    path('pharmas/<int:pk>/update/', supply.views.pharma_update, name='pharma_update'),  # 更新药企
    path('pharmas/<int:pk>/', supply.views.pharma_detail, name='pharma_detail'),  # 药企详情
    path('supplies/', supply.views.supply_list, name='supply_list'),  # 供货记录查看
    path('supplies/create/', supply.views.supply_create, name='supply_create'),  # 发布供货信息
    path('supplies/pharma_supplies/', supply.views.pharma_drug_supply, name='pharma_drug_supply'),  # 药企供货表单
    path('supplies/pharma_supplies/create/', supply.views.pharma_drug_supply_create, name='pharma_drug_supply_create'),  # 药企供货表单创建
    path('supplies/<str:batch_code>/', supply.views.supply_detail, name='supply_detail'),  # 供货详情
    # 药品库存管理
    path('inventories/', supply.views.inventory_list, name='inventory_list'),  # 库存查看
    path('inventories/<int:drug_id>/<int:hospital_id>/update/', supply.views.inventory_update, name='inventory_update'),  # 库存预警设置
    path('warning-logs/', supply.views.warning_log_list, name='warning_log_list'),  # 预警记录
]