from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app import schemas
from app.crud import create_top_sales_upc, get_top_sales_upc
from app.models import TopSalesUPC, StoreDetails
from strawberry.fastapi import GraphQLRouter
from app.graphql_schema import schema

# StoreDetails.__table__.drop(engine)
# StoreDetails.__table__.create(engine)

# Initialize FastAPI app
app = FastAPI()

# Create tables

models.Base.metadata.create_all(bind=engine)

# REST Endpoints
@app.post("/topsales/", response_model=schemas.TopSalesUPC)
def create_top_sales(top_sales: schemas.TopSalesUPCCreate, db: Session = Depends(get_db)):
    return create_top_sales_upc(db=db, top_sales=top_sales)

@app.get("/topsales/{upc_id}", response_model=schemas.TopSalesUPC)
def read_top_sales(upc_id: int, db: Session = Depends(get_db)):
    db_top_sales = get_top_sales_upc(db, upc_id=upc_id)
    if db_top_sales is None:
        raise HTTPException(status_code=404, detail="Top sales record not found")
    return db_top_sales

# GraphQL Endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
