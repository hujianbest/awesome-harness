from flask import Flask

app = Flask(__name__)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/orders/<order_id>/rebuild")
def rebuild(order_id: str):
    return {"accepted": True, "order_id": order_id}
