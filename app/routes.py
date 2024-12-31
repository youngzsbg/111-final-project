from flask import (
    Flask,
    request as flask_req,
    render_template
)
import requests

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("home.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/tasks")
def list_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>")
def task_detail(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code ==200:
        single_task = response.json().get("task")
        return render_template("detail.html", task=single_task)
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )


@app.get("/tasks/new")
def get_new_form():
    return render_template("new.html")

@app.post("/tasks/new")
def create_task():
    task_data = flask_req.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", message="Task successfully created")
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )


@app.get("/tasks/edit/<int:pk>")
def get_edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("edit.html", task=single_task)
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )

@app.post("/tasks/edit/<int:pk>")
def edit_task(pk):
    task_data = flask_req.form
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", message="Task successfully edited")
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )

@app.get("/tasks/delete/<int:pk>")
def get_delete_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("delete.html", task=single_task)
    return (
        render_template("error.html", status=response.status_code),
        response.status_code
    )

@app.post("/tasks/delete/<int:pk>")
def delete_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("success.html", message="Task successfully deleted")
    return (
        render_template("error.html", status= response.status_code),
        response.status_code
    )