from flask import Flask, json, request

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/')
def index():
    return 'Index Page'

@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(companies)

@api.route('/companies', methods=['POST'])
def new_company():
    companies.append(request.get_json())
    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug = True)