
import time
import tempfile
import streamlit as st
from pathlib import Path
import datetime
import difflib
import re
import pandas as pd
import pathlib
from requests.exceptions import HTTPError
from typing import Iterable
import xmlschema
import os
from xmlschema import XMLSchema, etree_tostring
#from mindee import Client, PredictResponse, product
import os.path
#from mindee import Client, PredictResponse, product
import regex
import json
import pypdfium2 as pdfium
import pprint
from collections import Counter
import psutil
correction=False

dict={}    #global value , save all info from invoice

file_path = 'obchodni_partneri.txt'

column_names = ['Kód obchodního partnera',
                'Obchodní partner', 'IČO', 'DIČ', 'Obec']

# Read only the first 5 columns of each line into a DataFrame
df = pd.read_csv(file_path, sep=';', encoding='latin-1',
                 header=None, names=column_names, usecols=range(5))


#####mistral processing #############

import base64
import requests
import os
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    global image_file
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        image_file.close()
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


def mistral_processsing(image_path_, file_path_):

    print('image_path', image_path_, 'file_path', file_path_)
    os.environ['api_key'] = '9RRW9GcOO5zThhaqigAAoEQ9R7aK02nZ'

    api_key = os.environ['api_key']
    model = "mistral-large-latest"

# Getting the base64 string
    print('before base64', image_path_)
    base64_image = encode_image(image_path_)
    image_file.close()



# Specify model
    model = "pixtral-12b-2409"

# Initialize the Mistral client
    client = Mistral(api_key=api_key)
    print('clint from mistral', client)

