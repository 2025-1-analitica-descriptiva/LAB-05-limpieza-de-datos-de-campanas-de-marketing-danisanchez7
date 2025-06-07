"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import zipfile
import glob
import os

def clean_campaign_data():
    # Leer todos los archivos ZIP en la carpeta input
    zip_files = glob.glob('./files/input/*.zip')
    
    # Lista para almacenar los dataframes
    dfs = []
    
    # Leer cada archivo ZIP
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file) as z:
            for filename in z.namelist():
                if filename.endswith('.csv'):
                    with z.open(filename) as f:
                        df = pd.read_csv(f)
                        dfs.append(df)
    
    # Concatenar todos los dataframes
    data = pd.concat(dfs, ignore_index=True)
    
    # Procesar client.csv
    client = data[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']]
    client['job'] = client['job'].str.replace('.', '').str.replace('-', '_')
    client['education'] = client['education'].str.replace('.', '_')
    client['education'] = client['education'].replace('unknown', pd.NA)
    client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
    client['mortgage'] = (client['mortgage'] == 'yes').astype(int)
    
    # Procesar campaign.csv
    campaign = data[['client_id', 'number_contacts', 'contact_duration', 
                    'previous_campaign_contacts', 'previous_outcome', 
                    'campaign_outcome', 'day', 'month']]
    campaign['previous_outcome'] = (campaign['previous_outcome'] == 'success').astype(int)
    campaign['campaign_outcome'] = (campaign['campaign_outcome'] == 'yes').astype(int)
    campaign['last_contact_date'] = pd.to_datetime('2022-' + campaign['month'] + '-' + 
                                                 campaign['day'].astype(str)).dt.strftime('%Y-%m-%d')
    campaign = campaign.drop(['day', 'month'], axis=1)
    
    # Procesar economics.csv
    economics = data[['client_id', 'cons_price_idx', 'euribor_three_months']]
    
    # Crear directorio output si no existe
    os.makedirs('./files/output', exist_ok=True)
    
    # Guardar archivos 
    client.to_csv('./files/output/client.csv', index=False)
    campaign.to_csv('./files/output/campaign.csv', index=False)
    economics.to_csv('./files/output/economics.csv', index=False)

clean_campaign_data()

"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """