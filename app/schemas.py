from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

class MonthlyData(BaseModel):
    month: int
    income: float
    expense: float
    balance: float

class YearlyReport(BaseModel):
    year: int
    months: List[MonthlyData]
    total_income: float
    total_expense: float
    yearly_balance: float

class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category: str
    date: date
    type: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True

class MonthlySummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float