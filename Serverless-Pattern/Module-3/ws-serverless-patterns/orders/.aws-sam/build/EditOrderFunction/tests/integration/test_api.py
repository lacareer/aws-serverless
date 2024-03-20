import json
import requests
import logging
import time
import uuid
import pytest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

order_1 = {
    "restaurantId": 1,
    "orderId": str(uuid.uuid4()),
    "orderItems": [
        {
            "id": 1,
            "name": "Spaghetti",
            "price": 9.99,
            "quantity": 1
        },
        {
            "id": 2,
            "name": "Pizza - SMALL",
            "price": 4.99,
            "quantity": 2
        },
    ],
    "totalAmount": 19.97
}

@pytest.fixture
def orders_endpoint(global_config):
  '''Returns the endpoint for the Orders service'''
  orders_endpoint = global_config["Module3ApiEndpoint"] + '/orders'
  logger.debug("Orders Endpoint = " + orders_endpoint)
  return orders_endpoint

@pytest.fixture
def user_token(global_config):
  '''Returns the user_token for authentication to the Orders service'''
  user_token = global_config["user1UserIdToken"]
  logger.debug("     User Token = " + user_token)
  return user_token


def test_access_orders_without_authentication(orders_endpoint):
  response = requests.post(orders_endpoint)
  assert response.status_code == 401


def test_add_new_order(global_config, orders_endpoint, user_token):
  response = requests.post(orders_endpoint, data=json.dumps(order_1),
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )
  logger.debug("Add new order response: %s", response.text)
  assert response.status_code == 200
  orderInfo = response.json()
  orderId = orderInfo['orderId']
  logger.debug("New orderId: %s", orderId)
  global_config['orderId'] = orderId
  assert orderInfo['status'] == "PLACED"

def test_get_order(global_config, orders_endpoint, user_token):
  response = requests.get(orders_endpoint + "/" + global_config['orderId'],
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )

  logger.debug(response.text)
  orderInfo = json.loads(response.text)
  assert orderInfo['orderId'] == global_config['orderId']
  assert orderInfo['status'] == "PLACED"
  assert orderInfo['totalAmount'] == 19.97
  assert orderInfo['restaurantId'] == 1
  assert len(orderInfo['orderItems']) == 2

def test_list_orders(global_config, orders_endpoint, user_token):
  response = requests.get(orders_endpoint,
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )
  orders = json.loads(response.text)
  assert len(orders['orders']) == 1
  assert orders['orders'][0]['orderId'] == global_config['orderId']
  assert orders['orders'][0]['totalAmount'] == 19.97
  assert orders['orders'][0]['restaurantId'] == 1
  assert len(orders['orders'][0]['orderItems']) == 2  

def test_edit_order(global_config, orders_endpoint, user_token):
    print(f"Modifying order {global_config['orderId']}")

    modifiedOrder = {
        "restaurantId": 1,
        "orderItems": [
            {
                "id": 1,
                "name": "Spaghetti",
                "price": 9.99,
                "quantity": 1
            },
            {
                "id": 2,
                "name": "Pizza - SMALL",
                "price": 4.99,
                "quantity": 1
            },
            {
                "id": 3,
                "name": "Salad - LARGE",
                "price": 9.99,
                "quantity": 1
            },
        ],
        "totalAmount": 25.97
    }

    response = requests.put(
        orders_endpoint + "/" + global_config['orderId'],
        data=json.dumps(modifiedOrder),
        headers={'Authorization': user_token, 'Content-Type': 'application/json'}
        )

    logger.debug(f'Modify order response: {response.text}')
    assert response.status_code == 200
    updatedOrder = response.json()
    assert updatedOrder['totalAmount'] == 25.97
    assert len(updatedOrder['orderItems']) == 3

def test_cancel_order(global_config, orders_endpoint, user_token):
  print(f"Canceling order {global_config['orderId']}")
  response = requests.delete(
      orders_endpoint + "/" + global_config['orderId'],
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )

  logger.debug(f'Cancel order response: {response.text}')
  assert response.status_code == 200
  orderInfo = json.loads(response.text)
  assert orderInfo['orderId'] == global_config['orderId']
  assert orderInfo['status'] == 'CANCELED'
  
  
def test_cancel_order_in_wrong_status(global_config, orders_endpoint, user_token, acknowledge_order_hook):
  response = requests.delete(orders_endpoint + "/" + global_config['ackOrderId'],
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )
  logger.debug(f'Cancel order response: {response.text}')
  # Verify OrderStatusError exception was raised because status not 'PLACED' as expected.
  assert response.status_code == 400

def test_create_order_idempotency(global_config, orders_endpoint, user_token):

  order_details = {
      "restaurantId": 200,
      "orderId": str(uuid.uuid4()),
      "orderItems": [
          {
              "name": "Pasta Carbonara",
              "price": 14.99,
              "id": 123,
              "quantity": 1
          }
      ],
      "totalAmount": 14.99
  }

  order_data = json.dumps(order_details)
  header_data = {'Authorization': user_token, 'Content-Type': 'application/json'}

  # Attempt to add an order three times!
  # With idempotency, all returned order IDs should match.
  response1 = requests.post(orders_endpoint, data=order_data, headers=header_data)
  response2 = requests.post(orders_endpoint, data=order_data, headers=header_data)
  response3 = requests.post(orders_endpoint, data=order_data, headers=header_data)

  orderId1 = response1.json().get("orderId")
  orderId2 = response2.json().get("orderId")
  orderId3 = response3.json().get("orderId")

  assert orderId1 == orderId2 == orderId3
  assert orderId1 != global_config['orderId']

  # Even though the add_order operation was invoked three times (3x), there should only be two (2) orders:
  #   1. First order created in this test suite by test_add_new_order()
  #   2. Second order created in this idempotence test method
  response = requests.get(orders_endpoint, headers=header_data)
  orders = json.loads(response.text)
  assert len(orders['orders']) == 2



  

