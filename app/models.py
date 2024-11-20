from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StoreDetails(Base):
    __tablename__ = 'store_details'

    store_id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    store_location = Column(String, nullable=True)
    upc_id = Column(Integer, ForeignKey('top_sales_upc.upc_id'), nullable=True)
    store_type = Column(String, nullable=True)

    top_sales = relationship('TopSalesUPC', back_populates='store_details')

class TopSalesUPC(Base):
    __tablename__ = 'top_sales_upc'

    upc_id = Column(Integer, primary_key=True, nullable=False)
    dim_store_id = Column(Integer, nullable=True)
    dim_product_id = Column(Integer, nullable=True)
    sales = Column(Integer, nullable=True)
    qty = Column(Integer, nullable=True)

    store_details = relationship('StoreDetails', back_populates='top_sales')
