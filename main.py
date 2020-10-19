#API services documentation on http://127.0.0.1:8000/docs#/ or http://127.0.0.1:8000/redoc
#The default documentation says the function name in a sentence
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    #Python types (str, int, float, bool, list, datetime, etc)
    name: str
    price: float
    is_offer: bool = None #bool values can be sent as True, true,1, on and yes otherwiese it is false

#We create an enum to limit the possible values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
def read_root():
    return {"Hello": "World"}

#http://127.0.0.1:8000/items/5?q=somequery
#We can also create async functions to improve the performance
#We are saying that item_id is requiered and q is optional
#q is our request param that in this case is optional
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    #We say that convert the object into a dictionary
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#Here we have body+path+request params
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#http://127.0.0.1:8000/name/?start_index=0&count=5
# We are getting two parameters in the get request
#It also has 2 default values
@app.get("/name/")
async def read_item(start_index: int = 0, count: int = 10):
    return fake_items_db[start_index : start_index + count]

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

#http://127.0.0.1:8000/users/1/items/abc?short=true
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


#run with uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
