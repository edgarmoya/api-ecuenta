import tabula
import re
import os

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
        return [p.values.tolist() for p in list(df)]

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
        return False if re.match(pattern, txt) else True

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

    def read_pdf(self, return_format="list") -> list:
        """Reads the corresponding PDF file, extracts data from the tables on each page,
        and returns the data either as a list of lists or a dictionary.

        Args:
        return_format (str): The format to return the data in, either 'list' or 'dict'. Default is 'list'.

        Returns:
            A list of lists or a dictionary containing the data from the table.
        """
        try:
            # Check if 'return_format' is valid
            assert return_format in ['list', 'dict'], "El formato debe ser 'list' o 'dict'"

            # read PDF file from path
            df = tabula.read_pdf(self.__file_path, pages='all', guess=True)
            # convert dataframe to list
            ls_all_pages = self.__dataframe_to_list(df)
            # flatten list of pages
            ls_lines = self.__flatten_pages(ls_all_pages)
            if return_format == "dict":
                return self.__convert_to_dict(ls_lines)
            else:
                return ls_lines
        except FileNotFoundError as e:
            return f'No se ha encontrado el archivo especificado en la ruta "{self.__file_path}".'
        except AssertionError as e:
            return str(e)
        except Exception:
            return 'Error al leer los datos, verifique que sea un archivo correcto'