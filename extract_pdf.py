import tabula
import re

class ExtractPDF:
    """Extracts table information from PDF files."""
    
    def __init__(self, file_path: str) -> None:
        """ Initializes a ExtractPDF object that reads a PDF file and extracts 
        information from its tables.
        Args:
            - file_path: The path to the PDF file to be processed.
        Raises:
            - TypeError: If the file path is not a string.
        """
        if not isinstance(file_path, str):
            raise TypeError('La ruta del archivo debe ser una cadena.')
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

    def read_pdf(self) -> list:
        """Reads the corresponding PDF file, extracts data from the tables on each page,
        and returns a list of lists with each row of the table.
        Returns:
            A list of lists with each row in the order: 
            [ID|Fecha|Importe Pagado|Mon|ID|Proveedor|Descuento|Importe a Pagar|Tipo de Operación|Resultado|Tipo de Pago]
        """
        try:
            # read PDF file from path
            df = tabula.read_pdf(self.__file_path, pages='all', guess=True)
            # convert dataframe to list
            ls_all_pages = self.__dataframe_to_list(df)
            # flatten list of pages
            ls_lines = self.__flatten_pages(ls_all_pages)
            return ls_lines
        except FileNotFoundError as e:
            return f'No se ha encontrado el archivo especificado en la ruta "{self.__file_path}".'
        except Exception:
            return 'Error al leer los datos, verifique que sea un archivo correcto'

if __name__ == '__main__':
    """This code is an example of how to use the ExtractPDF library to extract 
    data from a PDF file."""
    tb = ExtractPDF('estado.pdf')
    data = tb.read_pdf()

    for i, elem in enumerate(data):
        print(f'{i} -> {elem}')