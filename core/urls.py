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
    path('403/', core.views.permission_denied, name='403'),
    path('500/', core.views.server_error, name='500'),
    path('404/', core.views.page_not_found, name='404')
]