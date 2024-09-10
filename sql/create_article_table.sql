create table article(
	sequence int primary key auto_increment,
    article_id varchar(255) unique,
    original_title varchar(255),
    original_content text,
    href text,
    article_type varchar(50),
    translate_content text
    );
    
SELECT * FROM f1pipeline.article;
