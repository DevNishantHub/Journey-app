// Main application JavaScript - can be used for future interactivity
document.addEventListener("DOMContentLoaded", function() {
    console.log("Journey app main.js loaded.");

    // Example: Fetch today's tasks and log them (can be displayed on page later)
    fetch("/api/today")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error fetching today's tasks:", data.error);
            } else {
                console.log("Today's tasks:", data);
                // You could inject this into the page if needed
            }
        })
        .catch(error => {
            console.error("Failed to fetch /api/today:", error);
        });
});

