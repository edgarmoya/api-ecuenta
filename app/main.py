from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pdf_processing


app = FastAPI(
    title="Estado de Cuenta API",
    summary=(
        "Esta API permite analizar los archivos PDF con el estado de cuenta de los agentes de telecomunicaciones que pueden descargar a través de Transfermóvil"
    ),
    description=(
        "A partir del estado de cuentas la API ofrece distintos endpoints para:\n\n"
        "- Obtener el contenido completo del estado de cuenta en formato estructurado\n\n"
        "- Extraer información específica, como **depósitos**, **recargas** realizadas, **ganancias** y otros detalles relevantes\n\n"
    ),
    version="1.0.0",
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ecuenta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_processing.router, prefix="/pdf", tags=['Procesar PDF'])
