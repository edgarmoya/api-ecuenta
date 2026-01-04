import tabula
import re
import os

from typing import Literal, Union


class PdfExtractor:
    """Extracts table information from PDF files"""

    def __init__(self, file_path: str) -> None:
        """ Initializes a PdfExtractor object that reads a PDF file and extracts 
        information from its tables.
        Args:
            - file_path: The path to the PDF file to be processed.
        Raises:
            - TypeError: If the file path is not a string.
            - ValueError: If the file path is empty or does not have a .pdf extension.
            - FileNotFoundError: If the file does not exist.
        """
        if not isinstance(file_path, str):
            raise TypeError('La ruta del archivo debe ser una cadena')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        if not file_path.lower().endswith(".pdf"):
            raise ValueError("El archivo debe tener una extensión .pdf.")

        self.__file_path = file_path

    def __dataframe_to_list(self, df) -> list:
        """Converts a Pandas DataFrame object into a list of lists in Python."""
        return [p.values.tolist() for p in df]

    def __flatten_pages(self, pages: list) -> list:
        """This function flattens a list of pages, returning a list of lines."""
        lines = []
        for page in pages:
            for line in page:
                if self.__line_important(line):
                    lines.append(line)
        return lines

    def __line_important(self, line) -> bool:
        """Filter line to obtain only lines with important content"""
        pattern = '^(nan)+$'
        txt = ''.join(str(cell) for cell in line)
        return not re.match(pattern, txt)

    def __convert_to_dict(self, data: list) -> list[dict]:
        """
        Converts a list of rows into a list of dictionaries with structured keys.

        Args:
            data (list): A list of rows, where each row is a list containing payment-related information.

        Returns:
            list[dict]: A list of dictionaries where each dictionary represents a transaction
        """
        return [{
            "id": row[0],
            "date": row[1],
            "amount_paid": row[2],
            "currency": row[3],
            "supplier_id": str(row[4]),
            "discount": row[5],
            "amount_due": row[6],
            "transaction_type": row[7],
            "transaction_status": row[8],
            "payment_type": row[9],
        } for row in data]

    def read_pdf(self, return_format: Literal["list", "dict"] = "list") -> Union[list, list[dict]]:
        """
        Reads the PDF file, extracts table data from all pages,
        and returns it as a list of rows or a list of dictionaries.

        Args:
            return_format: Output format, either 'list' or 'dict'.

        Returns:
            Extracted data in the requested format.

        Raises:
            ValueError: If return_format is invalid.
            FileNotFoundError: If the PDF file does not exist.
            RuntimeError: If the PDF cannot be read or parsed.
        """
        # Check if 'return_format' is valid
        if return_format not in {"list", "dict"}:
            raise ValueError("El formato debe ser 'list' o 'dict'")

        try:
            df = tabula.read_pdf(
                self.__file_path,
                pages="all",
                guess=True,
                encoding="latin-1",
            )
        except FileNotFoundError:
            raise
        except Exception as exc:
            raise RuntimeError(
                f"Error al leer el PDF: {self.__file_path}"
            ) from exc

        pages = self.__dataframe_to_list(df)
        lines = self.__flatten_pages(pages)

        if return_format == "dict":
            return self.__convert_to_dict(lines)

        return lines
