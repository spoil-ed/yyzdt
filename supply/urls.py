from django.urls import path
import supply.views

app_name = 'supply'

urlpatterns = [
    # 药品供应管理
    path('pharmas/', supply.views.pharma_list, name='pharma_list'),  # 药企列表
    path('pharmas/create/', supply.views.pharma_create, name='pharma_create'),  # 创建药企
    path('pharmas/<int:pk>/update/', supply.views.pharma_update, name='pharma_update'),  # 更新药企
    path('pharmas/<int:pk>/', supply.views.pharma_detail, name='pharma_detail'),  # 药企详情
    path('supplies/pharma_supplies/', supply.views.pharma_drug_supply, name='pharma_drug_supply'),  # 药企供货表单
    path('supplies/pharma_supplies/create/', supply.views.pharma_drug_supply_create, name='pharma_drug_supply_create'),  # 药企供货表单创建
    # 药品库存管理
    path('inventories/', supply.views.inventory_list, name='inventory_list'),  # 库存查看
    path('pharma-drug-supply/<int:pk>/delete/', supply.views.pharma_drug_supply_delete, name='pharma_drug_supply_delete'),
]