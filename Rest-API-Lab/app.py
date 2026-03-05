from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
students = []
current_id = 1


# Home Route
@app.route("/")
def home():
    return jsonify({
        "message": "Student REST API is running"
    })


# GET All Students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200


# GET Single Student
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404


# CREATE Student
@app.route("/students", methods=["POST"])
def create_student():
    global current_id

    data = request.get_json()

    if not data or not data.get("name") or not data.get("age") or not data.get("course"):
        return jsonify({"error": "Missing fields"}), 400

    new_student = {
        "id": current_id,
        "name": data["name"],
        "age": data["age"],
        "course": data["course"]
    }

    students.append(new_student)
    current_id += 1

    return jsonify(new_student), 201


# UPDATE Student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    for student in students:
        if student["id"] == id:
            student["name"] = data.get("name", student["name"])
            student["age"] = data.get("age", student["age"])
            student["course"] = data.get("course", student["course"])
            return jsonify(student), 200

    return jsonify({"error": "Student not found"}), 404


# DELETE Student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return jsonify({"message": "Student deleted successfully"}), 200

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)