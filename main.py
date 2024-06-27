#https://www.youtube.com/watch?v=uNl8nlnBVMc
from fastapi.encoders import jsonable_encoder
from babel.numbers import format_currency
import json
from aiofile import async_open
from asyncio import sleep
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
#from documentacion import documentacion_cuentas, documentacion_estado, documentacion_loout, documentacion_mov, documentacion_saldo, documentacion_sesion
from documentacion import documentacion_cuentas, documentacion_estado, documentacion_loout, documentacion_mov, documentacion_saldo, documentacion_sesion
from genSaldo import generar_json_saldo
from genTarjetas import generar_json_tarjetas
from genCuentas import generar_json_cuentas
from genUltMovimientos import generarFechas
from fastapi import FastAPI, Depends, HTTPException, Header, Request, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.openapi.utils import get_openapi
from respuesta_modelos import Cuentas_response, PagoRespuesta, Saldo_response, Sesion_response, movimiento_respuesta
from solicitud_modelos import Movimientos, PagoRequest, Tarjeta, Usuario, Cuenta
from decimal import Decimal

app = FastAPI(description="API-Wallet", version="0.1.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/wallet/sesion')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "01330dc7af5264e5ef8f880486dbe52045c0c5f2b060daa372783ff10bacb2d9" # Ideal es que este en una variable de entorno bien oculto (openssl rand -hex 32)
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()
# Configuración de CORS
""" origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",  # Agrega las URLs necesarias
] """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

# Variable para realizar un seguimiento del número de solicitudes
request_count = 0
# Estructura para almacenar tokens inhabilitados (puede ser una lista, un conjunto, o una base de datos)
disabled_tokens = set()

#_____________________________________________

saldo_CA_p_99083422 = Decimal('1004500.00')
saldo_CA_p_96703737 = Decimal('234443.23')
saldo_CC_USD_93125576 = Decimal('545623.13')
#_____________________________________________

#--------------------------------------------------------------------------------------------------
description = """
La API de Wallet es un servicio que brinda a los usuarios la capacidad de gestionar 
sus cuentas

bancarias,realizar transacciones y acceder de forma segura a su información financiera.
 
Esta API se ha diseñado con un enfoque en la seguridad y la eficiencia. 🚀

Servicio con fines de entrenamiento
"""
def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title="API-challenge [entrenamiento]",#,app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=description,
            terms_of_service=app.terms_of_service,
            contact={
                    "name": "Mariano Imende",
                    "url": "http://contact/",
                    "email": "imende.mariano",
            },
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        
        # for _, method_item in app.openapi_schema.get('paths').items():
            
        #     for _, param in method_item.items():
        #         responses = param.get('responses')
        #         # remove 422 response, also can remove other status code
        #         # if '422' in responses:
        #         #     del responses['422']
    
    return app.openapi_schema

app.openapi = custom_openapi



#-----------------------------------------------------------------------------------------------------
# Configura los datos del usuario para demostración (deberías obtener esto de una base de datos)
USERS_DB = {
    "challenge": {
        "username": "challenge",
        "hashed_password": "$2b$12$NLrNyrG528pi3U7f42FnJuxOV3pA61f5u.0bvkI/xoJ3cOAEmTLDG", #
        "email" : "challenge@challenge.com.ar",
        "disabled" : False,
        
    },
    "prueba": {
        "username": "prueba",
        "hashed_password": "$2b$12$NLrNyrG528pi3U7f42FnJuxOV3pA61f5u.0bvkI/xoJ3cOAEmTLDG", #
        "email" : "prueba@challenge.com.ar",
        "disabled" : False,
        
    }
}

#esquema para los usuarios generales
class User(BaseModel):
  username:str
  email:Union[str, None] = None
  disabled:Union[bool, None] = None

#para los usuarios existentes
class UserInDB(User):
  hashed_password:str

  
def get_user(db,username):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    return[]

 
def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)
    

