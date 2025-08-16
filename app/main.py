from fastapi import FastAPI, Depends, HTTPException, Query 
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be either 'income' or 'expense'")
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int, 
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(get_db)
):
    db_transaction = crud.update_transaction(db, transaction_id=transaction_id, transaction=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.delete("/transactions/{transaction_id}", response_model=schemas.Transaction)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.delete_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.get("/summary/", response_model=schemas.MonthlySummary)
def get_summary(year: int = None, month: int = None, db: Session = Depends(get_db)):
    summary = crud.get_monthly_summary(db, year=year, month=month)
    return summary

@app.get("/report/yearly/", response_model=schemas.YearlyReport)
def get_yearly_report(
    year: int = Query(None, description="Year for report (default: current year)"),
    db: Session = Depends(get_db)
):
    if year is None:
        year = datetime.now().year
    return crud.get_yearly_report(db, year=year)