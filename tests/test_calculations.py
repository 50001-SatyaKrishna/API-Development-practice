from app.calculations import Calculator, BankAccount, InsufficientFunds
import pytest

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1,num2,expected):
    assert num1 + num2 == expected

def test_div():
    assert 4 / 2 == 2

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_withdraw(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(999)

