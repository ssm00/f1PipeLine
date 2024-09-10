create table image(
	sequence int primary key auto_increment,
    image_source text,
    image_name text,
    image_description text,
    article_id varchar(100),
	foreign key(article_id) references article (article_id)
    );
SELECT * FROM f1pipeline.image;