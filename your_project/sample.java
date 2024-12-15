import java.util.ArrayList;
import java.util.List;

public class UserManager {
    private List<User> users;

    public UserManager() {
        users = new ArrayList<>(); // @TODO: Replace in-memory list with a database or persistent storage.
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
        User toRemove = null;
        for (User user : users) {
            if (user.getName().equals(name)) {
                toRemove = user;
                break;
            }
        }
        if (toRemove != null) {
            users.remove(toRemove);
            System.out.println("User " + name + " removed.");
        } else {
            // @TODO: Add proper error handling for missing users.
            System.out.println("User " + name + " not found."); 
        }
    }

    public void sendWelcomeEmail(String email) {
        if (!email.contains("@")) {
            // @REFACTOR: Use a proper email validation library.
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

    public void generateUserReport() {
        StringBuilder report = new StringBuilder("User Report\n");
        report.append("Generated on: ").append(java.time.LocalDateTime.now()).append("\n\n");
        for (User user : users) {
            report.append("Name: ").append(user.getName())
                  .append(", Age: ").append(user.getAge())
                  .append(", Role: ").append(user.getRole()).append("\n");
        }
        // @TODO: Save the report to a file instead of printing it to the console.
        System.out.println(report.toString()); 
    }

    public static void main(String[] args) {
        UserManager manager = new UserManager();
        manager.addUser("Alice", 30, "admin");
        manager.addUser("Bob", 25, "user");
        manager.listUsers();

        manager.generateUserReport();
        manager.sendWelcomeEmail("test@example.com");
    }
}