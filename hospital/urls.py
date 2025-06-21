from django.urls import path
import hospital.views

app_name = 'hospital'

urlpatterns = [
    # 医院管理
    path('hospitals/', hospital.views.hospital_list, name='hospital_list'),  # 医院列表
    path('hospitals/create/', hospital.views.hospital_create, name='hospital_create'),  # 创建医院
    path('hospitals/<int:pk>/', hospital.views.hospital_detail, name='hospital_detail'),
    path('hospitals/<int:pk>/update/', hospital.views.hospital_update, name='hospital_update'),
    # path('hospitals/<int:pk>/delete/', hospital.views.hospital_delete, name='hospital_delete'),
]