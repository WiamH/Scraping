#!/usr/bin/env python3
#########################################################################################

# Código original MalzimKorzh
#https://github.com/maksimKorzh/one-time-scrapers/blob/master/scrapers/google_scraper.py 

# Modificado por Wiam Hechach

#########################################################################################

# Librerias
import requests
from bs4 import BeautifulSoup
import csv
import re
import time

class ScrapingGoo:

    # Punto de entrada del rastreador
    base_url = 'https://www.google.com/search'

    # Parámetros de cadena de consulta para rastrear las páginas de resultados // quitar numero en 'start'**
    pagination_params = {
        'q': 'empresas ciberseguridad catalunya',
        'sxsrf':'ALeKk02ENKWkSsNP4NngNbEWD6n6rNInlQ:1618785055023',
        'ei': 'H7N8YL14idRR9oSnkAs',
        'start': '',
        'sa': 'N',
        'ved': '2ahUKEwj9g7Ch7IjwAhUJahQKHXbCCbIQ8tMDegQICBBS',
        'biw': '558',
        'bih': '792',
        'dpr': '1.25',    
    }

    # Parámetros de cadena de consulta para la página de resultados inicial *
    initial_params = {
        'q': 'empresas ciberseguridad catalunya',
        'biw': '1536',
        'bih': '792',
        'sxsrf': 'ALeKk02Cf5-ctdfyFiO-nuuG-O-tIap3lw:1618769956719',
        'ei': 'JHh8YK_DK4mTlwSxmrsw',
        'oq': 'empresas ciberseguridad catalunya',
        'gs_lcp': 'Cgdnd3Mtd2l6EAMyBQgAEM0CMgUIABDNAjIFCAAQzQIyBQgAEM0COgcIIxCwAxAnOgcIABBHELADOgQIIxAnOgcIIxCwAhAnUPOpAliuxQJgo8oCaANwAngAgAGGA4gBqQiSAQcwLjUuMC4xmAEAoAEBqgEHZ3dzLXdpesgBCcABAQ',
        'sclient': 'gws-wiz',
        'ved': '0ahUKEwiv5fiBtIjwAhWJyYUKHTHNDgY4ChDh1QMIDg',
        'uact': '5',
    }

    # Solicitar encabezados ***
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'es-ES,es;q=0.9,ca;q=0.8,en;q=0.7',
        'cookie': 'CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; SEARCH_SAMESITE=CgQIn5IB; OGPC=19022519-1:; OTZ=5919460_48_52_123900_48_436380; 1P_JAR=2021-4-11-11; SID=8gewLFJJ1jx8Dd3nC7VcGP4V2AsbWpv7AQRknc6InOxRwlZ-8FNxP1AynCUoVBUAeNwQlg.; __Secure-3PSID=8gewLFJJ1jx8Dd3nC7VcGP4V2AsbWpv7AQRknc6InOxRwlZ-3ZCLxEJYJpXJLqY9-d1wjw.; HSID=Ak_Zya2x7u0IGJDCH; SSID=ANyPN_N058lTCMi6p; APISID=Ky8FKhFRLoRCVrtX/A8DjutaF59FbHtbh5; SAPISID=WMvnbHkhrhuPOKHB/AM3JoSs5Ki0pWKviu; __Secure-3PAPISID=WMvnbHkhrhuPOKHB/AM3JoSs5Ki0pWKviu; NID=213=jieJPCEKLSRPl3sckYoq_VFrryMvyiOWc306PAygd1gG3uQ1k2t9W7sZqRGckPiqxac7K6o5RLYUmnW2Hj73yfQrEDFo7j4VaQru2d4hIPAS_ptuV2FFOaZY9P5kP8v0IHyRediLtjzCXda4UmqXFkcFFmZsft8Knj95xvyZBZK0gLGq0207OM-BuqX1NPdreZW6FR2No2ALOt2SLLTEUS4SCbZuU2yVC6tJASEV4ukwfYJFf0ZBUagwzEsBUrJ5bSeiTKNO4abFwQ; DV=Q5PxPrLVtfZCcBeTcarDqyFOJlVjjteQ-dYmFlQHEwAAAED_3-zmRN3uPQAAAAgH7s-UDNE6KAAAAA',
        'referer': 'https://www.google.es/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    
    }

    # Resultado de raspado
    results = []    

    def fetch(self, query, page):

        ## Iniciar búsqueda initial_params (p.ej., "Linux mint")
        self.initial_params['q'] = query
        
        ## Si obtiene la primera página de resultados
        if not page:
            # Usar parámetros iniciales
            params = self.initial_params

        ## Sino, raspar las siguientes páginas
        else:
            params = self.pagination_params
            
            ### Especificar el número de página en formato página * 10
            params['start'] = str(page * 10)

            ### Iniciar búsqueda
            params['q'] = query
        
        ## Solicitar HTTP GET
        response = requests.get(self.base_url, params=params, headers=self.headers)
        print('Solicitud HTTP GET a URL:% s | Código de estado:% s' %  (response.url, response.status_code))
        
        ## Devolver respuesta HTTP
        return response

    # Analizar el texto de la respuesta y extraer los datos
    def parse(self, html):

        ## Analizar contenido
        content = BeautifulSoup(html, 'lxml')
        
        ## Extraer datos ***
        nombre = [nombre.text for nombre in content.findAll('h3', {'class': 'LC20lb DKV0Md'})]
        enlace = [enlace.next_element['href'] for enlace in content.findAll('div', {'class': 'yuRUbf'})]
        resumen = [resumen.text for resumen in content.findAll('div', {'class': 'IsZvec'})]
        
        ## Recorrer el numero de entradas
        for index in range(0, len(nombre)):
            self.results.append({
                'nombre': nombre[index],
                'enlace': enlace[index],
                'resumen': resumen[index],                        
            })
    
    # Escribir resultados rascados en un archivo CSV
    def write_csv(self):

        ## Verificar la lista de resultados no está vacía
        if len(self.results):
            print('Guardando resultado de búsqueda en: "resultados.csv"', end='')

            ### Escribir CSV
            with open('resultado.csv', 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
                writer.writeheader()

                #### Etiquetar las columnas del archivo
                for row in self.results:
                    writer.writerow(row)

            print('...Hecho!')

    # Almacenar respuesta HTML en el archivo para analizar
    def store_response(self, response):

        ## Si la respuesta es correcta
        if response.status_code == 200:

            ### Escribir respuesta en archivo HTML
            print('Respuesta guardada en: "resulado.html "', end='')
            with open('resultado.html', 'w') as html_file:
                html_file.write(response.text)
            
            print('...Hecho!')
        else:
            print('¡No OK, codigo respuesta diferente a 200!')


    # Cargar la respuesta HTML para analizar
    def load_response(self):
        html=''
        
        ## Acceder al archivo HTML
        with open('resultado.html', 'r') as html_file:
            for line in html_file.read():
                html += line

        ## Devuelve HTML como cadena
        return html
    

    # Arrancar el rastreador
    def run(self):

        # Recorrer el numero de paginas a raspar
        for page in range(0,2):
            if page: 
                
                # Realizar solicitud HTTP GET
                response = self.fetch('empresas ciberseguridad catalunya', page)
               
                # Analizar contenido
                self.parse(response.text)
            #else:
                #print('Pagina Inicial')

                
                #self.store_response(response)
                #html = self.load_response()

            # Esperear 5 segundos          
            time.sleep(5)
                

        # Escribe los resultados extraídos en un archivo CSV
        self.write_csv()

# Programa principal
if __name__ == '__main__':
    raspar = ScrapingGoo()
    raspar.run()




