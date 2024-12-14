USE epicevents;

INSERT INTO users (name_lastname, department, password, email, token, secret_key)
VALUES
('Cauquil Bastien', 'COM', 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae', 'bastien@example.com', NULL, NULL),
('Dupont Marie', 'GES', 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae', 'marie.dupont@example.com', NULL, NULL),
('Martin Jean', 'SUP', 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae', 'jean.martin@example.com', NULL, NULL);

INSERT INTO customers (name_lastname, email, phone, business_name, date_first_contact, last_date_update, sales_contact)
VALUES
('Client One', 'client1@example.com', 1234567890, 'Acme Corp', NOW(), NOW(), 1),
('Client Two', 'client2@example.com', 9876543210, 'Beta Inc', NOW(), NOW(), 2);

INSERT INTO contracts (customer_id, total_amount, settled_amount, creation_date, contract_sign)
VALUES
(1, 1000, 200, NOW(), FALSE),
(2, 5000, 1000, NOW(), TRUE);

INSERT INTO events (contract_id, title, date_hour_start, date_hour_end, address, guests, notes, support_contact)
VALUES
(1, 'Kick-off Meeting', NOW(), DATE_ADD(NOW(), INTERVAL 2 HOUR), '123 Main St', 10, 'Initial client meeting', 3),
(2, 'Follow-up Event', NOW(), DATE_ADD(NOW(), INTERVAL 3 HOUR), '456 Broad Ave', 25, 'Second meeting with stakeholders', 3);
