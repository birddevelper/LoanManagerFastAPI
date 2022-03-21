from datetime import timedelta


class Loan:

    # constructor of the class
    def __init__(self, initial_amount, annual_interest_rate, start_date):

        # check the initial amount of loan to be a number
        if not isinstance(initial_amount, int) and not isinstance(initial_amount, float) :
            raise ValueError("initial_amount must be a number")
        
        # check the annual interest rate of loan to be a number
        if not isinstance(annual_interest_rate, int) and not isinstance(annual_interest_rate, float) :
            raise ValueError("initial_amount must be a number")

        
        # check the initial amount of loan to be greater than 0, no body gets 0$ or less than 0$ loan
        if initial_amount <= 0:
            raise ValueError("initial_amount must be over 0")

        # check the annual interest rate to be greater or equal to 0 percent
        if annual_interest_rate < 0:
            raise ValueError("annual_interest_rate must be higher or equal to 0")

        # initiate loan parameters with given information
        self.initial_amount = initial_amount
        self.annual_interest_rate = annual_interest_rate
        self.start_date = start_date 
        self.payments = []
    



    # this method adds given payment data to the payment list in ascending reorder
    def add_payment(self, payment_amount, payment_date) :

        # check the payment amount to be greater than 0, no body pays 0$ or less than 0$
        if payment_amount <= 0:
            raise ValueError("payment_amount must be over 0")

        # if the payment is greater than the initial amount, some thing is going wrong!
        if payment_amount > self.initial_amount:
            raise ValueError("payment_amount must be less than initial_amount")


        # it doesn't make any sense to pay before the loan starts, does it?
        if payment_date < self.start_date :
            raise ValueError("payment_date can not be before the loan start date")
        
        index = 0
        #if payments list is empty or the given payment's date is greater than last payment in the list, append it
        if len(self.payments)==0 or payment_date > self.payments[-1]['payment_date']:
            self.payments.append({'payment_date' : payment_date, 'payment_amount': payment_amount})
        else:
            # otherwise find the currect position, and insert the given payment there
            while payment_date > self.payments[index]['payment_date'] and index < len(self.payments):
                index += 1
            self.payments.insert(index, {'payment_date' : payment_date, 'payment_amount': payment_amount})





    # this method calculate total balance including principal balance and the interest added
    def get_balance(self, to_date) :
        


        # check to_date not be before the starting date of the loan
        if(to_date < self.start_date):
            raise ValueError("to_date can not be before the loan start date")


        # here we calculate interest of each day based on the principal_balance of that day
        # thus, each time a payment occures, it affects the interst of loan then after
        base_date = self.start_date
        next_date = None
        interest = 0
        for payment in self.payments :
            
            # check if the current payment date is not after requested time, because it doesn't affect th interest
            if(payment['payment_date']>to_date) :
                break
            
            #get days difference between last calculated date and current payment date
            delta = payment['payment_date'] - base_date - (timedelta(days=1) if base_date == self.start_date else  timedelta(days=0))
            # get total amount of payment up to current payment date (current payment date excluded)
            total_payment = self.__get_total_payment(payment['payment_date'] - timedelta(days=1))

            # calculate principal balance
            principal_balance = self.initial_amount - total_payment
            # calculate the interest of principal balance of days in the period with same balance
            interest += principal_balance * (self.annual_interest_rate/100/365) * delta.days
           
            base_date = payment['payment_date']

        
        total_payment = self.__get_total_payment(to_date)
        # calculate principal balance up to requested date
        principal_balance = self.initial_amount - total_payment
        # get days difference between last calculated date and requested date
        delta =  to_date - base_date + (timedelta(days=1) if base_date != self.start_date else timedelta(days=0))
        # calculate the interest of principal balance of days in the period with same balance
        interest += principal_balance * (self.annual_interest_rate/100/365) * delta.days
        
        return principal_balance + interest


    # this private method calculates total of all payments to the requested date
    def __get_total_payment(self, to_date):
        
        total_payment = 0
        # as the list is already sorted, we can skip the summing loop as we faced with payment date greater than requested date
        for payment in self.payments :
            if(payment['payment_date']<=to_date) :
                total_payment += payment['payment_amount']
            else :
                break
        return total_payment
        
