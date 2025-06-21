from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from core.models import User
from hospital.models import Hospital, Doctor, Patient, DrugAdmin
from supply.models import Pharma, Drug, Supply, Inventory, WarningLog, PharmaDrugSupply
from transaction.models import Purchase, Sale, Prescription
import random
from datetime import datetime, timedelta
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        fake = Faker('zh_CN')
        Faker.seed(0)

        # 清空现有数据
        Prescription.objects.all().delete()
        Sale.objects.all().delete()
        Purchase.objects.all().delete()
        PharmaDrugSupply.objects.all().delete()
        WarningLog.objects.all().delete()
        Inventory.objects.all().delete()
        Supply.objects.all().delete()
        Drug.objects.all().delete()
        Pharma.objects.all().delete()
        DrugAdmin.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        Hospital.objects.all().delete()
        User.objects.all().delete()

        # 创建用户
        users = []
        roles = ['doctor', 'drug_admin', 'patient', 'pharma_admin']  # 不包括 system_admin

        # 固定管理员账号
        try:
            admin = User.objects.create_user(
                username='admin',
                email=fake.email(),
                password='testpassword123',
                name=fake.name(),
                role='system_admin',
                is_active=True,
                is_superadmin=True,
                is_superuser=True,
                date_joined=timezone.now()
            )
            users.append(admin)
            self.stdout.write(self.style.SUCCESS('Created user: admin'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Failed to create user admin: {e}'))

        # 每个其他角色至少生成一个用户
        for role in roles:
            username = f"{role}1"
            try:
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpassword123',
                    name=fake.name(),
                    role=role,
                    is_active=True,
                    is_superadmin=False,
                    is_superuser=False,
                    date_joined=timezone.now()
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create user {username}: {e}'))

        # 额外生成 5 个随机角色用户
        for i in range(5):
            role = random.choice(roles)
            username = f"{role}{i+2}"
            try:
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpassword123',
                    name=fake.name(),
                    role=role,
                    is_active=True,
                    is_superadmin=False,
                    is_superuser=False,
                    date_joined=timezone.now()
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create user {username}: {e}'))

        # 创建医院
        hospitals = []
        hospital_grades = ['三级甲等', '二级', '一级']
        hospital_types = ['综合医院', '专科医院', '社区医院']
        for i in range(3):
            try:
                hospital = Hospital.objects.create(
                    name=fake.company() + '医院',
                    address=fake.address(),
                    contact=fake.phone_number()[:15],
                    grade=random.choice(hospital_grades),
                    type=random.choice(hospital_types),
                    city=fake.city(),
                    email=fake.email(),
                    description=fake.text(max_nb_chars=200),
                    founded=fake.date_between(start_date='-30y', end_date='today'),
                    status=random.choice(['合作中', '待审核', '已终止'])
                )
                hospitals.append(hospital)
                self.stdout.write(self.style.SUCCESS(f'Created hospital: {hospital.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create hospital: {e}'))

        # 创建医生
        doctors = []
        doctor_users = [u for u in users if u.role == 'doctor']
        for i, user in enumerate(doctor_users[:5]):  # 最多 5 个医生
            try:
                doctor = Doctor.objects.create(
                    user=user,
                    hospital=random.choice(hospitals),
                    name=user.name,
                    title=random.choice(['主任医师', '副主任医师', '主治医师']),
                    contact=fake.phone_number()[:15]
                )
                doctors.append(doctor)
                self.stdout.write(self.style.SUCCESS(f'Created doctor: {doctor.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create doctor for {user.name}: {e}'))

        # 创建患者
        patients = []
        patient_users = [u for u in users if u.role == 'patient']
        for i, user in enumerate(patient_users[:5]):  # 最多 5 个患者
            try:
                patient = Patient.objects.create(
                    user=user,
                    name=user.name,
                    gender=random.choice(['M', 'F']),
                    birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    contact=fake.phone_number()[:15],
                    address=fake.address()[:255]
                )
                patients.append(patient)
                self.stdout.write(self.style.SUCCESS(f'Created patient: {patient.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create patient for {user.name}: {e}'))

        # 创建药品管理员
        drug_admins = []
        drug_admin_users = [u for u in users if u.role == 'drug_admin']
        for i, user in enumerate(drug_admin_users[:3]):  # 最多 3 个药品管理员
            try:
                drug_admin = DrugAdmin.objects.create(
                    user=user,
                    name=user.name,
                    hospital=random.choice(hospitals),
                    employee_id=f'EMP{i+1:03d}'
                )
                drug_admins.append(drug_admin)
                self.stdout.write(self.style.SUCCESS(f'Created drug admin: {drug_admin.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create drug admin for {user.name}: {e}'))

        # 创建药企
        pharmas = []
        for i in range(3):
            try:
                pharma = Pharma.objects.create(
                    name=fake.company() + '药业',
                    phone=fake.phone_number()[:20],
                    address=fake.address(),
                    description=fake.text(max_nb_chars=200),
                    status=random.choice(['合作中', '待审核', '已终止']),
                    founded=fake.date_between(start_date='-30y', end_date='today'),
                    contact=fake.phone_number()[:20],
                    email=fake.email(),
                    updated_at=timezone.now()
                )
                pharmas.append(pharma)
                self.stdout.write(self.style.SUCCESS(f'Created pharma: {pharma.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create pharma: {e}'))

        # 创建药品
        drugs = []
        drug_categories = ['Analgesic', 'Antibiotic', 'Antiviral', 'Cardiovascular']
        otc_types = ['prescription', 'otc_red', 'otc_green', 'not_otc']
        medical_insurance_types = ['class_a', 'class_b', 'class_c', 'not_covered']
        for i in range(10):
            try:
                drug = Drug.objects.create(
                    name=fake.word().capitalize() + '药',
                    spec=f'{random.randint(50, 500)}mg',
                    category=random.choice(drug_categories),
                    expiration=fake.date_between(start_date='today', end_date='+2y'),
                    manufacturer=fake.company(),
                    common_name=fake.word().capitalize(),
                    approval_number=f'H{random.randint(10000000, 99999999)}',
                    dosage_form=random.choice(['Tablet', 'Capsule', 'Injection']),
                    status=random.choice(['active', 'pending', 'inactive']),
                    storage_condition=random.choice(['Room temperature', 'Cool dry place']),
                    shelf_life=random.randint(12, 36),
                    otc_type=random.choice(otc_types),
                    medical_insurance=random.choice(medical_insurance_types)
                )
                drugs.append(drug)
                self.stdout.write(self.style.SUCCESS(f'Created drug: {drug.name}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create drug: {e}'))

        # 创建供应
        supplies = []
        for i in range(10):
            try:
                supply = Supply.objects.create(
                    batch_code=f'BATCH{i+1:03d}',
                    pharma=random.choice(pharmas),
                    drug=random.choice(drugs),
                    quantity=random.randint(100, 1000)
                )
                supplies.append(supply)
                self.stdout.write(self.style.SUCCESS(f'Created supply: {supply.batch_code}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create supply: {e}'))

        # 初始化库存
        for hospital in hospitals:
            for drug in drugs:
                try:
                    inventory, created = Inventory.objects.get_or_create(
                        hospital=hospital,
                        drug=drug,
                        defaults={
                            'warning_threshold': 100,
                            'current_quantity': 1000,  # 固定初始库存为 1000
                            'last_updated': timezone.now()
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created inventory for {hospital.name} - {drug.name}'))
                    else:
                        inventory.current_quantity = max(inventory.current_quantity, 1000)
                        inventory.save()
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create inventory: {e}'))

        # 创建预警日志
        for i in range(5):
            try:
                inventory = Inventory.objects.order_by('?').first()
                WarningLog.objects.create(
                    message=f'{inventory.drug.name} inventory low at {inventory.hospital.name}',
                    created_at=timezone.now() - timedelta(days=random.randint(1, 30))
                )
                self.stdout.write(self.style.SUCCESS(f'Created warning log: {i+1}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create warning log: {e}'))

        # 创建药企药品供应关系
        used_combinations = set()
        max_combinations = len(pharmas) * len(drugs)
        num_records = min(10, max_combinations)
        for i in range(num_records):
            while True:
                pharma = random.choice(pharmas)
                drug = random.choice(drugs)
                if (pharma.id, drug.id) not in used_combinations:
                    used_combinations.add((pharma.id, drug.id))
                    break
            try:
                PharmaDrugSupply.objects.create(
                    pharma=pharma,
                    drug=drug,
                    supply_start_date=fake.date_between(start_date='-1y', end_date='today'),
                    supply_end_date=fake.date_between(start_date='today', end_date='+1y') if random.choice([True, False]) else None,
                    is_primary_supplier=random.choice([True, False]),
                    certification_number=f'CERT{i+1:03d}',
                    remark=fake.text(max_nb_chars=100),
                    create_time=timezone.now(),
                    update_time=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Created pharma drug supply: {i+1}'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'Failed to create pharma drug supply: {e}'))

        # 创建采购记录
        purchase_statuses = ['待审核', '已审核', '已入库', '已拒绝']
        if not drug_admins:
            self.stdout.write(self.style.WARNING('No drug admins available, skipping purchase creation'))
        else:
            for i in range(10):
                drug = random.choice(drugs)
                hospital = random.choice(hospitals)
                try:
                    purchase = Purchase.objects.create(
                        purchase_id=f'PUR{i+1:03d}',
                        drug=drug,
                        pharma=random.choice(pharmas),
                        hospital=hospital,
                        quantity=500,  # 固定采购量为 500
                        price=round(random.uniform(5.0, 50.0), 2),
                        status='待审核',  # 确保采购已入库
                        admin=random.choice(drug_admins),
                        create_time=timezone.now() - timedelta(days=random.randint(1, 30))
                    )
                    # 更新库存
                    inventory, created = Inventory.objects.get_or_create(
                        hospital=hospital,
                        drug=drug,
                        defaults={'warning_threshold': 100, 'current_quantity': 0}
                    )
                    if purchase.status == '已审核':
                        inventory.current_quantity += purchase.quantity
                        inventory.save()
                    self.stdout.write(self.style.SUCCESS(f'Created purchase: {purchase.purchase_id}'))
                except (IntegrityError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create purchase {i+1:03d}: {e}'))

        # 创建销售记录
        sale_statuses = ['待支付', '已支付', '已取药']
        if not drug_admins:
            self.stdout.write(self.style.WARNING('No drug admins available, skipping sale creation'))
        else:
            for i in range(10):
                hospital = random.choice(hospitals)
                drug = random.choice(drugs)
                inventory = Inventory.objects.filter(hospital=hospital, drug=drug).first()
                if inventory and inventory.current_quantity > 0:
                    max_quantity = min(inventory.current_quantity, 50)
                    quantity = random.randint(1, max_quantity)
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped sale {i+1:03d}: No sufficient inventory for {drug.name} at {hospital.name}'))
                    continue
                try:
                    sale = Sale.objects.create(
                        sale_id=f'SALE{i+1:03d}',
                        drug=drug,
                        hospital=hospital,
                        patient=random.choice(patients),
                        quantity=quantity,
                        price=round(random.uniform(10.0, 100.0), 2),
                        status=random.choice(sale_statuses),
                        admin=random.choice(drug_admins),
                        create_time=timezone.now() - timedelta(days=random.randint(1, 30))
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created sale: {sale.sale_id}'))
                except (IntegrityError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create sale {i+1:03d}: {e}'))
                    continue

        # 创建处方记录
        for i in range(10):
            try:
                prescription = Prescription.objects.create(
                    patient=random.choice(patients),
                    drug=random.choice(drugs),
                    time=timezone.now() - timedelta(days=random.randint(1, 30)),
                    usage=fake.sentence(nb_words=5),
                    doctor=random.choice(doctors)
                )
                self.stdout.write(self.style.SUCCESS(f'Created prescription: {i+1}'))
            except (IntegrityError, ValueError) as e:
                self.stdout.write(self.style.ERROR(f'Failed to create prescription {i+1}: {e}'))

        self.stdout.write(self.style.SUCCESS('Test data population completed!'))