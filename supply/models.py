from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _
from hospital.models import Hospital
from transaction.models import Purchase, Sale, Prescription
from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

# 药品供应链模块

class Pharma(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('合作中', '合作中'), ('待审核', '待审核'), ('已终止', '已终止')], default='待审核')
    founded = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pharma'
        verbose_name = '药企'
        verbose_name_plural = '药企'

    def __str__(self):
        return self.name


class Drug(models.Model):
    # 基础信息
    name = models.CharField(max_length=255, null=False, verbose_name='药品名称')
    spec = models.CharField(max_length=50, blank=True, null=True, verbose_name='规格')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='类别')
    expiration = models.DateField(blank=True, null=True, verbose_name='有效期')
    manufacturer = models.CharField(max_length=255, blank=True, null=True, verbose_name='生产商')
    
    # 新增字段 - 来自表单
    common_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='通用名')
    approval_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='批准文号')
    dosage_form = models.CharField(max_length=50, blank=True, null=True, verbose_name='剂型')
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('正常')),
            ('pending', _('待审核')),
            ('inactive', _('停用')),
        ],
        default='active',
        verbose_name='状态'
    )
    
    # 药品特性字段
    storage_condition = models.CharField(max_length=50, blank=True, null=True, verbose_name='储存条件')
    shelf_life = models.IntegerField(blank=True, null=True, verbose_name='有效期(月)')
    otc_type = models.CharField(
        max_length=20,
        choices=[
            ('prescription', _('处方药')),
            ('otc_red', _('甲类非处方药')),
            ('otc_green', _('乙类非处方药')),
            ('not_otc', _('非OTC')),
        ],
        blank=True, 
        null=True,
        verbose_name='OTC类型'
    )
    medical_insurance = models.CharField(
        max_length=20,
        choices=[
            ('class_a', _('甲类')),
            ('class_b', _('乙类')),
            ('class_c', _('丙类')),
            ('not_covered', _('非医保')),
        ],
        blank=True, 
        null=True,
        verbose_name='医保类型'
    )

    class Meta:
        db_table = 'drug'
        verbose_name = '药品'
        verbose_name_plural = '药品'

    def __str__(self):
        return self.name
    
    @property
    def is_expiring_soon(self):
        """判断药品是否即将过期（3个月内）"""
        if not self.expiration:
            return False
        from datetime import datetime, timedelta
        three_months_later = datetime.now().date() + timedelta(days=90)
        return self.expiration <= three_months_later and self.expiration > datetime.now().date()

class Supply(models.Model):
    batch_code = models.CharField(max_length=50, primary_key=True, verbose_name='批次号')
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE, verbose_name='药企')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name='药品')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='数量')

    class Meta:
        db_table = 'supply'
        verbose_name = '药品供应'
        verbose_name_plural = '药品供应'

    def __str__(self):
        return f"{self.batch_code} - {self.drug.name}"

class Inventory(models.Model):
    hospital = models.ForeignKey(
        'hospital.Hospital',
        on_delete=models.CASCADE,
        related_name='inventories',
        verbose_name='医院'
    )
    
    drug = models.ForeignKey(
        'supply.Drug',  # 确保 drug 应用已注册
        on_delete=models.CASCADE,
        related_name='inventories',
        verbose_name='药品'
    )
    warning_threshold = models.IntegerField(default=100, verbose_name='预警阈值')
    current_quantity = models.IntegerField(default=0, verbose_name='当前库存')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        db_table = 'supply_inventory'  # 修改表名避免冲突
        verbose_name = '库存'
        verbose_name_plural = '库存'
        unique_together = ('hospital', 'drug')

    def __str__(self):
        return f"{self.drug.name} - {self.current_quantity}"

    @property
    def status(self):
        if self.current_quantity <= 0:
            return "缺货"
        elif self.current_quantity < self.warning_threshold:
            return "低库存"
        else:
            return "充足"
    
    @property
    def status_bg_color(self):
        if self.current_quantity <= 0:
            return "bg-red-50"
        elif self.current_quantity < self.warning_threshold:
            return "bg-yellow-50"
        else:
            return ""
    
    @property
    def status_badge_class(self):
        if self.current_quantity <= 0:
            return "bg-red-100 text-red-800"
        elif self.current_quantity < self.warning_threshold:
            return "bg-yellow-100 text-yellow-800"
        else:
            return "bg-green-100 text-green-800"

    @classmethod
    def update_inventory(cls, drug, quantity_change):
        """更新指定药品的库存数量"""
        inventory, created = cls.objects.get_or_create(drug=drug)
        inventory.current_quantity = F('current_quantity') + quantity_change
        inventory.save()
        inventory.refresh_from_db()  # 获取数据库中更新后的值
        return inventory
    
# 当创建新药品时，为所有医院创建该药品的库存记录
@receiver(post_save, sender=Drug)
def create_inventory_for_new_drug(sender, instance, created, **kwargs):
    if created:
        # 获取所有医院
        hospitals = Hospital.objects.all()
        
        # 为每个医院创建该药品的库存记录
        with transaction.atomic():
            for hospital in hospitals:
                Inventory.objects.get_or_create(
                    drug=instance,
                    hospital=hospital,
                    defaults={'warning_threshold': 100}
                )

