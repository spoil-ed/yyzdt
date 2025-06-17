-- 智药医典通数据库建表 SQL 脚本
-- 字符集、时区设置
CREATE DATABASE zhiyao_db DEFAULT CHARACTER SET utf8mb4;
USE zhiyao_db;
SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- 1. 药企
DROP TABLE IF EXISTS pharma;
CREATE TABLE pharma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(100),
    address VARCHAR(255),
    founded DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 药品
DROP TABLE IF EXISTS drug;
CREATE TABLE drug (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    spec VARCHAR(50),
    category VARCHAR(100),
    expiration DATE,
    manufacturer VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 医院
DROP TABLE IF EXISTS hospital;
CREATE TABLE hospital (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255),
    contact VARCHAR(100),
    grade VARCHAR(50),
    founded DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 医生
DROP TABLE IF EXISTS doctor;
CREATE TABLE doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    title VARCHAR(50),
    contact VARCHAR(100),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 患者
DROP TABLE IF EXISTS patient;
CREATE TABLE patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birth DATE,
    contact VARCHAR(100),
    address VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 药品管理员
DROP TABLE IF EXISTS drug_admin;
CREATE TABLE drug_admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hospital_id INT NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. 药品供应
DROP TABLE IF EXISTS supply;
CREATE TABLE supply (
    batch_code VARCHAR(50) PRIMARY KEY,
    pharma_id INT NOT NULL,
    drug_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (pharma_id) REFERENCES pharma(id),
    FOREIGN KEY (drug_id) REFERENCES drug(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. 库存
DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    drug_id INT NOT NULL,
    hospital_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    threshold INT CHECK (threshold >= 0),
    PRIMARY KEY (drug_id, hospital_id),
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. 进货记录
DROP TABLE IF EXISTS purchase;
CREATE TABLE purchase (
    purchase_id VARCHAR(50) PRIMARY KEY,
    drug_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    status VARCHAR(50),
    admin_id INT NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (admin_id) REFERENCES drug_admin(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. 销售记录
DROP TABLE IF EXISTS sale;
CREATE TABLE sale (
    sale_id VARCHAR(50) PRIMARY KEY,
    drug_id INT NOT NULL,
    hospital_id INT NOT NULL,
    patient_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    status VARCHAR(50),
    admin_id INT NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (admin_id) REFERENCES drug_admin(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. 用药记录
DROP TABLE IF EXISTS prescription;
CREATE TABLE prescription (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    drug_id INT NOT NULL,
    time DATETIME,
    `usage` VARCHAR(255),
    doctor_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. 医生与医院管理关系
DROP TABLE IF EXISTS doctor_hospital;
CREATE TABLE doctor_hospital (
    doctor_id INT NOT NULL,
    hospital_id INT NOT NULL,
    PRIMARY KEY (doctor_id, hospital_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. 用户表
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    name VARCHAR(100),
    role ENUM('admin', 'doctor', 'drug_admin', 'patient') NOT NULL,
    doctor_id INT,
    drug_admin_id INT,
    patient_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    is_superadmin BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    date_joined DATETIME,
    FOREIGN KEY (doctor_id) REFERENCES doctor(id),
    FOREIGN KEY (drug_admin_id) REFERENCES drug_admin(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================
-- ✅ 触发器
-- =============================
-- 自动插入库存提醒（若数量低于阈值）
DROP TRIGGER IF EXISTS trg_check_inventory_threshold;
DELIMITER $$
CREATE TRIGGER trg_check_inventory_threshold
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
  IF NEW.quantity < NEW.threshold THEN
    INSERT INTO warning_log (message, created_at)
    VALUES (CONCAT('药品ID ', NEW.drug_id, ' 在医院ID ', NEW.hospital_id, ' 库存低于预警阈值'), NOW());
  END IF;
END$$
DELIMITER ;

-- 创建预警日志表（如无）
DROP TABLE IF EXISTS warning_log;
CREATE TABLE warning_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  message VARCHAR(255),
  created_at DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================
-- 📊 视图
-- =============================
-- 各药品总库存统计视图
DROP VIEW IF EXISTS v_total_inventory;
CREATE VIEW v_total_inventory AS
SELECT d.name AS drug_name, SUM(i.quantity) AS total_quantity
FROM inventory i
JOIN drug d ON i.drug_id = d.id
GROUP BY d.name;

-- 各医院采购药品总金额
DROP VIEW IF EXISTS v_hospital_purchase_total;
CREATE VIEW v_hospital_purchase_total AS
SELECT h.id AS hospital_id, h.address, SUM(p.quantity * p.price) AS total_spent
FROM purchase p
JOIN drug_admin da ON p.admin_id = da.id
JOIN hospital h ON da.hospital_id = h.id
GROUP BY h.id, h.address;

-- =============================
-- 🔐 权限控制建议（需结合 Django 实现）
-- =============================
-- 示例：为数据库用户赋权（示意）
CREATE USER 'gov_viewer'@'%' IDENTIFIED BY 'secure_pwd';
GRANT SELECT ON zhiyao_db.* TO 'gov_viewer'@'%';
CREATE USER 'med_admin'@'%' IDENTIFIED BY 'admin_pwd';
GRANT ALL PRIVILEGES ON zhiyao_db.* TO 'med_admin'@'%';
FLUSH PRIVILEGES;