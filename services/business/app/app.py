"""Service starting point.
"""


import falcon

from web_api import RESTfulServer
from logic import Shopping
from configs import products as products_configs


# run using `gunicorn app[:falcon_api]`; `application` is by default used by gunicorn
falcon_api = application = falcon.API()

items = products_configs['items']
shopping = Shopping(products_configs['generator'](items))

restful_endpoint = RESTfulServer(falcon_api, shopping)
restful_endpoint.expose()