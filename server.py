from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, Indentity
from models import User, Message
from flask_socketio import SocketIO
from threading import Lock
import secrets
#comment this if tables are already created
#import table

#configurations
mutex=Lock()
app = Flask( __name__,static_url_path='/static')
api = Api(app)
app.secret_key='a24aca7a4e1686c098b34309624341f38f4c2b7f6d4fe48e1543ea62843e65fb' #generated using python secrets module
public = '-----BEGIN PUBLIC KEY-----\r\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClqUZ+qU/2xjOCI3GekauEjnNu\r\nU1tey0S9ptz3veEo9eCLSBm5A/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5\r\nvQKEmlJtmJnAuPSWMitJyoBeXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6\r\ns56CS5/FNFNTz0uMgQIDAQAB\r\n-----END PUBLIC KEY-----\r\n'
private='-----BEGIN RSA PRIVATE KEY-----\r\nMIICXQIBAAKBgQClqUZ+qU/2xjOCI3GekauEjnNuU1tey0S9ptz3veEo9eCLSBm5\r\nA/YOf14cvZyLespVQxx+cS1yBPi0rVX6xlwO3Ae5vQKEmlJtmJnAuPSWMitJyoBe\r\nXLHAfKvy6HHmulTxJ44TxYf+vjK85KShK9Z1Kqf6s56CS5/FNFNTz0uMgQIDAQAB\r\nAoGATyoDTAfw9IZmmuwBIbuO8Tt5oeEnqrcMVGzm72THsmE9OpHr6OQhs2/eM3HQ\r\n2z6EbhYyCaJgCzqg9wZWLg6YcqN6YpqGFtmvXUfaOaiOoiKR29/TGbEk5C0Zd+i5\r\noJB3USkgu/QwSCKBDgfb4bqI4hH5rZ5/IqbrBr2zIdu9XjkCQQDk6F6gaR+EpJAC\r\nhpM34hrhGwKuE4Y4ysyWC6JkHrSzy7mmQpycrTSwZT/7FN8jizEYtzTVnuX5D5ow\r\nuYlPKa+jAkEAuUSdATns2AcJ0Kv1MZ3QTWKfBOROYuuqqPZ+w9en+omHzg0vewUY\r\nqsVCo5t7roURqS6Ok0vd3Of6a60FN4kFiwJBAJugD5VnYvI/H1lYPQalRjj8sBnB\r\nVGOQHP918XW4GoqSWylZ6Dfs2gGDFLiTPBFiNILlK5qAaUGnBeFSgrO7V5kCQBac\r\nFwUVSqA6i6oZsjyx47/t7zYrnp1X4WXpXyMLaIacziQJW+gJgS8mD7Hjwb5Uowkg\r\nk2nKcnMJJHiLjv1uDW0CQQDSFXjqnn4C0WHvr4cBdeU1nF1LaBQDbaAHjLJ7B/bf\r\ngA8ecbRrrx6+yQjjXCP/8cA7Oj9YoNw6sGmiS01CPiCc\r\n-----END RSA PRIVATE KEY-----\r\n'
socketio = SocketIO(app)


#variables used to keep track of user data

session_mapping={}                                                                                                      #keeps track of websocket sessions
logged_in=[]                                                                                                            #keeps track of logged_in users
key_mapping={}                                                                                                          #maps 16 byte tokens to userids


jwt=JWT(app,authenticate, Indentity)                                                                                    #initialises jwt function
                                                                                                                        # /auth is the endpoint for jwt authorisation


#api for registeration
class Register(Resource):
    def get(self):                                                                                                      #returns registeration.html file on get request
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('registeration.html'),200,headers)

    def post(self):                                                                                                     #inserts data from the submitted form into user table
        data = request.get_json();

        username=User.find_by_username(data['username'])                                                                #to check if username already exists
        if(username==None):
            u=User.insert_user(data['username'], data['email'], data['password'], data['publickey'], data['privatekey'])
            #print(data['publickey'],"\n\n", data['privatekey'], "\n\n", data['password'] )
            return {"messege" : "success", "username":data['username']};
        else:
            return {"messege": "username already exists"};

#api for login
class Login(Resource):
    def get(self):                                                                                                      #returns login.html file on get request
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    def post(self):                                                                                                     #performs authentication
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
                logged_in.append(x.id)                                                                                  #inserts userid into logged_in variable
                key_mapping[x.id]=secrets.token_hex(16)                                                                 #initialises 16byte hex token and maps it to userid
            mutex.release()

            if state==0:
                return {"user_id" : x.id, "key" : key_mapping[x.id]};                                                   #returns userid and key values user for AES encryption(the key is the password) on client side
            else:
                return {"already_logged_in" : "True"};
        else:
            pass

