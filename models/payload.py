# payload.py
from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Tuple
from enum import Enum
from models.config import Database


class TimeUnit(str, Enum):
    minute = "MINUTE"
    hour = "HOUR"
    day = "DAY"

    @classmethod
    def from_str(cls, unit: str):
        """Mapeia unidade no plural ou minúscula para o enum correspondente."""
        mapping = {
            "minutes": cls.minute,
            "minute": cls.minute,
            "hours": cls.hour,
            "hour": cls.hour,
            "days": cls.day,
            "day": cls.day,
        }
        return mapping.get(unit.lower()) if unit else None


class LastVariablePayload(BaseModel):
    variable: str
    time: Optional[str] = None
    unit: Optional[str] = None

    # --- Validação de parâmetros ---
    @field_validator("time")
    def validar_tempo(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError("O parâmetro 'time' deve ser um número inteiro.")
        return v

    @field_validator("unit")
    def validar_unidade(cls, v):
        if v is None:
            return v
        if not TimeUnit.from_str(v):
            raise ValueError("Unidade inválida. Use: minute(s), hour(s) ou day(s).")
        return v

    # --- Montagem e execução da query ---
    def fetch(self) -> Dict:
        """
        Cria a query SQL e executa automaticamente no banco.
        Retorna uma lista de registros ou mensagem de erro.
        """
        try:
            # base query
            query = "SELECT `variable`, `value`, `timestamp` FROM `data` WHERE `variable` = %s"
            params: Tuple = (self.variable,)

            # verifica se deve aplicar intervalo
            if self.time and self.unit:
                unidade_sql = TimeUnit.from_str(self.unit).value
                query += f" AND `timestamp` >= NOW() - INTERVAL {int(self.time)} {unidade_sql}"
                query += " ORDER BY `timestamp` DESC"
            else:
                query += " ORDER BY `timestamp` DESC LIMIT 1"

            # executa no banco
            with Database() as db:
                result = db.executar_query(query, params)
                if result:
                    return {"data": result}
                else:
                    return {
                        "mensagem": f"Nenhum registro de {self.variable} foi encontrado.",
                        "query": query,
                        "params": params,
                    }

        except Exception as e:
            return {"erro": str(e)}
