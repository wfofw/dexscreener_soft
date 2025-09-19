from enum import Enum
from start import get_conn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TokenData(BaseModel):
    token: str
    mcap: float
    age: int

def get_from_db(token: str, mcap: float | None = None, age: int | None = None):
    with get_conn() as conn, conn.cursor() as cur:
        query = "select tokenname, tokenmcap, tokenage from newtb where tokenname = %s"
        params = [token.lower()]

        fn = lambda rows: [(x[0], x[1], x[2]) for x in rows]
        
        if mcap is not None:
            query += " and tokenmcap> %s"
            params.append(mcap)
        if age is not None:
            query += " and tokenage> %s"
            params.append(age)
        
        cur.execute(query, tuple(params))
        rows = cur.fetchall()

    return [TokenData(token=r[0], mcap=r[1], age=r[2]) for r in rows]


@app.get("/tokens/data/{token_name}", response_model=list[TokenData])
def get_model(
    token_name: str, 
    mcap_limit: int | None = None, 
    age_limit: int | None = None
):
    res = get_from_db(token_name, mcap_limit, age_limit)
    return res
