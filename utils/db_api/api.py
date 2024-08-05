import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000/api/v1"
USERNAME = "davlatbek"
PASSWORD = "d08980476"

def create_user(user_id, name, age, phonenumber, role):
    url = f"{BASE_URL}/users/"
    age = int(age)
    phonenumber = str(phonenumber)
    role = role.lower()

    try:
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status() 
        data = response.json()    
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    user_exist = any(user["id"] == str(user_id) for user in data)

    if not user_exist:
        try:
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"id": user_id, "name": name, "age": age, "phone_number": phonenumber, "role": role}
            )
            post_response.raise_for_status() 
            print("Foydalanuchi yaratildi.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            if post_response:
                print(f"Response content: {post_response.text}")  # Print response content for debugging
    else:
        print("Foydalnuvchi mavjud.")

def create_question(text):
    url = f"{BASE_URL}/applicant-questions/"

    try:
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the question already exists
    question_exists = any(question["text"] == text for question in data)

    if not question_exists:
        try:
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"text": text}
            )
            post_response.raise_for_status()
            print("Question created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
    else:
        print("Question already exists.")

def create_option(question_id, text):
    url = f"{BASE_URL}/applicant-options/"

    try:
        # Fetch existing options to check if the option already exists
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the option already exists for the given question
    option_exists = any(
        option["text"] == text and option["question"]["id"] == question_id
        for option in data
    )

    if not option_exists:
        try:
            # Post new option with nested dictionary for question
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"question": {"id": question_id}, "text": text}
            )
            post_response.raise_for_status()
            print("Option created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print(f"Response content: {post_response.text}")
    else:
        print("Option already exists for the given question.")

def create_applicant(user_id, option_id):
    payload = {
        'id': user_id,
        'selected_option': option_id
    }
    response = requests.post(f"{BASE_URL}/applicants/", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code != 200:
        print(f"Error creating applicant: {response.status_code} - {response.text}")

def create_student(user_id, option_id):
    payload = {
        'id': user_id,
        'selected_option': option_id
    }
    response = requests.post(f"{BASE_URL}/students/", json=payload, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code != 200:
        print(f"Error creating student: {response.status_code} - {response.text}")

def create_question_student(text):
    url = f"{BASE_URL}/student-questions/"

    try:
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the question already exists
    question_exists = any(question["text"] == text for question in data)

    if not question_exists:
        try:
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"text": text}
            )
            post_response.raise_for_status()
            print("Question created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
    else:
        print("Question already exists.")

def create_option_student(question_id, text):
    url = f"{BASE_URL}/student-options/"

    try:
        # Fetch existing options to check if the option already exists
        response = requests.get(url=url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")
        return

    # Check if the option already exists for the given question
    option_exists = any(
        option["text"] == text and option["question"]["id"] == question_id
        for option in data
    )

    if not option_exists:
        try:
            # Post new option with nested dictionary for question
            post_response = requests.post(
                url=url,
                auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json={"question": {"id": question_id}, "text": text}
            )
            post_response.raise_for_status()
            print("Option created successfully.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            print(f"Response content: {post_response.text}")
    else:
        print("Option already exists for the given question.")

def fetch_questions(role):
    url = f"{BASE_URL}/student-questions/" if role == "student" else f"{BASE_URL}/applicant-questions/"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching questions: {response.text}")
        return []

def fetch_options(role):
    url = f"{BASE_URL}/student-options/" if role == "student" else f"{BASE_URL}/applicant-options/"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching options: {response.text}")
        return []


# import requests
# from requests.auth import HTTPBasicAuth

# class APIClient:
#     def __init__(self, base_url, username, password):
#         self.base_url = base_url
#         self.auth = HTTPBasicAuth(username, password)

#     def _make_request(self, method, endpoint, json_data=None):
#         url = f"{self.base_url}/{endpoint}"
#         try:
#             if method == "GET":
#                 response = requests.get(url=url, auth=self.auth)
#             elif method == "POST":
#                 response = requests.post(url=url, auth=self.auth, json=json_data)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as req_err:
#             print(f"Request error occurred: {req_err}")
#         except ValueError as json_err:
#             print(f"JSON decoding failed: {json_err}")

#     def _check_existence(self, endpoint, key, value):
#         data = self._make_request("GET", endpoint)
#         return any(item[key] == value for item in data) if data else False

#     def _create_resource(self, endpoint, json_data, key, value):
#         if not self._check_existence(endpoint, key, value):
#             response = self._make_request("POST", endpoint, json_data=json_data)
#             if response:
#                 print(f"{endpoint.split('/')[0].capitalize()} created successfully.")
#         else:
#             print(f"{endpoint.split('/')[0].capitalize()} already exists.")

#     def create_user(user_id, name, age, phone_number, role):
#         url = "http://127.0.0.1:8000/api/v1/users/"
#         json_data = {
#             "id": user_id,  # Ensure the key matches what the API expects
#             "name": name,
#             "age": age,
#             "phone_number": phone_number,
#             "role": role
#         }
        
#         print(f"Sending data: {json_data}")
        
#         try:
#             response = requests.post(url, auth=HTTPBasicAuth("davlatbek", "d08980476"), json=json_data)
#             print(f"Response Status Code: {response.status_code}")
#             print(f"Response Content: {response.text}")
#             response.raise_for_status()
#             print("User created successfully.")
#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred: {http_err}")
#             print(f"Response content: {response.text}")
#         except requests.exceptions.RequestException as req_err:
#             print(f"Request error occurred: {req_err}")



#     def create_question(self, text):
#         endpoint = "applicant-questions/"
#         json_data = {"text": text}
#         self._create_resource(endpoint, json_data, "text", text)

#     def create_option(self, question_id, text):
#         endpoint = "applicant-options/"
#         json_data = {"question": {"id": question_id}, "text": text}
#         self._create_resource(endpoint, json_data, "text", text)

#     def create_applicant(self, applicant_id, option_id):
#         endpoint = "applicants/"
#         json_data = {"id": applicant_id, "selected_option": option_id}
#         self._create_resource(endpoint, json_data, "id", applicant_id)

#     def create_student(self, student_id, option_id):
#         endpoint = "students/"
#         json_data = {"id": student_id, "selected_option": option_id}
#         self._create_resource(endpoint, json_data, "id", student_id)

# # Example usage:
# # client = APIClient(BASE_URL, USERNAME, PASSWORD)
# # client.create_user(user_id="1", name="John Doe", age=30, phonenumber="1234567890", role="admin")
# # client.create_question(text="What is your favorite color?")
# # client.create_option(question_id="1", text="Blue")
# # client.create_applicant(applicant_id="1", option_id="1")
# # client.create_student(student_id="1", option_id="1")
