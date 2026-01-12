document.addEventListener("DOMContentLoaded", function () {
    const summarizeButton = document.querySelector(".but"); 
    const textArea = document.getElementById("input-text"); 
    const loadingBar = document.getElementById("loading-bar"); 

    summarizeButton.addEventListener("click", function () {
        if (textArea.value.trim() === "") {
            alert("Please enter some text before summarizing!");
            return;
        }
        summarizeButton.disabled = true;
        textArea.disabled = true;

        loadingBar.style.display = "block";

        fetch("/summary", {
            method: "POST",
            body: new URLSearchParams({ text: textArea.value }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response:", data); 
            if (data.redirect) {
                window.location.href = data.redirect; 
            } else {
                throw new Error("Invalid response from server");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Something went wrong. Please try again.");
            summarizeButton.disabled = false;
            textArea.disabled = false;
            loadingBar.style.display = "none";
        });
    });
});
