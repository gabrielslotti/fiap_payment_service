from pydantic import BaseModel
from enum import Enum


class StatusEnum(str, Enum):
    pending = 'Pendente'
    done = 'Efetuado'
    failed = 'Falha'
    canceled = 'Cancelado'


class PaymentUpdate(BaseModel):
    id: int
    status: StatusEnum


class PaymentCheckout(BaseModel):
    external_id: str
    value: float


class Payment(BaseModel):
    id: int
    external_id: str
    status: StatusEnum
    value: float


class PaymentCheckoutResponse(BaseModel):
    qrcode: str
    external_id: str
    status: StatusEnum
    value: float
