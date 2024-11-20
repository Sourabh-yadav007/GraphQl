import strawberry
from app.models import TopSalesUPC, StoreDetails
from app.database import get_db
from strawberry.types import Info
from sqlalchemy.orm import Session

# TopSalesUPC GraphQL Type
@strawberry.type
class TopSalesUPCType:
    upc_id: int
    dim_store_id: int
    dim_product_id: int
    sales: float
    qty: int

# StoreDetails GraphQL Type
@strawberry.type
class StoreDetailsType:
    store_id: int
    store_name: str
    store_location: str
    store_type: str
    upc_id: int

@strawberry.type
class CombinedStoreSalesType:
    top_sales_upc: TopSalesUPCType
    store_details: StoreDetailsType

# Query class for fetching data
@strawberry.type
class Query:
    @strawberry.field
    def top_sales_upc_with_store_details(self, info: Info, upc_id: int) -> CombinedStoreSalesType:
        db: Session = next(get_db())
        top_sales = db.query(TopSalesUPC).filter(TopSalesUPC.upc_id == upc_id).first()
        if not top_sales:
            raise ValueError("Top sales record not found")
        
        # Join with StoreDetails table
        store_details = db.query(StoreDetails).filter(StoreDetails.upc_id == upc_id).first()
        if not store_details:
            raise ValueError("Store details not found")
        
        return CombinedStoreSalesType(top_sales_upc=top_sales, store_details=store_details)

    # Fetch all TopSalesUPC and their associated StoreDetails
    @strawberry.field
    def all_top_sales_with_store_details(self, info: Info) -> list[CombinedStoreSalesType]:
        db: Session = next(get_db())
        top_sales_list = db.query(TopSalesUPC).all()
        combined_data = []
        for top_sales in top_sales_list:
            store_details = db.query(StoreDetails).filter(StoreDetails.upc_id == top_sales.upc_id).first()
            if store_details:
                combined_data.append(CombinedStoreSalesType(top_sales_upc=top_sales, store_details=store_details))
        return combined_data

    # Fetch all top sales UPC records
    @strawberry.field
    def top_sales_upc(self, info: Info) -> list[TopSalesUPCType]:
        db: Session = next(get_db())
        return db.query(TopSalesUPC).all()

    # Fetch top sales UPC records by various criteria
    @strawberry.field
    def top_sales_upc_by_criteria(
        self, 
        info: Info, 
        upc_id: int = None, 
        dim_store_id: int = None, 
        dim_product_id: int = None, 
        sales: int = None, 
        qty: int = None
    ) -> list[TopSalesUPCType]:
        db: Session = next(get_db())
        query = db.query(TopSalesUPC)
        
        if upc_id is not None:
            query = query.filter(TopSalesUPC.upc_id == upc_id)
        if dim_store_id is not None:
            query = query.filter(TopSalesUPC.dim_store_id == dim_store_id)
        if dim_product_id is not None:
            query = query.filter(TopSalesUPC.dim_product_id == dim_product_id)
        if sales is not None:
            query = query.filter(TopSalesUPC.sales == sales)
        if qty is not None:
            query = query.filter(TopSalesUPC.qty == qty)
        
        results = query.all()
        if not results:
            raise ValueError("No matching top sales records found")
        return results

    # Fetch all store details records
    @strawberry.field
    def store_details(self, info: Info) -> list[StoreDetailsType]:
        db: Session = next(get_db())
        return db.query(StoreDetails).all()

    # Fetch store details by various criteria
    @strawberry.field
    def store_details_by_criteria(
        self,
        info: Info,
        store_id: int = None,
        store_name: str = None,
        store_location: str = None,
        store_type: str = None
    ) -> list[StoreDetailsType]:
        db: Session = next(get_db())
        query = db.query(StoreDetails)

        if store_id is not None:
            query = query.filter(StoreDetails.store_id == store_id)
        if store_name is not None:
            query = query.filter(StoreDetails.store_name.ilike(f"%{store_name}%"))
        if store_location is not None:
            query = query.filter(StoreDetails.store_location.ilike(f"%{store_location}%"))
        if store_type is not None:
            query = query.filter(StoreDetails.store_type.ilike(f"%{store_type}%"))

        results = query.all()
        if not results:
            raise ValueError("No matching store details found")
        return results
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_top_sales_upc(
        self,
        info: Info,
        dim_store_id: int,
        dim_product_id: int,
        sales: float,
        qty: int,
    ) -> TopSalesUPCType:
        db: Session = next(get_db())
        new_record = TopSalesUPC(
            dim_store_id=dim_store_id,
            dim_product_id=dim_product_id,
            sales=sales,
            qty=qty,
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record

    @strawberry.mutation
    def create_store_details(
        self,
        info: Info,
        store_id: int,
        store_name: str,
        store_location: str,
        store_type: str,
        upc_id: int  # Pass upc_id as part of the mutation
    ) -> StoreDetailsType:
        db: Session = next(get_db())
        
        # Check if the TopSalesUPC exists for the provided upc_id
        top_sales_upc = db.query(TopSalesUPC).filter(TopSalesUPC.upc_id == upc_id).first()
        if not top_sales_upc:
            raise ValueError(f"TopSalesUPC with upc_id {upc_id} does not exist.")

        new_store_details = StoreDetails(
            store_id=store_id,
            store_name=store_name,
            store_location=store_location,
            store_type=store_type,
            upc_id=upc_id  # Link the store to a TopSalesUPC record
        )
        db.add(new_store_details)
        db.commit()
        db.refresh(new_store_details)
        return new_store_details

# Combine the Query and Mutation into the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# import strawberry
# from app.models import TopSalesUPC
# from app.database import get_db
# from strawberry.types import Info
# from sqlalchemy.orm import Session

# @strawberry.type
# class TopSalesUPCType:
#     upc_id: int
#     dim_store_id: int
#     dim_product_id: int
#     sales: float
#     qty: int

# @strawberry.type
# class Query:
#     @strawberry.field
#     def top_sales_upc(self, info: Info) -> list[TopSalesUPCType]:
#         db: Session = next(get_db())
#         return db.query(TopSalesUPC).all()

#     @strawberry.field
#     def top_sales_upc_by_criteria(
#         self, 
#         info: Info, 
#         upc_id: int = None, 
#         dim_store_id: int = None, 
#         dim_product_id: int = None, 
#         sales: int = None, 
#         qty: int = None
#     ) -> list[TopSalesUPCType]:
#         db: Session = next(get_db())
#         query = db.query(TopSalesUPC)
        
#         if upc_id is not None:
#             query = query.filter(TopSalesUPC.upc_id == upc_id)
#         if dim_store_id is not None:
#             query = query.filter(TopSalesUPC.dim_store_id == dim_store_id)
#         if dim_product_id is not None:
#             query = query.filter(TopSalesUPC.dim_product_id == dim_product_id)
#         if sales is not None:
#             query = query.filter(TopSalesUPC.sales == sales)
#         if qty is not None:
#             query = query.filter(TopSalesUPC.qty == qty)
        
#         results = query.all()
#         if not results:
#             raise ValueError("No matching top sales records found")
#         return results

# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     def create_top_sales_upc(
#         self,
#         info: Info,
#         dim_store_id: int,
#         dim_product_id: int,
#         sales: float,
#         qty: int,
#     ) -> TopSalesUPCType:
#         db: Session = next(get_db())
#         new_record = TopSalesUPC(
#             dim_store_id=dim_store_id,
#             dim_product_id=dim_product_id,
#             sales=sales,
#             qty=qty,
#         )
#         db.add(new_record)
#         db.commit()
#         db.refresh(new_record)
#         return new_record

# schema = strawberry.Schema(query=Query, mutation=Mutation)