from decimal import Decimal
from pydantic import BaseModel, Field

import re
from typing import Annotated, Final

import regex

#https://fastapi.tiangolo.com/tutorial/schema-extra-example/
#https://docs.pydantic.dev/latest/concepts/fields/#field-aliases
#/wallet/sesion
TEMPLATE_STR_REGEX: Final[re.Pattern] = re.compile(
    r"^(?=.*[A-Z])(?=.*[+*-])(?=.*[0-9]).{8}$"
)


class Usuario(BaseModel):
    username: str# = Field(..., pattern=r"^[a-zA-Z0-9]{6,10}$")
    password: str# = Field(..., pattern=r"^(?=.*[A-Z])(?=.*[+*-])(?=.*[0-9]).{8}$")
    #username: str = Field(..., examples=["challenge"],min_length=9, max_length=9, pattern=r"bearer")
    #password: str = Field(..., examples=["challenge"])

class SesionHeaders(BaseModel):
    Authorization: str = "Bearer"

#/wallet/cuentas    
class Tarjeta(BaseModel):
    numero_tarjeta: str = Field(...,description="numero de tarjeta", examples=["825840853443"], min_length=2, max_length=13)
   
#/wallet/saldo
class Cuenta(BaseModel):
    numero_cuenta: str = Field(..., examples=["99083422"])
    
#/wallet/ultmovimientos
class Movimientos(BaseModel):
    numero_cuenta: str
    tipo: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "numero_cuenta": "99083422",
                    "tipo": "CA $",
                }
            ]
        }
    }

# Modelo de solicitud
#/wallet/pago
class Importe(BaseModel):
    valor: Decimal  
    moneda: str

class Documento(BaseModel):
    tipo: str
    numero: str

class Cuenta(BaseModel):
    numero: str = Field(default=None,examples=["99083422"])
    tipo: str =  Field(default=None,examples=["CA $"])
class Wallet(BaseModel):
    nombre: str
    cuit: str

class Pagador(BaseModel):
    nombre: str
    numero_identificador: str
    documento: Documento
    cuenta: Cuenta
    wallet: Wallet

class Adquiridor(BaseModel):
    ticket: str
    cuil: str

class PagoRequest(BaseModel):
    qr_id: str
    qr: str
    Importe: Importe
    pagador: Pagador
    adquiridor: Adquiridor
