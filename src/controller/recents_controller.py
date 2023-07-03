from email import message
from functools import cache
from flask import request
from exceptions.parameter_not_found_exception import ParameterNotFoundException
from settings import CONTENT_TYPE_JSON_HEADER, APIKEY_VALIDATE_URL
from src.wsgi import application
from src.injector_factory import InjectorFactory
from nsj_gcf_utils.json_util import json_loads, json_dumps
from src.api_key_authentication import require_apikey
BASE_URL = f'/recents'


def _get_parameter(parameter_name : str, nullable: bool = False):
    req = request.args
    parameter = req.get(parameter_name)
    
    if not nullable and parameter is None:
        raise ParameterNotFoundException(f'Parâmetro obrigatorio {parameter_name} não informado na requisição')
    
    return parameter

def _get_all_parameters():
    grupo_empresarial = _get_parameter('grupo_empresarial', True)
    empresa = _get_parameter('empresa', True)
    estabelecimento = _get_parameter('estabelecimento', True)
    tenant = _get_parameter('tenant')
    email = _get_parameter('email')
    entity = _get_parameter('entity')
    return {
        'grupo_empresarial' : grupo_empresarial, 
        'empresa' : empresa, 
        'estabelecimento' : estabelecimento,
        'tenant': tenant, 
        'email' : email, 
        'entity': entity, 
    }
    
def _get_key_from_values(email, tenant, empresa, estabelecimento, grupo_empresarial, entity):
    return f"{email}_{tenant}_{empresa}_{grupo_empresarial}_{estabelecimento}_{entity}"
    
@application.route(BASE_URL, methods=['GET'])
@require_apikey(APIKEY_VALIDATE_URL)
def get_recents():
    try:
        key = _get_key_from_values(**_get_all_parameters())
        primary_key = _get_parameter('primary_key')
        cache_service = InjectorFactory.get_redis_service()
        
        data = cache_service.get_list(key, primary_key)
        return (json_dumps(data),200, CONTENT_TYPE_JSON_HEADER)
    except ParameterNotFoundException as e:
        return (json_dumps({'message': f'{str(e)}'}), 400, CONTENT_TYPE_JSON_HEADER)
    except Exception as e:
        return (json_dumps({'message': f'{str(e)}'}), 500, CONTENT_TYPE_JSON_HEADER)
    
    
@application.route(BASE_URL, methods=['POST'])
@require_apikey(APIKEY_VALIDATE_URL)
def post_recent():
    try:
        parameters = _get_all_parameters()
        key = _get_key_from_values(**parameters)
        primary_key = _get_parameter('primary_key', )
        cache_service = InjectorFactory.get_redis_service()
        
         
        cache_service.save_in_list(key, request.json, primary_key)
        return ('{}', 201, CONTENT_TYPE_JSON_HEADER)
    
    except ParameterNotFoundException as e:
        return (json_dumps({'message': f'{str(e)}'}), 400, CONTENT_TYPE_JSON_HEADER)
    except Exception as e:
        return (json_dumps({'message': f'{str(e)}'}), 500, CONTENT_TYPE_JSON_HEADER)
    