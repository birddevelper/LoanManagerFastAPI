from datetime import date, datetime
from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field



class InputPayment(BaseModel):
    payment_amount: float
    payment_date : date


class InputLoan(BaseModel):
    initial_amount : float = Field(..., example="1000")
    annual_interest_rate : float = Field(..., example="2.7")
    start_date : date = Field(..., example="2022-09-09")