#valida la existencia del usuario y password
def autenticate_user(db,username,password):
    user = get_user(db, username)
    if isinstance(user, User) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    if verify_password(password, user.hashed_password) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)#valor predeterminado
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_JWT = jwt.encode(data_copy, key=SECRET_KEY,algorithm=ALGORITHM)
    return token_JWT

#función que obtiene el username dentro del token JWT
def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
             raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
             raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    user = get_user(USERS_DB,username)     
    if not user:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

#garantiza que el token no haya expirado
def get_user_disable_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user

# Middleware para validar el token en rutas protegidas
def validate_token(token: str):
    if token in disabled_tokens:
        # El token se encuentra en la lista de tokens inhabilitados, se considera inválido
        return False
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
            return False
    except JWTError:
        return False
    return True

from fastapi.responses import JSONResponse

#get_swagger_ui_html(openapi_url="/docs", title="FastAPSSSSSSI", swagger_favicon_url="https://www.infobae.com/pf/resources/favicon/favicon.ico?d=2061")
from fastapi.openapi.docs import get_swagger_ui_html
# #https://dev.to/kludex/how-to-change-fastapis-swagger-favicon-4j6
# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return get_swagger_ui_html(
#         openapi_url="/openapi.json",
#         title="Wallet",
#         swagger_favicon_url="https://www.infobae.com/pf/resources/favicon/favicon.ico?d=2061"
#     )
    
# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return get_swagger_ui_html(
#         openapi_url="/openapi.json",
#         title="Wallet",
#         swagger_favicon_url=""
#     ) 
    # return """
    # <h1>API Docs</h1>
    # <p>Redirecting to <a href="/docs">docs</a>...</p>
    # <p>Redirecting to <a href="/redoc">redoc</a>...</p>
    # <p>Redirecting to <a href="/openapi.json">openapi.json</a>...</p>
    # """

#https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags
@app.post('/wallet/sesion', response_model=Sesion_response ,** documentacion_sesion(),tags=["Usuario"])
async def sesion(usuario: Usuario):
    
    username = usuario.username # data.get("username")
    password = usuario.password #data.get("password")
    user = autenticate_user(USERS_DB, username,password)
#     async def token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = autenticate_user(USERS_DB, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_JWT = create_token({"sub": user.username}, access_token_expires)

    json = {
            "access_token": access_token_JWT,
            "token_type": "bearer",
            "access_token_expires": str(access_token_expires)}
    if username == "challenge":
        json.update({"tarjetas": [{"descripcion": "BANCO HIPOTECARIO", "numero": "825840853443"}, {"descripcion": "BANCO HSBC", "numero": "423455721156"}, {"descripcion": "BANCO DE LA PROVINCIA DE BUENOS AIRES", "numero": "595278769781"}]})
    else:
        json.update(generar_json_tarjetas())
    #sleep(1000)
    return json

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        
        """Maneja las excepciones de validación de solicitud."""
        if "json_invalid" in str(exc):
            return JSONResponse(status_code=422, content={"detail": "json invalido"})
        elif "Field required'" in str(exc.body):
            return JSONResponse(status_code=400, content={"detail": "Bad Request"})
        elif "string_too_long" in str(exc):
            print(str(exc))
            return JSONResponse(status_code=400, content={"detail":exc.errors()[0]['msg'] + " - " + str(exc.errors()[0]['input']) + str(exc.errors()[0]['ctx'])})
        elif "No se pudo validar las credenciales" in str(exc):
            return JSONResponse(status_code=401, content={"detail": "Error de autenticación"})
        elif "Internal Server Error" in str(exc):
            return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
        elif "otro_tipo_de_error_adicional" in str(exc):
            return JSONResponse(status_code=408, content={"detail": "Tiempo de espera excedido"})
        else:
        # Manejar otros tipos de errores de validación
            return await request.exception_handler(exc)
    except:
            print(str(exc))
            #return JSONResponse(status_code=500, content={"ssssdetalle": "Error interno del servidor"})
    
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     if "json_invalid" in str(exc):
#         return JSONResponse(status_code=422, content={"detail": "json invalido"})
#     return await request.exception_handler(exc)

