# 项目名称

这是复旦大学数据库与实现[DATA130039A]的期末课程设计。“智药医典通” 是一个基于 Django 框架开发的药品供应与使用管理平台，面向药企、医院、医生、患者和政府监管部门，支持从药品生产到用药全生命周期的数据记录与管理。该系统结合国家“互联网+医疗”及“数据要素”发展战略，具有高实用性和推广潜力，适用于药品供应链管理、库存管理和监管审查。本 README 文件详细说明了开发环境的设置、数据库初始化流程、测试数据导入方法、项目运行步骤与使用方法，以及团队成员的分工情况。

## 开发环境

运行和开发本项目需要以下环境：

- **操作系统**：Windows 11。
- **编程语言**：
  - Python 3.11.11（已确认）。
  - JavaScript（Node.js 22.5.1 已安装，但当前无 npm 依赖，前端未初始化）。

- **框架和库**：
  - Django 4.2.5（Web 框架）。
  - mysqlclient 2.2.3 和 PyMySQL 1.1.1（MySQL 数据库连接）。
  - django-pandas 0.6.6、numpy 1.26.4、pandas 2.2.1（数据处理相关）。
  - faker 37.4.0（随机数据生成）。

- **数据库**：MySQL 8.0.41（已确认）。
- **其他工具**：
  - GitHub Desktop 用于提交与下载代码。
  - Visual Studio Code（已确认，作为代码编辑器）。
  - Python 虚拟环境（已确认，名为 `db`）

请确保在继续之前安装并配置好上述工具。

## 数据库初始化流程

按照以下步骤初始化数据库：

按照以下步骤初始化 MySQL 数据库：

1. **安装 MySQL**：
   - 可通过以下命令验证 MySQL 8.0.41 安装完成：
     ```bash
     mysql --version
     ```

2. **创建数据库**：
   - 打开终端并运行：
     ```bash
     mysql -u root -p
     ```
   - 输入 MySQL 根用户密码后，创建数据库：
     ```sql
     CREATE DATABASE meme;
     ```

3. **设置**：
   - 在 Django 的 `database\settings.py` 文件中配置数据库：
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'meme',
             'USER': 'root',
             'PASSWORD': '你的密码',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```


4. **运行数据库迁移**：
   - 在项目根目录下，激活虚拟环境：
     ```bash
     conda activate db
     ```
   - 运行 Django 迁移命令以创建表结构：
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

## 测试数据导入方法

运行以下命令导入测试数据以在开发或测试中填充数据库：

- 确保一定要先运行 Django 迁移命令以创建表结构
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- 然后运行以下命令导入测试数据：
  ```bash
  python manage.py populate_test_data
  ```

## 项目运行步骤与使用方法

按照以下步骤在本地运行项目：

1. **克隆仓库**（如果使用 Git）：
   ```bash
   git clone https://github.com/spoil-ed/yyzdt.git
   cd meme
   ```

2. **激活虚拟环境**：
   ```bash
   conda activate db
   ```

3. **安装 Python 依赖**：
   - 使用提供的 `requirements.txt`：
     ```bash
     pip install -r requirements.txt
     ```

4. **启动 Django 开发服务器**：
   ```bash
   python manage.py runserver
   ```

5. **访问应用程序**：
   - 打开浏览器，访问 `http://localhost:8000`。
   - 登录页面：`http://localhost:8000/login/`。
   - 采用账号密码 admin/testpassword123 登录。
   - 其他账号随机生成，由用户管理页面得到账号，密码皆为 testpassword123。
## 小组成员

项目由以下团队成员开发：

- **余星磊** 项目构建、前后端代码编写、期末展示准备、辅助编写期末报告
- **黄亦绪** 项目构建、前后端代码编写、期末展示准备、辅助编写期末报告
- **金力铖** 期中期末汇报材料准备、期末报告主要内容编写
- **金潇睿** 期中期末汇报材料准备、辅助编写期末报告
