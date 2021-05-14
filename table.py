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

create_table_message = '''create table message(
    message_id INTEGER primary key AUTOINCREMENT,
    content varchar(500) not null,
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    userid INTEGER not null,
    recipientid INTEGER not null ,
  	constraint fk_usid foreign key (userid) references users(userid)
  	CONSTRAINT fk_usid_1 foreign key (recipientid) references users(userid)
);'''


cursor.execute(create_table_users)
cursor.execute(create_table_message)
print("tables created")

connect.commit()
connect.close()