from cat.mad_hatter.decorators import hook
 
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