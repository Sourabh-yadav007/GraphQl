from sqlalchemy import Column, Integer, Float
from app.database import Base

class TopSalesUPC(Base):
    __tablename__ = 'top_sales_upc'

    upc_id = Column(Integer, primary_key=True, nullable=False)
    dim_store_id = Column(Integer, nullable=True)
    dim_product_id = Column(Integer, nullable=True)
    sales = Column(Float, nullable=True)
    qty = Column(Float, nullable=True)
