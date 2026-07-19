"""A minimal Task API used to demonstrate an automated CI/CD pipeline.

Endpoints:
    GET    /health           -> liveness check used by CI/CD and orchestrators
    GET    /tasks             -> list all tasks
    POST   /tasks             -> create a task ({"title": "..."})
    PATCH  /tasks/<id>         -> update a task's "done" status
    DELETE /tasks/<id>         -> delete a task
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(force=True, silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(force=True, silent=True) or {}
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = data.get("done", task["done"])
            return jsonify(task), 200
    return jsonify({"error": "task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        return jsonify({"error": "task not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
