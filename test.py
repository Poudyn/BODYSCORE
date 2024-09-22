from flask import Flask, render_template, request, redirect, url_for
from flask import Response

app = Flask(__name__)
app.template_folder = 'Admin'  # مشخص کردن پوشه قالب‌ها
app.static_folder = 'static'

# تعریف مسیر لاگین
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None) 
        print(url_for('admin_dashboard'))
        if username == 'admin' and password == 'password':
            return Response('success',200)
        else:
            return Response('wrong auth',401)
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('dashboard.html')

@app.route('/')
def index():
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return 'You have been redirected!'



@app.route('/set/<string:part>', methods=['POST'])
def setcontent(part):
    if 'image' not in request.files:
        print('image not uploaded')
        return Response("please upload image", status=400)
    file = request.files['image']
    if file.filename == '':
        return Response("please select file", status=400)
    if file and allowed_file(file.filename):
        if part == "profile":
            file_path = os.path.join(UPLOAD_FOLDER, "profile.jpg")
            file.save(file_path)
            return Response('profile changed',200)
        elif part == "bex":
            bexescount = len(os.listdir(BODY_EXAMPLES))
            file_path = os.path.join(BODY_EXAMPLES, f"{bexescount + 1}.jpg")
            file.save(file_path)
            return Response(f'Body example added ({bexescount + 1})',200)
        elif part == "fex":
            bexescount = len(os.listdir(FACE_EXAMPLES))
            file_path = os.path.join(FACE_EXAMPLES, f"{bexescount + 1}.jpg")
            file.save(file_path)
            return Response(f'Face example added ({bexescount + 1})',200)
    else:
        print("not allowed file")
        
    return Response("Allowed file types are png, jpg, jpeg", status=400)

