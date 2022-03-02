# Loan Manager

The loanManager is a tiny application that calculates principal balance and interest added. It exposes 3 endpoint as following list :

- POST /loan/initiate (initiate the loan)
- POST /loan/addpayment (add payment information)
- GET /loan/getbalance (get balance up to requested date)


## Interest calculation

In the getbalance endpoint, we calculate interest of each day based on the principal_balance of that day, thus, each time a payment occures, it affects the balance and the interest of loan then after. For example assume the initial amount of loan is 1000$ and the start date is 2021-02-01, and the first payment is 100$ on 2021-02-05, then, if we get balance on 2021-02-10, the interest from 2021-02-02 to 2021-02-4 will be calculated based on 1000$ and from 2021-02-05 to 2021-02-10 will be calculated based on 900$. **It is important to mention that the interest calculation starts from the day after the start_date of loan, so the start date is excluded, and the requested date of balance is included**.

## How to install

This application works with Python 7.3.3+ and is coded in FastAPI framework.

Run following command in project root directory to install required packages:

```shell
pip install -r requirments.txt
```

## How to run the application
Execute following command in project root directory, it will run a web server :

```shell
python server.py
```

## How to use application

One of advantages of FastAPI over Flask is its auto OpenAPI doc generation, so you can easily see all endpoints and their description and usage at a glance. Our app's swaggerUI is located at :

http://localhost:8005/docs



After running the application, its REST apis can be accessed with following addresses :

POST http://127.0.0.1:8005/loan/initiate

Payload example :

```json
{
    "initial_amount" : 1000,
    "annual_interset_rate" : 36.5,
    "start_date" : "2012-09-12"
}
```
---

POST http://127.0.0.1:8005/loan/addpayment

Payload example :
```json
{
  "payment_amount" : 300,
  "payment_date" : "2017-11-19"
}
```
---
Example call for getbalance endpoint :

GET http://127.0.0.1:8005/loan/getbalance?todate=2012-10-10



## How to test
Just run the following command in project root directory :

```shell
python -m unittest
```