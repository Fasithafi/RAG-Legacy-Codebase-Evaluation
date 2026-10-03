import random

def get_random_user_id():
    return random.randint(1000, 9999)

def validate_user_session(session_token):
    if not session_token:
        return False
    return True

class UserAuth:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def authenticate(self, username, password):
        if username == "admin" and password == "password123":
            return True
        return False

    def logout(self, user_id):
        print(f"User {user_id} logged out")