#api for homepage which displays all registered usernames
class homepage(Resource):
    def get(self, name):                                                                                                #returns homepage.html
        print(name)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('homepage.html'), 200, headers)

    @jwt_required()                                                                                                     #decorator for jtw authentication
    def post(self, name):                                                                                               #returns all usernames
        print(name)
        u=User.return_all_users()
        return {"names":u}


class chat(Resource):
    def get(self, name, name1):                                                                                         #returns chat_room.html
        print(name)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('chat_room.html'), 200, headers)

    @jwt_required()
    def post(self, name, name1):                                                                                        #check if jwt token is valid or not
        return {"authenticated":"True"}


class logout_force(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('logout_force.html'), 200, headers)

    def post(self):
        data = request.get_json();
        username = authenticate(data['username'],data['password'])
        if(username!=None):
            mutex.acquire()
            i=username.id
            if i in logged_in:
                logged_in.remove(i)  # removes username from logged_in list
            mutex.release()

            key_mapping[i] = "None"  # removex 16 byte hex token created

            return {"message" : "successful"}
        else:
            return {"message" : "invalid username or password"}


@app.route("/")
def red():                                                                                                              #redirects user from / to /login
    return redirect(url_for('login'))


@app.route("/logout/<name>")
def logout(name):                                                                                                       #performs logout operations
    i=int(name)

    mutex.acquire()
    if i in logged_in:
        logged_in.remove(i)                                                                                             #removes username from logged_in list
    mutex.release()

    key_mapping[int(name)]="None"                                                                                       #removex 16 byte hex token created

    return render_template('logout.html')                                                                               #this html file erases the user password stored on client side


#socket control
#api to establish socket connection and retreive ECDH keys
@socketio.on('connect_user')
def create_connection(json):                                                                                            #establishes socket connection and receives userid and recipientid
    print('connected')


    session_mapping[json['userid']]=request.sid                                                                         #maps userid to session id
    print(session_mapping)
    text_hist=Message.find_by_userids(json['userid'], json['recipientid'])                                              #retreives text history between user and recipient

    user=User.return_pub_pri_keys(json['userid'])                                                                       #retreives user public and private keys
    recipient=User.return_pub_pri_keys(json['recipientid'])                                                             #retreives recipient public key

    json['recipient_publickey']=recipient[0]                                                                            #recipient[0] contains public key   recipient=[publickey, privatekey]
    json['user_publickey']=user[0]
    json['user_privatekey']=user[1]
    json['text_hist']=text_hist
    json['you'] = User.find_by_id(json['userid']).username                                                              #retreives username
    #json['key'] = key_mapping[int(json['userid'])]

    if int(json['userid']) in key_mapping.keys():                                                                       #checks if key is there in the key_mapping
        json['key'] = key_mapping[int(json['userid'])]
    else:
        json['key'] = "None"

    print(json['key'])
    json['mapping']={json['userid'] : json['you'], json['recipientid']:User.find_by_id(json['recipientid']).username}   #maps username to userid

    print(json)
    socketio.emit('connect_return', json, room=request.sid)

#api to route text to appropriate destination
@socketio.on('sending_text')
def send_and_receive_text(json, methods=['GET', 'POST']):
    receiver_session_id = json['recipientid']

    print(str(json))

    user_name_1=User.find_by_id(json['userid']).username                                                                #find user and receivers userids
    recipient_name=User.find_by_id(json['recipientid']).username

    Message.insert_message(json['userid'], json['recipientid'], json['message'])                                        #insert message into database to store it

    if(receiver_session_id not in session_mapping):
        json['username'] = user_name_1
        print(json)
        socketio.emit('text_response', json, room=request.sid)
    else:
        receiver_session_id = session_mapping[json['recipientid']]
        print(user_name_1, recipient_name)
        json['username'] = user_name_1
        json['recipient'] = recipient_name
        #print(json)
        socketio.emit('text_response', json, room=receiver_session_id)                                                  #sends data back to both user and receiver
        socketio.emit('text_response', json, room=request.sid)                                                          #data contains username and encrypted message




api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(logout_force, '/logout')
api.add_resource(homepage,'/homepage/<name>')
api.add_resource(chat,'/homepage/<name>/<name1>')


if __name__ == '__main__':
    socketio.run(app, port=80)

