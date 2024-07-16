
from fastapi import APIRouter, Response

from src.controller import AccountController
from src.domain.models import Account, LoginRequest

_controller = AccountController()
router = APIRouter(prefix="/account", tags=["account"], default_response_class=Response)


@router.post("/signup", )
def signup(account: Account):
    return _controller.create_account(account=account)


@router.post("/login")
def login(login: LoginRequest):
    return _controller.login(login=login)


@router.get("/{account_id}")
def get_account(account_id: str):
    return _controller.get_account_by_id(id=account_id)
