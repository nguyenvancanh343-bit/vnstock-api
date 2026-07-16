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
@app.get("/debug/{ticker}")
def debug_fundamental(ticker: str):
    try:
        stock = Vnstock().stock(symbol=ticker.upper(), source='VCI')
        df = stock.finance.ratio(period='year', lang='vi')
        return {
            "columns": [str(c) for c in df.columns.tolist()],
            "shape": list(df.shape),
            "sample": df.tail(2).to_dict(orient='records')
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
        @app.get("/try/{ticker}")
def try_fundamental(ticker: str):
    result = {}
    tk = ticker.upper()

    # Cách 1: company overview (thường có P/E, P/B)
    try:
        stock = Vnstock().stock(symbol=tk, source='TCBS')
        ov = stock.company.overview()
        result["overview_TCBS"] = ov.to_dict(orient='records')
    except Exception as e:
        result["overview_TCBS_error"] = str(e)

    # Cách 2: price board (bảng giá có nhiều chỉ số)
    try:
        stock = Vnstock().stock(symbol=tk, source='VCI')
        pb = stock.trading.price_board([tk])
        result["price_board"] = pb.to_dict(orient='records')
    except Exception as e:
        result["price_board_error"] = str(e)

    # Cách 3: ratio nhưng lấy cột 2 gần nhất, xoay lại
    try:
        stock = Vnstock().stock(symbol=tk, source='VCI')
        df = stock.finance.ratio(period='year', lang='en')
        # Lọc vài chỉ số định giá phổ biến theo item_id
        keys = ['pe','pb','roe','roa','eps','marketCap']
        rows = df[df['item_id'].isin(keys)] if 'item_id' in df.columns else df.head(0)
        result["ratio_filtered"] = rows.to_dict(orient='records')
    except Exception as e:
        result["ratio_filtered_error"] = str(e)

    return result
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
