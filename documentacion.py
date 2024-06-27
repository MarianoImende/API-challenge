from ast import Dict

from pydantic import BaseModel
#https://fastapi.tiangolo.com/advanced/additional-responses/
def documentacion_sesion() -> Dict:

        documentation = {
        "summary": "Crear un nuevo token",
        "description": "Ejemplo de solicitud:",
        "response_description": "Access token creado satisfactoriamente",
        "responses": {
            200: {
                "description": "Token creado satisfactoriamente",
                "content": {
                    "application/json": {
                        # "schema": {
                        # "$ref": "#/components/schemas/Item"
                    #}
                        "example": {"access_tokens": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaGFsbGVuZ2UiLCJleHAiOjE3MTA0Mjc0NTJ9.7dB7Oo-5xumCSq0uY1_eujdlZB8OOgbSULrtx65uGv0","token_type": "bearer","access_token_expires": 1800.0,"tarjetas": [{"descripcion": "BANCO HIPOTECARIO","numero": "825840853443"},{"descripcion": "BANCO HSBC","numero": "423455721156"},{"descripcion": "BANCO DE LA PROVINCIA DE BUENOS AIRES","numero": "595278769781"}]}
                    }
                }
            },            
            400: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Bad Request"}
                    }
                }
            },
            401: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            404: {
                "description": "Error recurso no encontrado",
                "content": {
                    "application/json": {
                        "example": {"detail": "Not Found"}
                    }
                }
            },
            422: {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation

#--------------------------------------------------------------------------------

    
def documentacion_cuentas() -> Dict:

        documentation = {
        "summary": "Obtiene cuentas en base al numero de tarjeta enviado",
        "description": "Ejemplo de solicitud:",
        "response_description": "listado de cuentas asociadas a la tarjeta",
        "responses": {
            200: {
                "description": "Cuentas obtenida satisfactoriamente",
                "content": {
                    "application/json": {
                        "example": {"cuentas": [{"numero_cuenta": "99083422", "tipo": "CA $"}]}
                    }
                }
            },
            504: {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "example": {"detail": "El campo 'numero_tarjeta' es inválido."}
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation
    
    
#--------------------------------------------------------------------------------

    
def documentacion_saldo() -> Dict:

        documentation = {
        "summary": "Obtiene el saldo en base a un numero de cuenta.",
        "description": "Ejemplo de solicitud:",
        "response_description": "Informa el saldo de la cuenta",
        "responses": {
            200: {
                "description": "Saldo obtenido satisfactoriamente",
                "content": {
                    "application/json": {
                        "example": {"saldo": "545,00"}
                    }
                }
            },
            400: {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "example": {"detail": "El campo 'numero' es inválidos"}
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation
    
        
#--------------------------------------------------------------------------------

    
def documentacion_mov() -> Dict:

        documentation = {
        "summary": "Obtiene los movimientos por rango de fechas",
        "description": "Ejemplo de solicitud:",
        "response_description": "Informa los movimientos de la cuenta",
        "responses": {
            200: {
                "description": "Movimientos obtenidos satisfactoriamente",
                "content": {
                    "application/json": {
                        
                        "example": {"movimientos": [{"fecha": "20240512", "monto": "20000.00", "descripcion": "Ingreso en efectivo"}]}
                       
                    }
                }
            },
            400: {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "example": {"detail": "Datos inválidos"}
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation
    
def documentacion_estado() -> Dict:

        documentation = {
        "summary": "Obtiene el estado del usuario",
        "description": "Ejemplo de solicitud: para este recurso, no de debe enviar un body, simplemente ingrese el token en la interafaz authorizations (botón en la esquina superior derecha de su pantalla en los autodocs de Swagger UI (en /docs) icono del candado), donde puede escriba su clave API en el el campo value. Esto establecerá el Authorization encabezado en los encabezados de la solicitud.",
        "response_description": "Informa el estado del usuario",
        "responses": {
            200: {
                "description": "información recuperada satisfactoriamente",
                "content": {
                    "application/json": {
                        "example":{"username": "challenge", "email": "string", "disabled": "boolean", "hashed_password": "string"}
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation

def documentacion_loout() -> Dict:

        documentation = {
        "summary": "Cierra la sesion",
        "description": "Ejemplo de solicitud: para este recurso, no de debe enviar un body, simplemente ingrese el token en la interafaz authorizations (botón en la esquina superior derecha de su pantalla en los autodocs de Swagger UI (en /docs) icono del candado), donde puede escriba su clave API en el el campo value. Esto establecerá el Authorization encabezado en los encabezados de la solicitud.",
        "response_description": "Deshabilita el token",
        "responses": {
            200: {
                "description": "proceso termindao satisfactoriamente",
                "content": {
                    "application/json": {
                        "example": {"message": "Has cerrado sesión exitosamente"}
                    }
                }
            },
            401: {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
            500: {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            }
        }
    }
        return documentation
    