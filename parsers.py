import pandas as pd
from openpyxl import load_workbook
import xlrd
from abc import ABC
from typing import Iterator
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseBlobParser
from langchain.document_loaders.blob_loaders.schema import Blob
import warnings
 
class XLSXExcelParser(BaseBlobParser, ABC):
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        warnings.simplefilter(action='ignore', category=UserWarning)
        with blob.as_bytes_io() as file:
            if blob.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                wb = load_workbook(file, data_only=True)
            content = {}
            for page in wb.sheetnames:
                df = pd.read_excel(file, sheet_name=page, keep_default_na=False, engine='openpyxl')
                df.dropna(axis=0, how='all', inplace=True)  
                df.dropna(axis=1, how='all', inplace=True)  
                sheet_data_list = df.to_dict(orient='records')  
                filtered_data_list = [
                    {key: value.replace('\n', '') if isinstance(value, str) else value
                     for key, value in record.items() if value != ''}
                    for record in sheet_data_list
                ]
                filtered_data_list = [record for record in filtered_data_list if record]  
                if filtered_data_list:  
                    content[page] = filtered_data_list
 
        content = str(content)
        yield Document(page_content=content, metadata={})
class XLSExcelParser(BaseBlobParser, ABC):
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        warnings.simplefilter(action='ignore', category=UserWarning)
        with blob.as_bytes_io() as file:
            if blob.mimetype == "application/vnd.ms-excel":
                wb = pd.read_excel(file, sheet_name=None, engine='xlrd')
            content = {}
            for sheet_name, sheet_data in wb.items():
                sheet_data_list = sheet_data.to_dict(orient='records')    
                content[sheet_name] = sheet_data_list
 
        content = str(content)
        yield Document(page_content=content.replace('\n', ''), metadata={})
 
class CSVParser(BaseBlobParser):
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        warnings.simplefilter(action='ignore', category=UserWarning)
        with blob.as_bytes_io() as file:
            if blob.mimetype == "text/csv":
                df = pd.read_csv(file)
                content = df.to_dict(orient='records')
                content = str(content)
                yield Document(page_content=content, metadata={})
