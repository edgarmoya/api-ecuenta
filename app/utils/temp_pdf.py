from contextlib import asynccontextmanager
import aiofiles
import tempfile
import os

@asynccontextmanager
async def temp_pdf_file(params):
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    try:
        async with aiofiles.open(path, "wb") as f:
            await f.write(await params.file.read())
        yield path
    finally:
        if os.path.exists(path):
            os.remove(path)
