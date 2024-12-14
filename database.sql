CREATE DATABASE IF NOT EXISTS epicevents;
USE epicevents;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_lastname VARCHAR(100) NOT NULL,
    department ENUM('COM', 'GES', 'SUP') NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    token VARCHAR(300),
    secret_key VARCHAR(300)
) ENGINE=InnoDB;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_lastname VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    business_name VARCHAR(100),
    date_first_contact TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_date_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    sales_contact INT NOT NULL,
    FOREIGN KEY (sales_contact) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    total_amount FLOAT DEFAULT 0,
    settled_amount FLOAT DEFAULT 0,
    remaining_amount FLOAT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contract_sign BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    title VARCHAR(100),
    date_hour_start TIMESTAMP,
    date_hour_end TIMESTAMP,
    address VARCHAR(255),
    guests INT DEFAULT 0,
    notes TEXT,
    support_contact INT,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (support_contact) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

DELIMITER //

-- Trigger pour calculer remaining_amount avant insertion du contrat
CREATE TRIGGER contracts_BEFORE_INSERT
BEFORE INSERT ON contracts
FOR EACH ROW
BEGIN
    SET NEW.remaining_amount = NEW.total_amount - NEW.settled_amount;
END//
  
-- Trigger pour calculer remaining_amount avant mise à jour du contrat
CREATE TRIGGER contracts_BEFORE_UPDATE
BEFORE UPDATE ON contracts
FOR EACH ROW
BEGIN
    SET NEW.remaining_amount = NEW.total_amount - NEW.settled_amount;
END//

DELIMITER ;
