from sqlalchemy.orm import Session
from . import models, schemas

def create_top_sales_upc(db: Session, top_sales: schemas.TopSalesUPCCreate):
    db_top_sales = models.TopSalesUPC(**top_sales.dict())
    db.add(db_top_sales)
    db.commit()
    db.refresh(db_top_sales)
    return db_top_sales

def get_top_sales_upc(db: Session, upc_id: int):
    return db.query(models.TopSalesUPC).filter(models.TopSalesUPC.upc_id == upc_id).first()
