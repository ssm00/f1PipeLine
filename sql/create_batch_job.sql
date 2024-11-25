CREATE TABLE batch_jobs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'RUNNING', 'SUCCESS', 'FAILED'
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration int,
    formatted_duration varchar(20),
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
