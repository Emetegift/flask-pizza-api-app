from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from  http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required, get_jwt_identity


order_namespace=Namespace('orders', description='Name space for Order')

order_model=order_namespace.model(
    'Order',{
        'id':fields.Integer(description="An ID"),
        'size':fields.String(required=True,desciption='Size of order',
                enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
        'order_status':fields.String(required=True, description="The Status of an order", 
                enum=['PENDING','IN_TRANSIT','DELIVERED']),
        'flavour':fields.String(required=True,description='Pizza flavour'),
        'quantity':fields.Integer(required=True, description='Quantity of order')
    }
)

order_status_model = order_namespace.model(
    'OrderStatus',{
        'order_status':fields.String(require=True, description="Order ststus",
                    enum=['PENDING','IN_TRANSIT','DELIVERED'])
    }
)
@order_namespace.route('/orders')
class GetCreateOrder(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Get all orders"
    )
    @jwt_required()
    def get(self):
        """Get all orders
        """
        orders=Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Place an order"
    )
    @jwt_required()
    def post(self):
        """Place an order
        """
        
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
        
        new_order =Order(
            size=data['size'],
            quantity= data['quantity'],
            flavour=data['flavour']
        )
        
        new_order.user = current_user
        
        new_order.save()
        
        return new_order, HTTPStatus.CREATED
        
    @order_namespace.route('/order/<int:order_id>')
    class GetUdateDeleteOrder(Resource):
        
        @order_namespace.marshal_with(order_model)
        @order_namespace.doc(
        description = "Retrieve an order by id",
        params = {
            'order_id': 'An ID for an order'
        }
    )
        @jwt_required()
        def get(self, order_id):
            """Retrieve an order by id
            """
            order = Order.get_by_id(order_id)
            return order, HTTPStatus.OK
        
        @order_namespace.expect(order_model)
        @order_namespace.marshal_with(order_model)
        @order_namespace.doc(
            description = "Update an order by id",
            params = {
            'order_id': 'An ID for an order'
            }
        )

        @jwt_required()
        def put(self, order_id):
            """Update an order by id
            """ 
            order_to_update = Order.get_by_id(order_id)
            
            data = order_namespace.payload
            
            order_to_update.quantity = data["quantity"]
            order_to_update.size = data["size"]
            order_to_update.flavour = data["flavour"]
            
            # db.session.commit()
            order_to_update.update()
            
            return order_to_update, HTTPStatus.OK
        @order_namespace.doc(
            description = "Delete an order by id",
                params = {
            'order_id': 'An ID for an order'
        }
        )
        @jwt_required()
        def delete(self, order_id):
            """Delete an order by id
            """
            order_to_delete = Order.get_by_id(order_id)
            
            order_to_delete.delete()
            
            return {"message":"Deleted successfully"}, HTTPStatus.OK
            
    @order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
    class GetSpecificOrderByUser(Resource):
        @order_namespace.marshal_with(order_model)
        @order_namespace.doc(
        description = "Get a user specific order by user id and order id",
            params = {
            'order_id': 'An ID for an order',
            'user_id':'An ID for a specific user\'s orders '
            }
        )
        @jwt_required()
        def get(self, user_id, order_id):
            """Get a user specific order
            """
            user = User.get_by_id(user_id)
            
            order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
            return order, HTTPStatus.OK
        
    @order_namespace.route('/user/<int:user_id>/orders')   
    class GetUserOrders(Resource):
        @order_namespace.marshal_list_with(order_model)
        @order_namespace.doc(
        description = "Get all user order by user id",
            params = {
            'user': 'An ID for a user'
            }
        )
        @jwt_required()
        def get(self, user_id):
            """Get all users orders
            """
            user = User.get_by_id(user_id)
            
            orders = user.orders
            
            return orders, HTTPStatus.OK
            
    @order_namespace.route('/order/status/<int:order_id>') 
    class UpdateOrderStatus(Resource):
        
        @order_namespace.expect(order_status_model)
        @order_namespace.marshal_with(order_model)
        @order_namespace.doc(
        description = "Update an order\'s status",
            params = {
            'order_id': 'An ID for an order'
            }
        )
        @jwt_required()
        def patch(self, order_id):
            """Update an order's status
            """
            data = order_namespace.payload
            
            order_to_update = Order.get_by_id(order_id)
            
            order_to_update.order_status = data["order_status"]
            
            db.session.commit()
            
            return order_to_update, HTTPStatus.OK
    
        
        