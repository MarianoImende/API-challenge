from fastapi import FastAPI

app = FastAPI()


@app.get("/sesion")
async def root():

    response = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaGFsbGVuZ2UiLCJleHAiOjE3MTA0Mjc0NTJ9.7dB7Oo-5xumCSq0uY1_eujdlZB8OOgbSULrtx65uGv0",
    "token_type": "bearer",
    "access_token_expires": 1800.0,
    "tarjetas": [
        {
            "descripcion": "BANCO HIPOTECARIO",
            "numero": "825840853443"
        },
        {
            "descripcion": "BANCO HSBC",
            "numero": "423455721156"
        },
        {
            "descripcion": "BANCO DE LA PROVINCIA DE BUENOS AIRES",
            "numero": "595278769781"
        }
    ]
}
    return response


if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app="sesion:app", host="127.0.0.1", port=8010,reload=True)
    uvicorn.run(app, host="127.0.0.1", port=8001)
    #uvicorn.run(app="1:app", host="127.0.0.1", port=60, reload=True,)