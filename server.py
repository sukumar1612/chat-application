from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, Indentity
from models import User, Message
from flask_socketio import SocketIO
from threading import Lock


mutex=Lock()

app = Flask( __name__,static_url_path='/static')
api = Api(app)
app.secret_key='a24aca7a4e1686c098b34309624341f38f4c2b7f6d4fe48e1543ea62843e65fb' #generated using python secrets module

# for websockets
public = '-----BEGIN PUBLIC KEY-----\r\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClqUZ+qU/2xjOCI3GekauEjnNu\r\nU1tey0S9ptz3veEo9eCLSBm5A/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5\r\nvQKEmlJtmJnAuPSWMitJyoBeXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6\r\ns56CS5/FNFNTz0uMgQIDAQAB\r\n-----END PUBLIC KEY-----\r\n'
private='-----BEGIN RSA PRIVATE KEY-----\r\nMIICXQIBAAKBgQClqUZ+qU/2xjOCI3GekauEjnNuU1tey0S9ptz3veEo9eCLSBm5\r\nA/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5vQKEmlJtmJnAuPSWMitJyoBe\r\nXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6s56CS5/FNFNTz0uMgQIDAQAB\r\nAoGATyoDTAfw9IZmmuwBIbuO8Tt5oeEnqrcMVGzm72THsmE9OpHr6OQhs2/eM3HQ\r\n2z6EbhYyCaJgCzqg9wZWLg6YcqN6YpqGFtmvXUfaOaiOoiKR29/TGbEk5C0Zd+i5\r\noJB3USkgu/QwSCKBDgfb4bqI4hH5rZ5/IqbrBr2zIdu9XjkCQQDk6F6gaR+EpJAC\r\nhpM34hrhGwKuE4Y4ysyWC6JkHrSzy7mmQpycrTSwZT/7FN8jizEYtzTVnuX5D5ow\r\nuYlPKa+jAkEAuUSdATns2AcJ0Kv1MZ3QTWKfBOROYuuqqPZ+w9en+omHzg0vewUY\r\nqsVCo5t7roURqS6Ok0vd3Of6a60FN4kFiwJBAJugD5VnYvI/H1lYPQalRjj8sBnB\r\nVGOQHP918XW4GoqSWylZ6Dfs2gGDFLiTPBFiNILlK5qAaUGnBeFSgrO7V5kCQBac\r\nFwUVSqA6i6oZsjyx47/t7zYrnp1X4WXpXyMLaIacziQJW+gJgS8mD7Hjwb5Uowkg\r\nk2nKcnMJJHiLjv1uDW0CQQDSFXjqnn4C0WHvr4cBdeU1nF1LaBQDbaAHjLJ7B/bf\r\ngA8ecbRrrx6+yQjjXCP/8cA7Oj9YoNw6sGmiS01CPiCc\r\n-----END RSA PRIVATE KEY-----\r\n'
socketio = SocketIO(app)
session_mapping={}


jwt=JWT(app,authenticate, Indentity)   # /auth is the endpoint

item=[["4","bob"],["1","alice"],["2","jake"],["3","john"],["5","samantha"],["6","me"]]
logged_in=[]

class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('registeration.html'),200,headers)

    def post(self):
        data = request.get_json();
        u=User.insert_user(data['username'], data['email'], data['password'], data['publickey'], data['privatekey'])
        print(data['publickey'],"\n\n", data['privatekey'], "\n\n", data['password'] )
        return {"messege" : "success", "username":data['username']};

class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        data = request.get_json();
        print(data)
        x=authenticate(data['username'],data['password'])
        if(x!=None):
            print(x.id)
            state=0

            mutex.acquire()
            if x.id in logged_in:
                state=1
            else:
                logged_in.append(x.id)
            mutex.release()

            if state==0:
                return {"user_id" : x.id};
            else:
                return {"already_logged_in" : "True"};
        else:
            pass

class homepage(Resource):
    def get(self, name):
        print(name)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('homepage.html'), 200, headers)

    @jwt_required()
    def post(self, name):
        print(name)
        u=User.return_all_users()
        return {"names":u}


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(homepage,'/homepage/<name>')
@app.route("/")
def red():
    return redirect(url_for('login'))

@app.route("/logout/<name>")
def logout(name):
    i=int(name)

    mutex.acquire()
    if i in logged_in:
        logged_in.remove(i)
    mutex.release()

    return redirect(url_for('login'))


#socket control

class chat(Resource):
    def get(self, name, name1):
        print(name)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('chatroom.html'), 200, headers)

    @jwt_required()
    def post(self, name, name1):
        return {"authenticated":"True"}

api.add_resource(chat,'/homepage/<name>/<name1>')

@socketio.on('textmessages')
def create_connection(json):
    #print(request.sid)
    print('connected')
    #print(json)

    session_mapping[json['userid']]=request.sid
    print(session_mapping)
    text_hist=Message.find_by_userids(json['userid'], json['recipientid'])

    user=User.return_pub_pri_keys(json['userid'])
    recipient=User.return_pub_pri_keys(json['recipientid'])

    json['recipient_publickey']=recipient[0]
    json['user_publickey']=user[0]
    json['user_privatekey']=user[1]
    json['text_hist']=text_hist
    json['mapping']={json['userid'] : User.find_by_id(json['userid']).username, json['recipientid']:User.find_by_id(json['recipientid']).username}

    print(json)
    socketio.emit('connect_return', json, room=request.sid)


@socketio.on('sending_text')
def send_and_receive_text(json, methods=['GET', 'POST']):
    receiver_session_id = json['recipientid']

    print(str(json))

    user_name_1=User.find_by_id(json['userid']).username
    recipient_name=User.find_by_id(json['recipientid']).username

    Message.insert_message(json['userid'], json['recipientid'], json['message'])

    if(receiver_session_id not in session_mapping):
        json['userid'] = user_name_1
        socketio.emit('text_response', json, room=request.sid)
    else:
        receiver_session_id = session_mapping[json['recipientid']]
        json['userid'] = user_name_1
        json['recipientid'] = recipient_name
        socketio.emit('text_response', json, room=receiver_session_id)
        socketio.emit('text_response', json, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, port=80)

