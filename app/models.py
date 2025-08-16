from sqlalchemy import Column, Integer, String, Float, Date
from datetime import datetime
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    date = Column(Date, default=datetime.utcnow)
    type = Column(String, nullable=False)  # "income" or "expense"