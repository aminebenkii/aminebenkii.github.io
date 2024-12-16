<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize inputs
    $name = htmlspecialchars(strip_tags($_POST['name']));
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
    $subject = htmlspecialchars(strip_tags($_POST['subject']));
    $message = htmlspecialchars(strip_tags($_POST['message']));

    // Validate email
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("Invalid email address.");
    }

    // Setup email
    $to = "aminebenkirane19@gmail.com";
    $headers = "From: $email\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    $email_body = "Name: $name\n";
    $email_body .= "Email: $email\n\n";
    $email_body .= "Subject: $subject\n\n";
    $email_body .= "Message:\n$message\n";

    // Attempt to send email
    if (mail($to, $subject, $email_body, $headers)) {
        // Redirect to a Thank You page
        header("Location: thank_you.html");
        exit();
    } else {
        error_log("Mail failed to send. Email data: " . print_r($_POST, true));
        echo "Failed to send your message. Please try again later.";
    }
} else {
    // For non-POST requests
    echo "Invalid request method.";
}
?>
