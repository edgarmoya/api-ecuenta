import logging

from .pdf_extractor import PdfExtractor
from collections import Counter

logger = logging.getLogger(__name__)


class PdfAnalyzer:
    """Class for analyzing data extracted from a PDF file"""

    def __init__(self, file_path: str) -> None:
        """
        Initializes the PdfAnalyzer object by extracting data from the PDF.

        Args:
            file_path (str): Path to the PDF file to be processed.
        """
        try:
            self.__table: list[dict] = PdfExtractor(file_path).read_pdf(return_format='dict')
        except Exception as e:
            logger.info(f'{e}')

    def remove_all_duplicates_by_supplier(self, transactions: list[dict]) -> list[dict]:
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

    def transactions(self, transaction_status: str = 'all') -> list[dict]:
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

    def deposits(self, transaction_status: str = 'successful') -> tuple[float, list]:
        """Calculates the total amount deposited in the bank"""
        total_amount = 0
        data = []
        for row in self.transactions(transaction_status):
            if row['transaction_type'] == 'Recarga Bolsa CUP':
                data.append(row)
                total_amount += row['amount_paid']

        return total_amount, data

    def sales(self, transaction_status: str = 'successful') -> tuple[float, float, float, float, float, float, float, float, float, float, list[dict]]:
        """Calculates the total amount deducted for recharges"""
        totals = {
            'total_amount': 0,
            'total_saldo': 0,
            'total_propia': 0,
            'total_movil': 0,
            'total_nauta': 0,
            'total_nauta_hogar': 0,
            'total_factura': 0,
            'total_electrica': 0,
            'total_paquetes': 0
        }

        excluded_types = ['Estado de Cuenta', 'Recarga Bolsa CUP', 'Transferencia Banco']
        type_mapping = {
            'Venta de Saldo AT': 'total_saldo',
            'Recarga Propia AT': 'total_propia',
            'Recarga Movil': 'total_movil',
            'Recarga Nauta AT': 'total_nauta',
            'Recarga Nauta Hogar AT': 'total_nauta_hogar',
            'Pago Factura AT': 'total_factura',
            'Factura Electrica': 'total_electrica',
            'Compra Paquetes Cubacel': 'total_paquetes'
        }

        data = []
        for row in self.transactions(transaction_status):
            t_type = row.get('transaction_type')
            amount = row.get('amount_paid', 0)

            if t_type in type_mapping:
                totals[type_mapping[t_type]] += amount

            if t_type not in excluded_types:
                totals['total_amount'] += amount
                data.append(row)

        profits = totals['total_amount'] / 0.9 - totals['total_amount']

        return (
            round(totals['total_amount'], 2),
            round(totals['total_saldo'], 2),
            round(totals['total_propia'], 2),
            round(totals['total_movil'], 2),
            round(totals['total_nauta'], 2),
            round(totals['total_nauta_hogar'], 2),
            round(totals['total_factura'], 2),
            round(totals['total_electrica'], 2),
            round(totals['total_paquetes'], 2),
            round(profits, 2),
            data
        )
