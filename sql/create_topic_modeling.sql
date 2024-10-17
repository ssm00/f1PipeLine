create table topic_modeling(
	sequence int primary key auto_increment,
    topic json,
    best_topic_num int,
    best_coherence_num int,
    coherence_values text,
    created_at datetime
);

select * from topic_modeling;
alter table topic_modeling change column seq sequence int;