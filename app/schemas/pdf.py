from pydantic import BaseModel
from fastapi import Query, UploadFile, File
from typing import List, Optional, Literal
from .transaction import TransactionData

class PdfContentRequest(BaseModel):
    file: UploadFile = File(...),
    status: Literal['all', 'successful', 'failed'] = Query('sucessful', description="Estado de laa transacción")
    page: Optional[int] = Query(None, ge=1, description="Número de página a extraer")
    limit: Optional[int] = Query(None, ge=5, description="Cantidad de transacciones por página")

class PdfTransactionsResponse(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    results: List[TransactionData]
    
class PdfDepositsResponse(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    total_amount: float
    results: List[TransactionData]

class PdfSalesResponse(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    total_amount: float
    total_saldo: float
    total_propia: float
    total_movil: float
    total_nauta: float
    total_nauta_hogar: float
    total_factura: float
    profits: float
    results: List[TransactionData]
