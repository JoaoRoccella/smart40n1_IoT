from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    tags=["Geral"],
    summary="Verifica se a API está rodando",
    description="Rota para verificar se a API está operacional. Retorna uma mensagem simples.",
    response_description="Mensagem de status da API.",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "message": "OK, a API está rodando. Consulte /docs para a documentação."
                    }
                }
            },
        },
        500: {"description": "Erro interno do servidor"},
    },
)
async def root():
    return {"message": "OK, a API está rodando. Consulte /docs para a documentação."}


@router.get(
    "/helloThere",
    tags=["Geral"],
    summary="Mensagem de saudação",
    description="Rota que retorna uma mensagem de saudação.",
    response_description="Mensagem de saudação.",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {"example": {"message": "General Kenobi!"}}
            },
        },
        500: {"description": "Erro interno do servidor"},
    },
)
async def helloThere():
    return {"message": "General Kenobi!"}
