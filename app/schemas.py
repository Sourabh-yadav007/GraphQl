# app/schemas.py
from pydantic import BaseModel

class TopSalesUPCBase(BaseModel):
    upc_id: int
    dim_store_id: int
    dim_product_id: int
    sales: int
    qty: int

class TopSalesUPCCreate(TopSalesUPCBase):
    pass

class TopSalesUPC(TopSalesUPCBase):
    class Config:
        from_attributes = True

class StoreDetailsBase(BaseModel):
    store_id: int
    store_name: str
    store_location: str
    store_type: str

class StoreDetailsCreate(StoreDetailsBase):
    pass

class StoreDetails(StoreDetailsBase):
    class Config:
        from_attributes = True