# Define the messages for the chat
    messages = [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": '''extract data from invoice and make the following output, fill only goods,

                tale care that LineExtensionTaxAmount = str(float(LineExtensionAmount) * 0.21) add 21% to LineExtensionAmount
                LineExtensionAmountTaxInclusive= LineExtensionAmount +  LineExtensionTaxAmount
                take care that you process all items goods and  :
                
                Document type will be always 1,
                if faktura is in CZK, set ForeignCurrencyCode to   None,
                set LineExtensionAmountCurr to None,
                set LineExtensionAmountTaxInclusiveCurr to None,
                set Issuyngsystem to SVIDOC.
                be sure that you process all items goods
                "Invoice": {
        "DocumentType": "Zde bude zatÃ­m vÅ¾dy hodnota 1 oznaÄujÃ­cÃ­ typ dokumentu Faktura - daÅˆovÃ½ doklad",
        "ID": "Lidsky ÄitelnÃ© ÄÃ­slo dokladu napÅ™. FV-2024-10-001267",
        "UUID": "GUID identifikace od emitujÃ­cÃ­ho systÃ©mu napÅ™. 13D39D26-D9FF-4C28-82C9-62F755EE6564 nebo jinÃ½ unikÃ¡tnÃ­ identifikÃ¡tor",
        "IssuingSystem": "Identifikace systÃ©mu, kterÃ½ odesÃ­lÃ¡/generuje fakturu napÅ™. SVIDOC",
        "IssueDate": "Datum vystavenÃ­ napÅ™. 2024-05-14",
        "TaxPointDate": "Datum zdanitelnÃ©ho plnÄ›nÃ­ napÅ™. 2024-05-13",
        "VATApplicable": "Je pÅ™edmÄ›tem DPH napÅ™. true nebo false",
        "Note": "PoznÃ¡mka",
        "LocalCurrencyCode": "KÃ³d lokÃ¡lnÃ­ mÄ›ny napÅ™. CZK",
        "ForeignCurrencyCode": "KÃ³d cizÃ­ mÄ›ny, pokud je pouÅ¾ita napÅ™. EUR, pokud se jednÃ¡ o tuzemskou fakturu v CZK bude zde None",
        "CurrRate": "Kurz cizÃ­ mÄ›ny napÅ™. 24.0, pokud je pouÅ¾ita, jinak 1",
        "RefCurrRate": "VztaÅ¾nÃ½ kurz cizÃ­ mÄ›ny, vÄ›tÅ¡inou 1",
        "SupplierParty": {
            "Party": {
                "PartyIdentification": {
                    "ID": "IÄŒ subjektu dodavatele napÅ™. 07829965"
                },
                "PartyName": {
                    "Name": "NÃ¡zev subjektu dodavatele napÅ™. TREVOS, a.s."
                }
            }
        },
        "CustomerParty": {
            "Party": {
                "PartyIdentification": {
                    "ID": "IÄŒ subjektu odbÄ›ratele napÅ™. 03748600"
                },
                "PartyName": {
                    "Name": "NÃ¡zev subjektu dodavatele napÅ™. Stavebniny DEK a.s."
                }
            }
        }
        "InvoiceLines": {
            "InvoiceLine": [
                {
                    "ID": "UnikÃ¡tnÃ­ alfanumerickÃ½ identifikÃ¡tor Å™Ã¡dku dokladu napÅ™.1, 2, 3",
                    "InvoicedQuantity": {
                        "UnitCode": "Jednotka ÃºÄtovanÃ©ho mnoÅ¾stvÃ­ napÅ™. ks",
                        "Text": "ÃšÄtovanÃ© mnoÅ¾stvÃ­ napÅ™. 3"
                    },
                    "LineExtensionAmount": "CelkovÃ¡ cena bez danÄ› na Å™Ã¡dku v tuzemskÃ© mÄ›nÄ›",
                    "LineExtensionAmountCurr": "CelkovÃ¡ cena bez danÄ› na Å™Ã¡dku v cizÃ­ mÄ›nÄ› pokud je pouÅ¾ita, jinak None",
                    "LineExtensionAmountTaxInclusive": "CelkovÃ¡ cena vÄetnÄ› danÄ› na Å™Ã¡dku v tuzemskÃ© mÄ›nÄ›",
                    "LineExtensionAmountTaxInclusiveCurr": "CelkovÃ¡ cena vÄetnÄ› danÄ› na Å™Ã¡dku v cizÃ­ mÄ›nÄ› pokud je pouÅ¾ita, jinak None",
                    "LineExtensionTaxAmount": "ÄŒÃ¡stka danÄ› na Å™Ã¡dku v tuzemskÃ© mÄ›nÄ›",
                    "UnitPrice": "JednotkovÃ¡ cena bez danÄ› na Å™Ã¡dku v tuzemskÃ© mÄ›nÄ›",
                    "UnitPriceTaxInclusive": "JednotkovÃ¡ cena s danÃ­ na Å™Ã¡dku v tuzemskÃ© mÄ›nÄ›",
                    "ClassifiedTaxCategory": {
                        "Percent": "ProcentnÃ­ sazba DPH",
                        "VATCalculationMethod": "ZpÅ¯sob vÃ½poÄtu DPH"
                    },
                    "Item": {
                        "Description": "Popis poloÅ¾ky",
                        "ID": "IdentifikÃ¡tor poloÅ¾ky, pokud je dostupnÃ½, jinak None"
                    }
                }
            ]
        }
    }
}'''
                #"text": "design optimal prompt from extraction data from invoice image "
                },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

# Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    print('chat response', chat_response)
    
    result=chat_response.choices[0].message.content

    

   



    #with open('data.json', 'w') as f:
    #    json.dump('sample.json', f)

    print('mistral processing: ', result)
  
    print(file_path_)
   
    print('result type', type(result))

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    y=json.loads(pattern.findall(result)[0])

    print('after regex', y)
    #import unicode
    #y={k:unicode(v).encode('utf-8') for k,v in y.iteritems()}
    #utf8_string=json.dumps(y, ensure_ascii=False)
    print()
    print('len', len(y))
    print('type', type(y))

    json_string=json.dumps(y)
    print(json_string)
    print(type(json_string))
    
    



    with open(file_path_, 'w', encoding='utf-8') as f:
       json.dump(y, f,  indent=4, ensure_ascii=False)
       f.close()
    return result

#####################end of mistral processing ####################################

def find_company_index(company):
    n = 4
    cutoff = 0.6

    close_matches = difflib.get_close_matches(company,
                                              df['Obchodní partner'], n, cutoff)
    try:
        find_item = str(df[df['Obchodní partner'] ==
                        close_matches[0]].index.values[0])

    except:
        find_item = '0'

    return (find_item)


def find_company_ico(company):
    n = 4
    cutoff = 0.6

    close_matches = difflib.get_close_matches(company,
                                              df['Obchodní partner'], n, cutoff)
    try:
        find_item = str(df[df['Obchodní partner'] ==
                        close_matches[0]].index.values[0])

    except:
        find_item = '1'

    return (str(df.iloc[int(find_item)]['IČO']))


def find_ico(company):
    # company=company.lower()
    print('company (FIND ICO)', company)

    file_path = 'obchodni_partneri.txt'

    column_names = ['Kód obchodního partnera',
                    'Obchodní partner', 'IČO', 'DIČ', 'Obec']
    ico_list = []

# Read only the first 5 columns of each line into a DataFrame
    df = pd.read_csv(file_path, sep=';', encoding='latin-1',
                     header=None, names=column_names, usecols=range(5))
    list_companies = df['Obchodní partner'].to_list()

    print(difflib.get_close_matches(company, list_companies, cutoff=0.35))

    index_company = list_companies.index(company)
    return (df.iloc[index_company]['IČO'])

    # for index, row in df.iterrows():
    #  if (difflib.SequenceMatcher(None, company, row['Obchodní partner']).ratio()) > 0.7:
    #    ico_list.append(row['IČO'])
    # if len(ico_list) == 0:
    #  for index, row in df.iterrows():
    #    seek_text=row['Obchodní partner']
    #
    #    if company.find(seek_text) != -1:
    #      print(ico_list)
    #      print('seek text', seek_text)
    #      ico_list.append(row['IČO'])
    # if len(ico_list) == 0:
    #  return('99999999')
    # else:
    #  return(ico_list[0])


def find_company_dic(company):
    n = 4
    cutoff = 0.6

    close_matches = difflib.get_close_matches(company,
                                              df['Obchodní partner'], n, cutoff)
    try:
        find_item = str(df[df['Obchodní partner'] ==
                        close_matches[0]].index.values[0])

    except:
        find_item = '1'

    return (str(df.iloc[int(find_item)]['DIČ']))


def filling_mindee_xml(image_file, file_path_):
    import xml.etree.ElementTree as ET

    myfile = open('protokol_conversion.txt', 'a')

    mytree = ET.parse('priklad.isdoc')
    myroot = mytree.getroot()

    mindee_client = Client(api_key="6a452f8cde548a2e5acef5017bba701d ")
    input_doc = mindee_client.source_from_path(image_file)
    result: PredictResponse = mindee_client.parse(product.InvoiceV4, input_doc)

    # iterating through the all values.
    for item in myroot[4].iter():

        path = pathlib.Path(image_file)

        myfile.writelines('Filename:' + path.name)
        myfile.writelines('\n')

        item.text = str(result.document.inference.prediction.date.value)
        print('Invoice date:', item.text)
        myfile.writelines('Invoice date:' + item.text)
        myfile.writelines('\n')
        dict['Invoice date'] = item.text

    for item in myroot[3].iter():
        item.text = str(result.document.inference.prediction.date.value)

    for item in myroot[1].iter():
        item.text = str(
            result.document.inference.prediction.invoice_number.value)
        print('Invoice number', str(
            result.document.inference.prediction.invoice_number.value))
        # data_processing_text+=('Invoice number' + str(result.document.inference.prediction.invoice_number.value))
        myfile.writelines(
            'Invoice number' + str(result.document.inference.prediction.invoice_number.value))
        myfile.writelines('\n')

        dict['Invoice number'] = item.text

    for item in myroot[6].iter():
        item.text = ' '

    for item in myroot[7].iter():
        item.text = ' '

    for item in myroot[9].iter('{http://isdoc.cz/namespace/2013}ForeignCurrencyCode'):
        item.text = '   '

     # iterating through the all values.
    for item in myroot[10].iter(): #current rate
        item.text='1'

     # iterating through the all values.
    for item in myroot[11].iter(): #reference current rate
        item.text='1'
 
 

    for count, item in enumerate(myroot[12].iter('{http://anydomain.cz/branch/developer/head}UserfieldName')):
        item.text = ' -- '

    for item in myroot[12].iter('{http://anydomain.cz/branch/developer/head}AdditionalHeadDiscount'):
        item.text = '0'

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}UserID'):
        item.text = '0001'

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}CatalogFirmIdentification'):
        item.text = find_company_index(
            str(result.document.inference.prediction.supplier_name.value))

    ico = []
    for supplier_company_registrations_elem in result.document.inference.prediction.supplier_company_registrations:
        ico.append(supplier_company_registrations_elem.value)
        # print('Supplier company ICO):', supplier_company_registrations_elem.value)

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}ID'):
        # item.text=find_company_ico(str(result.document.inference.prediction.supplier_name.value))
        # item.text=ico[1] if len(ico) > 1 else find_ico(str(result.document.inference.prediction.supplier_name.value))
        item.text = supplier_company_registrations_elem.value

        # if len(ico) > 1:
        #  if ico[1] != find_ico(str(result.document.inference.prediction.supplier_name.value)):
        #    ico[1]=find_ico(str(result.document.inference.prediction.supplier_name.value))
        #    ico[0]='CZ' + ico[1]
        #    item.text=ico[1]
        item.text = supplier_company_registrations_elem.value
        print('Supplier company ICO :', item.text)
        myfile.writelines('Supplier company ICO :' + item.text)
        myfile.writelines('\n')
        dict['Supplier ICO'] = item.text

        currency=str(result.document.inference.prediction.locale.value)
        if len(currency) == 4:
            currency='CZK'
        print('Original currency', currency)
        myfile.writelines('Original currency' + currency)

        myfile.writelines('\n')
        dict['Original currency'] = currency

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}Name'):
        # item.text= str(result.document.inference.prediction.supplier_name.value)
        item.text = result.document.inference.prediction.supplier_name.value

    # my_dict['AccountingCustomerParty']['Party']['PartyIdentification']['ID']=item_['buyer_ic']
    # my_dict['AccountingSupplierParty']['Party']['PartyIdentification']['CatalogFirmIdentification']=find_company_index(item_['seller_name'])

    # my_dict['IssueDate']=item['issue_date']

    # my_dict['AccountingSupplierParty']['Party']['PartyName']['Name']=item_['seller_name']
    # my_dict['AccountingSupplierParty']['Party']['PostalAddress']['StreetName']=''

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
        # item.text= find_company_dic(str(result.document.inference.prediction.supplier_name.value))
        # item.text=ico[0] if len(ico) > 1 else 'CZ' + find_ico(str(result.document.inference.prediction.supplier_name.value))
        item.text = 'CZ' + supplier_company_registrations_elem.value
        print('Supplier company DIC: ', item.text)
        myfile.writelines('Supplier company DIC: ' + item.text)
        myfile.writelines('\n')
        dict['Supplier DIC'] = item.text

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}StreetName'):
        item.text = '  '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}BuildingNumber'):
        item.text = '  '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}PostalZone'):
        item.text = ' '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}CityName'):
        item.text = df['Obec'].iloc[int(find_company_index(
            str(result.document.inference.prediction.supplier_name.value)))]

    # my_dict['AccountingSupplierParty']['Party']['PostalAddress']['BuildingNumber']=''
    # my_dict['AccountingSupplierParty']['Party']['PostalAddress']['CityName']=df['Obec'].iloc[int(find_company_index(item['seller_name']))]
    # my_dict['AccountingSupplierParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['AccountingSupplierParty']['Party']['PostalAddress']['PostalZone']=''

    # my_dict['AccountingSupplierParty']['Party']['PartyTaxScheme'][0]['CompanyID']=item_['buyer_dic']
    # my_dict['TaxPointDate']=item_['taxable_fulfillment_date']

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}RegisterKeptAt'):
        item.text = '-- '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}RegisterFileRef'):
        item.text = '-- '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}RegisterDate'):
        item.text = '2016-01-01 '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}Telephone'):
        item.text = '-- '

    for item in myroot[13].iter('{http://isdoc.cz/namespace/2013}ElectronicMail'):
        item.text = ' -- '

    # my_dict['AccountingSupplierParty']['Party']['Contact']['Name']=''
    # my_dict['AccountingSupplierParty']['Party']['Contact']['Telephone']=''
    # my_dict['AccountingSupplierParty']['Party']['Contact']['ElectronicMail']=''
    # my_dict['AccountingSupplierParty']['Party']['RegisterIdentification']['RegisterKeptAt']=''
    # my_dict['AccountingSupplierParty']['Party']['RegisterIdentification']['RegisterFileRef']=''
    # my_dict['AccountingSupplierParty']['Party']['RegisterIdentification']['RegisterDate']=''

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}UserID'):
        item.text = '0001'

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}CatalogFirmIdentification'):
        # item.text=find_company_index(str(result.document.inference.prediction.supplier_name.value))
        item.text = '001'

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}ID'):
        # item.text=find_company_ico(str(result.document.inference.prediction.supplier_name.value))
        # item.text=ico[1] if len(ico) > 1 else find_ico(str(result.document.inference.prediction.supplier_name.value))
        item.text = supplier_company_registrations_elem.value

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}Name'):
        item.text = str(
            result.document.inference.prediction.supplier_name.value)
        print('Supplier name:', item.text)
        myfile.writelines('Supplier name:' + item.text)
        myfile.writelines('\n')
        dict['Supplier name'] = item.text

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}StreetName'):
        item.text = ' '

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}BuildingNumber'):
        item.text = ' '

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}CityName'):
        item.text = df['Obec'].iloc[int(find_company_index(
            str(result.document.inference.prediction.supplier_name.value)))]

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
        # item.text=find_company_dic(str(result.document.inference.prediction.supplier_name.value))
        # item.text=ico[0] if len(ico) > 1 else 'CZ' + find_ico(str(result.document.inference.prediction.supplier_name.value))
        item.text = 'CZ' + supplier_company_registrations_elem.value
        print('Supplier company DIC ;', item.text)
        myfile.writelines('Supplier company DIC ;' + item.text)
        myfile.writelines('\n')
        dict['Supplier DIC']=item.text

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}RegisterKeptAt'):
        item.text = ' -- '

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}RegisterFileRef'):
        item.text = ' -- '

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}RegisterDate'):
        item.text = str(result.document.inference.prediction.date.value)

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}Telephone'):
        item.text = '--'

    for item in myroot[14].iter('{http://isdoc.cz/namespace/2013}ElectronicMail'):
        item.text = ' '

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}PostalZone'):
        item.text = ' '

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}ElectronicMail'):
        item.text = ' '

    # my_dict['SellerSupplierParty']['Party']['PartyIdentification']['User']='0001'
    # my_dict['SellerSupplierParty']['Party']['PartyIdentification']['CatalogFirmIdentification']=find_company_index(item_['seller_name'])
    # my_dict['SellerSupplierParty']['Party']['PartyIdentification']['ID']=item_['seller_ic']
    # my_dict['SellerSupplierParty']['Party']['PartyName']['Name']=item_['seller_name']
    # my_dict['SellerSupplierParty']['Party']['PostalAddress']['StreetName']=''
    # my_dict['SellerSupplierParty']['Party']['PostalAddress']['BuildingNumber']=''
    # my_dict['SellerSupplierParty']['Party']['PostalAddress']['CityName']=df['Obec'].iloc[int(find_company_index(item['seller_name']))]
    # my_dict['SellerSupplierParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['SellerSupplierParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['SellerSupplierParty']['Party']['PartyTaxScheme'][0]['CompanyID']=item_['seller_dic']
    # my_dict['SellerSupplierParty']['Party']['Contact']['Name']=''
    # my_dict['SellerSupplierParty']['Party']['Contact']['Telephone']=''
    # my_dict['SellerSupplierParty']['Party']['Contact']['ElectronicMail']=''

    ico = []
    for customer_company_registrations_elem in result.document.inference.prediction.customer_company_registrations:
        ico.append(customer_company_registrations_elem.value)

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}ID'):
        # item.text=str(find_company_ico(str(result.document.inference.prediction.supplier_name.value)))
        item.text = ico[1] if len(ico) > 1 else '   '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}Name'):
        if result.document.inference.prediction.customer_name.value == None:
            item.text = 'SV Metal spol. s r.o'

        else:
            if result.document.inference.prediction.customer_name.value .find(result.document.inference.prediction.supplier_name.value) != -1 or result.document.inference.prediction.supplier_name.value .find(result.document.inference.prediction.customer_name.value) != -1:
                item.text = 'SV Metal spol. s r.o.'
                print('item.text 16', item.text)
            else:
                item.text = result.document.inference.prediction.customer_name.value
        print('Customer name', item.text)
        myfile.write('Customer name :' + item.text)
        myfile.writelines('\n')
        dict['Customer name'] = item.text

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = ico[1] if len(ico) > 1 else '25257366'
        print('Customer ICO :', item.text)
        myfile.writelines('Customer ICO :' + item.text)
        myfile.writelines('\n')
        dict['Customer ICO ']=item.text

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}StreetName'):
        item.text = ' '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}BuildingNumber'):
        item.text = ' '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}CityName'):
        item.text = ' '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}PostalZone'):
        item.text = ' '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
        # item.text= find_company_dic(str(result.document.inference.prediction.supplier_name.value))
        item.text = ico[0] if len(ico) > 1 else 'CZ25257366'
        print('Customer DIC :', item.text)
        myfile.writelines('Customer DIC :' + item.text)
        myfile.writelines('\n')
        dict['Customer DIC']=item.text

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}Telephone'):
        item.text = ' '

    for item in myroot[16].iter('{http://isdoc.cz/namespace/2013}ElectronicMail'):
        item.text = ' '

    # my_dict['Extensions']['extenzeH:UserfieldName'][0]['@xmlns:extenzeH']=''
    # my_dict['Extensions']['extenzeH:UserfieldName']['#text']=''
    # my_dict['Extensions']['extenzeH:UserfieldName'][0]['@xmlns:extenzeH']=''

    # my_dict['Extensions']['extenzeH:AdditionalHeadDiscount'][0]['@xmlns:extenzeH']=''
    # my_dict['Extensions']['extenzeH:AdditionalHeadDiscount']['#text']=''

    # my_dict['AccountingSupplierParty']['Party']['RegisterIdentification']['RegisterDate']='2016-01-01'
    # my_dict['SellerSupplierParty']['Party']['RegisterIdentification']['RegisterDate']='2016-01-01'
    ico = []
    for customer_company_registrations_elem in result.document.inference.prediction.customer_company_registrations:
        ico.append(customer_company_registrations_elem.value)

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}ID'):
        # item.text=str(find_company_ico(str(result.document.inference.prediction.supplier_name.value)))
        item.text = ico[1] if len(ico) > 1 else '25257366'

    # if str(result.document.inference.prediction.supplier_name.value).upper() == str(result.document.inference.prediction.customer_name.value).upper():
    #  for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}Name' ):
    #    item.text= 'SV Metal s.r.o.'
    # else:
    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}Name'):
        # item.text= str(result.document.inference.prediction.customer_name.value)
        if result.document.inference.prediction.customer_name.value == None:
            item.text = 'SV Metal spol. s r.o.'
        else:
            if result.document.inference.prediction.customer_name.value .find(result.document.inference.prediction.supplier_name.value) != -1 or result.document.inference.prediction.supplier_name.value .find(result.document.inference.prediction.customer_name.value) != -1:
                item.text = 'SV Metal spol. r.o.'
            else:
                item.text = result.document.inference.prediction.customer_name.value

#  for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}Name' ):
#    item.text=str(result.document.inference.prediction.customer_name.value)

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}StreetName'):
        item.text = ' '

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}BuildingNumber'):
        item.text = ' '

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}CityName'):
        item.text = ' '

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
        # item.text = str(find_company_ico(str(result.document.inference.prediction.supplier_name.value)))
        item.text = ico[0] if len(ico) > 1 else 'CZ25257366'

    for item in myroot[15].iter('{http://isdoc.cz/namespace/2013}Telephone'):
        item.text = ' '

    # my_dict['AccountingCustomerParty']['Party']['PartyIdentification']['UserID']=''
    # my_dict['AccountingCustomerParty']['Party']['PartyIdentification']['CatalogFirmIdentification']=''
    # my_dict['AccountingCustomerParty']['Party']['PartyIdentification']['ID']=''
    # my_dict['AccountingCustomerParty']['Party']['PartyName']['Name']=item_['buyer_name']
    # my_dict['AccountingCustomerParty']['Party']['PostalAddress']['StreetName']=''
    # my_dict['AccountingCustomerParty']['Party']['PostalAddress']['BuildingNumber']=''
    # my_dict['AccountingCustomerParty']['Party']['PostalAddress']['CityName']=df['Obec'].iloc[int(find_company_index(item['buyer_name']))]

    # my_dict['AccountingCustomerParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['AccountingCustomerParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['AccountingCustomerParty']['Party']['PartyTaxScheme'][0]['CompanyID']=item_['buyer_dic']
    # my_dict['AccountingCustomerParty']['Party']['Contact']['Name']=''
    # my_dict['AccountingCustomerParty']['Party']['Contact']['Telephone']=''
    # my_dict['AccountingCustomerParty']['Party']['Contact']['ElectronicMail']=''

    # my_dict['BuyerCustomerParty']['Party']['PartyIdentification']['UserID']=''
    # my_dict['BuyerCustomerParty']['Party']['PartyIdentification']['CatalogFirmIdentification']=''
    # my_dict['BuyerCustomerParty']['Party']['PartyIdentification']['ID']=''
    # my_dict['BuyerCustomerParty']['Party']['PartyName']['Name']=item_['buyer_name']
    # my_dict['BuyerCustomerParty']['Party']['PostalAddress']['StreetName']=''
    # my_dict['BuyerCustomerParty']['Party']['PostalAddress']['BuildingNumber']=''
    # my_dict['BuyerCustomerParty']['Party']['PostalAddress']['CityName']=df['Obec'].iloc[int(find_company_index(item['buyer_name']))]

    # my_dict['BuyerCustomerParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['BuyerCustomerParty']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['BuyerCustomerParty']['Party']['PartyTaxScheme'][0]['CompanyID']=item_['buyer_dic']
    # my_dict['BuyerCustomerParty']['Party']['Contact']['Name']=''
    # my_dict['BuyerCustomerParty']['Party']['Contact']['Telephone']=''
    # my_dict['BuyerCustomerParty']['Party']['Contact']['ElectronicMail']=''

    # my_dict['OrderReferences']['OrderReference'][0]['id']='0000'
    # my_dict['OrderReferences']['OrderReference'][0].pop('id')
    # my_dict['OrderReferences']['OrderReference'][0]['SalesOrderID']='0000'
    # my_dict['OrderReferences']['OrderReference'][0]['ExternalOrderID']=''
    # my_dict['OrderReferences']['OrderReference'][0]['IssueDate']=''

    # my_dict['OrderReferences']['OrderReference'][1]['id']=''
    # my_dict['OrderReferences']['OrderReference'][1]['SalesOrderID']=''
    # my_dict['OrderReferences']['OrderReference'][1]['ExternalOrderID']=''
    # my_dict['OrderReferences']['OrderReference'][1]['IssueDate']=''

        for item in myroot[17].iter('{http://isdoc.cz/namespace/2013}ExternalOrderID'):
            item.text = ' '

        for item in myroot[17].iter('{http://isdoc.cz/namespace/2013}IssueDate'):
            item.text = str(result.document.inference.prediction.date.value)

        for item in myroot[17].iter('{http://isdoc.cz/namespace/2013}SalesOrderID'):
            item.text = ' '

        for item in myroot[17].iter('{http://isdoc.cz/namespace/2013}ExternalOrderID'):
            item.text = ' '

        for item in myroot[17].iter('{http://isdoc.cz/namespace/2013}IssueDate'):
            item.text = str(result.document.inference.prediction.date.value)

    # my_dict['DeliveryNoteReferences']['DeliveryNoteReference'][0]['@id']=''
    # my_dict['DeliveryNoteReferences']['DeliveryNoteReference'][0]['ID']=''
    # my_dict['DeliveryNoteReferences']['DeliveryNoteReference'][0]['IssueDate']=''

    for item in myroot[18].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = ' '

    for item in myroot[18].iter('{http://isdoc.cz/namespace/2013}IssueDate'):
        item.text = str(result.document.inference.prediction.date.value)

    # my_dict['OriginalDocumentReferences']['OriginalDocumentReference'][0]['@id']=''
    # my_dict['OriginalDocumentReferences']['OriginalDocumentReference'][0]['ID']=item_['invoice_number']
    # my_dict['OriginalDocumentReferences']['OriginalDocumentReference'][0]['IssueDate']=''

    for item in myroot[19].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = ' '

    for item in myroot[19].iter('{http://isdoc.cz/namespace/2013}IssueDate'):
        item.text = str(result.document.inference.prediction.date.value)

    # my_dict['Delivery']['Party']['PartyIdentification']['UserID']=''
    # my_dict['Delivery']['Party']['PartyIdentification']['CatalogFirmIdentification']=''
    # my_dict['Delivery']['Party']['PartyIdentification']['ID']=item_['seller_ic']
    # my_dict['Delivery']['Party']['PartyName']['Name']=item_['buyer_name']
    # my_dict['Delivery']['Party']['PostalAddress']['StreetName']=''
    # my_dict['Delivery']['Party']['PostalAddress']['BuildingNumber']=''
    # my_dict['Delivery']['Party']['PostalAddress']['CityName']=''
    # my_dict['Delivery']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['Delivery']['Party']['PostalAddress']['PostalZone']=''
    # my_dict['Delivery']['Party']['PartyTaxScheme'][0]['CompanyID']=item_['buyer_dic']
    # my_dict['Delivery']['Party']['Contact']['Name']=''
    # my_dict['Delivery']['Party']['Contact']['Telephone']=''
    # my_dict['Delivery']['Party']['Contact']['ElectronicMail']=''

    ico = []
    for customer_company_registrations_elem in result.document.inference.prediction.customer_company_registrations:
        ico.append(customer_company_registrations_elem.value)

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}ID'):
        # item.text=str(find_company_ico(str(result.document.inference.prediction.supplier_name.value)))
        item.text = ico[1] if len(ico) > 1 else '25257366'

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}Name'):
        item.text = result.document.inference.prediction.customer_name.value
        if result.document.inference.prediction.customer_name.value == None:
            item.text = 'SV Metal spol. s r.o.'
        else:
            if result.document.inference.prediction.customer_name.value .find(result.document.inference.prediction.supplier_name.value) != -1 or result.document.inference.prediction.supplier_name.value .find(result.document.inference.prediction.customer_name.value) != -1:
                item.text = 'SV Metal spol. s r.o.'

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}StreetName'):
        item.text = ' '

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}BuildingNumber'):
        item.text = ' '

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}CityName'):
        item.text = ' '

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}PostalZone'):
        item.text = ' '

    if len(ico) > 0:
        for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
            item.text = str(ico[0])
    else:
        for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}CompanyID'):
            item.text = ico[0] if len(ico) > 1 else 'CZ25257366'

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}Telephone'):
        item.text = ' '

    for item in myroot[20].iter('{http://isdoc.cz/namespace/2013}ElectronicMail'):
        item.text = ' '

    # my_dict['InvoiceLines']['InvoiceLine'][0]['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['OrderReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['OrderReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['DeliveryNoteReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['DeliveryNoteReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['OriginalDocumentReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['OriginalDocumentReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['InvoicedQuantity']['@unitCode']='ks'
    # my_dict['InvoiceLines']['InvoiceLine'][0]['InvoicedQuantity']['#test']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['LineExtensionAmountCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['LineExtensionAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['LineExtensionAmountTaxInclusiveCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['LineExtensionAmountTaxInclusive']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['LineExtensionTaxAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['UnitPrice']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['UnitPriceTaxInclusive']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['ClassifiedTaxCategory']['Percent']='21'
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Note']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['Description']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['CatalogueItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['SecondarySellersItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['TertiarySellersItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['BuyersItemIdentification']['ID']=''

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}LineID'):
        item.text = ' '

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}OrderReference'):
        item.text = ' '

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}InvoicedQuantity'):
        item.text = '1'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmountCurr'):
        item.text = '0.0'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmountCurr'):
        item.text = '0.0'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmount'):
        item.text = '0.00'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmountTaxInclusiveCurr'):
        item.text = '0.0'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}UnitPrice'):
        item.text = '0.00'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}UnitPriceTaxInclusive'):
        item.text = '0.00'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}Percent'):
        item.text = '0'

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}Note'):
        item.text = ' '

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}Description'):
        item.text = ' '

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}ExpirationDate'):
        item.text = str(result.document.inference.prediction.date.value)

    for item in myroot[21].iter('{http://isdoc.cz/namespace/2013}ID'):
        if len(item.text) > 1:
            item.text = '0'

    for count, item in enumerate(myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmountTaxInclusive')):
        item.text = '0.00'

# replacing values from table of invoice items
    data = {
        "description": [' '],
        "quantity": [' '],
        "unit_price": [' '],
        "total_amount": [' ']
    }


# load data into a DataFrame object:
    df_ = pd.DataFrame(data)

    # je nutne osetrit kdyz se df_ vrati prazdne
    # overit na fakture c. 43
    # if df_.empty
    for index, line_items_elem in enumerate(result.document.inference.prediction.line_items):
        df_.at[index, 'description'] = line_items_elem.description
        df_.at[index, 'quantity'] = (
            line_items_elem.quantity) if line_items_elem.quantity != None else '1'
        df_.at[index, 'unit_price'] = (line_items_elem.unit_price)
        df_.at[index, 'total_amount'] = line_items_elem.total_amount

        print('Description: ', line_items_elem.description)
        print('Quantity: ', df_.at[index, 'quantity'])
        print('Unit price: ', df_.at[index, 'unit_price'])
        print('Total amount: ', df_.at[index, 'total_amount'])
        # if df_.loc[index,'unit_price']==None or  df_.loc[index,'quantity'] == None or df_.loc[index,'Total_amount'] == None:
        #  df_.drop()
        #  entering_missing_data(index)

    df_.dropna(subset=['quantity'], inplace=True)
    df_.dropna(subset=['unit_price'], inplace=True)
    df_.dropna(subset=['total_amount'], inplace=True)
    myfile.writelines('Descriptio og goods ')
    myfile.writelines('\n')
    myfile.writelines(str(df_))
    myfile.writelines('\n')

    for count, item in enumerate(myroot[21].iter('{http://isdoc.cz/namespace/2013}InvoicedQuantity')):
        if count < len(df_.index):
            item.text = str(
                df_.iloc[count-1]['quantity']) if len(str(df_.iloc[count-1]['quantity'])) > 0 else '1'

        else:
            item.text = '0'

    for count, item in enumerate(myroot[21].iter('{http://isdoc.cz/namespace/2013}UnitPrice')):
        if count < len(df_.index):
            item.text = str(df_.iloc[count-1]['unit_price']
                            ) if df_.iloc[count-1]['unit_price'] > 0 else '1'
        else:
            item.text = '0'

    for count, item in enumerate(myroot[21].iter('{http://isdoc.cz/namespace/2013}Description')):
        if count < len(df_.index):
            item.text = str(df_.iloc[count-1]['description'])
        else:
            item.text = '0'

    for count, item in enumerate(myroot[21].iter('{http://isdoc.cz/namespace/2013}LineExtensionAmount')):
        if count < len(df_.index):
            item.text = str(df_.iloc[count-1]['total_amount']
                            ) if df_.iloc[count-1]['total_amount'] != None else 0.00
        else:
            item.text = '0'

    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['Name']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['Note']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['ExpirationDate']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['Specification']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['Quantity']['@unitCode']='ks'
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['Quantity']['#text']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][0]['BatchOrSerialNumber']=''

    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['Name']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['Note']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['ExpirationDate']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['Specification']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['Quantity']['@unitCode']='ks'
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['Quantity']['#text']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Item']['StoreBatches']['StoreBatch'][1]['BatchOrSerialNumber']=''
    # my_dict['InvoiceLines']['InvoiceLine'][0]['Extensions']['extenzeL:UserfieldName'][0]['@xmlns:extenzeL']=''

    # my_dict['InvoiceLines']['InvoiceLine'][1]['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['OrderReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['OrderReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['DeliveryNoteReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['DeliveryNoteReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['InvoicedQuantity']['@unitCode']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['InvoicedQuantity']['#text']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['LineExtensionAmountCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['LineExtensionAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['LineExtensionAmountTaxInclusiveCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1][ 'LineExtensionAmountTaxInclusive']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['LineExtensionTaxAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['UnitPrice']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['UnitPriceTaxInclusive']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['ClassifiedTaxCategory']['Percent']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['ClassifiedTaxCategory']['VATCalculationMethod']
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Note']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Item']['Description']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Item']['CatalogueItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Item']['SellersItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Item']['TertiarySellersItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][1]['Item']['BuyersItemIdentification']['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['ID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['DeliveryNoteReference']['@ref']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['DeliveryNoteReference']['LineID']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['InvoicedQuantity']['@unitCode']='ks'
    # my_dict['InvoiceLines']['InvoiceLine'][2]['InvoicedQuantity']['#text']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['LineExtensionAmountCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['LineExtensionAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['LineExtensionAmountTaxInclusiveCurr']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['LineExtensionAmountTaxInclusive']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['LineExtensionTaxAmount']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['UnitPrice']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['ClassifiedTaxCategory']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['ClassifiedTaxCategory']['Percent']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['ClassifiedTaxCategory']['VATCalculationMethod']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['Note']=''
    # my_dict['InvoiceLines']['InvoiceLine'][2]['Item']['Description']=''

    # my_dict['NonTaxedDeposits']['NonTaxedDeposit'][0]['ID']=''
    # my_dict['NonTaxedDeposits']['NonTaxedDeposit'][0]['VariableSymbol']=''
    # my_dict['NonTaxedDeposits']['NonTaxedDeposit'][0]['DepositAmountCurr']=''
    # my_dict['NonTaxedDeposits']['NonTaxedDeposit'][0]['DepositAmount']=''

    for item in myroot[22].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = '--'

    for item in myroot[22].iter('{http://isdoc.cz/namespace/2013}DepositAmountCurr'):
        item.text = '0.00'

    for item in myroot[22].iter('{http://isdoc.cz/namespace/2013}VariableSymbol'):
        item.text = '--'

    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['ID']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['VariableSymbol']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['TaxableDepositAmountCurr']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['TaxableDepositAmount']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['TaxInclusiveDepositAmountCurr']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['TaxInclusiveDepositAmount']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['ClassifiedTaxCategory']['Percent']
    # my_dict['TaxedDeposits']['TaxedDeposit'][0]['ClassifiedTaxCategory']['VATCalculationMethod']=''

    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['ID']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['VariableSymbol']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['TaxableDepositAmountCurr']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['TaxableDepositAmount']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['TaxInclusiveDepositAmountCurr']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['TaxInclusiveDepositAmount']=''
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['ClassifiedTaxCategory']['Percent']
    # my_dict['TaxedDeposits']['TaxedDeposit'][1]['ClassifiedTaxCategory']['VATCalculationMethod']=''

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = ' '

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}VariableSymbol'):
        item.text = ' '

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}TaxableDepositAmountCurr'):
        item.text = '0.00'

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}TaxableDepositAmount'):
        item.text = '0.00'

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveDepositAmount'):
        item.text = '0.00'

    for item in myroot[23].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveDepositAmountCurr'):
        item.text = '0.00'

    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxableAmount']=item['total_without_vat']
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxAmount']=item['total_incl_vat']
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['AlreadyClaimedTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['DifferenceTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][0]['TaxCategory']['Percent']=''

    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['AlreadyClaimedTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['DifferenceTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][1]['TaxCategory']['Percent']=''

    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['AlreadyClaimedTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxableAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxableAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxInclusiveAmountCurr']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['DifferenceTaxInclusiveAmount']=''
    # my_dict['TaxTotal']['TaxSubTotal'][2]['TaxCategory']['Percent']=''

    # my_dict['TaxTotal']['TaxAmountCurr']=''
    # my_dict['TaxTotal']['TaxAmount']=''

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxableAmountCurr'):
        item.text = '0.00'

    for count, item in enumerate(myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxableAmount')):

        if count == 0:
            item.text = str(
                result.document.inference.prediction.total_net.value)
            print('Total net value: ', item.text)
            myfile.writelines('Total net value: ' + item.text)
            myfile.writelines('\n')
        else:
            item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxAmountCurr'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxAmount'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveAmountCurr'):
        item.text = '0.00'

    for count, item in enumerate(myroot[24].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveAmount')):
        if count == 0:
            item.text = str(
                result.document.inference.prediction.total_amount.value)
            print('Total value : ', item.text)
            myfile.writelines('Total value : ' + item.text)
            myfile.writelines('\n')
        else:
            item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxableAmountCurr'):
        item.text = '0'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxableAmount'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxAmountCurr'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxAmount'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxableAmountCurr'):
        item.text = '0.00'

    for count, item in enumerate(myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxableAmount')):
        item.text = '0'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxAmountCurr'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxAmount'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmountCurr'):
        item.text = '0.00'

    for count, item in enumerate(myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmount')):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxInclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxInclusiveAmount'):
        item.text = '0.00'

    for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}Percent'):
        item.text = '21'

    for count, item in enumerate(myroot[24].iter()):

        if count == 9:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxableAmount'):
                item.text = '0.00'

        if count == 13:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmount'):
                item.text = '0.00'

        if count == 30:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxableAmount'):
                item.text = '0.00'

        if count == 34:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmount'):
                item.text = '0.00'

        if count == 51:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxableAmount'):
                item.text = '0.00'

        if count == 55:
            for item in myroot[24].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmount'):
                item.text = '0.00'

    # my_dict['LegalMonetaryTotal']['TaxExclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['TaxExclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['TaxInclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['TaxInclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['AlreadyClaimedTaxExclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['AlreadyClaimedTaxExclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['AlreadyClaimedTaxInclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['AlreadyClaimedTaxInclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['DifferenceTaxExclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['DifferenceTaxExclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['DifferenceTaxInclusiveAmount']=''
    # my_dict['LegalMonetaryTotal']['DifferenceTaxInclusiveAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['PayableRoundingAmount']=''
    # my_dict['LegalMonetaryTotal']['PayableRoundingAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['PaidDepositsAmount']=''
    # my_dict['LegalMonetaryTotal']['PaidDepositsAmountCurr']=''
    # my_dict['LegalMonetaryTotal']['PayableAmount']=''
    # my_dict['LegalMonetaryTotal']['PayableAmountCurr']=''

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}TaxExclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}TaxExclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}TaxInclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxExclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxExclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}AlreadyClaimedTaxInclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxExclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxExclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxInclusiveAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}DifferenceTaxInclusiveAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PayableRoundingAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PayableRoundingAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PaidDepositsAmount'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PaidDepositsAmountCurr'):
        item.text = '0.00'

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PayableAmount'):
        item.text = str(
            result.document.inference.prediction.total_amount.value)

    for item in myroot[25].iter('{http://isdoc.cz/namespace/2013}PayableAmountCurr'):
        item.text = '0.00'

    # my_dict['PaymentMeans']['Payment'][0]['PaidAmount']=''
    # my_dict['PaymentMeans']['Payment'][0]['PaymentMeansCode']=''
    # my_dict['PaymentMeans']['Payment'][0]['Details']['DocumentID']=''
    # my_dict['PaymentMeans']['Payment'][0]['Details']['IssueDate']=''

    # my_dict['PaymentMeans']['Payment'][1]['PaidAmount']=''
    # my_dict['PaymentMeans']['Payment'][1]['PaymentMeansCode']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['PaymentDueDate']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['ID']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['BankCode']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['Name']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['IBAN']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['BIC']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['VariableSymbol']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['ConstantSymbol']=''
    # my_dict['PaymentMeans']['Payment'][1]['Details']['SpecificSymbol']=''

    # my_dict['PaymentMeans']['Payment'][2]['PaidAmount']=''
    # my_dict['PaymentMeans']['Payment'][2]['PaymentMeansCode']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['PaymentDueDate']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['ID']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['BankCode']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['Name']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['IBAN']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['BIC']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['VariableSymbol']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['ConstantSymbol']=''
    # my_dict['PaymentMeans']['Payment'][2]['Details']['SpecificSymbol']=''

    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][0]['ID']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][0]['BankCode']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][0]['Name']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][0]['IBAN']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][0]['BIC']=''

    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][1]['ID']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][1]['BankCode']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][1]['Name']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][1]['IBAN']=''
    # my_dict['PaymentMeans']['AlternateBankAccounts']['AlternateBankAccount'][1]['BIC']=''

    # my_dict.pop('Extensions' )

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}DocumentID'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}IssueDate'):
        item.text = str(result.document.inference.prediction.date.value)

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}PaymentMeansCode'):
        item.text = '10'

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}ID'):
        item.text = '0001'

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}BankCode'):
        item.text = '0000'

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}IBAN'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}BIC'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}VariableSymbol'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}ConstantSymbol'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}SpecificSymbol'):
        item.text = ' '

    for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}PaymentDueDate'):
        for item in myroot[26].iter('{http://isdoc.cz/namespace/2013}PaymentDueDate'):
            # item_['issue_date']=datetime.datetime.strptime(item_['issue_date'], "%d.%m.%Y").strftime("%Y-%m-%d")

            if result.document.inference.prediction.due_date.value != None:
                item.text = result.document.inference.prediction.due_date.value
            else:
                item.text = result.document.inference.prediction.date.value

    print(df_)
    print()
    myfile.writelines(
        '-----------------------------------------------------------------------------------------------')
    myfile.writelines('\n')
    print('print from procedure  ', 'test.isdoc')
    mytree.write('temporary.isdoc',  encoding='utf-8', xml_declaration=True)

    infile = "temporary.isdoc"
    outfile = file_path_

    delete_list = ["ns0:", "<ForeignCurrencyCode>", "</ForeignCurrencyCode>"]
    with open(infile) as fin, open(outfile, "w+") as fout:
        for line in fin:
            for word in delete_list:
                line = line.replace(word, "")
            fout.write(line)
    return


# main ()
# remove protokol conversion



def convert(file_path):
    working_dir = os.getcwd()
    i = 0  # index of input file
    val_list = []

    while (i < len(file_path)):
        # separate filename and change file type
        head, tail = os.path.split(file_path[i])
        base_name, _ = os.path.splitext(tail)
        # separate filename and change file type
        new_file_path = base_name + "." + "isdoc"
        try:
            #mindee_client = Client(api_key="50a18642a4f354d983511b86d7b3214b")
            mindee_client = Client(api_key='6a452f8cde548a2e5acef5017bba701d')
        except HTTPError as e:
            print(e.response.text)

        if not os.path.exists(working_dir + '/isdoc'):
            os.mkdir(working_dir + "/isdoc")

        filling_mindee_xml(
            file_path[i], working_dir + '/isdoc/' + new_file_path)

        my_schema = xmlschema.XMLSchema('isdoc-invoice-6.0.2.xsd')

        if my_schema.is_valid(working_dir + '/isdoc/' + new_file_path):
            val_list.append(new_file_path + ' ISDOC Validation is O.K. ')
        else:
            val_list.append(new_file_path + ' ISDOC Validation is incorrect ')
        i += 1
    return val_list




def update(edf):
    edf.to_csv(csvfn, index=False)
    

##### MAIN ###############

st.image('page_13_img_1.jpg')
st.sidebar.title('conversion scan copy of invoices to  formattted json by aid of Mistral AI, support jpg, jpeg, a pdf')


st.balloons()  # Celebration balloons


st.sidebar.write('Download selected files, and then click on convert')
uploaded_files = st.sidebar.file_uploader(
    'Choose invoices to be converted to isdoc format:', accept_multiple_files=True)

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files=''
uploaded_files_list=[]

for q in uploaded_files:
    uploaded_files_list.append(q.name)


uploaded_files_test_list=st.session_state.uploaded_files 
print('type of uploaded_files', type(uploaded_files))
res = list((Counter(uploaded_files_list)-Counter(uploaded_files_list)).elements())
print('##################### counter ', res)

if len(uploaded_files_test_list)!= len(uploaded_files_list):
    st.session_state.uploaded_files = uploaded_files_list

    uploaded_files_test_list=st.session_state.uploaded_files 


    print('********Uploaded files: ', uploaded_files_list,'   ', st.session_state.uploaded_files)



            

    if not os.path.exists(os.getcwd() + '/isdoc'):
        os.mkdir(os.getcwd() + "/isdoc")
    else:
        files = os.listdir(os.getcwd() + "/isdoc")
    # removes all files in directoryt
 

            # create directory /json


    if not os.path.exists(os.getcwd() + '/json'):
        os.mkdir(os.getcwd() + "/json")
    else:
        files = os.listdir(os.getcwd() + "/json")
    # removes all files in directoryt
        for file in files:
            os.remove(os.getcwd() + "/json/"+file)

            #create directory /invoice

    if not os.path.exists(os.getcwd() + '/invoices'):
        os.mkdir(os.getcwd() + "/invoices")
    else:
        files = os.listdir(os.getcwd() + "/invoices")
# removes all files in directoryt
        for file in files:
            os.remove(os.getcwd() + "/invoices/"+file)

    # create directory for pdf /invoice_pdf

    if not os.path.exists(os.getcwd() + '/invoices_pdf'):
        os.mkdir(os.getcwd() + "/invoices_pdf")
    else:
        files = os.listdir(os.getcwd() + "/invoices_pdf")
# removes all files in directoryt
    for file in files: 
       os.remove(os.getcwd() + "/invoices_pdf/"+file)


    print('uploaded_files: ', uploaded_files)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        print(uploaded_file.name)
        split_tup = os.path.splitext(uploaded_file.name)
        print(split_tup)
 
# extract the file name and extension, pdffile support
        print(split_tup[0])
        print(split_tup[1])

    # os.mkdir(path)

        if split_tup[1].upper()=='.PDF':
            print('PDF format')
            with open(os.path.join(os.getcwd() + '/invoices_pdf/' + uploaded_file.name), "wb") as g:
                g.write(uploaded_file.getbuffer())
                print('download pdf to /invoices_pdf: ', os.path.join(os.getcwd() + '/invoices_pdf/' + uploaded_file.name))
        # Load a document
 
            print(' convert from path: ',os.getcwd() + '/invoices_pdf/' + uploaded_file.name)
            pdf = pdfium.PdfDocument(os.getcwd() + '/invoices_pdf/' + uploaded_file.name)
            print('pdf length' ,len(pdf))
        

        # Loop over pages and render


 
            for i in range(len(pdf)):
                    page = pdf[i]
                    image = page.render(scale=4).to_pil()
                    image.save(os.getcwd() + '/invoices/' + split_tup[0] + '.jpeg', 'JPEG')
                    print('upload jpeg: ',os.getcwd() + '/invoices/' + split_tup[0]  +'.jpeg' )

         


        else:
            with open(os.path.join(os.getcwd() + '/invoices/' + uploaded_file.name), "wb") as f:
         
                   f.write(uploaded_file.getbuffer())
        g.close()

    for uploaded_file in uploaded_files:

        base = os.path.splitext(uploaded_file.name)[0]
        print('base:', base)
        new_file_name = uploaded_file.name
        new_file_name = os.path.join(str(base) + ".isdoc")

        files_path = os.listdir(os.getcwd() + '/invoices')


 
        new_file_name = os.path.join(str(base) + ".json")
        print('new file name:', new_file_name)
        print('Mistal processing:' , os.path.join(os.getcwd() + '/invoices/'+ base+'.jpeg'))
        mistral_processsing(os.path.join(os.getcwd() + '/invoices/'+base +'.jpeg'), os.path.join(os.getcwd() + '/json/'+new_file_name))



        proc = psutil.Process()
        print(' Open Files', proc.open_files())

       
        
##############







 
    
exit_app = st.sidebar.button("Shut Down, close the windows, and press ctrl C in terminal")
   





