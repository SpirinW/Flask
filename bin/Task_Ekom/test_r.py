import requests

url = "http://127.0.0.1:5000/get_form"

test_data = [
    {
        "email": "test_mail@example.com",
        "phone_number": "+7 999 999 99 11",
        "birth_date": "2000-01-01",
    },
    {"user_email": "e@example.com", "order_date": "9.12.2024"},
    {"field1": "text123", "field2": "text1234"},
]

for data in test_data:
    response = requests.post(url, data=data)
    print(f"Input: {data}\nResponse: {response.json()}\n")
