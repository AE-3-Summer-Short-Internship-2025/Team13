CREATE TABLE families (
    id INT PRIMARY KEY AUTO_INCREMENT,
    family_name VARCHAR(100) NOT NULL,
    kids INT NOT NULL,
    adults INT NOT NULL,
    prefecture VARCHAR(50),
    city_ward VARCHAR(100),
    block_number VARCHAR(50),
    building VARCHAR(100),
    postal_code VARCHAR(10)
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    phone VARCHAR(16) UNIQUE,
    rakuten_id VARCHAR(100) UNIQUE,
    family_id INT,
    FOREIGN KEY (family_id) REFERENCES families(id)
);

CREATE TABLE items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    owner_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
quantity
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
