import decimal
from typing import List, Optional
from pydantic import BaseModel
from solicitud_modelos import Importe


# Respuesta: /wallet/sesion
class Tarjeta(BaseModel):
    descripcion: str
    numero: str

class Sesion_response(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str
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



