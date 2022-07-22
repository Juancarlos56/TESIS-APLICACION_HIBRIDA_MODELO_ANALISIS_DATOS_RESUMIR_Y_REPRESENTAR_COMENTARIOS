# BACKEND - TESIS: CREACIÓN DE UNA APLICACION HIBRIDA CON IONIC Y UN MODELO DE ANALISIS DE DATOS PARA RESUMIR Y REPRESENTAR COMENTARIOS



Nota: 
- Agregar documentos de configuracion de firebase 
1. vars/enviroment.env
```
SECRET_KEY='' # Del proyecto en Django
DEBUG=True
apiKey=""
messagingSenderId=""
appId=""
tokenAPI=""
```

2. ResumenCommentsAPI/ClavesPrivadas/serviceAccount.json

```
{
    "type": "",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_x509_cert_url": ""
}
```
- Agregar archivos de configuracion de red Neuronal: 

Ruta a nivel manage.py: /static/modelo/TextSummarizationT5/
Archivos: 
- config.json 
- pytorch_model.bin
- tokenizer.json
- tokenizer_config.json
- special_tokens_map.json
