CREATE TABLE batch_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    message TEXT,
    created_at DATETIME NOT NULL,
    INDEX idx_created_at (created_at)
);