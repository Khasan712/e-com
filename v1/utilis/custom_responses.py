

from types import NoneType


def success_response():
    return {
        'status': True
    }


def error_response(**kwargs):
    return {
        'status': False,
        "errors": kwargs
    }


def serializer_error_response(serializer_errors):
    return {
        "status": False, 
        "errors": {**{
            key: value[0] 
            for key, value in serializer_errors.items()
        }}
    }


def lang_error_response(lang):
    return {
        'status': False,
        'error': "Given language incorrect!"
    }


def lang_not_given_response():
    return {
        'status': False,
        'error': "Language not given!"
    }

def serializer_without_paginator_res(serializer_data, **kwargs):
    return {
        'status': True,
        "data": serializer_data
    }

def params_error_repsonse(*args):
    if args:
        errors = {}
        for arg in args:
            errors[arg] = "Not given or incorrect "
        return {
            "status": False,
            "errors": errors
        }
    return {
        'status': False,
        "error": "Given params incorrect or not given"
    }
    