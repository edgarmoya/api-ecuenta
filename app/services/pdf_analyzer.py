from .pdf_extractor import PdfExtractor
from collections import Counter
from typing import List, Dict

class PdfAnalyzer:
    """Class for analyzing data extracted from a PDF file"""

    def __init__(self, file_path: str) -> None:
        """
        Initializes the PdfAnalyzer object by extracting data from the PDF.

        Args:
            file_path (str): Path to the PDF file to be processed.
        """
        try:
            self.__table: List[Dict] = PdfExtractor(file_path).read_pdf(return_format='dict')
        except Exception as e:
            print(f'{e}')

    def remove_all_duplicates_by_supplier(self, transactions: List[Dict]) -> List[Dict]:
        """
        Removes all transactions where the supplier appears more than once in the list

        Args:
            transactions: A list of transactions

        Returns:
            list: A list containing only transactions from unique suppliers
        """
        # Count how many times each supplier_id appears
        supplier_counts = Counter([t['supplier_id'] for t in transactions])

        # Filter transactions, removing those whose supplier appears more than once
        return list(filter(lambda t: supplier_counts[t['supplier_id']] == 1, transactions))

    def transactions(self, transaction_status: str = 'all') -> List[Dict]:
        """Return transactions based on the specified status

        Args:
            transaction_status (str): The status of the transactions to return.
            Possible values are 'all', 'successful', or 'failed'

        Returns:
            list: A list of transactions matching the specified status
        """
        filtered_table = self.remove_all_duplicates_by_supplier(self.__table) # table without rollback
        if transaction_status == 'all':
            return filtered_table
        elif transaction_status == 'successful':
            return list(filter(lambda r: r['transaction_status'] == 'Exitosa', filtered_table))
        elif transaction_status == 'failed':
            return list(filter(lambda r: r['transaction_status'] == 'Fallida', filtered_table))
        else:
            raise ValueError("El estado de la transacción no es válido. Debe ser 'all', 'successful' o 'failed'")

    def deposits(self, transaction_status: str = 'successful') -> List[Dict]:
        """Calculates the total amount deposited in the bank"""
        total_amount = 0
        data = []
        for row in self.transactions(transaction_status):
            if row['transaction_type'] == 'Recarga Bolsa CUP':
                data.append(row)
                total_amount += row['amount_paid']
        return total_amount, data

    def sales(self, transaction_status: str = 'successful') -> List[Dict]:
        """Calculates the total amount deducted for recharges"""
        total_amount, total_saldo, total_movil, total_nauta = 0, 0, 0, 0
        total_nauta_hogar, total_factura, total_propia = 0, 0, 0
        data = []
        for row in self.transactions(transaction_status):
            if row['transaction_type'] == 'Venta de Saldo AT':
                total_saldo += row['amount_paid']
            if row['transaction_type'] == 'Recarga Propia AT':
                total_propia += row['amount_paid']
            if row['transaction_type'] == 'Recarga Movil':
                total_movil += row['amount_paid']
            if row['transaction_type'] == 'Recarga Nauta AT':
                total_nauta += row['amount_paid']
            if row['transaction_type'] == 'Recarga Nauta Hogar AT':
                total_nauta_hogar += row['amount_paid']
            if row['transaction_type'] == 'Pago Factura AT':
                total_factura += row['amount_paid']
            if row['transaction_type'] not in ['Estado de Cuenta', 'Recarga Bolsa CUP']:
                data.append(row)
                total_amount += row['amount_paid']
        profits = total_amount / 0.9 - total_amount
        return round(total_amount, 2), round(total_saldo, 2), round(total_propia, 2), round(total_movil, 2), round(total_nauta, 2), round(total_nauta_hogar, 2), round(total_factura, 2), round(profits, 2), data
