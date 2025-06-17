from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User
from hospital.models import Doctor, Patient, DrugAdmin

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建关联的角色表记录"""
    if created:
        if instance.role == 'doctor':
            Doctor.objects.create(user=instance)
        elif instance.role == 'patient':
            Patient.objects.create(user=instance)
        elif instance.role == 'drug_admin':
            DrugAdmin.objects.create(user=instance)

@receiver(pre_save, sender=User)
def update_related_profile(sender, instance, **kwargs):
    """用户角色变更时更新关联的角色表记录"""
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            # 角色变更时，删除旧角色关联
            if old_user.role != instance.role:
                if old_user.role == 'doctor':
                    Doctor.objects.filter(user=old_user).delete()
                elif old_user.role == 'patient':
                    Patient.objects.filter(user=old_user).delete()
                elif old_user.role == 'drug_admin':
                    DrugAdmin.objects.filter(user=old_user).delete()
        except User.DoesNotExist:
            pass