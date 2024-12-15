Here's the refactored code after fixing the issues annotated by the TODO and REFACTOR tags:

```java
import java.util.ArrayList;
import java.util.List;
import java.nio.file.*;
import java.io.*;

// Importing library for email validation.
import org.apache.commons.validator.routines.EmailValidator;

public class UserManager {
    
    // Change ArrayList to a DB for persistence, you might need to adjust it to your chosen DB.
    private DB<User> users = new DB<>("usersDB");

    public UserManager() {
    }

    public void addUser(String name, int age, String role) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Name must be a non-empty string.");
        }
        if (age < 0) {
            throw new IllegalArgumentException("Age must be a positive number.");
        }
        if (role == null || role.isEmpty()) {
            role = "user"; // Default role.
        }
        users.add(new User(name, age, role));
        System.out.println("User " + name + " added."); 
    }

    public void removeUser(String name) {
        User removedUser = users.remove(name);

        if (removedUser != null) { 
            System.out.println("User " + name + " removed."); 
        } else {
            throw new IllegalArgumentException("User not found.");
        }
    }

    public void sendWelcomeEmail(String email) {
        if (!EmailValidator.getInstance().isValid(email)) { 
            throw new IllegalArgumentException("Invalid email address."); 
        }
        System.out.println("Welcome email sent to " + email + "!"); // Simulate email sending
    }

    public void listUsers() {
        System.out.println("Users in the system:");
        for (User user : users) {
            System.out.println("- " + user.getName() + " (Age: " + user.getAge() + ", Role: " + user.getRole() + ")");
        }
    }

    public void generateUserReport() throws IOException {
        StringBuilder report = new StringBuilder("User Report\n");
        report.append("Generated on: ").append(java.time.LocalDateTime.now()).append("\n\n");
        for (User user : users) {
            report.append("Name: ").append(user.getName())
                  .append(", Age: ").append(user.getAge())
                  .append(", Role: ").append(user.getRole()).append("\n");
        }

        Path path = Paths.get("UserReport.txt");
        Files.write(path, report.toString().getBytes());
    }

    // Main method stays the same, depends on how you implement the DB in the DB class.
    public static void main(String[] args) {
        UserManager manager = new UserManager();
        manager.addUser("Alice", 30, "admin");
        manager.addUser("Bob", 25, "user");
        manager.listUsers();

        try{
            manager.generateUserReport();
        } catch(IOException e){
            e.printStackTrace();
        }
        manager.sendWelcomeEmail("test@example.com");
    }
}
```
Please note, this assumes you have the Apache Commons Validator library added as a dependency in your project and you will need to properly implement a database connection to replace the ArrayList, the "DB" class is there just for the example purpose.