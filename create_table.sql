use fund;
create table fund (
	id int auto_increment primary key,
    fcid char(10),
    name varchar(20) character set utf8mb4,
    management float default 0.00,
    custodial float default 0.00,
    distribution float default 0.00);