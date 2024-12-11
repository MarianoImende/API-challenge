import decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from solicitud_modelos import Importe


# Respuesta: /wallet/sesion
class Tarjeta(BaseModel):
    descripcion: str
    numero: str

class Sesion_response(BaseModel):
    # access_token: str = Field(..., examples=["uyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaGFsbGVuZ2UiLCJleHAiOjE3MTA0Mjc0NTJ9.7dB7Oo-5xumCSq0uY1_eujdlZB8OOgbSULrtx65uGv0"],min_length=1, max_length=90)
    # token_type: str = Field(..., examples=["bearer"],min_length=6, max_length=6, pattern=r"bearer",description="siempre bearer")
    # access_token_expires: str = Field(..., examples=["1800.0"])
    # tarjetas: Optional[List[Tarjeta]] = Field(..., examples=[[{"descripcion": "BANCO HIPOTECARIO","numero": "825840853443"},{"descripcion": "BANCO HSBC","numero": "423455721156"},{"descripcion": "BANCO DE LA PROVINCIA DE BUENOS AIRES","numero": "595278769781"}]])

    access_token: str
    token_type: str
    access_token_expires: int
    tarjetas: Optional[List[Tarjeta]]

#/wallet/cuentas
class Cuenta(BaseModel):
    numero_cuenta: str
    tipo: str

class Cuentas_response(BaseModel):
    cuentas: List[Cuenta]

#/wallet/saldo
class Saldo_response(BaseModel):
    saldo: decimal.Decimal
    moneda: str
    
#/wallet/movimientos
class Movimientos_r(BaseModel):
    fecha: str
    monto: str
    descripcion: str
    
class movimiento_respuesta(BaseModel):
    movimientos: List[Movimientos_r]

# Modelo de respuesta

class PagoRespuesta(BaseModel):
    qr_id: str
    importe: Importe
    transaccion: dict



