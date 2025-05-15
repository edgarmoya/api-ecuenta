from fastapi import FastAPI, Request
from app.api.v1 import pdf, auth, user
from contextlib import asynccontextmanager
from app.db.database import create_db_and_tables

from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

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
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == HTTP_401_UNAUTHORIZED and exc.detail == "Not authenticated":
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "No autenticado. Por favor, incluye un token válido"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(auth.router, prefix="/auth", tags=['Autenticación'])
app.include_router(user.router, prefix="/user", tags=['Usuario'])
app.include_router(pdf.router, prefix="/pdf", tags=['Procesar PDF'])