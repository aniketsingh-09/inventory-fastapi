from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./inventory.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management System")

@app.get("/")
def root():
    return {"status": "Inventory API running"}

@app.post("/products")
def add_product(name: str, quantity: int, price: int):
    db = SessionLocal()
    product = Product(name=name, quantity=quantity, price=price)
    db.add(product)
    db.commit()
    return {"message": "Product added"}

@app.get("/products")
def get_products():
    db = SessionLocal()
    return db.query(Product).all()
