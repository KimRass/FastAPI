from fastapi import FastAPI, HTTPException

app = FastAPI()

# GET 메서드로 요청을 처리하는 핸들러
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# POST 메서드로 요청을 처리하는 핸들러
@app.post("/items/")
async def create_item(item_name: str):
    return {"item_name": item_name}

# PUT 메서드로 요청을 처리하는 핸들러
@app.put("/items/{item_id}")
async def update_item(item_id: int, new_item_name: str):
    return {"item_id": item_id, "new_item_name": new_item_name}

# DELETE 메서드로 요청을 처리하는 핸들러
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id == 1:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
