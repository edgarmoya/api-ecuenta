from fastapi import FastAPI, File, UploadFile, Query
import tempfile
from extract_pdf import ExtractPDF

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.post("/table-content/")
async def content(
    file: UploadFile = File(...), 
    page: int = Query(None, alias="page", ge=0),  # Page
    limit: int = Query(None, alias="limit", ge=1)  # Rows for each page
):
    try:
        # Save the PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name

        pdf_data = ExtractPDF(temp_pdf_path).read_pdf()
        json_data = [{
            "id": row[0],
            "date": row[1],
            "amount_paid": row[2],
            "currency": row[3],
            "supplier_id": str(row[4]),  # Ensure supplier_id is a string
            "discount": row[5],
            "amount_due": row[6],
            "transaction_type": row[7],
            "result": row[8],
            "payment_type": row[9],
        } for row in pdf_data]

        # If no exist `page` and `limit`, return all data
        if page is None or limit is None:
            return {"results": json_data}

        # Apply pagination
        paginated_data = json_data[page * limit: (page + 1) * limit]

        return {
            "total": len(json_data),
            "page": page,
            "limit": limit,
            "results": paginated_data
        }

    except Exception as e:
        return {"error": str(e)}

