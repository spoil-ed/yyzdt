from django.db import models
from core.models import User

# 医院与医疗管理模块

class Hospital(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name='医院名称')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    contact = models.CharField(max_length=15, blank=True, null=True, verbose_name='联系方式')
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name='等级')  # 改为 CharField
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name='类型')  # 改为 CharField
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在城市')  # 改为 CharField
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='邮箱')
    description = models.TextField(blank=True, null=True, verbose_name='医院简介')
    founded = models.DateField(blank=True, null=True, verbose_name='成立日期')
    STATUS_CHOICES = (
        ('合作中', '合作中'),
        ('待审核', '待审核'),
        ('已终止', '已终止'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='待审核', verbose_name='状态')

    class Meta:
        db_table = 'hospital'
        verbose_name = '医院'
        verbose_name_plural = '医院'

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name='医院')
    name = models.CharField(max_length=100, null=False, verbose_name='姓名')
    # department = models.CharField(max_length=100, null=False, verbose_name='科室')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name='职称')
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系方式')

    class Meta:
        db_table = 'doctor'
        verbose_name = '医生'
        verbose_name_plural = '医生'

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    name = models.CharField(max_length=100, null=False, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth = models.DateField(blank=True, null=True, verbose_name='出生日期')
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系方式')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')

    class Meta:
        db_table = 'patient'
        verbose_name = '患者'
        verbose_name_plural = '患者'

    def __str__(self):
        return self.name

class DrugAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')
    name = models.CharField(max_length=100, null=False, verbose_name='姓名')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name='医院')
    employee_id = models.CharField(max_length=100, unique=True, verbose_name='员工编号')

    class Meta:
        db_table = 'drug_admin'
        verbose_name = '药品管理员'
        verbose_name_plural = '药品管理员'

    def __str__(self):
        return self.name
