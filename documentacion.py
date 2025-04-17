from ast import Dict
            
#https://fastapi.tiangolo.com/advanced/additional-responses/

def documentacion_sesion() -> dict:
    return {
    "summary": "Crear un nuevo token",
    "description": "Enviando credenciales v\u00e1lidas, el m\u00e9todo devuelve un token JWT que debe ser utilizado en los dem\u00e1s recursos del servicio.",
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
                                "description": "Permite solo caracteres alfanum\u00e9ricos (may\u00fasculas, min\u00fasculas, n\u00fameros). Longitud: 6 a 10 caracteres.",
                                "pattern": "^[a-zA-Z0-9]{6,10}$",
                                "minLength": 6,
                                "maxLength": 10,
                                "examples": [
                                    "challenge"
                                ]
                            },
                            "password": {
                                "type": "string",
                                "description": "Debe tener 8 caracteres exactos, al menos una letra may\u00fascula, un n\u00famero y uno de los s\u00edmbolos '+', '*', '-'.",
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
                        "password": "M1i+sqss"
                    }
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Sesi\u00f3n iniciada exitosamente",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "access_token": {
                                "type": "string",
                                "description": "Token de acceso JWT",
                                "pattern": "^[a-zA-Z0-9]{20,40}\\.[a-zA-Z0-9]+\\.[a-zA-Z0-9_-]+$"
                            },
                            "token_type": {
                                "type": "string",
                                "description": "Tipo de token",
                                "pattern": "^bearer$"
                            },
                            "access_token_expires": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Tiempo de expiraci\u00f3n del token en segundos (entero positivo)."
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
                                            "pattern": "^[A-Z\\s]{1,20}$"
                                        },
                                        "numero": {
                                            "type": "string",
                                            "description": "N\u00famero de tarjeta",
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
        }
    }
}


def documentacion_cuentas() -> dict:
    return {
    "summary": "Obtiene cuentas en base al n\u00famero de tarjeta enviado",
    "description": "Se debe enviar el n\u00famero de tarjeta en la solicitud.",
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
                                            "description": "N\u00famero de cuenta bancaria (6 a 12 d\u00edgitos)"
                                        },
                                        "tipo": {
                                            "type": "string",
                                            "pattern": "^[A-Z\\s$]{2,10}$",
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
        "504": {
            "description": "N\u00famero de tarjeta inv\u00e1lido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El campo 'numero_tarjeta' es inv\u00e1lido."
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "description": "N\u00famero de tarjeta v\u00e1lido (15 a 19 d\u00edgitos)"
                            }
                        },
                        "required": [
                            "numero_tarjeta"
                        ]
                    },
                    "example": {
                        "numero_tarjeta": "82584085344322999"
                    }
                }
            }
        }
    }
}


def documentacion_saldo() -> dict:
    return {
    "summary": "Obtiene el saldo en base a un n\u00famero de cuenta.",
    "description": "Se requiere el n\u00famero de cuenta para obtener el saldo.",
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
                                "description": "Saldo en formato num\u00e9rico con coma decimal"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "N\u00famero de cuenta inv\u00e1lido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El campo 'numero' es inv\u00e1lido"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "description": "N\u00famero de cuenta entre 6 y 12 d\u00edgitos"
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
    "description": "Se debe enviar el n\u00famero de cuenta y el rango de fechas.",
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
                                            "pattern": "^\\d{8}$",
                                            "description": "Fecha en formato YYYYMMDD"
                                        },
                                        "monto": {
                                            "type": "string",
                                            "pattern": "^[0-9]+(\\.[0-9]{2})?$",
                                            "description": "Monto en formato decimal (Ej: 20000.00)"
                                        },
                                        "descripcion": {
                                            "type": "string",
                                            "maxLength": 100,
                                            "description": "Descripci\u00f3n de la transacci\u00f3n"
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
            "description": "Datos inv\u00e1lidos",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Datos inv\u00e1lidos"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "description": "N\u00famero de cuenta entre 6 y 12 d\u00edgitos"
                            },
                            "desde": {
                                "type": "string",
                                "pattern": "^\\d{8}$",
                                "description": "Fecha inicial en formato YYYYMMDD"
                            },
                            "hasta": {
                                "type": "string",
                                "pattern": "^\\d{8}$",
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
                        "numero": "99083422",
                        "desde": "20240101",
                        "hasta": "20240430"
                    }
                }
            }
        }
    }
}


def documentacion_estado() -> dict:
    return {
    "summary": "Obtiene el estado del usuario",
    "description": "No se debe enviar un body. Solo se requiere un token v\u00e1lido en el header Authorization (usando el candado en /docs).",
    "response_description": "Informa el estado del usuario",
    "responses": {
        "200": {
            "description": "Informaci\u00f3n recuperada satisfactoriamente",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
    "summary": "Cierra la sesi\u00f3n",
    "description": "No se debe enviar un body. Solo se requiere un token v\u00e1lido en el header Authorization (candado en /docs).",
    "response_description": "Deshabilita el token",
    "responses": {
        "200": {
            "description": "Proceso terminado satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Has cerrado sesi\u00f3n exitosamente"
                    },
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Mensaje de confirmaci\u00f3n de logout"
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
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
                                "pattern": "^[A-Z\u00d1a-z\u00f10-9\\s'\\-\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da,.:]+$",
                                "description": "Mensaje de error devuelto por el servidor"
                            }
                        }
                    }
                }
            }
        }
    }
}
