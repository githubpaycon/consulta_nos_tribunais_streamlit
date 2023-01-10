import pandas as pd
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