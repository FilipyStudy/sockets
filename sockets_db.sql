create schema python_sockets;

use python_sockets;
drop table login;

drop table action_logs;
show tables;

create table login (
	id int not null auto_increment,
    username varchar(32) not null,
    psw text not null,
    hash_check text not null,
    primary key (id)
);

create table action_logs (
	username_id int not null,
    username varchar(32) not null,
    act text not null,
    foreign key (username_id) references login(id) on update cascade
);

insert into login (username, psw, hash_check) values ("admin", 
											      "d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892", 
                                                  "d7c9be51056b8d631a3940a66c85fd7b180c1db12bff83d039eb0e89d2de8c33");
                                                  
                                                  
                                                  
select * from login where username = "admin";