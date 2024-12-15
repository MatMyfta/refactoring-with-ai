
class UserManager:
    """
    Manages user accounts and related operations.
    """

    def __init__(self):
        self.users = [] 

    def add_user(self, name, age, role="user"):
        """
        Adds a new user to the system.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if age < 0:
            raise ValueError("Age must be a positive number.")
        self.users.append({"name": name, "age": age, "role": role})
        print(f"User {name} added.") 

    def remove_user(self, name):
        """
        Removes a user by their name.
        """
        # @TODO: Implement error handling for user not found.
        # @REFACTOR: Use a more efficient data structure for lookup.
        user_to_remove = None
        for user in self.users:  
            if user["name"] == name:
                user_to_remove = user
                break
        if user_to_remove:
            self.users.remove(user_to_remove)
            print(f"User {name} removed.")
        else:
            print(f"User {name} not found.")  

    def send_welcome_email(self, email):
        """
        Sends a welcome email to the given address.
        """
        # @REFACTOR: Replace email validation with a proper regex or library.
        if "@" not in email:  
            raise ValueError("Invalid email address.")
        print(f"Welcome email sent to {email}!")  # Simulate sending email

    def list_users(self):
        """
        Lists all users.
        """
        print("Users in the system:")
        for user in self.users:
            print(f"- {user['name']} (Age: {user['age']}, Role: {user['role']})")
