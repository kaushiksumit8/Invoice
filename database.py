from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.utcnow)
    items = relationship("Item", back_populates="invoice")

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)
    cost = Column(Float)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    invoice = relationship("Invoice", back_populates="items")

    def total_cost(self):
        return self.amount * self.cost

engine = create_engine('sqlite:///invoices.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
