from fastapi import APIRouter, Depends
from models.smart40n1 import LastVariablePayload

router = APIRouter()


@router.get(
    "/{variable}/last",
    tags=["Bancada Smart4.0 N1"],
    summary="Último valor de uma variável",
    description="Retorna o último valor registrado para a variável especificada.",
    response_description="O último valor registrado para a variável.",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "variable": "temperatura",
                                "value": "23",
                                "timestamp": "2024-10-01T12:34:56Z",
                            }
                        ]
                    }
                }
            },
        },
        400: {"description": "Parâmetros inválidos"},
        404: {"description": "Variável não encontrada"},
        500: {"description": "Erro interno do servidor"},
    },
)
@router.get(
    "/{variable}/last/{time}/{unit}",
    tags=["Bancada Smart4.0 N1"],
    summary="Último valor de uma variável em um intervalo de tempo",
    description="Retorna o último valor registrado para a variável especificada dentro do intervalo de tempo fornecido.",
    response_description="O último valor registrado para a variável no intervalo de tempo especificado.",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "variable": "temperatura",
                                "value": "22",
                                "timestamp": "2024-10-01T12:30:00Z",
                            },
                            {
                                "variable": "temperatura",
                                "value": "23",
                                "timestamp": "2024-10-01T12:34:56Z",
                            },
                        ]
                    }
                }
            },
        },
        400: {"description": "Parâmetros inválidos"},
        404: {"description": "Variável não encontrada"},
        422: {
            "description": "Unidade de tempo inválida",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "unit"],
                                "msg": "Unidade inválida. Use: minute(s), hour(s) ou day(s).",
                                "type": "value_error",
                            }
                        ]
                    }
                }
            },
        },
        500: {"description": "Erro interno do servidor"},
    },
)
async def get_last_variable(payload: LastVariablePayload = Depends()):
    """
    Endpoint delega toda a validação e execução da query ao smart40n1.py.
    """
    return payload.fetch()
