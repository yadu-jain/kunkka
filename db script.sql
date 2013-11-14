CREATE TABLE IF NOT EXISTS bookings
(
	ID INT AUTO_INCREMENT PRIMARY KEY,
	booking_id INT,
	agent_id INT,
	status CHAR(2),
	from_city VARCHAR(100),
	to_city VARCHAR(100),
	journey_date DATETIME,
	booking_date DATETIME,
	amount DOUBLE(10,2),
	total_seats INT
);

CREATE TABLE IF NOT EXISTS agents
(
	agent_id INT,
	name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS ips
(
	ID INT AUTO_INCREMENT PRIMARY KEY,
	ip VARCHAR(30),
	host VARCHAR(50),
	agent_id INT 
);