# 当创建新医院时，为所有药品创建该医院的库存记录
@receiver(post_save, sender=Hospital)
def create_inventory_for_new_hospital(sender, instance, created, **kwargs):
    if created:
        # 获取所有药品
        drugs = Drug.objects.all()
        
        # 为每个药品创建该医院的库存记录
        with transaction.atomic():
            for drug in drugs:
                Inventory.objects.get_or_create(
                    drug=drug,
                    hospital=instance,
                    defaults={'warning_threshold': 100}
                )

# 当创建采购记录时，增加对应药品的库存
@receiver(post_save, sender=Purchase)
def increase_inventory_on_purchase(sender, instance, created, **kwargs):
    # 判断是否为新增记录且状态为已入库，或者记录被更新且状态变为已入库
    if (created and instance.status == '已入库') or (not created and instance.tracker.has_changed('status')):
        # 获取或创建库存记录
        inventory, _ = Inventory.objects.get_or_create(
            drug=instance.drug,
            hospital=instance.hospital,
            defaults={
                'warning_threshold': 100,
                'current_quantity': 0
            }
        )
        if not created and instance.tracker.has_changed('status'):
            if instance.status == '已入库':
                # 增加库存
                inventory.current_quantity = F('current_quantity') + instance.quantity
                inventory.save()
            elif instance.status != "已入库" and instance.tracker.previous('status') == '已入库':
                # 减少库存
                print("Decreasing inventory for drug:")
                if inventory.current_quantity - instance.quantity < 0:
                    if not created:
                        instance.status = instance.tracker.previous('status')
                        instance.save()
                    # 返回错误信息
                    raise ValueError('库存不足，无法执行此操作')
                inventory.current_quantity = F('current_quantity') - instance.quantity
                inventory.save()
            
        elif created and instance.status == '已入库':
            # 增加库存
            inventory.current_quantity = F('current_quantity') + instance.quantity
            inventory.save()

# 当删除采购记录时，减少对应药品的库存
@receiver(post_delete, sender=Purchase)
def decrease_inventory_on_purchase_delete(sender, instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            drug=instance.drug,
            hospital=instance.hospital  # 假设Purchase模型有hospital字段
        )
        print("Decreasing inventory for drug:")
        # 减少库存数量
        if inventory.current_quantity - instance.quantity < 0:
            print("Inventory quantity is insufficient for deletion.")
            instance.status = instance.tracker.previous('status')
            # 返回错误信息
            raise ValueError('库存不足，无法执行此操作')
        inventory.current_quantity = F('current_quantity') - instance.quantity
        inventory.save()
    except Inventory.DoesNotExist:
        pass  # 库存记录不存在，无需处理

# 当创建销售记录时，减少对应药品的库存
@receiver(post_save, sender=Sale)
def decrease_inventory_on_sale(sender, instance, created, **kwargs):
    # 判断是否为新增记录且状态为已取药，或者记录被更新且状态变为已取药
    if (created and instance.status == '已取药') or (not created and instance.tracker.has_changed('status') and instance.status == '已取药'):
        # 获取或创建库存记录
        inventory, _ = Inventory.objects.get_or_create(
            drug=instance.drug,
            hospital=instance.hospital,
            defaults={'warning_threshold': 100}
        )
        # 减少库存数量
        if inventory.current_quantity - instance.quantity < 0:
            if not created:
                instance.status = instance.tracker.previous('status')
                instance.save()
            # 返回错误信息
            raise ValueError('库存不足，无法执行此操作')
        inventory.current_quantity = F('current_quantity') - instance.quantity
        inventory.save()

# 当删除销售记录时，增加对应药品的库存
@receiver(post_delete, sender=Sale)
def increase_inventory_on_sale_delete(sender, instance, **kwargs):
    try:
        inventory = Inventory.objects.get(
            drug=instance.drug,
            hospital=instance.hospital  # 假设Sale模型有hospital字段
        )
        
        # 增加库存数量
        inventory.current_quantity = F('current_quantity') + instance.quantity
        inventory.save()
    except Inventory.DoesNotExist:
        pass  # 库存记录不存在，无需处理

class WarningLog(models.Model):
    message = models.CharField(max_length=255, blank=True, null=True, verbose_name='警告信息')
    created_at = models.DateTimeField(verbose_name='创建时间')

    class Meta:
        db_table = 'warning_log'
        verbose_name = '预警日志'
        verbose_name_plural = '预警日志'

    def __str__(self):
        return self.message

# 新增：药企药品供应关系模型
class PharmaDrugSupply(models.Model):
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE, verbose_name='药企')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name='药品')
    supply_start_date = models.DateField(verbose_name='供应开始日期')
    supply_end_date = models.DateField(blank=True, null=True, verbose_name='供应结束日期')
    is_primary_supplier = models.BooleanField(default=False, verbose_name='是否为主要供应商')
    certification_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='资质证书编号')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'pharma_drug_supply'
        verbose_name = '药企药品供应关系'
        verbose_name_plural = '药企药品供应关系'
        unique_together = ('pharma', 'drug')  # 确保药企与药品关系唯一

    def __str__(self):
        status = '（主要供应商）' if self.is_primary_supplier else ''
        return f"{self.pharma.name} 供应 {self.drug.name}{status}"
    
    @property
    def is_current_supplying(self):
        """判断当前是否处于供应期"""
        today = date.today()
        if self.supply_end_date:
            return self.supply_start_date <= today <= self.supply_end_date
        return self.supply_start_date <= today