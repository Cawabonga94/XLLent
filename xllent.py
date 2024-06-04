from cat.mad_hatter.decorators import hook
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .parsers import XLSXExcelParser, XLSExcelParser, CSVParser
 
 
@hook
def rabbithole_instantiates_parsers(file_handlers: dict, cat) -> dict:
 
    new_handlers = {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": XLSXExcelParser(),
        "application/vnd.ms-excel": XLSExcelParser(),
        "text/csv": CSVParser()
    }
     
    file_handlers = file_handlers | new_handlers
    return file_handlers

@hook(priority=99)
def rabbithole_instantiates_splitter(text_splitter, cat):
    text_splitter._chunk_size = 512
    text_splitter._chunk_overlap = 128
    return text_splitter