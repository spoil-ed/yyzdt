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
    # 医生管理
    path('doctors/', hospital.views.doctor_list, name='doctor_list'),  # 医生列表
    path('doctors/create/', hospital.views.doctor_create, name='doctor_create'),  # 创建医生
    path('doctors/<int:pk>/update/', hospital.views.doctor_update, name='doctor_update'),  # 更新医生
    # path('doctors/<int:pk>/delete/', hospital.views.doctor_delete, name='doctor_delete'),
    # 药品管理员管理
    path('drug-admins/', hospital.views.drug_admin_list, name='drug_admin_list'),  # 药品管理员列表
    path('drug-admins/create/', hospital.views.drug_admin_create, name='drug_admin_create'),  # 创建药品管理员
    # path('drug-admins/<int:pk>/delete/', hospital.views.drug_admin_delete, name='drug_admin_delete'),
    # 医生与医院关系
    path('doctor-hospitals/', hospital.views.doctor_hospital_list, name='doctor_hospital_list'),  # 关系列表
    path('doctor-hospitals/create/', hospital.views.doctor_hospital_create, name='doctor_hospital_create'),  # 创建关系
    # path('doctor-hospitals/<int:pk>/delete/', hospital.views.doctor_hospital_delete, name='doctor_hospital_delete'),
]