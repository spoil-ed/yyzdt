# Yao-Duo-Duo/core/decorators.py

from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # 检查用户是否登录
            if not request.user.is_authenticated:
                return redirect('core:login')
            
            # 检查用户角色是否在允许的角色列表中
            if request.user.role not in allowed_roles:
                messages.error(request, '你没有权限访问该页面。')
                return redirect('core:index')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator