#export ENV_FILE_LOCATION=./.env
from back_end import app
from flask import Flask,jsonify,request,Blueprint
from flask_restful import Api,Resource
from json import dumps
# from back_end.models import Account, DataRecord, History
from back_end.models import Account,hash_password,check_password
from flask_jwt_extended import JWTManager, create_access_token, jwt_required ,get_jwt_identity
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import datetime
import os
from flask.views import MethodView
import cv2
from back_end import test_
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
catalog = Blueprint('back_end', __name__)
@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class SignupApi(MethodView):
    def post(self):
        body = request.get_json()
        username =  body['username']
        password = hash_password(body['password'])
        sign_up = {'_id': username,'password':password}
        sign_up_instance = Account
        sign_up_instance.insert(sign_up)
        get_id = sign_up_instance.find_one( sort=[('_id', -1)] )
        return {'id': str(get_id["_id"])}, 200

class LoginApi(MethodView):
    def post(self):
        body = request.get_json()
        username = body['username']
        login_instance = Account
        get_id = login_instance.find_one({"_id":username})
        print(get_id)
        if not get_id:
            return {'error': 'Username or password invalid'}, 402
        password=get_id['password']
        authorized = check_password(password,body['password'])
        if not authorized:
            return {'error': 'Username or password invalid'}, 401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(get_id['_id']), expires_delta=expires)
        return {'token': access_token}, 200

class PredictApi(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        now = datetime.datetime.now()
        file = request.files['file']

        if file and allowed_file(file.filename):

            fileExt = file.filename.rsplit('.', 1)[1].lower()
            path = os.path.join(app.config['UPLOAD_FOLDER'], str(datetime.datetime.timestamp(now))+"."+fileExt)
            file.save(path)

            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            height = img.shape[0]
            width = img.shape[1]
            if width!=1024 and height!=768:
                dim = (1024, 768)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                cv2.imwrite(path, resized)
            # reponse
            value_predict = test_.call_test(path)
            return {'predict':int(value_predict)+3,'filename':str(path)},200
        return {'error':True,'message':'file is require'},400


#post is json
# class HistoryApi(Resource):
#     @jwt_required
#     def get(self):
#         history = History.objects().to_json()
#         return {'data':history}
#     def post(self):
#         body = request.get_json()
#         return body




# api.add_resource(PredictApi, '/api/predict') 

signup =  SignupApi.as_view('signup')
app.add_url_rule('/api/auth/signup', view_func=signup, methods=['GET', 'POST'])

login =  LoginApi.as_view('login')
app.add_url_rule('/api/auth/login', view_func=login, methods=['GET', 'POST'])


predict =  PredictApi.as_view('predict')
app.add_url_rule('/api/predict', view_func=predict, methods=['GET', 'POST'])




# api.add_resource(HistoryApi,'/api/history')
