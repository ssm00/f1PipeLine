CREATE TABLE image_tag (
    image_sequence BIGINT,
    tag_sequence BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (image_sequence, tag_sequence),
    FOREIGN KEY (image_sequence) REFERENCES image (sequence) ON DELETE CASCADE,
    FOREIGN KEY (tag_sequence) REFERENCES tag (sequence) ON DELETE CASCADE,
    INDEX idx_tag_sequence (tag_sequence)
);
use f1pipeline_dev;
select * from batch_jobs;