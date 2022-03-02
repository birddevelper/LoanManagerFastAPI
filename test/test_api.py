from server import app
from unittest import TestCase
from fastapi import FastAPI
from fastapi.testclient import TestClient
import json
import sys
from server import app

def parse_response(response):
    return response.json()
    
class TestApiIntegration(TestCase):
    def setUp(self):
        self.app = TestClient(app)

    # test initiate endpoint with correct parameter
    def test_initiate_loan(self) :
       response = parse_response(self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 2.5, start_date ='2012-09-08' ))))
                                
       self.assertIn('message', response)
       self.assertEqual(response['message'], 'OK')

    # test initiate endpoint with invalid parameter
    def test_initiate_loan_invalid_parameters(self) :
       response = parse_response(self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 2.5, start_date ='Two' ))))
                                
       self.assertIn('detail', response)
       

    # test /addpayment endpoint with correct parameter
    def test_add_payment(self) :
       self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 2.5, start_date ='2012-09-08' )),
                                content_type='application/json')

       response = parse_response(self.app.post("/loan/addpayment",
                                data=json.dumps(dict(payment_amount=1000,  payment_date ='2012-10-08' )),
                                content_type='application/json'))
                                
       self.assertIn('message', response)
       self.assertEqual(response['message'], 'OK')


    # test /addpayment endpoint with invalid parameter
    def test_add_payment(self) :
       self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 2.5, start_date ='2012-09-08' )))

       response = parse_response(self.app.post("/loan/addpayment",
                                data=json.dumps(dict(payment_amount=1000,  payment_date ='20121008' ))))
                                
       self.assertIn('detail', response)
       

    # test /getbalance endpoint with correct parameter
    def test_get_balance(self) :

       self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 36.5, start_date ='2012-09-08' )))

       self.app.post("/loan/addpayment",
                                data=json.dumps(dict(payment_amount=200,  payment_date ='2012-09-11' )))

       response_1 = parse_response(self.app.get("/loan/getbalance?todate=2012-09-10"))
       response_2 = parse_response(self.app.get("/loan/getbalance?todate=2012-09-13"))

       self.assertIn('message', response_1)
       self.assertIn('balance', response_1)
       self.assertEqual(response_1['message'], 'OK')
       self.assertEqual(response_1['balance'], 1002) # interest = 2 * 1$ = 2$
       self.assertIn('message', response_2)
       self.assertIn('balance', response_2)
       self.assertEqual(response_2['message'], 'OK')
       self.assertEqual(response_2['balance'], 804.4) # interest = 2 * 1$ + 3 * 0.8$ = 4.4



    # test /getbalance endpoint with invalid parameter
    def test_get_balance_invalid_date(self) :

       self.app.post("/loan/initiate",
                                data=json.dumps(dict(initial_amount=1000, annual_interest_rate = 36.5, start_date ='2012-09-08' )))

       self.app.post("/loan/addpayment",
                                data=json.dumps(dict(payment_amount=200,  payment_date ='2012-09-11' )))

       response_1 = parse_response(self.app.get("/loan/getbalance?todate=20120910"))
       self.assertIn('detail', response_1)


    # test /getbalance endpoint with when no loan is initiated
    def test__get_balance_when_no_loan_initiated(self) :

       response = parse_response(self.app.get("/loan/getbalance?todate=2012-09-10"))
       self.assertIn('detail', response)
       self.assertEqual(response['detail'], 'Loan is not initiated')


    # test /addpayment endpoint when no loan is initiated
    def test__add_payment_when_no_loan_initiated(self) :

        response = parse_response(self.app.post("/loan/addpayment",
                                data=json.dumps(dict(payment_amount=200,  payment_date ='2012-09-11' ))))
        self.assertIn('detail', response)
        self.assertEqual(response['detail'], 'Loan is not initiated')

