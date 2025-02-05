from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import re

app = Flask(__name__)
db = TinyDB("db.json")

# Типы данных
FIELD_TYPES = {
    "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    "phone": r"^\+7 \d{3} \d{3} \d{2} \d{2}$",
    "date": r"^(?:\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})$"
}

def validate_field(value):
    for field_type, pattern in FIELD_TYPES.items():
        if re.match(pattern, value):
            return field_type
    return "text"

@app.route("/get_form", methods=["POST"])
def get_form():
    form_data = request.form.to_dict()
    templates = db.all()

    for template in templates:
        match = all(
            field_name in form_data and validate_field(form_data[field_name]) == field_type
            for field_name, field_type in template.items() if field_name != "name"
        )
        if match:
            return jsonify({"form_template": template["name"]})

    # Если подходящий шаблон не найден
    field_types = {k: validate_field(v) for k, v in form_data.items()}
    return jsonify(field_types)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
