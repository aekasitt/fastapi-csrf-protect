# FastAPI CSRF Protect

[![Package version](https://img.shields.io/pypi/v/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Format](https://img.shields.io/pypi/format/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Python version](https://img.shields.io/pypi/pyversions/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![License](https://img.shields.io/pypi/l/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)
[![Top](https://img.shields.io/github/languages/top/aekasitt/fastapi-csrf-protect)](.)
[![Languages](https://img.shields.io/github/languages/count/aekasitt/fastapi-csrf-protect)](.)
[![Size](https://img.shields.io/github/repo-size/aekasitt/fastapi-csrf-protect)](.)
[![Last commit](https://img.shields.io/github/last-commit/aekasitt/fastapi-csrf-protect/master)](.)
[![Documentation](https://img.shields.io/badge/pdoc-555?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwBAMAAAClLOS0AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAkUExURUdwTJHtkZDtkI/vj2rOYFXBQn3deZDukDuzAHDTaFrES4HhfmcEZqoAAAAHdFJOUwCAv0Df788Wv3t3AAACCElEQVQ4y42UsXKcMBCGuVC4Pc6FJuPGRzLDnK/xnAsKP0IeIU+QLhyFEHoAVlJlNxJHlwbBVY4LyeeXs4BLCnQzCTOAZj+0K+3/iyD4zwvhIIiiey/+iVRB8LnJPJBq6QA8eeBRuI8R8UFKTYbc7QGqQRIAOa++KKAD6LW4nQMFwgIB7gMlLaPQz8GVMlhxjD2AoKVcSeKl2jCAyq2K/5yBsiINRqSx+QwUcmhgFNmXOWivzO2CZsWTlyrl2U69qPmMjUi0pBqreY0bvi8BGGHzVaVKJnWHi2o5bwlhOI4JGF9yzeuTPua+5qoHEHvfDAvF398qPz70vboRl4DV8vESCC3HqSfsAAotkNf0sY1HhnR+AZTQruzrBXAHLLe/h9HDtIRwFa+v3XvL4bX8NXpvrLTDb31tImdezvO7dgipAYTOmhyYXAYptOvNuPVR99Ry24BieJlqEX8bdzhUWlBo3JQTMExZ//X7BNplmCgN4t3FFdecnUHJcHLi6ogfEurCujdlMwK38AMItd/FETp0TD2vi6nvW3AHYkje1VmcKJ6humyn46hB1ebkqPwhsYkJs8+jmLYp2Z5AgwkfnlRLPR7BsBTYUH3M7pEVRAMcT2dXbbWLM6d/SEFi6pKayVU75z2Oh3FKoKt7Lv/IkRw6M4mJXKrerP8aII6vz8MVxvsv//gNfQBIOvQNeKr0GQAAAABJRU5ErkJggg==)](https://aekasitt.github.io/fastapi-csrf-protect)

[![Protect Banner](static/protect-banner.svg)](https://github.com/aekasitt/fastapi-csrf-protect/blob/master/static/protect-banner.svg)

## Features

FastAPI extension that provides stateless Cross-Site Request Forgery (XSRF) Protection support.
Aimed to be easy to use and lightweight, we adopt [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie) mitigation pattern.
If you were familiar with `flask-wtf` library this extension suitable for you.
This extension inspired by `fastapi-jwt-auth` 😀

- Storing `fastapi-csrf-token` in cookies or serve it in template's context

## Installation

The easiest way to start working with this extension with pip

```bash
pip install fastapi-csrf-protect
# or
uv add fastapi-csrf-protect
```

## Getting Started

The following examples show you how to integrate this extension to a FastAPI App

### Example Login Form

```python
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic_settings import BaseSettings

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CsrfSettings(BaseSettings):
  secret_key: str = "asecrettoeverybody"
  cookie_samesite: str = "none"

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get("/login")
def form(request: Request, csrf_protect: CsrfProtect = Depends()):
  """
  Returns form template.
  """
  csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
  response = templates.TemplateResponse(
    "form.html", {"request": request, "csrf_token": csrf_token}
  )
  csrf_protect.set_csrf_cookie(signed_token, response)
  return response

@app.post("/login", response_class=JSONResponse)
async def create_post(request: Request, csrf_protect: CsrfProtect = Depends()):
  """
  Creates a new Post
  """
  await csrf_protect.validate_csrf(request)
  response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})
  csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
  return response

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

```

### How to send the CSRF token in your client code

#### HTML Form (Server-side rendered)

```html
<form method="post" action="/login">
  <input type="hidden" name="token_key" value="{{ csrf_token }}">
  <!-- other fields -->
</form>
```
#### AJAX (JavaScript)

```javascript
fetch("/items/123", {
  method: "DELETE",
  headers: {
    "X-CSRFToken": getCookie("csrftoken")
  },
  credentials: "include"
});
```

> [!IMPORTANT]
> - The flexible sub-package ignores the token_location setting — tokens from either header or body are always accepted.
> - CSRF token validation still requires a matching CSRF cookie as in the base package.
> - Priority is given to header over body when both are present.

### 📌 Flexible Mode (fastapi_csrf_protect.flexible)

Some applications combine **Server-Side Rendering (SSR)** with **API endpoints** in the same project.
For example:
  - **SSR pages** rendered with Jinja2 templates that use HTML forms (CSRF token in **form body**)
  - **AJAX / API calls** (e.g. DELETE, PUT, PATCH) that pass the CSRF token in the **HTTP header**

The main fastapi-csrf-protect package is **opinionated** and expects the CSRF token in **one location only** (either header or body).
For hybrid apps, this can be inconvenient.

The **flexible sub-package** provides a drop-in replacement for CsrfProtect that **always accepts CSRF tokens from either the header or the form body**, with the following priority:
  - **Header**: X-CSRFToken
  - **Body**: token_key (form-data)

### When to use flexible

Use fastapi_csrf_protect.flexible if:
  - You have both SSR pages and API endpoints in the same project.
  - Some requests (like DELETE) cannot send a body but still require CSRF validation.
  - You want to avoid maintaining two different CSRF configurations.

If your app only uses **one** method to send CSRF tokens, stick to the **core package** for a stricter policy.
## Contributions

### Prerequisites

* [git](https://git-scm.com/) - --fast-version-control
* [python](https://www.python.org) 3.9 and above - High-level general-purpose programming language
* [uv](https://docs.astral.sh/uv) - Extremely fast Python package & project manager, written in Rust

The following guide walks through setting up your local working environment using `git`
as distributed version control system and `uv` as Python package and version manager.
If you do not have `git` installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>
  
  ```bash
  brew install git
  ```
</details>

<details>
  <summary> Install via binary installer (Linux) </summary>
  
  * Debian-based package management
  ```bash
  sudo apt install git-all
  ```

  * Fedora-based package management
  ```bash
  sudo dnf install git-all
  ```
</details>

If you do not have `uv` installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>

  ```bash
  brew install uv
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>

Once you have `git` distributed version control system installed, you can
clone the current repository and  install any version of Python above version
3.9 for this project. The following commands help you set up and activate a
Python virtual environment where `uv` can download project dependencies from the `PyPI`
open-sourced registry defined under `pyproject.toml` file.

<details>
  <summary> Set up environment and synchronize project dependencies </summary>

  ```bash
  git clone git@github.com:aekasitt/fastapi-csrf-protect.git
  cd fastapi-csrf-protect
  uv venv --python 3.9.6
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

### Roadmap

* Fix CI/CD and GitHub Pages integration
* Add code samples when setting up and running tests
* Drop support for Python 3.9 by October, 2025
* (Syntax 3.9 -> 3.10) Replace `Optional[...]` with `None | ...`
* (Syntax 3.9 -> 3.10) Replace `Union[..., ...]` with `... | ...`
* Correct front-end samples in `README.md`
* Add `flexible` examples
* Rewrite `Flexible Mode` section in `README.md`
* Experiment with `granian[uvloop]` and `granian[rloop]`

### Getting started

To contribute to the project, fork the repository and clone to your local device
and install preferred testing dependency [pytest](https://github.com/pytest-dev/pytest)
Alternatively, run the following command on your terminal to do so:

```bash
uv sync --dev
```

Testing can be done by the following command post-installation:

```bash
uv sync --dev --group tests
pytest
```

## Change-logs

* **0.3.1** Adopt [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)

  :construction: **BREAKING CHANGE**
  0.3.0 -> 0.3.1: `generate_csrf` marked for deprecation

* **0.3.2** Add `token_location` config (either `body` or `header`); Unset to prevent token reuse

  :construction: **BREAKING CHANGE**
  0.3.1 -> 0.3.2: `validate_csrf` is now async

* **0.3.5** Introduced Pydantic V2 related bug fixed in version 0.3.6; Affects `cookie_samesite`
* **0.3.6** Fixed `cookie_samesite` validation bug introduced in previous version
* **1.0.0** Remove deprecated `generate_csrf`, please use `generate_csrf_tokens` returning tuple
* **1.0.1** Fix cookie unsetting when configuring lib with cookie `Secure` and / or `SameSite=None`
* **1.0.2** Improve boolean handling for `LoadConfig`
* **1.0.3** Failed experiement to integrate `mypyc` compilation due to dependency injection pattern
* **1.0.4** Added flexible mode when `token_location` is omitted and multiple location checks

  :construction: **FAILED ROLLOUT**
  1.0.3 -> 1.0.4: Rolled out with WIP code; immediately deleted version from PyPI

* **1.0.5** Remove `@dataclass` leftover from failed experiment; Clarify failure reasons under tests
* **1.0.6** Fix `Stream consumed` when submitted tokens via form data, `isinstance` consumes body
* **1.0.7** Fix add preverification content submitted in `Flexible Mode`; Add test selection flags

### Run Examples

To run the provided examples, first you must install extra dependencies
[granian](https://github.com/emmett-framework/granian) and [minijinja](https://github.com/mitsuhiko/minijinja/tree/main/minijinja-py)
Alternatively, run the following command on your terminal to do so

```bash
uv sync --group=examples
```

Running the example utilizing form submission

```bash
granian --interface asgi examples.body:app
```

Running the example utilizing headers via JavaScript

```bash
granian --interface asgi examples.header:app
```

## License

This project is licensed under the terms of the MIT license.
