from fastapi import APIRouter, Depends
from app.services.pdf_analyzer import PdfAnalyzer
from app.schemas.pdf import PdfContentRequest, PdfTransactionsResponse, PdfDepositsResponse, PdfSalesResponse
import tempfile

router = APIRouter()

@router.post("/transactions/", summary="Obtener todas las transacciones", response_model=PdfTransactionsResponse)
async def transactions(params: PdfContentRequest = Depends()):
    """
    Extrae todas las transacciones del estado de cuenta, de forma paginada si se especifica *file* y *page*
    - **file**: Archivo PDF del estado de cuenta
    - **status**: Estado de las transacciones
    - **page** (opcional): Número de página
    - **limit** (opcional): Número de transacciones por cada página
    """
    try:
        # Read request data
        status = params.status if params.status else None
        page = params.page if params.page else None
        limit = params.limit if params.limit else None

        # Save the PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await params.file.read())

        pdf_data = PdfAnalyzer(temp_pdf.name).transactions(transaction_status=status)

        # If no exist `page` and `limit`, return all data
        if page is None or limit is None:
            return PdfTransactionsResponse(results=pdf_data)

        # Apply pagination
        paginated_data = pdf_data[(page - 1) * limit: page * limit]

        return PdfTransactionsResponse(
            total=len(pdf_data), page=page, limit=limit, results=paginated_data
        )
    except Exception as e:
        return {"error": str(e)}

@router.post("/deposits/", summary="Obtener todos los depósitos realizados", response_model=PdfDepositsResponse)
async def deposits(params: PdfContentRequest = Depends()):
    """
    Extrae todos los depósitos del estado de cuenta, de forma paginada si se especifica *file* y *page*
    - **file**: Archivo PDF del estado de cuenta
    - **status**: Estado de las transacciones
    - **page** (opcional): Número de página
    - **limit** (opcional): Número de transacciones por cada página
    """
    try:
        # Read request data
        status = params.status if params.status else None
        page = params.page if params.page else None
        limit = params.limit if params.limit else None

        # Save the PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await params.file.read())

        total_amount, pdf_data = PdfAnalyzer(temp_pdf.name).deposits(transaction_status=status)

        # If no exist `page` and `limit`, return all data
        if page is None or limit is None:
            return PdfDepositsResponse(total_amount=total_amount, results=pdf_data)

        # Apply pagination
        paginated_data = pdf_data[(page - 1) * limit: page * limit]

        return PdfDepositsResponse(
            total=len(pdf_data), page=page, limit=limit, total_amount=total_amount, results=paginated_data
        )
    except Exception as e:
        return {"error": str(e)}

@router.post("/sales/", summary="Obtener todas las ventas realizadas y las ganancias", response_model=PdfSalesResponse)
async def sales(params: PdfContentRequest = Depends()):
    """
    Extrae todas las ventas del estado de cuenta, de forma paginada si se especifica *file* y *page*
    - **file**: Archivo PDF del estado de cuenta
    - **status**: Estado de las transacciones
    - **page** (opcional): Número de página
    - **limit** (opcional): Número de transacciones por cada página
    """
    try:
        # Read request data
        status = params.status if params.status else None
        page = params.page if params.page else None
        limit = params.limit if params.limit else None

        # Save the PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await params.file.read())

        total_amount, total_saldo, total_propia, total_movil, total_nauta, total_nauta_hogar, total_factura, total_electrica, profits, pdf_data = PdfAnalyzer(temp_pdf.name).sales(transaction_status=status)

        # If no exist `page` and `limit`, return all data
        if page is None or limit is None:
            return PdfSalesResponse(
                total_amount=total_amount,
                total_saldo=total_saldo,
                total_propia=total_propia,
                total_movil=total_movil,
                total_nauta=total_nauta,
                total_nauta_hogar=total_nauta_hogar,
                total_factura=total_factura,
                total_electrica=total_electrica,
                profits=profits, 
                results=pdf_data
            )

        # Apply pagination
        paginated_data = pdf_data[(page - 1) * limit: page * limit]

        return PdfSalesResponse(
            total=len(pdf_data), 
            page=page, 
            limit=limit, 
            total_amount=total_amount,
            total_saldo=total_saldo,
            total_propia=total_propia,
            total_movil=total_movil,
            total_nauta=total_nauta,
            total_nauta_hogar=total_nauta_hogar,
            total_factura=total_factura,
            total_electrica=total_electrica,
            profits=profits,
            results=paginated_data
        )
    except Exception as e:
        return {"error": str(e)}