from flask import request

def logger():
    print(f'{request.method} {request.path}')
