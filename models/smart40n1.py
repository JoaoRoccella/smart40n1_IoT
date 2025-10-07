import os
from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Tuple
from enum import Enum
from models.config import Database


class TimeUnit(str, Enum):
    minute = "MINUTE"
    hour = "HOUR"
    day = "DAY"

    @classmethod
    def from_str(cls, unit: str):
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

    def fetch(self) -> Dict:
        try:
            db_type = os.getenv("DB_TYPE", "mysql").lower()

            # --- base da query (placeholders mudam) ---
            if db_type == "sqlite":
                query = "SELECT timestamp, variable, value FROM data WHERE variable = ?"
                params: Tuple = (self.variable,)
            else:
                query = "SELECT `timestamp`, `variable`, `value` FROM `data` WHERE `variable` = %s"
                params: Tuple = (self.variable,)

            # --- intervalo de tempo ---
            if self.time and self.unit:
                unidade_sql = TimeUnit.from_str(self.unit).value

                if db_type == "sqlite":
                    # SQLite aceita unidades em minúsculo com plural opcional
                    unit_sqlite = unidade_sql.lower() + "s"
                    query += f" AND timestamp >= DATETIME('now', '-{int(self.time)} {unit_sqlite}')"
                    query += " ORDER BY timestamp DESC"
                else:
                    query += f" AND `timestamp` >= NOW() - INTERVAL {int(self.time)} {unidade_sql}"
                    query += " ORDER BY `timestamp` DESC"
            else:
                query += " ORDER BY timestamp DESC LIMIT 1"

            # --- executa ---
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
