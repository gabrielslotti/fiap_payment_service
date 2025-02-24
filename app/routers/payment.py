import httpx
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.mercadopago import MercadoPago
from app.models.payment import Payment as PaymentModel
from app.schemas.payment import (
    PaymentCheckout, PaymentCheckoutResponse, PaymentUpdate
)
from .. import database, config


@lru_cache()
def get_settings():
    """
    Config settings function.
    """
    return config.Settings()


conf_settings = get_settings()

router = APIRouter()


@router.post(
    "/qrcode",
    response_model=PaymentCheckoutResponse,
    status_code=status.HTTP_200_OK
)
def generate_qrcode(
    payment: PaymentCheckout, db_session: Session = Depends(database.get_db)
):
    """
    Fake Mercado Pago QRCode Generator.

    :param payment: Payment schema.
    :param db_session: Database session.
    """
    payment_raw = payment.model_dump()
    payment_raw['status'] = 'Pendente'

    db_payment = PaymentModel(**payment_raw)
    db_session.add(db_payment)
    db_session.commit()
    db_session.refresh(db_payment)

    # Call Mercado Pago to generate QRCode
    qrcode = MercadoPago().gen_qrcode()

    return PaymentCheckoutResponse(
        id=db_payment.id,
        external_id=db_payment.external_id,
        status=db_payment.status,
        value=db_payment.value,
        qrcode=qrcode
    )


@router.post(
    "/callback", response_model=PaymentUpdate, status_code=status.HTTP_200_OK
)
def callback(
    payment: PaymentUpdate, db_session: Session = Depends(database.get_db)
):
    """
    Callback to receive Mercado Pago payment updates.

    :param payment: Payment udpate schema.
    :param db_session: Database session.
    """

    db_payment = (
        db_session.query(PaymentModel)
                  .filter(PaymentModel.id == payment.id)
                  .one_or_none()
    )

    if not db_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )

    db_payment.status = payment.status

    db_session.add(db_payment)
    db_session.commit()
    db_session.refresh(db_payment)

    # Callback Orders Service to create the order
    if db_payment.status == "Efetuado":
        req = httpx.post(
            f"{conf_settings.order_service_url}/order/create",
            json={
                "external_id": db_payment.external_id
            }
        )

        if req.status_code != 201:
            raise HTTPException(
                status_code=400,
                detail="Error calling back order service"
            )

    return PaymentUpdate(id=db_payment.id, status=db_payment.status)
