import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, engine
from app.factories import TopSalesUPCFactory
from app.models import TopSalesUPC

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency with the production database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_top_sales():
    # Use factory to generate fake data
    fake_data = TopSalesUPCFactory.build()

    response = client.post("/topsales/", json={
        "upc_id": fake_data.upc_id,
        "dim_store_id": fake_data.dim_store_id,
        "dim_product_id": fake_data.dim_product_id,
        "sales": fake_data.sales,
        "qty": fake_data.qty
    })

    assert response.status_code == 200
    data = response.json()
    assert data["upc_id"] == fake_data.upc_id
    assert data["dim_store_id"] == fake_data.dim_store_id
    assert data["dim_product_id"] == fake_data.dim_product_id
    assert data["sales"] == fake_data.sales
    assert data["qty"] == fake_data.qty

    # Clean up the record after the test
    db = next(override_get_db())
    db.query(TopSalesUPC).filter(TopSalesUPC.upc_id == fake_data.upc_id).delete()
    db.commit()

def test_get_top_sales():
    db = next(override_get_db())
    TopSalesUPCFactory._meta.sqlalchemy_session = db
    fake_data = TopSalesUPCFactory.build()
    db.add(fake_data)
    db.commit()
    db.refresh(fake_data)

    response = client.get(f"/topsales/{fake_data.upc_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["upc_id"] == fake_data.upc_id
    assert data["dim_store_id"] == fake_data.dim_store_id
    assert data["dim_product_id"] == fake_data.dim_product_id
    assert data["sales"] == fake_data.sales
    assert data["qty"] == fake_data.qty

    # Clean up the record after the test
    # db.query(TopSalesUPC).filter(TopSalesUPC.upc_id == fake_data.upc_id).delete()
    # db.commit()