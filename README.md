# Chat application

A basic chat application made using flask and javascript

## Overview

#### The chat application serves the following html pages

- Registeration page
![Features](https://github.com/sukumar1612/chat-application/blob/master/registeration.PNG)

- Login page
![Features](https://github.com/sukumar1612/chat-application/blob/master/login.PNG)

- Homepage page
![Features](https://github.com/sukumar1612/chat-application/blob/master/homepage.PNG)

- Chatroom page
![Features](https://github.com/sukumar1612/chat-application/blob/master/chatroom.PNG)

## Features
- User authentication and session management 

- End to End encryption using ECDH

- Passwords stored as Hash files

- One-to-one messaging

- SocketIO for sending messages 

- Messages are stored in the database encrypted

- Built using relational database (SQLite)

- Server follows Rest principles

## Installation
### On Windows
- Install anaconda

- Open cmd

- Create a virtual environment using conda
```bash
conda create -n environment_name
```

- Activate virtual environment
```bash
conda activate environment_name
```

- Install python version 3.9.4
```bash
conda install python=3.9.4
```

#### To run on local machine comment uwsgi in requirements.txt

- Install necessary packages inside virtual environment
```bash
pip install -r requirements.txt
```


## Usage
#### Inside virtual environment

- Run the server
```bash
python server.py
```

- Open the browser and type 127.0.0.1 then press Enter
- Register user by clicking the link below the log in button in the login page
- Put correct username and password in the login page
- Log in to see the list of users
- select a user and chat 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update requirements.txt as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
