from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
from dbcreds import production_mode
from validhelpers import check_data

app = Flask(__name__)

@app.get('/hello')
def get_hello():
    return "Hello World"

@app.get('/api/candies')
def get_all_candies():
    keys = ["name", "description", "price"]
    result = run_statement("CALL get_all_candies")
    snacks = []
    if (type(result) == list):
        for candy in result:
            snacks.append(dict(zip(keys, candy)))
        return make_response(jsonify(snacks), 200)
    else:
        return make_response(jsonify(result), 500)


@app.get('/api/candies')
def get_candies():
    keys = ["name", "description", "price"]
    id_input = request.args.get('idInput') 
    result = run_statement("CALL read_candy(?)", [id_input])
    shelfs = []
    if (type(result) == list):
        for candy in result:
            shelfs.append(dict(zip(keys, candy)))
        return make_response(jsonify(shelfs), 200)
    else:
        return make_response(jsonify(result), 500)


@app.post('/api/candies')
def insert_candies():
    required_data = ['name', 'description', 'price']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    description = request.json.get('description')
    price = request.json.get('price')
    result = run_statement("CALL insert_candy(?,?,?)", [name, description, price])
    if result == None:
        return "New candy recorded in DB!"
    else:
        return "Sorry, something went wrong"


@app.patch('/api/candies')
def patch_candies():
    required_data = ['id', 'price']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    id = request.json.get('id')
    price = request.json.get('price')
    result = run_statement("CALL edit_candy(?,?)", [id, price])
    if result == None:
        return "Candy price updated successfully"
    else:
        return "Sorry, something went wrong"


@app.delete('/api/candies')
def delete_candies():
    check_result = check_data(request.json, ['id'])
    if check_result != None:
        return check_result
    id = request.json.get('id')
    result = run_statement("CALL delete_candy(?)", [id])
    if result == None:
        return "Successfully deleted Candy {}".format(id)
    else:
        return "Candy {} does not exist".format(id)
    

if (production_mode == True):
    print("Running server in production mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in testing mode")
    app.run(debug=True)

