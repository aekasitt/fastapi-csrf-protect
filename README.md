# FastAPI CSRF Protect

[![Build Status](https://travis-ci.com/aekazitt/fastapi-csrf-protect.svg?branch=master)](https://travis-ci.com/aekazitt/fastapi-csrf-protect)
[![Package Vesion](https://img.shields.io/pypi/v/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Format](https://img.shields.io/pypi/format/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![License](https://img.shields.io/pypi/l/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)

## Features

FastAPI extension that provides Cross-Site Request Forgery (XSRF) Protection support (easy to use and lightweight).
If you were familiar with `flask-wtf` library this extension suitable for you.
This extension inspired by `fastapi-jwt-auth` 😀

- Storing `fastapi-csrf-token` in cookies or serve it in template's context

## Installation

The easiest way to start working with this extension with pip

```bash
pip install fastapi-csrf-protect
```

## Usage

### With Context and Headers

```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class CsrfSettings(BaseModel):
  secret_key:str = 'asecrettoeverybody'

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get('/form')
def form(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Returns form template.
  '''
  csrf_token = csrf_protect.generate_csrf()
  response = templates.TemplateResponse('form.html', {
    'request': request, 'csrf_token': csrf_token
  })
  return response

@app.post('/posts', response_class=ORJSONResponse)
def create_post(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Creates a new Post
  '''
  csrf_token = csrf_protect.get_csrf_from_headers(request.headers['X-CSRFToken'])
  csrf_protect.validate_csrf(csrf_token)
  # Do stuff

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return ORJSONResponse(
    status_code=exc.status_code,
      content={ 'detail':  exc.message
    }
  )

```

### With Cookies

```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class CsrfSettings(BaseModel):
  secret_key:str = 'asecrettoeverybody'

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get('/form')
def form(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Returns form template.
  '''
  response = templates.TemplateResponse('form.html', { 'request': request })
  csrf_protect.set_csrf_cookie(response)
  return response

@app.post('/posts', response_class=ORJSONResponse)
def create_post(request: Request, csrf_protect:CsrfProtect = Depends()):
  '''
  Creates a new Post
  '''
  csrf_protect.validate_csrf_in_cookies(request)
  # Do stuff

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return ORJSONResponse(status_code=exc.status_code, content={ 'detail':  exc.message })

```

## License

This project is licensed under the terms of the MIT license.
