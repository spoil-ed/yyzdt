-- 智药医典通数据库建表 SQL 脚本（方案一版）
-- 字符集、时区设置
CREATE DATABASE zhiyao_db DEFAULT CHARACTER SET utf8mb4;
USE zhiyao_db;
SET NAMES utf8mb4;
SET time_zone = '+00:00';

-- 1. 药企表
DROP TABLE IF EXISTS pharma;
CREATE TABLE pharma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(100),
    address VARCHAR(255),
    founded DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 药品表
DROP TABLE IF EXISTS drug;
CREATE TABLE drug (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    spec VARCHAR(50),
    category VARCHAR(100),
    expiration DATE,
    manufacturer VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 医院表
DROP TABLE IF EXISTS hospital;
CREATE TABLE hospital (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255),
    contact VARCHAR(100),
    grade VARCHAR(50),
    founded DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 医生表
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

-- 5. 患者表
DROP TABLE IF EXISTS patient;
CREATE TABLE patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birth DATE,
    contact VARCHAR(100),
    address VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 药品管理员表
DROP TABLE IF EXISTS drug_admin;
CREATE TABLE drug_admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hospital_id INT NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. 药品供应表
DROP TABLE IF EXISTS supply;
CREATE TABLE supply (
    batch_code VARCHAR(50) PRIMARY KEY,
    pharma_id INT NOT NULL,
    drug_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (pharma_id) REFERENCES pharma(id),
    FOREIGN KEY (drug_id) REFERENCES drug(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. 库存表（移除quantity字段）
DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    drug_id INT NOT NULL,
    hospital_id INT NOT NULL,
    threshold INT CHECK (threshold >= 0),
    initial_quantity INT DEFAULT 0 CHECK (initial_quantity >= 0),
    PRIMARY KEY (drug_id, hospital_id),
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. 进货记录表（新增时间字段）
DROP TABLE IF EXISTS purchase;
CREATE TABLE purchase (
    purchase_id VARCHAR(50) PRIMARY KEY,
    drug_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    status VARCHAR(50),
    admin_id INT NOT NULL,
    purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (admin_id) REFERENCES drug_admin(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. 销售记录表（新增时间字段）
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
    sale_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drug_id) REFERENCES drug(id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(id),
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (admin_id) REFERENCES drug_admin(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. 用药记录表
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

-- 12. 医生与医院关系表
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

-- 14. 药企药品供应关系表
DROP TABLE IF EXISTS pharma_drug_supply;
CREATE TABLE pharma_drug_supply (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pharma_id INT NOT NULL,
    drug_id INT NOT NULL,
    supply_start_date DATE NOT NULL,
    supply_end_date DATE,
    is_primary_supplier BOOLEAN DEFAULT FALSE,
    certification_number VARCHAR(100),
    remark VARCHAR(255),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pharma_id) REFERENCES pharma(id) ON DELETE CASCADE,
    FOREIGN KEY (drug_id) REFERENCES drug(id) ON DELETE CASCADE,
    UNIQUE KEY uk_pharma_drug (pharma_id, drug_id),
    INDEX idx_pharma_id (pharma_id),
    INDEX idx_drug_id (drug_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='药企与药品供应关系表，记录药企能供应的药品种类及相关信息';

-- =============================
-- ✅ 触发器（基于视图计算库存）
-- =============================
DROP TRIGGER IF EXISTS trg_check_inventory_threshold;
DELIMITER $$
CREATE TRIGGER trg_check_inventory_threshold
AFTER INSERT ON sale
OR AFTER UPDATE ON sale
OR AFTER INSERT ON purchase
OR AFTER UPDATE ON purchase
FOR EACH ROW
BEGIN
    DECLARE v_drug_id INT;
    DECLARE v_hospital_id INT;
    DECLARE v_current_quantity INT;
    DECLARE v_threshold INT;
    
    IF (TG_TABLE_NAME = 'sale') THEN
        SET v_drug_id = NEW.drug_id;
        SET v_hospital_id = NEW.hospital_id;
    ELSE
        SET v_drug_id = NEW.drug_id;
        SET v_hospital_id = (SELECT hospital_id FROM drug_admin WHERE id = NEW.admin_id);
    END IF;
    
    SELECT current_quantity, threshold 
    INTO v_current_quantity, v_threshold
    FROM v_current_inventory
    WHERE drug_id = v_drug_id AND hospital_id = v_hospital_id;
    
    IF v_current_quantity < v_threshold THEN
        INSERT INTO warning_log (message, created_at)
        VALUES (CONCAT('药品ID ', v_drug_id, ' 在医院ID ', v_hospital_id, ' 库存低于预警阈值，当前数量：', v_current_quantity), NOW());
    END IF;
END$$
DELIMITER ;

-- 预警日志表
DROP TABLE IF EXISTS warning_log;
CREATE TABLE warning_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  message VARCHAR(255),
  created_at DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================
-- 📊 视图（实时计算库存）
-- =============================
-- 1. 当前库存实时计算视图
DROP VIEW IF EXISTS v_current_inventory;
CREATE VIEW v_current_inventory AS
SELECT 
    d.id AS drug_id,
    d.name AS drug_name,
    h.id AS hospital_id,
    h.address AS hospital_address,
    i.threshold AS inventory_threshold,
    i.initial_quantity AS initial_stock,
    (
        i.initial_quantity 
        + COALESCE(SUM(p.quantity), 0) 
        - COALESCE(SUM(s.quantity), 0)
    ) AS current_quantity
FROM drug d
CROSS JOIN hospital h
LEFT JOIN inventory i ON i.drug_id = d.id AND i.hospital_id = h.id
LEFT JOIN purchase p ON p.drug_id = d.id 
    AND EXISTS (SELECT 1 FROM drug_admin da WHERE da.id = p.admin_id AND da.hospital_id = h.id)
LEFT JOIN sale s ON s.drug_id = d.id AND s.hospital_id = h.id
GROUP BY d.id, d.name, h.id, h.address, i.threshold, i.initial_quantity;

-- 2. 总库存统计视图
DROP VIEW IF EXISTS v_total_inventory;
CREATE VIEW v_total_inventory AS
SELECT d.name AS drug_name, SUM(vi.current_quantity) AS total_quantity
FROM v_current_inventory vi
JOIN drug d ON vi.drug_id = d.id
GROUP BY d.name;

-- 3. 医院采购金额视图
DROP VIEW IF EXISTS v_hospital_purchase_total;
CREATE VIEW v_hospital_purchase_total AS
SELECT h.id AS hospital_id, h.address, SUM(p.quantity * p.price) AS total_spent
FROM purchase p
JOIN drug_admin da ON p.admin_id = da.id
JOIN hospital h ON da.hospital_id = h.id
GROUP BY h.id, h.address;

-- =============================
-- 🔐 权限控制（不变）
-- =============================
CREATE USER 'gov_viewer'@'%' IDENTIFIED BY 'secure_pwd';
GRANT SELECT ON zhiyao_db.* TO 'gov_viewer'@'%';
CREATE USER 'med_admin'@'%' IDENTIFIED BY 'admin_pwd';
GRANT ALL PRIVILEGES ON zhiyao_db.* TO 'med_admin'@'%';
FLUSH PRIVILEGES;