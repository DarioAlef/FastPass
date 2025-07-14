# app/routes/home.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 1) Criamos um "roteador" para agrupar rotas relacionadas à "home"
router = APIRouter()

# 2) Apontamos onde estão nossos templates HTML
#    Aqui, templates ficam em: <raiz_do_projeto>/app/templates
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    """
    Função que trata requisições GET para a rota "/".
    - 'request' é obrigatório ao usar templates (Jinja2 espera acessar coisas da requisição).
    - Retornamos o template 'home.html' preenchido.
    """
    # Podemos passar um dicionário de variáveis para o template:
    context = {
        "request": request,        # sempre necessário para Jinja2 funcionar
        "title": "FastPass",  # título dinâmico
    }
    # Renderiza e retorna o HTML
    return templates.TemplateResponse("home.html", context)
