from germanAmortizationMethod import german_Amortization_Method
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
#from jose import JWTError, jwt
#from datetime import datetime, timedelta

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Configuración de JWT y hashing
SECRET_KEY = "tu_clave_secreta_super_segura_aqui"  # Cambia esto por una clave segura
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones básicas para autenticación
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class BondBase(BaseModel):
    user_id: int
    nominal_value: float
    commercial_value: float
    coupon_rate: float
    market_rate: float
    payment_frequency: int
    duration: int
    bonus: float
    flotation: float
    cavali: float
    structuration: float = 0.0
    colocation: float = 0.0
    total_grace_period: int = 0
    partial_grace_period: int = 0

class BondResponse(BaseModel):
    id: int
    nominal_value: float
    commercial_value: float
    coupon_rate: float
    market_rate: float
    payment_frequency: int = 2
    duration: int
    bonus: float
    flotation: float
    cavali: float
    structuration: float = 0.0
    colocation: float = 0.0
    total_grace_period: int = 0
    partial_grace_period: int = 0

    class Config:
        from_attributes = True  # Permite que Pydantic trabaje con SQLAlchemy

class FlowBase(BaseModel):
    bond_id: int
    period: int
    initial_balance: float
    amortization: float
    coupon: float
    bonus: float
    net_flow: float
    final_balance: float

    class Config:
        from_attributes = True  # Permite que Pydantic trabaje con SQLAlchemy

class ResultsBase(BaseModel):
    bond_id: int
    TCEA: float
    TREA: float
    Precio_Maximo: float
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    username: str = None
    user_id: int = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint para crear usuario con contraseña hasheada
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    # Hashear la contraseña antes de guardar
    hashed_password = get_password_hash(user.password)
    
    db_user = models.UserDB(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully", "username": user.username}

# Endpoint para login y obtener token
@app.post("/login", response_model=LoginResponse)
async def login(user_login: UserLogin, db: db_dependency):
    # Buscar usuario en la base de datos
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user_login.username).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Verificar contraseña
    if not verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {
        "success": True,
        "message": "Login successful",
        "username": db_user.username,
        "user_id": db_user.id
    }


@app.post("/bonds", response_model=BondResponse, status_code=status.HTTP_201_CREATED)
async def create_bond(bond: BondBase, db: db_dependency):
    db_bond = models.BondDB(**bond.model_dump())
    db_bond.payment_frequency = 2  # Default value for payment frequency
    db.add(db_bond)
    db.commit()
    db.refresh(db_bond)
    flows,results = german_Amortization_Method(db_bond)

    # Save flows to database
    for flow in flows:
        db_flow = models.FlowDB(
            bond_id=db_bond.id,
            period=flow.period,
            initial_balance=round(flow.initial_balance,2),
            amortization=round(flow.amortization,2),
            coupon=round(flow.coupon,2),
            bonus=round(flow.bonus, 2),
            net_flow=round(flow.net_flow,2),
            final_balance=round(flow.final_balance, 2)
        )
        db.add(db_flow)
    
    db.commit()  # Commit all flows at once

    # Save results to database
    db_results = models.ResultsDB(
        bond_id=db_bond.id,
        TCEA=round(results.TCEA, 4),
        TREA=round(results.TREA, 4),
        Precio_Maximo=round(results.Precio_Maximo, 2)
    )
    db.add(db_results)
    db.commit()  # Commit results

    # Return the created bond
    return db_bond

@app.get("/bonds/{user_id}", response_model=list[BondResponse], status_code=status.HTTP_200_OK)
async def get_bonds(user_id: int, db: db_dependency):
    db_bonds = db.query(models.BondDB).filter(models.BondDB.user_id == user_id).all()
    if not db_bonds:
        raise HTTPException(status_code=404, detail="Bonds not found")
    
    return db_bonds

@app.delete("/bonds/{bond_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bond(bond_id: int, db: db_dependency):
    db_bond = db.query(models.BondDB).filter(models.BondDB.id == bond_id).first()
    if not db_bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    
    db.delete(db_bond)
    db.commit()
    
    return {"message": "Bond deleted successfully"}

@app.put("/bonds/{bond_id}", response_model=BondResponse, status_code=status.HTTP_200_OK)
async def update_bond(bond_id: int, bond: BondBase, db: db_dependency):
    db_bond = db.query(models.BondDB).filter(models.BondDB.id == bond_id).first()
    if not db_bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    
    for key, value in bond.model_dump().items():
        setattr(db_bond, key, value)
    
    db.commit()
    db.refresh(db_bond)
    
    # Recalculate flows and results after updating the bond
    flows, results = german_Amortization_Method(db_bond)

    # Clear existing flows and results
    db.query(models.FlowDB).filter(models.FlowDB.bond_id == bond_id).delete()
    db.query(models.ResultsDB).filter(models.ResultsDB.bond_id == bond_id).delete()

    # Save new flows to database
    for flow in flows:
        db_flow = models.FlowDB(
            bond_id=db_bond.id,
            period=flow.period,
            initial_balance=round(flow.initial_balance, 2),
            amortization=round(flow.amortization, 2),
            coupon=round(flow.coupon, 2),
            bonus=round(flow.bonus, 2),
            net_flow=round(flow.net_flow, 2),
            final_balance=round(flow.final_balance, 2)
        )
        db.add(db_flow)
    
    db.commit()

@app.get("/bonds/{bond_id}/flows", response_model=list[FlowBase], status_code=status.HTTP_200_OK)
async def get_bond_flows(bond_id: int, db: db_dependency):
    db_flows = db.query(models.FlowDB).filter(models.FlowDB.bond_id == bond_id).all()
    if not db_flows:
        raise HTTPException(status_code=404, detail="Flows not found for this bond")
    
    return db_flows

@app.get("/bonds/{bond_id}/results", response_model=ResultsBase, status_code=status.HTTP_200_OK)
async def get_bond_results(bond_id: int, db: db_dependency):
    db_results = db.query(models.ResultsDB).filter(models.ResultsDB.bond_id == bond_id).first()
    if not db_results:
        raise HTTPException(status_code=404, detail="Results not found for this bond")
    
    return db_results



def main():
    print("Bienvenido a la API de Fijanzas")
            #  id  NV     CV     CR          MR           PF  D    B    F      CC    struct  col  TGP PGP  
#    bond = Bond(1, 1200, 1200, 0.028635700, 0.002004008, 3, 6, 0.009, 0.0045, 0.005, 0.008, 0.009, 1, 1)
#
#    flows,results = german_Amortization_Method(bond)
#    print("Flujos:")
#    for flow in flows:
#        flow_dict = vars(flow)
#        formatted_flow = {}
#        for key, value in flow_dict.items():
#            if isinstance(value, float):
#                formatted_flow[key] = round(value, 2)
#            else:
#                formatted_flow[key] = value
#        print(formatted_flow)
#    print("\nResultados:")
#    print("TCEA:", round(results.TCEA, 4))
#    print("TREA:", round(results.TREA, 4))
#    print("Precio Máximo:", round(results.Precio_Maximo, 2))



if __name__ == "__main__":
    main()