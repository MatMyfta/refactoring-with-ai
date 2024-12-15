class UserManager {
    /**
     * Manages user accounts and related operations.
     */
    constructor() {
      this.users = [];
    }
  
    addUser(name, age, role = "user") {
      /**
       * Adds a new user to the system.
       */
      if (!name || typeof name !== "string") {
        throw new Error("Name must be a non-empty string.");
      }
      if (age < 0) {
        throw new Error("Age must be a positive number.");
      }
      this.users.push({ name, age, role });
      console.log(`User ${name} added.`); 
    }
  
    removeUser(name) {
      /**
       * Removes a user by their name.
       */
      const userIndex = this.users.findIndex((user) => user.name === name);
      if (userIndex !== -1) {
        this.users.splice(userIndex, 1);
        console.log(`User ${name} removed.`);
      } else {
        // @TODO: Implement error handling for missing users.
        console.log(`User ${name} not found.`); 
      }
    }
  
    sendWelcomeEmail(email) {
      /**
       * Sends a welcome email to the given address.
       */
      if (!email.includes("@")) {
        // @REFACTOR: Use a more robust email validation.
        throw new Error("Invalid email address."); 
      }
      console.log(`Welcome email sent to ${email}!`); // Simulate sending email
    }
  
    listUsers() {
      /**
       * Lists all users.
       */
      console.log("Users in the system:");
      this.users.forEach((user) => {
        console.log(`- ${user.name} (Age: ${user.age}, Role: ${user.role})`);
      });
    }
  }