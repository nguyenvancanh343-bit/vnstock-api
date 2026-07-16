from fastapi import FastAPI
from vnstock import Vnstock
import uvicorn
import os

app = FastAPI()


@app.get("/")
def home():
    return {"status": "vnstock API is running"}


@app.get("/price/{ticker}")
def get_price(ticker: str):
    try:
        stock = Vnstock().stock(symbol=ticker.upper(), source='VCI')
        df = stock.quote.history(start='2025-01-01', end='2026-12-31', interval='1D')
        data = df.tail(60).to_dict(orient='records')
        return {"ok": True, "ticker": ticker.upper(), "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/try/{ticker}")
def try_fundamental(ticker: str):
    result = {}
    tk = ticker.upper()
    try:
        stock = Vnstock().stock(symbol=tk, source='TCBS')
        ov = stock.company.overview()
        result["overview_TCBS"] = ov.to_dict(orient='records')
    except Exception as e:
        result["overview_TCBS_error"] = str(e)
    try:
        stock = Vnstock().stock(symbol=tk, source='VCI')
        pb = stock.trading.price_board([tk])
        result["price_board"] = pb.to_dict(orient='records')
    except Exception as e:
        result["price_board_error"] = str(e)
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
