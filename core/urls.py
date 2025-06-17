from django.urls import path
import core.views

app_name = 'core'

urlpatterns = [
    # 认证相关
    path('login/', core.views.login, name='login'),
    path('logout/', core.views.logout, name='logout'),
    path('', core.views.index, name='index'),
    path('register/', core.views.register, name='register'),
    path('user/', core.views.user_list, name='user_list'),
    path('user/create/', core.views.user_create, name='user_create'),
    path('user/<int:pk>/update/', core.views.user_update, name='user_update'),
    path('user/<int:pk>/detail/', core.views.user_detail, name='user_detail'),
    # 政府监管功能
    path('government/data/', core.views.government_data, name='government_data'),
    path('government/report/', core.views.government_report, name='government_report'),
]