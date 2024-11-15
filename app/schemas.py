from pydantic import BaseModel

class TopSalesUPCBase(BaseModel):
    upc_id: int
    dim_store_id: int
    dim_product_id: int
    sales: float
    qty: float

class TopSalesUPCCreate(TopSalesUPCBase):
    pass

class TopSalesUPC(TopSalesUPCBase):
    class Config:
        from_attributes = True