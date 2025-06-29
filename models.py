from sqlalchemy import Boolean, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class BondDB(Base):
    __tablename__ = "bonds"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nominal_value = Column(Float)
    commercial_value = Column(Float)
    coupon_rate = Column(Float)
    market_rate = Column(Float)
    payment_frequency = Column(Integer)
    duration = Column(Integer)
    bonus = Column(Float)
    flotation = Column(Float)
    cavali = Column(Float)
    structuration = Column(Float, default=0.0)
    colocation = Column(Float, default=0.0)
    total_grace_period = Column(Integer, default=0)
    partial_grace_period = Column(Integer, default=0)

    # Relationships
    flows = relationship("FlowDB", back_populates="bond", cascade="all, delete-orphan")
    results = relationship("ResultsDB", back_populates="bond", cascade="all, delete-orphan")
    user = relationship("UserDB", back_populates="bonds")

class FlowDB(Base):
    __tablename__ = "flows"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bond_id = Column(Integer, ForeignKey("bonds.id"))
    period = Column(Integer)
    initial_balance = Column(Float)
    amortization = Column(Float)
    coupon = Column(Float)
    bonus = Column(Float)
    net_flow = Column(Float)
    final_balance = Column(Float)
    
    # Relationship
    bond = relationship("BondDB", back_populates="flows")

class ResultsDB(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bond_id = Column(Integer, ForeignKey("bonds.id"))
    TCEA = Column(Float)
    TREA = Column(Float)
    Precio_Maximo = Column(Float)
    
    # Relationship
    bond = relationship("BondDB", back_populates="results")

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))

    # Relationships
    bonds = relationship("BondDB", back_populates="user", cascade="all, delete-orphan")