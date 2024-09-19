from fastapi import FastAPI

app = FastAPI()

@app.get("/")


async def root():
    return {"message":"hello main"}

@app.post("/")

async def post():
    return {"message": "hello from the post route"}

@app.put("/")
async def post():
    return {"message": "hello from the put route"}





