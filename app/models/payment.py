from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[Integer] = mapped_column(type_=Integer, primary_key=True)
    external_id: Mapped[String(120)] = mapped_column(type_=String(120))
    value: Mapped[Numeric(10, 2)] = mapped_column(type_=Numeric(10, 2))
    status: Mapped[String(60)] = mapped_column(type_=String(60))
