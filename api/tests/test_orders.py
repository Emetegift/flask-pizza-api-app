import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.orders import Order
from flask_jwt_extended import create_access_token

class OrderTestCase(unittest.TestCase):
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
        
        # Function to test the getting of all orders
    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')
        
        headers = {
            "Authorization":f"Bearer {token}"
        }
        response = self.client.get('/orders/orders', headers=headers)
        
        assert response.status_code == 200
        
        assert response.json == []
        
        # Function to test the  creation of an order
    def test_create_order(self):
        token = create_access_token(identity='testuser') 
        
        data = {
            "quantity": 1,
            "size": "SMALL",
            "flavour": "Apple"
        }
        
        headers = {
            "Authorization": f"Bearer {token}"
        }   
        
        response = self.client.post('/orders/orders', json=data, headers=headers)
        
        assert response.status_code == 201
        
        orders = Order.query.all()
        
        order_id = orders[0].id
        
        assert order_id == 1
        
        assert len(orders) == 1
        
        assert response.json['size'] == 'Sizes.SMALL'
        
        # Function to test for the retrieval of an single order
    def test_get_single_order(self):
        
        order = Order (
            size =  "SMALL",
            quantity = 1,
            flavour =  "Apple"
        )
        
        order.save()
        
        token = create_access_token(identity='testuser')
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = self.client.get('/orders/order/1', headers=headers)
        
        # order = Order.query.all()
        
        # assert len(order) == 1
        
        assert response.status_code == 200