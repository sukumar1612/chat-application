from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, Indentity
from models import User

from threading import Lock

import socket
import sys

mutex=Lock()

app = Flask( __name__,static_url_path='/static')
api = Api(app)
app.secret_key='a24aca7a4e1686c098b34309624341f38f4c2b7f6d4fe48e1543ea62843e65fb' #generated using python secrets module

jwt=JWT(app,authenticate, Indentity)   # /auth is the endpoint

item=[["4","bob"],["1","alice"],["2","jake"],["3","john"],["5","samantha"],["6","me"]]
logged_in=[]

class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('registeration.html'),200,headers)

    def post(self):
        data = request.get_json();
        u=User.insert_user(data['username'], data['email'], data['password'])
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

#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("8.8.4.4", 80))
#local_ip = s.getsockname()[0]
#s.close()


#app.run(host=local_ip,port=80,debug=True)

app.run()
