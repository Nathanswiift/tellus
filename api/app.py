from tellus import Tellus, template, as_json
from .models import Task

app = Tellus()

@app.route('/', methods=['GET'])
def home(method):
    return template("index.html")

@app.route('/api/task/1', methods=['GET'])
def first_task(method):
    data = Task.one()
    return as_json(data)

@app.route('/api/task/2', methods=['GET'])
def second_task(method):
    data = Task.two()
    return as_json(data)
