import logging

logging.basicConfig(level=logging.INFO, filename='bank_system.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Bank:
    def __init__(self):
        self.accounts = {}
        self.loans = {}
        self.mortgages = {}

    def create_account(self, account_type, account_number, account_holder_name, initial_deposit=0):
        if account_type == "savings":
            self.accounts[account_number] = SavingsAccount(account_number, account_holder_name, initial_deposit)
        elif account_type == "checking":
            self.accounts[account_number] = CheckingAccount(account_number, account_holder_name, initial_deposit)
        elif account_type == "tfsa":
            self.accounts[account_number] = TaxFreeSavingsAccount(account_number, account_holder_name, initial_deposit)
        elif account_type == "rrsp":
            self.accounts[account_number] = RegisteredRetirementSavingsPlan(account_number, account_holder_name, initial_deposit)

        logging.info(f"Account {account_number} created for {account_holder_name}.")

    def create_loan(self, loan_id, borrower_name, principal_amount, interest_rate, term_years):
        self.loans[loan_id] = Loan(loan_id, borrower_name, principal_amount, interest_rate, term_years)
    
    def create_mortgage(self, mortgage_id, borrower_name, principal_amount, interest_rate, term_years, property_address):
        self.mortgages[mortgage_id] = Mortgage(mortgage_id, borrower_name, principal_amount, interest_rate, term_years, property_address)

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)


class BankAccount:
    def __init__(self, account_number, account_holder_name, balance=0):
        self._account_number = account_number
        self.account_holder_name = account_holder_name
        self._balance = balance
        self.transaction_history = []  # Initialize an empty list for transaction history
        logging.info(f"Created a new bank account for: {self.account_holder_name}")

    def deposit(self, amount):
        self._balance += amount
        self.transaction_history.append(('Deposit', amount))  # Log the deposit
        logging.info(f"Deposit of {amount} made to account: {self._account_number}")

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            self.transaction_history.append(('Withdrawal', amount))  # Log the withdrawal
            logging.info(f"Withdrawal of {amount} from account: {self._account_number}")
        else:
            logging.error("Insufficient funds for withdrawal.")
            raise ValueError("Insufficient funds")

    def display_account_details(self):
        print(f"Account Number: {self._account_number}\nAccount Holder: {self.account_holder_name}\nBalance: {self._balance}")

    def print_transaction_history(self):
        print("Transaction history:")
        for transaction in self.transaction_history:
            print(f"{transaction[0]}: {transaction[1]}")


class SavingsAccount(BankAccount):
    def __init__(self, account_number, account_holder_name, balance=0, minimum_balance=100):
        super().__init__(account_number, account_holder_name, balance)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if self._balance - amount < self.minimum_balance:
            logging.error("Withdrawal would bring account below minimum balance.")
            raise ValueError("Withdrawal would bring account below minimum balance")
        else:
            super().withdraw(amount)
    
    def apply_interest(self):
        interest - self._balance * 0.01
        self._balance += interest
        logging.info(f"Interest of {interest} applied to {self._account_number}. New balance: {self._balance}")


class CheckingAccount(BankAccount):
    def send_etransfer(self, recipient_account_number, amount):
        if self._balance >= amount:
            self._balance -= amount
            logging.info(f"E-Transfer of {amount} sent to {recipient_account_number}.")
        else:
            logging.error("Failed E-Transfer attempt due to insufficient funds.")
            raise ValueError("Insufficient funds for E-Transfer")

    def withdraw(self, amount):
        super().withdraw(amount)


class DebitCard:
    def __init__(self, card_number, linked_account):
        self.card_number = card_number
        self.linked_account = linked_account

    def pay_with_card(self, amount):
        try:
            self.linked_account.withdraw(amount)
            logging.info(f"Payment of {amount} made with card {self.card_number}")
        except ValueError as e:
            logging.error(f"Payment failed with card {self.card_number: {str(e)}}")
        
    def change_pin(self, new_pin):
        logging.info(f"PIN changed successfully for card: {self.card_number}")


class CreditCard(DebitCard):
    def __init__(self, card_number, linked_account, credit_limit):
        super().__init__(card_number, linked_account)
        self.credit_limit = credit_limit

    def set_credit_limit(self, limit):
        self.credit_limit = limit

    def charge_interest(self):
        if self._balance > 0:
            interest = self._balance * 0.02
            self._balance += interest
            logging.info(f"Interest of {interest} charged to card {self.card_number}")


class ATMMachine:
    def __init__(self, location, bank):
        self.location = location
        self.bank = bank

    def insert_card(self, card_number):
        logging.info(f"Card {card_number} inserted into ATM at {self.location}")

    def authenticate(self, pin):
        # authenticate pin maybe?
        return True

    def select_account(self, account_number):
        logging.info(f"Account {account_number} selected at ATM")

    def perform_transaction(self, transaction_type, amount):
        pass


class TaxFreeSavingsAccount(SavingsAccount):
    def __init__(self, account_number, account_holder_name, balance=0):
        super().__init__(account_number, account_holder_name, balance)
        logging.info(f"TFSA account {account_number} created for {account_holder_name}")
        

