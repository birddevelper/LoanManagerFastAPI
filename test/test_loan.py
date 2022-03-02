from unittest import TestCase
import loan
from datetime import datetime, date



class TestLoan(TestCase):
    
    # test new loan creation
    def test_correct_loan_creation(self):
        new_loan = loan.Loan(1000,2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertEqual(new_loan.start_date, datetime.strptime('2012-11-10', '%Y-%m-%d').date(), "loan start_date is not set correclly")
        self.assertEqual(new_loan.initial_amount, 1000, "loan initial_amount is not set curreclly")
        self.assertEqual(new_loan.annual_interest_rate, 2.5, "loan annual_interest_rate is not set curreclly")
        # check zero annual interest
        new_loan = loan.Loan(5000,0,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertEqual(new_loan.start_date, datetime.strptime('2012-11-10', '%Y-%m-%d').date(), "loan start_date is not set correclly")
        self.assertEqual(new_loan.initial_amount, 5000, "loan initial_amount is not set curreclly")
        self.assertEqual(new_loan.annual_interest_rate, 0, "loan annual_interest_rate is not set curreclly")


    # test loan creation with invalid initial amount
    def test_loan_creation_with_invalid_initial_amount(self):
        self.assertRaises(ValueError,loan.Loan,0,2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,-900,2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,'vuvuvu',2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,'1000',2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,None,2.5,datetime.strptime('2012-11-10', '%Y-%m-%d').date())

    # test loan creation with invalid annual interest rate
    def test_loan_creation_with_invalid_annual_interest(self):
        self.assertRaises(ValueError,loan.Loan,1000,'2.5',datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,900,'ee',datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,1000,-1,datetime.strptime('2012-11-10', '%Y-%m-%d').date())
        self.assertRaises(ValueError,loan.Loan,1000,None,datetime.strptime('2012-11-10', '%Y-%m-%d').date())

        

    # test add payment with correct data
    def test_add_payment_with_correct_parameters(self):
        new_loan = loan.Loan(1000,2.5,datetime.strptime('2010-11-10','%Y-%m-%d').date())
        # add series of payments
        new_loan.add_payment(100,datetime.strptime('2012-10-01','%Y-%m-%d').date())
        new_loan.add_payment(200,datetime.strptime('2013-12-01','%Y-%m-%d').date())
        new_loan.add_payment(300.5,datetime.strptime('2011-11-01','%Y-%m-%d').date())
        new_loan.add_payment(400,datetime.strptime('2012-11-01','%Y-%m-%d').date())
        new_loan.add_payment(600,datetime.strptime('2014-09-02','%Y-%m-%d').date())
        new_loan.add_payment(500,datetime.strptime('2012-01-20','%Y-%m-%d').date())
        
        # first item must be the earliest payment by date
        self.assertEqual(new_loan.payments[0]['payment_date'],datetime.strptime('2011-11-01', '%Y-%m-%d').date(), "add_payment does not work correctly")
        self.assertEqual(new_loan.payments[0]['payment_amount'],300.5,"add_payment does not work correctly")
        # last item must be the latest payment by date
        self.assertEqual(new_loan.payments[5]['payment_date'],datetime.strptime('2014-09-02', '%Y-%m-%d').date(), "add_payment does not work correctly")
        self.assertEqual(new_loan.payments[5]['payment_amount'],600,"add_payment does not work correctly")
        # checking a middle item in the list
        self.assertEqual(new_loan.payments[2]['payment_date'],datetime.strptime('2012-10-01', '%Y-%m-%d').date(), "add_payment does not work correctly")
        self.assertEqual(new_loan.payments[2]['payment_amount'],100, "add_payment does not work correctly")

    # test add payment with incorrect amount of payment
    def test_add_payment_with_incorrect_amount(self):
        new_loan = loan.Loan(1000,2.5,'2010-11-10')
        # add series of payments with invalid payment amount
        self.assertRaises(ValueError,new_loan.add_payment,-100,datetime.strptime('2012-10-01','%Y-%m-%d').date())
        self.assertRaises(ValueError,new_loan.add_payment,0,datetime.strptime('2012-10-01','%Y-%m-%d').date())
        #this amount is more than the initial loan amount
        self.assertRaises(ValueError,new_loan.add_payment,1200,datetime.strptime('2012-10-01','%Y-%m-%d').date())
    
    # test add payment with incorrect date of payment
    def test_add_payment_with_incorrect_date(self):
        new_loan = loan.Loan(1000,2.5,datetime.strptime('2010-11-10','%Y-%m-%d').date())
        # add series of payments with invalid payment date
        self.assertRaises(ValueError,new_loan.add_payment,100,datetime.strptime('2010-10-01','%Y-%m-%d').date()) # the date is before start of loan


    # test get balance method 
    def test_get_balance(self):

        #create a loan with 1000 initial amount and 36.5 percent of interest rate  ~= 0.001 per day
        new_loan = loan.Loan(1000,36.5,datetime.strptime('2010-11-01','%Y-%m-%d').date())
        new_loan.add_payment(200,datetime.strptime('2010-11-03','%Y-%m-%d').date())
        new_loan.add_payment(100,datetime.strptime('2010-11-04','%Y-%m-%d').date())
        new_loan.add_payment(500,datetime.strptime('2010-11-06','%Y-%m-%d').date())
        #test a date before payments start
        self.assertEqual(new_loan.get_balance(datetime.strptime('2010-11-02','%Y-%m-%d').date()),1001,"get_balance does not work correctly") # interest = 1 * 1$
        #test a date equal to a payment date
        self.assertEqual(new_loan.get_balance(datetime.strptime('2010-11-03','%Y-%m-%d').date()),801.8,"get_balance does not work correctly") # interest = 1*1$ + 1*0.8$
        #test a date in middle of payments
        self.assertEqual(new_loan.get_balance(datetime.strptime('2010-11-05','%Y-%m-%d').date()),703.2,"get_balance does not work correctly") # interest = 1*1$ + 1*0.8$ + 2*$0.7
        #test a date after all payments
        self.assertEqual(new_loan.get_balance(datetime.strptime('2010-11-09','%Y-%m-%d').date()),204,"get_balance does not work correctly") # interest = 1*1$ + 1*0.8$ + 2*$0.7 + 4*0.2$


    # test get bakance method with invalid date format
    def test_get_balance_invalid_date(self):
        #create a loan with 5000 initial amount starting from 2010-11-01
        new_loan = loan.Loan(1000,36.5,datetime.strptime('2010-11-01','%Y-%m-%d').date())
        self.assertRaises(ValueError,new_loan.get_balance,datetime.strptime('2010-09-01','%Y-%m-%d').date()) # balance date before the starting date