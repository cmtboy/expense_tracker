from sqlalchemy.orm import Session
from datetime import datetime, date
from . import models, schemas

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        amount=transaction.amount,
        description=transaction.description,
        category=transaction.category,
        date=transaction.date,
        type=transaction.type
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionCreate):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.amount = transaction.amount
        db_transaction.description = transaction.description
        db_transaction.category = transaction.category
        db_transaction.date = transaction.date
        db_transaction.type = transaction.type
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction

def get_monthly_summary(db: Session, year: int = None, month: int = None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.date >= start_date,
        models.Transaction.date < end_date
    ).all()
    
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

def get_yearly_report(db: Session, year: int):
    # Initialize results
    monthly_data = []
    total_income = 0.0
    total_expense = 0.0
    
    # Get data for each month
    for month in range(1, 13):
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        transactions = db.query(models.Transaction).filter(
            models.Transaction.date >= start_date,
            models.Transaction.date < end_date
        ).all()
        
        month_income = sum(t.amount for t in transactions if t.type == "income")
        month_expense = sum(t.amount for t in transactions if t.type == "expense")
        
        monthly_data.append({
            "month": month,
            "income": month_income,
            "expense": month_expense,
            "balance": month_income - month_expense
        })
        
        total_income += month_income
        total_expense += month_expense
    
    return {
        "year": year,
        "months": monthly_data,
        "total_income": total_income,
        "total_expense": total_expense,
        "yearly_balance": total_income - total_expense
    }