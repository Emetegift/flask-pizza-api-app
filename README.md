# Simple Pizza Delivery Service API

This is a simple pizza delivery service API built with Flask-RESTX. It allows users to create orders, add items to orders, and calculate the total price of an order. The API is documented using Swagger UI, and has been tested with both Insomnia and pytest.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- pip

### Installation

1. Clone the repository
```
git clone https://github.com/Emetegift/flask-pizza-delivery-api.git
```

2. Install the required packages
```
pip install -r requirements.txt
```

3. Start the server
```
flask run
```

4. Access the API documentation
```
http://localhost:5000/api/doc/
```

## Usage

### Creating Orders

To create a new order, make a POST request to the `/orders` endpoint with the following payload:

```
class Sizes(Enum):
    {
    SMALL="small"
    MEDIUM="medium"
    LARGE="large"
    EXTRA_LARGE="extra_large"
    }
```

This will create a new order and return a JSON response with the order ID.

### Adding Items to Orders

To add an item to an order, make a POST request to the `/orders/{order_id}/items` endpoint with the following payload:

```
{
    class OrderStatus(Enum):
    PENDING="pending"
    IN_TRANSIT="in_transit"
    DELIVERED="delivered"
}
```

This will add the item to the specified order and return a JSON response with the item ID.

### Calculating Total Price

To calculate the total price of an order, make a GET request to the `/orders/{order_id}/total` endpoint. This will return a JSON response with the total price of the order.

## Testing

This project has been tested with both Insomnia and pytest. To run the tests, use the following command:

```
pytest
```

This will run all the tests in the `tests` directory and output the results to the console.

## Built With

- Flask-RESTX - Web framework
- Swagger UI - API documentation tool
- Insomnia - API testing tool
- Pytest - Testing framework

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
