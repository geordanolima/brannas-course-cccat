from fastapi import status

def test_create_account(db_clear, account_controller, account, login):
    _account = account_controller.create_account(account=account)
    assert _account.status_code == status.HTTP_200_OK


def test_login(db_clear, account_controller, account, login):
    _account = account_controller.create_account(account=account)
    _login = account_controller.login(login=login)
    assert _account.status_code == status.HTTP_200_OK
    assert _login.status_code == status.HTTP_200_OK
