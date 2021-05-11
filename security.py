from user import User

user=[
    User(4,"bob","123")
]

username_mapping={u.username : u for u in user}

userid_mapping={u.id : u for u in user}


def authenticate(username ,password):
    user=username_mapping.get(username,None)
    if user and user.password == password:
        return user

def Indentity(payload):
    user_id=payload['identity']
    return userid_mapping.get(user_id, None)