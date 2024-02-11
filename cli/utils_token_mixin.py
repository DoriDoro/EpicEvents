import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command

from cli.utils_messages import (
    create_invalid_error_message,
    create_success_message,
)

UserModel = get_user_model()


SECRET_KEY = "a5e8d8385c959c80926c13c986ebef2ecb"


class JWTTokenMixin:
    help = (
        "Mixin to generate a JWT token, validate the token, get the corresponding user "
        "and handle the login if no token. The token will be saved in a file: token.txt"
    )
    token = None
    payload = None
    user = None

    # generate token and validate token
    def generate_token(self, user_id, email, expires_delta=datetime.timedelta(hours=1)):
        """Generate a JWT token."""
        now = datetime.datetime.utcnow()
        payload = {
            "user_id": user_id,
            "email": email,
            "iat": now,
            "exp": now + expires_delta,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        with open(settings.JWT_PATH, "w") as file:
            file.write(token)

        return token

    def verify_token(self):
        """Verify the JWT token."""
        try:
            self.payload = jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            self.login()
            return
        except jwt.InvalidTokenError:
            self.login()
            return

    def get_user(self):
        """get corresponding user to the token"""
        self.verify_token()
        if self.payload is None:
            return
        self.user = UserModel.objects.filter(id=self.payload.get("user_id")).first()

    def login(self):
        data = self.get_login_data()
        self.make_login_changes(data)

    def logout(self):
        self.payload = None
        self.token = None
        with open(settings.JWT_PATH, "w") as file:
            file.write("")

    def get_login_data(self):
        self.stdout.write()
        self.display_input_title("Enter email and password to login:")
        return {
            "email": self.email_input("Email address"),
            "password": self.password_input("Password"),
        }

    def make_login_changes(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user is not None:
            self.token = self.generate_token(user.pk, user.email)

            create_success_message("Employee", "logged in")
        else:
            create_invalid_error_message("email or password")
            self.login()

    def handle(self, *args, **options):
        # self.logout()
        with open(settings.JWT_PATH, "r") as file:
            self.token = file.read()
            self.get_user()
