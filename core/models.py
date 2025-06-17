from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None, role=None, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        if not password:
            raise ValueError('密码不能为空')
        if not role:
            raise ValueError('用户角色不能为空')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)  # 使用 set_password 方法加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, password, email, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('system_admin', '系统管理员'),
        ('doctor', '医生'),
        ('drug_admin', '药品管理员'),
        ('patient', '患者'),
        ('pharma_admin', '药企管理员'),
    )

    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='邮箱')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='姓名')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    is_active = models.BooleanField(default=True, verbose_name='账户是否激活')
    is_superadmin = models.BooleanField(default=False, verbose_name='超级管理员')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups',
        blank=True,
        verbose_name='用户组'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',
        blank=True,
        verbose_name='用户权限'
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_full_name(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username
