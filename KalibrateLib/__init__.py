from .funciones import getToken

def OSVersion():
    det = """Detalles de la libreria =============
    Libreria para agilizar el uso de las api de kalibrate
    USO:
    Consultar con John Arteaga

    getColumnsSite _____
    regresa 3 arreglos:
        SiteInfo : data principal del site
        CompetitorSites : informacion sobre 'competitor site' 
        SiteGroupings : informacion sobre 'site grouping'
    
    Nota importante _____
    Para modificar las columnas que se retornan, se debe editar el archivo funciones.py
    agregar las columnas en la funcion correspondiente y volver a compilar el archivo WHL:

    --> python .\setup.py bdist_wheel

    Publicar en GITHUB para obtener la version linux del archivo WHL y cagar en el Lakehouse
    """

    
    return det