class RegisteredRetirementSavingsPlan(SavingsAccount):
    def __init__(self, account_number, account_holder_name, balance=0, contribution_room=0):
        super().__init__(account_number, account_holder_name, balance)
        self.contribution_room = contribution_room
        logging.info(f"RRSP account {account_number} created for {account_holder_name}")


class Loan:
    def __init__(self, loan_id, borrower_name, principal_amount, interest_rate, term_years):
        self.loan_id = loan_id
        self.borrower_name = borrower_name
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.balance = principal_amount
        logging.info(f"Loan {loan_id} created for {borrower_name}.")

    def make_payment(self, amount):
        self.balance -= amount
        logging.info(f"Payment of {amount} made on loan {self.loan_id}. New balance: {self.balance}.")


class Mortgage(Loan):
    def __init__(self, mortgage_id, borrower_name, principal_amount, interest_rate, term_years, property_address):
        super().__init__(mortgage_id, borrower_name, principal_amount, interest_rate, term_years)
        self.property_address = property_address
        logging.info(f"Mortgage {mortgage_id} for property {property_address} created for {borrower_name}.")

# Example instantiation of a BankAccount
logging.info("Beginning program")
def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

def main_menu(bank):
    while True:
        print_header("Tahas Banking System Main Menu")
        print("""
1. Create a new account
2. Access an existing account
3. Apply for a loan
4. Apply for a mortgage
5. Exit
""")
        user_choice = input("Please choose an option (1-5): ").strip()

        if user_choice == "1":
            create_account_flow(bank)
        elif user_choice == "2":
            access_account_flow(bank)
        elif user_choice == "3":
            apply_for_loan_flow(bank)
        elif user_choice == "4":
            apply_for_mortgage_flow(bank)
        elif user_choice == "5":
            print("\nThank you for giving me all your money. Bye!")
            break
        else:
            print("\nInvalid option, please try again.")

def create_account_flow(bank):
    print_header("Create a New Account")
    account_holder_name = input("Enter the account holder's name: ").strip()
    account_number = input("Enter a new account number: ").strip()
    print("\nType of account:\n1. Savings\n2. Checking\n3. TFSA\n4. RRSP")
    account_type = input("Choose an account type (1-4): ").strip()

    if account_type == "1":
        account_type = "savings"
    elif account_type == "2":
        account_type = "checking"
    elif account_type == "3":
        account_type = "tfsa"
    elif account_type == "4":
        account_type = "rrsp"

    initial_deposit = float(input("Initial deposit amount: "))
    bank.create_account(account_type, account_number, account_holder_name, initial_deposit)
    print(f"\n{account_type.upper()} account created successfully for {account_holder_name}.")

def apply_for_loan_flow(bank):
    print_header("Apply for a Loan")
    loan_id = input("Enter a unique loan ID: ").strip()
    borrower_name = input("Enter the borrower's name: ").strip()
    principal_amount = float(input("Enter the principal loan amount: "))
    interest_rate = float(input("Enter the interest rate (as a decimal): "))
    term_years = int(input("Enter the term of the loan in years: "))
    
    bank.create_loan(loan_id, borrower_name, principal_amount, interest_rate, term_years)
    print("\nLoan application successful.")

def apply_for_mortgage_flow(bank):
    print_header("Apply for a Mortgage")
    mortgage_id = input("Enter a unique mortgage ID: ").strip()
    borrower_name = input("Enter the borrower's name: ").strip()
    principal_amount = float(input("Enter the principal mortgage amount: "))
    interest_rate = float(input("Enter the interest rate (as a decimal): "))
    term_years = int(input("Enter the term of the mortgage in years: "))
    property_address = input("Enter the property address: ").strip()
    
    bank.create_mortgage(mortgage_id, borrower_name, principal_amount, interest_rate, term_years, property_address)
    print("\nMortgage application successful.")

def access_account_flow(bank):
    print_header("Access an Existing Account")
    account_number = input("Enter your account number: ").strip()
    account = bank.get_account(account_number)
    if account:
        account_flow(account)
    else:
        print("\nAccount not found.")

def account_flow(account):
    while True:
        print_header("Account Menu")
        print("""
1. Deposit
2. Withdraw
3. Display Account Details
4. Display Transaction History
5. Return to Main Menu
""")
        user_choice = input("Choose an option (1-5): ").strip()

        if user_choice == "1":
            amount = float(input("Enter the amount to deposit: "))
            account.deposit(amount)
            print("\nDeposit successful.")
        elif user_choice == "2":
            amount = float(input("Enter the amount to withdraw: "))
            try:
                account.withdraw(amount)
                print("\nWithdrawal successful.")
            except ValueError as e:
                print(f"\n{e}")
        elif user_choice == "3":
            account.display_account_details()
        elif user_choice == "4":
            account.print_transaction_history()
        elif user_choice == "5":
            break
        else:
            print("\nInvalid option, please try again.")

if __name__ == "__main__":
    bank = Bank()
    main_menu(bank)
