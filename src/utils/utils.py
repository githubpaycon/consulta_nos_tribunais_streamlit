import pandas as pd
from funcsforspo_l.fpython.functions_for_py import *
from io import BytesIO

def to_excel_for_download_button(path_df):
    """
    pt-br
    Recupera os bytes para fazer um download de um .xlsx pelo botão download_button do streamlit

    english
    Retrieves the bytes to download an .xlsx by the download_button button of the streamlit

    Args:
        path_df (str): path xlsx df
        
    Use:
        >>> df_xlsx = to_excel_for_download_button('file.xlsx')
        >>> st.download_button(label='📥 Download xlsx...',
        >>>                     data=df_xlsx ,
        >>>                     file_name= 'extraction.xlsx')
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.read_excel(path_df)
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1) 
    writer.save()
    processed_data = output.getvalue()
    return processed_data
    
def verifica_colunas_stf(df: pd.DataFrame):
    verification = True
    cols_stf = ['PARTE', 'IDENTIFICACAO', 'NUMERO UNICO', 'DATA AUTUACAO', 'MEIO', 'PUBLICIDADE', 'TRAMITE']
    for col in df.columns:
        if not col in cols_stf:
            verification = False
            break
        
    return verification


def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str=False) -> str:
    """Converte pdf(s) em texto com pypdf
    
    ### pip install pypdf
    
    ## Atenção, só funciona corretamente em PDF's que o texto é selecionável!
    
    Use:
        ...
    
    Args:
        path_pdf (str): caminho do pdf
        export_from_file_txt (bool | str): passar um caminho de arquivo txt para o texto sair

    Returns:
        str: texto do PDF
    """
    
    text = []
    from pypdf import PdfReader

    reader = PdfReader(path_pdf)
    pages = reader.pages
    for page in pages:
        text.append(page.extract_text())
    else:
        text = transforma_lista_em_string(text)
        
        if export_from_file_txt:
            with open('extraction_pdf.txt', 'w', encoding='utf-8') as f:
                f.write(text)
        return text