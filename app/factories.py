import factory
from app.models import TopSalesUPC
from app.database import SessionLocal 

class TopSalesUPCFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TopSalesUPC
        sqlalchemy_session = None
        #sqlalchemy_session_persistence = 'commit'

    upc_id = factory.Faker('random_int', min=1, max=1000)
    dim_store_id = factory.Faker('random_int', min=1, max=100)
    dim_product_id = factory.Faker('random_int', min=1, max=100)
    sales = factory.Faker('random_number', digits=5)
    qty = factory.Faker('random_number', digits=3)