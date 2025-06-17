from django.db import models
# 交易与记录模块

class Purchase(models.Model):
    purchase_id = models.CharField(max_length=50, primary_key=True, verbose_name='采购编号')
    drug = models.ForeignKey('supply.Drug', on_delete=models.CASCADE, verbose_name='药品')
    pharma = models.ForeignKey('supply.Pharma', on_delete=models.SET_NULL, null=True, verbose_name='药企')  # 新增药企外键
    hospital = models.ForeignKey('hospital.Hospital', on_delete=models.CASCADE, verbose_name='医院')
    quantity = models.IntegerField(null=False, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='价格')
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name='状态')
    admin = models.ForeignKey('hospital.DrugAdmin', on_delete=models.CASCADE, verbose_name='药品管理员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 新增创建时间字段
    
    STATUS_CHOICES = [
            ('pending', '待审核'),
            ('approved', '已审核'),
            ('stored', '已入库'),
            ('rejected', '已拒绝'),
        ]

    class Meta:
        db_table = 'purchase'
        verbose_name = '进货记录'
        verbose_name_plural = '进货记录'

    def __str__(self):
        return self.purchase_id
    
    @property
    def total_amount(self):
        """计算采购总金额"""
        return self.quantity * self.price

class Sale(models.Model):
    sale_id = models.CharField(max_length=50, primary_key=True, verbose_name='销售编号')
    drug = models.ForeignKey('supply.Drug', on_delete=models.CASCADE, verbose_name='药品')
    hospital = models.ForeignKey('hospital.Hospital', on_delete=models.CASCADE, verbose_name='医院')
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE, verbose_name='患者')
    quantity = models.IntegerField(null=False, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='价格')
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name='状态')
    admin = models.ForeignKey('hospital.DrugAdmin', on_delete=models.CASCADE, verbose_name='药品管理员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 新增创建时间字段

    class Meta:
        db_table = 'sale'
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录'

    def __str__(self):
        return self.sale_id
    @property
    def total_amount(self):
        """计算采购总金额"""
        return self.quantity * self.price

class Prescription(models.Model):
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE, verbose_name='患者')
    drug = models.ForeignKey('supply.Drug', on_delete=models.CASCADE, verbose_name='药品')
    time = models.DateTimeField(blank=True, null=True, verbose_name='开药时间')
    usage = models.CharField(max_length=255, blank=True, null=True, verbose_name='用法')
    doctor = models.ForeignKey('hospital.Doctor', on_delete=models.CASCADE, verbose_name='医生')

    class Meta:
        db_table = 'prescription'
        verbose_name = '用药记录'
        verbose_name_plural = '用药记录'

    def __str__(self):
        return f"Prescription for {self.patient.name} - {self.drug.name}"
    
