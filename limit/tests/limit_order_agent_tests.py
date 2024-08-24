import unittest
from limit_order_agent import LimitOrderAgent
from trading_framework import ExecutionException

class MockExecutionClient:
    def __init__(self):
        self.orders_executed = []

    def buy(self, product_id, amount):
        if amount <= 0:
            raise ExecutionException("Invalid amount to buy.")
        self.orders_executed.append({'product_id': product_id, 'buy_sell_flag': 'buy', 'amount': amount})

    def sell(self, product_id, amount):
        if amount <= 0:
            raise ExecutionException("Invalid amount to sell.")
        self.orders_executed.append({'product_id': product_id, 'buy_sell_flag': 'sell', 'amount': amount})

class TestLimitOrderAgent(unittest.TestCase):
    
    def setUp(self):
        self.mock_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.mock_client)
    
    def test_buy_ibm_below_100(self):
        self.agent.buy_ibm_below_100('IBM', 99)
        self.assertEqual(len(self.mock_client.orders_executed), 1)
        self.assertEqual(self.mock_client.orders_executed[0]['product_id'], 'IBM')
        self.assertEqual(self.mock_client.orders_executed[0]['amount'], 1000)

    def test_add_order_and_execute(self):
        self.agent.add_order('buy', 'AAPL', 100, 150)
        self.agent.price_tick('AAPL', 145)
        self.assertEqual(len(self.mock_client.orders_executed), 1)
        self.assertEqual(self.mock_client.orders_executed[0]['product_id'], 'AAPL')
        self.assertEqual(self.mock_client.orders_executed[0]['buy_sell_flag'], 'buy')
        self.assertEqual(self.mock_client.orders_executed[0]['amount'], 100)
    
    def test_no_order_execution_above_limit(self):
        self.agent.add_order('buy', 'AAPL', 100, 150)
        self.agent.price_tick('AAPL', 155)
        self.assertEqual(len(self.mock_client.orders_executed), 0)
    
    def test_add_sell_order_and_execute(self):
        self.agent.add_order('sell', 'GOOGL', 50, 2000)
        self.agent.price_tick('GOOGL', 2005)
        self.assertEqual(len(self.mock_client.orders_executed), 1)
        self.assertEqual(self.mock_client.orders_executed[0]['product_id'], 'GOOGL')
        self.assertEqual(self.mock_client.orders_executed[0]['buy_sell_flag'], 'sell')
        self.assertEqual(self.mock_client.orders_executed[0]['amount'], 50)

if __name__ == '__main__':
    unittest.main()
