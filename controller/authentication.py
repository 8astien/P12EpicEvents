import jwt
import bcrypt
from controller.management import ManagementController
from controller.support import SupportController
from controller.sales import SalesController
from view.authentification import AuthentificationMenu, AuthenticationViews
from view.principal import MainView
from model.authentication import create_jwt, decode_token
from model.user import User
from sentry_config import initialize_sentry

# Initialize Sentry for error handling
initialize_sentry()


class AuthenticationController(AuthentificationMenu):
    def __init__(self):
        # Display the main authentication menu
        AuthentificationMenu.main_authentification_menu()
        # Retrieve user choice
        choice = MainView.choice()
        # Handle user authentication choice
        handle_authentication_choice(choice)


def handle_authentication_choice(choice):
    while True:
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 3:
                if choice == 1:
                    # Create a JWT token for the user
                    name_lastname, password = AuthenticationViews.token_creation()
                    user = User.find_all()
                    user = next(
                        (u for u in user if u.name_lastname == name_lastname
                         and bcrypt.checkpw(password.encode(), u.password.encode())),
                        None
                    )
                    if user:
                        # Encode JWT and display it to the user
                        encoded_jwt = create_jwt(user)
                        AuthenticationViews.token_print(encoded_jwt)
                    else:
                        # Display authentication error
                        AuthenticationViews.error_authentication()
                elif choice == 2:
                    # Verify and decode a JWT token provided by the user
                    token = AuthenticationViews.token_cheking()
                    user = User.find_all()
                    user = next((u for u in user if u.token == token), None)
                    if user:
                        try:
                            # Decode JWT token and check its expiration
                            decoded_jwt = decode_token(token, user)
                            if decoded_jwt:
                                MainView.message_connection_token()
                                # Redirect user based on department
                                if user.department == 'COM':
                                    SalesController(user)
                                elif user.department == 'GES':
                                    ManagementController(user)
                                elif user.department == 'SUP':
                                    SupportController(user)
                                else:
                                    MainView.message_no_department()
                            else:
                                # Display error message if token is invalid
                                AuthenticationViews.invalid_token()
                        except jwt.ExpiredSignatureError:
                            # Display token expiration message
                            AuthenticationViews.expiration_date_token()
                        except jwt.InvalidTokenError:
                            # Display error message if token is invalid
                            AuthenticationViews.invalid_token()
                    else:
                        # Display error message if token is invalid
                        AuthenticationViews.invalid_token()
                elif choice == 3:
                    # Exit the program
                    exit()
            else:
                # Ask user to enter a number between 1 and 3
                print("Veuillez saisir un nombre entre 1 et 3!")
        else:
            # Display message if user did not enter a whole number
            MainView.message_no_whole_number()

        # Restart the main controller to display the authentication menu again
        AuthenticationController()
        # Get new user choice
        choice = MainView.choice()
