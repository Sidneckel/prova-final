from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "acabado"}

@app.get("/square/{x}")
def square(x: int):
    return {"result": x * x}  # corrigido

@app.get("/double/{x}")
def double(x: int):
    return {"result": x * 2}
