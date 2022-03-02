from datetime import date
from fastapi import APIRouter, HTTPException
from fastapi import Query
from fastapi.responses import JSONResponse
from loanManager import LoanManager
from messages import SuccessfulMessage, SuccessfulMessageWithData, ErrorMessage
from input_schema import InputLoan, InputPayment


loan_manager = LoanManager()

#APIRouter creates path operations for item module
router = APIRouter(
    prefix="/loan",
    tags=["Loan"]
)



# endpoint to initiate loan
@router.post("/initiate",
    summary="Initiate a loan",
    status_code=201,
    responses={ 201: {"model": SuccessfulMessage, "description": "Loan initiated successfull"},
                400: {"model": ErrorMessage, "description": "Invalid input parmaters"}})
async def initiate_loan( input_loan : InputLoan):
    # Get loan parameters sent from client
    try :
        loan_manager.create_loan(input_loan.initial_amount, input_loan.annual_interest_rate, input_loan.start_date)

    except ValueError as value_error :
        raise HTTPException(status_code=400, detail= str(value_error))


    return JSONResponse(content={'message' : 'OK'})
    




# endpoint to add payment
@router.post("/addpayment",
    summary="Add payment to existing loan",
    status_code=201,
    responses={ 201: {"model": SuccessfulMessage, "description": "Payment added successfully"},
                404: {"model": ErrorMessage, "description": "Loan is not initiated"}})
async def add_payment( payment : InputPayment):

     # retrieve existing loan   
    loan = loan_manager.get_loan()

    # if no loan is already initiated return 404 http error
    if loan is None :
        raise HTTPException(status_code=404, detail='Loan is not initiated')
    try :

        loan.add_payment(payment.payment_amount, payment.payment_date)

    except ValueError as value_error :
        raise HTTPException(status_code=400, detail= str(value_error))


    return JSONResponse(content={'message' : 'OK'})


# endpoint to get the balance
@router.get("/getbalance",
    summary="get the balance of loan up to requested date ",
    status_code=200,
    responses={ 200: {"model": SuccessfulMessageWithData, "description": "Balance successfully retrieved"},
                404: {"model": ErrorMessage, "description": "Loan is not initiated"}})
def get_balance(to_date: date = Query(
                ...,
                alias="todate",
                title="date of blanace",
                description="The date that you want to calculate balance up to that date",
                )):

    # retrieve existing loan
    loan = loan_manager.get_loan()

    # if no loan is already initiated return 404 http error 
    if loan is None :
        raise HTTPException(status_code=404, detail='Loan is not initiated')

    try :
        # call the balance method of loan object
        balance = loan.get_balance(to_date)

    except ValueError as value_error :
        raise HTTPException(status_code=400, detail= str(value_error))

    
    return JSONResponse(content = {'message' : 'OK', 'balance' : round(balance,2) })