@app.post('/wallet/cuentas', response_model=Cuentas_response, **documentacion_cuentas(),tags=["Rutas protegidas"])
async def cuentas(tarjeta: Tarjeta, user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
         
    if not tarjeta.numero_tarjeta.isdigit() or not tarjeta.numero_tarjeta or not isinstance(tarjeta.numero_tarjeta, str):
       raise HTTPException(status_code=400, detail="El campo 'numero_tarjeta' es inválido.")
        
    if user.username == "challenge":    
     
      if tarjeta.numero_tarjeta == "825840853443":
            return {"cuentas": [{"numero_cuenta": "99083422", "tipo": "CA $"}, {"numero_cuenta": "96703737", "tipo": "CA $"}, {"numero_cuenta": "93125576", "tipo": "CA USD"}]}
      elif tarjeta.numero_tarjeta == "423455721156":
            return {"cuentas": [{"numero_cuenta": "1209383422", "tipo": "CA $"}]}
      elif tarjeta.numero_tarjeta == "595278769781":
            return {"cuentas": [{"numero_cuenta": "34948473811", "tipo": "CC $"},{"numero_cuenta": "102033534534521", "tipo": "CA $"}]}
      else:
          raise HTTPException(status_code=400, detail="El campo 'numero_tarjeta' es inválido.")
    else:
     return generar_json_cuentas()
     
@app.post('/wallet/saldo',response_model=Saldo_response,**documentacion_saldo(),tags=["Rutas protegidas"])
async def saldo(cuenta: Cuenta , user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
    
    if not cuenta.numero.isdigit() or not cuenta.numero or not isinstance(cuenta.numero, str):
           raise HTTPException(status_code=400, detail="El campo 'numero_cuenta' es inválido.")

    if user.username == "challenge":
        if cuenta.numero == "99083422":
            return {"saldo":saldo_CA_p_99083422,"moneda":"ARS"} #
            #return {"saldo": format_currency(abs(saldo_CA_p_99083422), 'ARS', locale='es_AR'),"moneda":"USD"}
        elif cuenta.numero == "96703737":
            return {"saldo": saldo_CA_p_96703737,"moneda":"ARS"}
        elif cuenta.numero == "93125576":
            return {"saldo": saldo_CC_USD_93125576,"moneda":"USD"}
        elif cuenta.numero == "1209383422":
            return {"saldo": "$19.209,19"}
        elif cuenta.numero == "34948473811":
            return {"saldo": "$0.000,00"}
        elif cuenta.numero == "102033534534521":
            return {"saldo": "$150498.000,00"}
        # else: ESTA COMENTADO A PROPOSITO
        #   raise HTTPException(status_code=400, detail="El campo 'numero_cuenta' es inválido.")
    else:
        json_generado = generar_json_saldo()
        return json_generado
    
@app.post('/wallet/ultmovimientos', response_model=movimiento_respuesta, **documentacion_mov(),tags=["Rutas protegidas"])
async def ultmovimientos(mov: Movimientos, fecha_desde: str, fecha_hasta: str, user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
   
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
       
    if not mov.numero_cuenta.isdigit() or not mov.numero_cuenta:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    
    if len(fecha_desde) != 8 or len(fecha_hasta) != 8:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    try:
        datetime.strptime(fecha_desde, "%Y%m%d")
        datetime.strptime(fecha_hasta, "%Y%m%d")
    except ValueError:
            raise HTTPException(status_code=400, detail="Datos inválidos")
    
    if user.username == "challenge":
        if mov.numero_cuenta == "99083422":
            return {"movimientos": [{"fecha": "20230931", "monto": -2878.73, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230831", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20231201", "monto": -2818.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230702", "monto": 3375.00, "descripcion": "Transferencia Credito"}, {"fecha": "20230131", "monto": -9009.80, "descripcion": "Compra"}]}
        elif mov.numero_cuenta == "96703737":
            return {"movimientos": [{"fecha": "20230123", "monto": 10828.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230831", "monto": -1182.17, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230121", "monto": 2575.53, "descripcion": "Compra"}, {"fecha": "20230111", "monto": -9339.8, "descripcion": "Compra"}]}
        elif mov.numero_cuenta == "93125576":
            return {"movimientos": [{"fecha": "20231005", "monto": -118.00, "descripcion": "Retiro de cajero automático"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25575.43, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -9339.00, "descripcion": "Pago de impuestos y servicio"}]}
        elif mov.numero_cuenta == "1209383422":
            return {"movimientos": [{"fecha": "20231205", "monto": 5578.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25575.43, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -9339.00, "descripcion": "Pago de impuestos y servicio"}]}   
        elif mov.numero_cuenta == "34948473811":
            return {"movimientos": [{"fecha": "20231205", "monto": 78.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -28158.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20230114", "monto": -28308.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -31.56, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25075.40, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -7399.00, "descripcion": "Pago de impuestos y servicio"}]}      
        elif mov.numero_cuenta == "102033534534521":
            return {"movimientos": [{"fecha": "20230123", "monto": 10828.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230831", "monto": -1182.17, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230121", "monto": 2575.53, "descripcion": "Compra"}, {"fecha": "20230111", "monto": -9339.8, "descripcion": "Compra"}]}
        else: 
           raise HTTPException(status_code=400, detail="Datos inválidos")
    else:    
           return generarFechas(fecha_desde,fecha_hasta)

    
@app.post('/wallet/pago', response_model=PagoRespuesta,tags=["Rutas protegidas"])
async def pago(Pago_request: PagoRequest): #, user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)

    # Extraer datos del modelo de solicitud
    qr_id = Pago_request.qr_id
    importe = Pago_request.Importe    
    pagador = Pago_request.pagador
    adquiridor = Pago_request.adquiridor
    cuenta = Pago_request.pagador.cuenta.numero
    # Validar que se proporcionen los datos esenciales
    if not qr_id or not importe or not pagador or not adquiridor:
        raise HTTPException(status_code=400, detail="Datos incompletos en la solicitud")

   
    if cuenta == "99083422":
        global saldo_CA_p_99083422
        saldo_CA_p_99083422 = saldo_CA_p_99083422 - Decimal(importe.valor)
    if cuenta == "96703737":
        global saldo_CA_p_96703737
        saldo_CA_p_96703737 = saldo_CA_p_96703737 - Decimal(importe.valor) 
    if cuenta == "93125576":
        global saldo_CC_USD_93125576
        saldo_CC_USD_93125576 = saldo_CC_USD_93125576 - Decimal(importe.valor)
        
    # Simulación de procesamiento de pago
    response_data = {
        "qr_id": qr_id,
        "importe": importe,
        "transaccion": {
            "codigo": "101",
            "descripcion": "Approved",
            "fecha": datetime.utcnow().isoformat() + "Z",
            "codigo_autorizacion": "xizF2ugr3",
            "importe": importe,
        },
    }

    return response_data

@app.delete('/wallet/logout', **documentacion_loout(),tags=["Rutas protegidas"])
async def logout(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')  
       
    if token and token.scheme == "Bearer":
        # Utiliza token.credentials para acceder al token
        token_value = token.credentials
        # Inhabilita el token agregándolo a la lista de tokens inhabilitados
        disabled_tokens.add(token_value)
        # Devuelve un mensaje indicando que la sesión se ha cerrado exitosamente
    return {" message": "Has cerrado sesión exitosamente"}

@app.get('/wallet/estado', **documentacion_estado(),tags=["Rutas protegidas"])
async def estado(user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):#str = Depends(oauth2_scheme) determina que la ruta es privada
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
    return user
