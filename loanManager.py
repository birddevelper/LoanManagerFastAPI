import loan


class LoanManager:
    def __init__(self):
        self.current_loan = None
        
    # this method creats a loan given its amount, interst rate and start date
    # it rests the loan each time it being called
    def create_loan(self, initial_amount, annual_interset_rate, start_date):
        # Create new loan object and set it to current loan
        self.current_loan = loan.Loan(initial_amount,annual_interset_rate,start_date)
        
        return self.current_loan

    # this method returns the current loan
    def get_loan(self):
        return self.current_loan