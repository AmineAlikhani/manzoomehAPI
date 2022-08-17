from bclib import edge
import json

options = {
    "server": "localhost:8080",
    "router": {
        "restful": ["/api"],
        "web": ["/web"],
    }
}

app = edge.from_options(options)

# To generate data
@app.cache()
def generate_data() -> list:
    import string
    import random    
    data_list = list()
    for i in range(10):
        data_list.append({
        "id": i,
        "name": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "price": random.randrange(1000, 10000, 100),
        "inventory": random.randrange(0, 150, 1),
        })
    return data_list
data_base = generate_data()

# Samples can be used to add or edit new data
# This can happen if used as a LIST in the URL
sample_data = [{"id":11,"name":"One Hundred Years of Solitude","price":5000,"inventory":100}]
sample_multiple_data = [{"id":12,"name":"The Brothers Karamazov","price":6000,"inventory":2},{"id":13,"name":"The Plague","price":5050,"inventory":3}]

# Edit request, uses original product id/new information 
@app.restful_action(
    app.url(":api/edit/:id/:sample"))
def edit_api(context: edge.RESTfulContext):  
    id = int(context.url_segments.id)  
    print(f"Admin sent a request to edit item {id}")
    information = context.url_segments.sample
    information = json.loads(information)
    for item in information:
        new_information = {
            "id": int(item["id"]),
            "name": item["name"],
            "price": int(item["price"]),
            "inventory": int(item["inventory"]),
            }
    for item in data_base:
        if item["id"] == id:
            for product in data_base:
                if product["id"] == new_information["id"] and new_information["id"] != id:
                    return {"Error": "Duplicate id!"}
            data_base.remove(item)
            data_base.append(new_information)
            print(f"Product {id} changed to {new_information}")
            return {"message": f" Product: {id} changed to {new_information} successfully!"}
    return {"Error":f"Product {id} does not exist!"}

# Add new product request
@app.restful_action(
    app.url(":api/add/:sample"))
def add_data(context: edge.RESTfulContext):    
    information = context.url_segments.sample
    information = json.loads(information)
    print(f"Admin requested to add {information} to data base ")
    for item in information:
        new_product = {
            "id": int(item["id"]),
            "name": item["name"],
            "price": int(item["price"]),
            "inventory": int(item["inventory"]),
            }
        for product in data_base:
            if product["id"] == item["id"]:
                print("Error: Unable to add product. Id is already in use")
                return {"Error": f"product id: {item['id']} is already in use"}
        data_base.append(new_product)
    return {"message": f"{information} added successfully"}

# Delete product, filtered by id
@app.restful_action(
    app.url(":api/delete/:id"))
def delete_api(context: edge.RESTfulContext):
    print("Process deleting filtered by id")
    id = int(context.url_segments.id)
    print("Admin sent delete request!")
    for product in data_base:
        if product["id"] == id:
            print(f"{product['name']} is deleted")
            data_base.remove(product)
            return {"message":f"Product {id} deleted successfully"}
    return {"Error":f"Product {id} does not exist!"}
   
# GET data base information
@app.restful_action(
    app.url(":api/"))
def get_api(context: edge.RESTfulContext):
    print("Admin sent request to view data base")
    return data_base

# GET data base information based on product id
@app.restful_action(
    app.url(":api/:id"))
def get_filtered(context: edge.RESTfulContext):
    id = int(context.url_segments.id)
    print(f"Admin sent request to view item {id} from data base")
    for product in data_base:
        if product["id"] == id:
            return product
    return {"Error":f"Product {id} does not exist!"}

app.listening()     