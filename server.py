from datetime import timedelta
import json
import os
import io
from flask import Flask, jsonify, redirect, render_template, request, send_file, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, verify_jwt_in_request
from werkzeug.utils import secure_filename
import detection
from flask_cors import CORS
from flask import Response
import threading
from jdatetime import datetime

UPASS = "Tw*Ga9MO00)h#uDgaN%y5QL18P$VrY8E%OqXax^%PizcN"
UNAME = "hW0lcey"
SECKEY = "ZCp1l__7_AsuQs&_TM!MGw&5JTmm6x^("
UPLOAD_FOLDER = 'uploads'
BODY_EXAMPLES = 'static/photos/bodyex'
FACE_EXAMPLES = 'static/photos/faceex'
PROFILE_PHOTO = 'static/photos/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SAFE_URL = 'http://127.0.0.1:5500'

lock = threading.Lock()


def today():
    today = datetime.now()
    return today.strftime("%Y/%m/%d")


def save_user_to_json(fullname, phone):
    with lock:
        with open('users.json', 'r+') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []

            new_user = {'fullname': fullname, "phone": phone, "date": today()}
            users.append(new_user)

            f.seek(0)
            json.dump(users, f, indent=4)


def read_file_from_path(file_path):
    with open(file_path, 'rb') as f:
        file_stream = io.BytesIO(f.read())
    return file_stream


def safeurl(url):
    if SAFE_URL in url:
        return True
    return False


def allowed_file(filename: str):
    for i in ALLOWED_EXTENSIONS:
        print("check formt : " + filename)
        if filename.endswith(i):
            return True
    return False


app = Flask(__name__)
app.config['SECRET_KEY'] = SECKEY
app.template_folder = 'Admin'
app.static_folder = 'static'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
CORS(app)
jwt = JWTManager(app)


@app.route('/fex')
def getfexes():
    files = os.listdir(FACE_EXAMPLES)
    return jsonify({"files": files})


@app.route('/bex')
def getbexes():
    files = os.listdir(BODY_EXAMPLES)
    return jsonify({"files": files})


def delfile(filepath):
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        print("Del file error  : ", e)
        return False


@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = ""
    print(f"request from  {request.referrer}")
    if 'image' not in request.files:
        print('image not uploaded')
        return Response("please upload image", status=400)
    file = request.files['image']
    if file.filename == '':
        return Response("please select file", status=400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        decres = detection.faceDetect(file_path)
        if decres:
            filestream = read_file_from_path(file_path)
            delfile(file_path)
            return send_file(filestream, mimetype='image/jpeg')
        else:
            delfile(file_path)
            return Response("face not found", status=400)

    return Response("Allowed file types are png, jpg, jpeg", status=400)


@app.route('/help', methods=['GET', 'POST'])
def save_user():
    if request.method == 'POST':
        fullname = request.json.get('fullname', None)
        phone = request.json.get('phone', None)
        exists = False

        with open('users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data:
                if fullname == i['fullname'] and i['phone'] == phone:
                    exists = True

        if not exists:
            fullname = request.json.get('fullname', None)
            phone = request.json.get('phone', None)
            save_user_to_json(fullname, phone)
            return Response('success', 200)
        else:
            return Response('user exists', 400)

    return Response('set params', 400)

########################
######
######### ADMIN#########
######
########################


@app.route('/rem/<string:part>', methods=['POST'])
@jwt_required()
def remcontent(part):
    try:
        verify_jwt_in_request(fresh=True)
        if request.json:
            filename = request.json.get('exname', None)
            if not filename:
                return Response('example name not found', 400)
            if part == "fex":
                file_path = os.path.join(FACE_EXAMPLES, filename)
                if delfile(file_path):
                    return Response(f'face example with name "{file_path}" deleted', 200)
                else:
                    return Response('face example not found', 200)
            elif part == "bex":
                file_path = os.path.join(BODY_EXAMPLES, filename)
                if delfile(file_path):
                    return Response(f'body example with name "{file_path}" deleted', 200)
                else:
                    return Response('body example not found', 200)
    except Exception as e:
        print(e)
        return redirect('dashboard.html')


@app.route('/set/<string:part>', methods=['POST'])
@jwt_required()
def setcontent(part):
    try:
        verify_jwt_in_request(fresh=True)
        if 'image' not in request.files:
            print('image not uploaded')
            return Response("please upload image", status=400)
        file = request.files['image']
        if file.filename == '':
            return Response("please select file", status=400)
        if file and allowed_file(file.filename):
            if part == "profile":
                file_path = os.path.join(PROFILE_PHOTO, "profile.jpg")
                file.save(file_path)
                return Response('profile changed', 200)
            elif part == "bex":
                bexescount = len(os.listdir(BODY_EXAMPLES))
                file_path = os.path.join(
                    BODY_EXAMPLES, f"{bexescount + 1}.jpg")
                file.save(file_path)
                return Response(f'Body example added ({bexescount + 1})', 200)
            elif part == "fex":
                bexescount = len(os.listdir(FACE_EXAMPLES))
                file_path = os.path.join(
                    FACE_EXAMPLES, f"{bexescount + 1}.jpg")
                file.save(file_path)
                return Response(f'Face example added ({bexescount + 1})', 200)
        else:
            print("not allowed file")

        return Response("Allowed file types are png, jpg, jpeg", status=400)
    except Exception as e:
        print(e)
        return redirect('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username == 'admin' and password == 'password':
            access_token = create_access_token(identity=username, fresh=True)
            return jsonify({'access_token': access_token}), 200
        else:
            return Response('wrong auth', 401)
    return render_template('dashboard.html')


@app.route('/getusers', methods=['GET'])
@jwt_required()
def get_users():
    try:
        verify_jwt_in_request(fresh=True)
        with open('users.json', 'r', encoding='utf-8') as f:
            data: list = json.load(f)
            content = ""
            numid = 1
            for i in data:
                item = f"-{numid}-\n"
                item += i['fullname'] + "\n"
                item += i['phone'] + "\n"
                item += i['date'] + "\n------------------------------\n"
                content += item
                numid += 1
            with open('users.txt', 'w') as f:
                f.write(content)
            return send_file('users.txt', as_attachment=True)

        return Response('set params', 400)
    except Exception as e:
        print(e)
        return redirect('dashboard.html')


@app.route('/status', methods=['GET'])
@jwt_required()
def get_status():
    try:
        verify_jwt_in_request(fresh=True)
        return Response("login", 200)
    except Exception as e:
        print(e)
        return Response("login", 200)
