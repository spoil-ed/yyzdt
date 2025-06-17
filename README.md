本 Django 框架基于 https://docs.djangoproject.com/zh-hans/5.2/intro/tutorial01/ 教程编写。
以及视频教学 [Django 教程](https://www.bilibili.com/video/BV1NL41157ph)

首先，输入命令创建项目
```shell
django-admin startproject database Yao-Duo-Duo
```

用指令运行项目
```shell
python manage.py runserver
```

创建应用
```shell
py manage.py startapp supply
py manage.py startapp hospital
py manage.py startapp transaction
py manage.py startapp core
``` 

注册应用

编写 URL 映射

编写视图函数

### 

安装第三方模块
```shell
pip install mysqlclient
```

执行命令同步数据库
```shell
python manage.py makemigrations
python manage.py migrate
```

要将智药医典通数据库的主要表划分为两到三部分，可以根据业务逻辑、功能模块或数据关联性进行分组。以下是分析和建议的操作步骤：

### 分析
数据库包含12个主要表和1个日志表，涉及药企、药品、医院、医生、患者、药品管理、库存、交易等功能。划分的依据可以是：
1. **功能模块**：如药品管理、医院管理、交易记录。
2. **数据关联性**：如哪些表之间有强外键关系或频繁联表查询。
3. **业务场景**：如监管、医院内部管理、供应链。

根据表的功能和关联性，建议以下两种划分方式：

---

### 方案一：按功能模块划分为三部分
将表分为**药品供应链**、**医院与医疗管理**、**交易与记录**三个模块，逻辑清晰，适合分开管理或模块化开发。

#### 1. 药品供应链模块
包含与药品生产、供应、库存相关的表：
- `pharma`（药企）
- `drug`（药品）
- `supply`（药品供应）
- `inventory`（库存）
- `warning_log`（库存预警日志）

**理由**：这些表围绕药品的生产、供应和库存管理，数据流从药企到医院库存，适合供应链管理场景。

#### 2. 医院与医疗管理模块
包含与医院、医生、患者相关的表：
- `hospital`（医院）
- `doctor`（医生）
- `patient`（患者）
- `drug_admin`（药品管理员）
- `doctor_hospital`（医生与医院管理关系）

**理由**：这些表聚焦于医院内部的组织结构和人员管理，适合医院管理场景。

#### 3. 交易与记录模块
包含与药品交易和用药记录相关的表：
- `purchase`（进货记录）
- `sale`（销售记录）
- `prescription`（用药记录）

**理由**：这些表记录药品的采购、销售和处方使用，适合交易和监管场景。

#### 操作步骤
1. **逻辑分组**：
   - 在代码或文档中明确上述分组，更新数据库设计文档。
   - 例如，Django 模型可按模块组织在不同文件中，如 `supply/models.py`、`hospital/models.py`、`transaction/models.py`。

2. **视图调整**：
   - 确保视图（如 `v_total_inventory`、`v_hospital_purchase_total`）按模块引用对应表。
   - 如 `v_total_inventory` 属于供应链模块，`v_hospital_purchase_total` 涉及交易模块。

3. **权限分配**：
   - 为每个模块设置不同权限。例如：
     - 供应链模块：只允许药企和库存管理员访问。
     - 医院管理模块：医院管理员和医生访问。
     - 交易模块：药品管理员和监管机构访问。
   - 在 Django 中通过 `auth_permission` 或自定义权限类实现。

4. **数据库分区（可选）**：
   - 若数据量大，可将不同模块的表存储在不同数据库实例或 schema 中，使用 Django 的多数据库配置（`settings.DATABASES`）。

```
Yao-Duo-Duo/
├── database/
│   ├── urls.py
│   ├── settings.py
├── core/
│   ├── templates/core/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   ├── static/ (可能为空)
│   ├── views.py
│   ├── urls.py
│   ├── models.py (可能为空，使用 auth.User)
├── hospital/
│   ├── templates/hospital/ (可能包含 doctor_list.html 等)
│   ├── static/
│   ├── views.py
│   ├── urls.py
│   ├── models.py (可能包含 Doctor, Hospital, Patient)
├── supply/
│   ├── templates/supply/ (可能包含 pharma_list.html 等)
│   ├── static/
│   ├── views.py
│   ├── urls.py
│   ├── models.py (可能包含 Pharmacy, Drug, Inventory)
├── transaction/
│   ├── templates/transaction/ (可能包含 purchase_list.html 等)
│   ├── static/
│   ├── views.py
│   ├── urls.py
│   ├── models.py (可能包含 Purchase, Sale, Prescription)
├── templates/ (项目级模板，可能包含 login.html 等)
├── static/ (项目级静态文件)
```