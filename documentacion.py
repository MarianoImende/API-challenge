from ast import Dict
            
#https://fastapi.tiangolo.com/advanced/additional-responses/

def documentacion_bienvenida() -> dict:
    return {
        "summary": "Bienvenida",
        "description": "Bienvenido a la API de entrenamiento:",
        "response_description": "Bienvenido a la API de entrenamiento",
        "responses": {
            200: {
                "description": "Bienvenido a la API de entrenamiento",
                "content": {
                    "application/json": {
                        "example": {
                            "mensaje": "Bienvenido a la API de entrenamiento",
                            "Contrato": "/docs"
                        }
                    }
                }
            }            
        }
    }

def documentacion_sesion() -> dict:
    return {
    "summary": "Crear un nuevo token",
    "description": "Enviando credenciales válidas, el método devuelve un token JWT que debe ser utilizado en los demás recursos del servicio.",
    "response_description": "Access token creado satisfactoriamente",
    "openapi_extra": {
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Permite solo caracteres alfanuméricos (mayúsculas, minúsculas, números). Longitud: 6 a 10 caracteres.",
                                "pattern": "^[a-zA-Z0-9]{6,10}$",
                                "minLength": 6,
                                "maxLength": 10,
                                "examples": [
                                    "challenge"
                                ]
                            },
                            "password": {
                                "type": "string",
                                "description": "Debe tener 8 caracteres exactos, al menos una letra mayúscula, un número y uno de los símbolos '+', '*', '-'.",
                                "pattern": "^(?=.*[A-Z])(?=.*[+*-])(?=.*[0-9]).{8}$",
                                "minLength": 8,
                                "maxLength": 8,
                                "examples": [
                                    "M1i+sqss",
                                    "Op-loi+0",
                                    "R*1ndfew"
                                ]
                            }
                        },
                        "required": [
                            "username",
                            "password"
                        ]
                    },
                    "example": {
                        "username": "challenge",
                        "password": "challenge"
                    }
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Sesión iniciada exitosamente",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "access_token": {
                                "type": "string",
                                "description": "Token de acceso JWT",
                                "pattern": "^[a-zA-Z0-9]{20,40}\.[a-zA-Z0-9]+\.[a-zA-Z0-9_-]+$"
                            },
                            "token_type": {
                                "type": "string",
                                "description": "Tipo de token",
                                "pattern": "^bearer$"
                            },
                            "access_token_expires": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Tiempo de expiración del token en segundos (entero positivo)."
                            },
                            "tarjetas": {
                                "type": "array",
                                "description": "Lista de tarjetas asociadas a la cuenta",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "descripcion": {
                                            "type": "string",
                                            "description": "Nombre del banco",
                                            "pattern": "^[A-Z\s]{1,20}$"
                                        },
                                        "numero": {
                                            "type": "string",
                                            "description": "Número de tarjeta",
                                            "pattern": "^[0-9]{15,19}$"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "example": {
                        "access_token": "token.jwt.secreto",
                        "token_type": "bearer",
                        "access_token_expires": 1800,
                        "tarjetas": [
                            {
                                "descripcion": "NOVA TRUST BANK",
                                "numero": "825840853443"
                            },
                            {
                                "descripcion": "TITANIUM FINANCE BANK",
                                "numero": "423455721156"
                            },
                            {
                                "descripcion": "ASTRA CAPITAL BANK",
                                "numero": "595278769781"
                            }
                        ]
                    }
                }
            }
        },
        
        "401": {
                "description": "No autorizado",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            },
        "404": {
                "description": "Recurso no encontrado",
                "content": {
                    "application/json": {
                        "example": {"detail": "Not Found"}
                    }
                }
            },
         "422": {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
          "500": {
                "description": "Generic Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Error interno del servidor"}
                    }
                }
            },
            "504": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {"detail": "Bad Request"}
                    }
                }
            },
    }
}


def documentacion_cuentas() -> dict:
    return {
    "summary": "Obtiene cuentas en base al número de tarjeta enviado",
    "description": "Se debe enviar el número de tarjeta en la solicitud.",
    "response_description": "Listado de cuentas asociadas a la tarjeta",
    "responses": {
        "200": {
            "description": "Cuentas obtenidas satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "cuentas": [
                            {
                                "numero_cuenta": "99083422",
                                "tipo": "CA $"
                            }
                        ]
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cuentas": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "numero_cuenta": {
                                            "type": "string",
                                            "pattern": "^[0-9]{6,12}$",
                                            "description": "Número de cuenta bancaria (6 a 12 dígitos)"
                                        },
                                        "tipo": {
                                            "type": "string",
                                            "pattern": "^[A-Z\s$]{2,10}$",
                                            "description": "Tipo de cuenta (Ej: CA $, CC $)"
                                        }
                                    },
                                    "required": [
                                        "numero_cuenta",
                                        "tipo"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El campo 'numero_tarjeta' es inválido."
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
       "422": {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
        "500": {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    },
    "openapi_extra": {
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "numero_tarjeta": {
                                "type": "string",
                                "pattern": "^[0-9]{15,19}$",
                                "description": "Número de tarjeta válido (15 a 19 dígitos)"
                            }
                        },
                        "required": [
                            "numero_tarjeta"
                        ]
                    },
                    "example": {
                        "numero_tarjeta": "825840853443"
                    }
                }
            }
        }
    }
}


