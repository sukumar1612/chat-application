import sqlite3
connect = sqlite3.connect('data.db')
cursor = connect.cursor()

create_table_users = '''create table users(
    userid INTEGER primary key AUTOINCREMENT,
    username varchar(100) not null,
    email varchar(100) not null,
    password varchar(100) not null,
    public_key varchar(2000) not null,
    private_key varchar(2000) not null
);'''

create_table_messege = '''create table messege(
    messege_id INTEGER primary key AUTOINCREMENT,
    content varchar(500) not null,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    userid INTEGER not null,
  	constraint fk_usid foreign key (userid) references user(userid)
);'''

create_table_conversation='''create table conversation(
    user_id_1 INTEGER not null,
    user_id_2 INTEGER not null,
    messege_id INTEGER primary key,
  	CONSTRAINT fk_usid_1 foreign key (user_id_1) references user(userid),
  	constraint fk_usid_2 foreign key (user_id_2) references user(userid),
  	constraint fk_msid_2 foreign key (messege_id) references messege(messege_id)
);'''

print("tables created")
cursor.execute(create_table_users)
cursor.execute(create_table_messege)
cursor.execute(create_table_conversation)


connect.commit()
connect.close()