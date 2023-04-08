import unittest # unittest is inbuilt, it does not need to be installed
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.users import User
from werkzeug.security import generate_password_hash

class  UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        
        self.appctx = self.app.app_context()
        
        self.appctx.push()
        
        self.client = self.app.test_client()
        
        db.create_all()
        
        #tearDown help to reset an app before creating another table
    def tearDown(self):
        
        db.drop_all()
        
        self.appctx.pop()
        
        self.app=None
        
        self.client=None
        
    def test_user_registration(self):
        
        data = {
            "username":"Ani Paul",
            "email":"ani@gmail.com",
            "password":"password"
        }
        
        
        response = self.client.post('/auth/signup', json=data)
        
        user = User.query.filter_by(email='ani@gmail.com').first()
         
        assert user.username == "Ani Paul"
        
        assert response.status_code == 201
        
    def test_user_login(self):
            
        data = {
            "email":"ani@gmail.com",
            "password":"password"
        }
        response = self.client.post('/auth/login', json=data)
        
        assert response.status_code == 200
        
        
        