def documentacion_saldo() -> dict:
    return {
    "summary": "Obtiene el saldo en base a un número de cuenta.",
    "description": "Se requiere el número de cuenta para obtener el saldo.",
    "response_description": "Informa el saldo de la cuenta",
    "responses": {
        "200": {
            "description": "Saldo obtenido satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "saldo": "545,00"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "saldo": {
                                "type": "string",
                                "pattern": "^[0-9]+(,[0-9]{2})?$",
                                "description": "Saldo en formato numérico con coma decimal"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Número de cuenta inválido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El campo 'numero' es inválido"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "422": {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
        "500": {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    },
    "openapi_extra": {
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "numero": {
                                "type": "string",
                                "pattern": "^[0-9]{6,12}$",
                                "description": "Número de cuenta entre 6 y 12 dígitos"
                            }
                        },
                        "required": [
                            "numero"
                        ]
                    },
                    "example": {
                        "numero": "99083422"
                    }
                }
            }
        }
    }
}


def documentacion_mov() -> dict:
    return {
    "summary": "Obtiene los movimientos por rango de fechas",
    "description": "Se debe enviar el número de cuenta y el rango de fechas.",
    "response_description": "Informa los movimientos de la cuenta",
    "responses": {
        "200": {
            "description": "Movimientos obtenidos satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "movimientos": [
                            {
                                "fecha": "20240512",
                                "monto": "20000.00",
                                "descripcion": "Ingreso en efectivo"
                            }
                        ]
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "movimientos": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "fecha": {
                                            "type": "string",
                                            "pattern": "^\d{8}$",
                                            "description": "Fecha en formato YYYYMMDD"
                                        },
                                        "monto": {
                                            "type": "string",
                                            "pattern": "^[0-9]+(\.[0-9]{2})?$",
                                            "description": "Monto en formato decimal (Ej: 20000.00)"
                                        },
                                        "descripcion": {
                                            "type": "string",
                                            "maxLength": 100,
                                            "description": "Descripción de la transacción (maxLength: 100)"
                                        }
                                    },
                                    "required": [
                                        "fecha",
                                        "monto",
                                        "descripcion"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Datos inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Datos inválidos"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "422": {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
        "500": {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    },
    "openapi_extra": {
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "numero": {
                                "type": "string",
                                "pattern": "^[0-9]{6,12}$",
                                "description": "Número de cuenta entre 6 y 12 dígitos"
                            },
                            "fecha_desde": {
                                "type": "string",
                                "pattern": "^\d{8}$",
                                "description": "Fecha inicial en formato YYYYMMDD"
                            },
                            "fecha_hasta": {
                                "type": "string",
                                "pattern": "^\d{8}$",
                                "description": "Fecha final en formato YYYYMMDD"
                            }
                        },
                        "required": [
                            "numero",
                            "desde",
                            "hasta"
                        ]
                    },
                    "example": {
                                 "numero_cuenta": "99083422",
                                 "tipo": "CA $"
                               }
                }
            }
        }
    }
}


def documentacion_estado() -> dict:
    return {
    "summary": "Obtiene el estado del usuario",
    "description": "No se debe enviar un body. Solo se requiere un token válido en el header Authorization (usando el candado en /docs).",
    "response_description": "Informa el estado del usuario",
    "responses": {
        "200": {
            "description": "Información recuperada satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "username": "challenge",
                        "email": "string",
                        "disabled": "boolean",
                        "hashed_password": "string"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string"
                            },
                            "email": {
                                "type": "string",
                                "format": "email"
                            },
                            "disabled": {
                                "type": "boolean"
                            },
                            "hashed_password": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
         "422": {
                "description": "Error json invalido",
                "content": {
                    "application/json": {
                        "example": {"detail": "json invalido"}
                    }
                }
            },
        "500": {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    }
}


def documentacion_logout() -> dict:
    return {
    "summary": "Cierra la sesión",
    "description": "No se debe enviar un body. Solo se requiere un token válido en el header Authorization (candado en /docs).",
    "response_description": "Deshabilita el token",
    "responses": {
        "200": {
            "description": "Proceso terminado satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Has cerrado sesión exitosamente"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Mensaje de confirmación de logout"
                            }
                        }
                    }
                }
            }
        },
        "401": {
            "description": "No autorizado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No se pudo validar las credenciales"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        },
        "500": {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error interno del servidor"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-ZÑa-zñ0-9\s'\-áéíóúÁÉÍÓÚ,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    }
}

