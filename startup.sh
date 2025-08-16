#!/bin/bash
# Initialize SQLite DB if it doesn't exist
if [ ! -f "/tmp/expense_tracker.db" ]; then
  echo "Initializing database..."
  python -c "
from app.database import engine, Base
from app.models import *
Base.metadata.create_all(bind=engine)
print('Database initialized!')
"
fi

uvicorn app.main:app --host 0.0.0.0 --port $PORT