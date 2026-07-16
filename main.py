from fastapi import FastAPI
from vnstock import Vnstock
import uvicorn
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "vnstock API is running"}

@app.get("/fundamental/{ticker}")
def get_fundamental(ticker: str):
    try:
        stock = Vnstock().stock(symbol=ticker.upper(), source='VCI')
        ratio = stock.finance.ratio(period='quarter', lang='vi').head(1)
        data = ratio.to_dict(orient='records')
        return {"ok": True, "ticker": ticker.upper(), "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/price/{ticker}")
def get_price(ticker: str):
    try:
        stock = Vnstock().stock(symbol=ticker.upper(), source='VCI')
        df = stock.quote.history(start='2025-01-01', end='2026-12-31', interval='1D')
        data = df.tail(60).to_dict(orient='records')
        return {"ok": True, "ticker": ticker.upper(), "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