def documentacion_pago_qr() -> dict:
    return {
        "summary": "Procesa un pago a por medio de QR",
        "description": "Recibe información del pagador, importe y adquirente a partir de un código QR interoperable.",
        "response_description": "Pago procesado correctamente",
        "openapi_extra": {
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "qr_id": {"type": "string", "description": "Identificador único del código QR generado"},
                                "qr": {"type": "string", "description": "Contenido completo del código QR interoperable"},
                                "Importe": {
                                    "type": "object",
                                    "description": "Datos del importe a pagar",
                                    "properties": {
                                        "valor": {
                                            "type": "number",
                                            "minimum": 0,
                                            "description": "Valor numérico del importe total"
                                        },
                                        "moneda": {
                                            "type": "string",
                                            "pattern": "^[A-Z]{3}$",
                                            "description": "Moneda en formato ISO 4217 (ej: ARS)"
                                        }
                                    },
                                    "required": ["valor", "moneda"]
                                },
                                "pagador": {
                                    "type": "object",
                                    "description": "Información del usuario que realiza el pago",
                                    "properties": {
                                        "nombre": {"type": "string", "description": "Nombre completo del pagador"},
                                        "numero_identificador": {
                                            "type": "string",
                                            "pattern": "^[0-9]{6,12}$",
                                            "description": "Número identificador de la cuenta o del cliente"
                                        },
                                        "documento": {
                                            "type": "object",
                                            "description": "Documento identificatorio del pagador",
                                            "properties": {
                                                "tipo": {
                                                    "type": "string",
                                                    "pattern": "^(DNI|CUIT|LC|LE)$",
                                                    "description": "Tipo de documento válido"
                                                },
                                                "numero": {
                                                    "type": "string",
                                                    "pattern": "^[0-9]{7,9}$",
                                                    "description": "Número de documento"
                                                }
                                            },
                                            "required": ["tipo", "numero"]
                                        },
                                        "cuenta": {
                                            "type": "object",
                                            "description": "Cuenta desde la cual se realiza el pago",
                                            "properties": {
                                                "numero": {
                                                    "type": "string",
                                                    "pattern": "^[0-9]{6,12}$",
                                                    "description": "Número de cuenta bancaria"
                                                },
                                                "tipo": {
                                                    "type": "string",
                                                    "pattern": "^(CA \$|CC \$)$",
                                                    "description": "Tipo de cuenta (Caja de Ahorro o Cuenta Corriente en pesos)"
                                                }
                                            },
                                            "required": ["numero", "tipo"]
                                        },
                                        "wallet": {
                                            "type": "object",
                                            "description": "Información de la billetera virtual utilizada",
                                            "properties": {
                                                "nombre": {"type": "string", "description": "Nombre de la billetera virtual"},
                                                "cuit": {
                                                    "type": "string",
                                                    "pattern": "^[0-9]{2}-[0-9]{8}-[0-9]$",
                                                    "description": "CUIT del proveedor de la billetera"
                                                }
                                            },
                                            "required": ["nombre", "cuit"]
                                        }
                                    },
                                    "required": ["nombre", "numero_identificador", "documento", "cuenta", "wallet"]
                                },
                                "adquiridor": {
                                    "type": "object",
                                    "description": "Entidad que recibe el pago",
                                    "properties": {
                                        "ticket": {"type": "string", "description": "Código del ticket generado por el adquirente"},
                                        "cuil": {
                                            "type": "string",
                                            "pattern": "^[0-9]{2}-[0-9]{8}-[0-9]$",
                                            "description": "CUIL de la entidad adquirente"
                                        }
                                    },
                                    "required": ["ticket", "cuil"]
                                }
                            },
                            "required": ["qr_id", "qr", "Importe", "pagador", "adquiridor"]
                        },
                        "example": {
                            "qr_id": "QR123456789",
                            "qr": "00020101021153039865802AR...",
                            "Importe": {"valor": 12500.5, "moneda": "ARS"},
                            "pagador": {
                                "nombre": "Lucía González",
                                "numero_identificador": "99083422",
                                "documento": {"tipo": "DNI", "numero": "30123456"},
                                "cuenta": {"numero": "99083422", "tipo": "CA $"},
                                "wallet": {"nombre": "Wallet Argentina", "cuit": "20-30123456-3"}
                            },
                            "adquiridor": {
                                "ticket": "TCK123456789",
                                "cuil": "27-27888999-7"
                            }
                        }
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Pago realizado correctamente",
                "content": {
                    "application/json": {
                        "example": {
                            "mensaje": "El pago fue procesado con éxito",
                            "estado": "aprobado",
                            "codigo_autorizacion": "APROB123456"
                        },
                        "schema": {
                            "type": "object",
                            "properties": {
                                "mensaje": {
                                            "type": "string", 
                                            "description": "Mensaje de confirmación del resultado",
                                            "pattern": "^{1,30}$"
                                            },
                                "estado": {
                                    "type": "string",
                                    "pattern": "^(aprobado|rechazado|pendiente)$",
                                    "description": "Estado final del procesamiento del pago"
                                },
                                "codigo_autorizacion": {"type": "string", 
                                                        "description": "Código de autorización emitido",
                                                        "pattern": "^(APROB[0-9]{6}|RECHA[0-9]{6}|PEND[0-9]{6})$"}
                            }
                        }
                    }
                }
            }
        }
    }

