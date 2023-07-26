// Function to show/hide the spinner
function toggleSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    const linkButton = document.getElementById('linkButton');

    if (show) {
        spinner.style.display = 'block';
        linkButton.disabled = true;
    } else {
        spinner.style.display = 'none';
        linkButton.disabled = false;
    }
}

// Function to make the API call and set the link in the anchor tag
function getApiDataAndSetLink() {
    toggleSpinner(true); // Show the spinner

    fetch('http://127.0.0.1:8000/getUrl/') // Replace with your API endpoint URL
        .then(response => response.json())
        .then(data => {
            toggleSpinner(false); // Hide the spinner

            const linkButton = document.getElementById('linkButton');

            // Create a new anchor element
            const linkElement = document.createElement('a');
            linkElement.href = data;
            linkElement.target = '_blank';
            linkElement.innerText = 'Open Sheet';

            // Clear the button's content and append the anchor element
            linkButton.innerHTML = '';
            linkButton.appendChild(linkElement);
        })
        .catch(error => {
            console.error('Error:', error);
            toggleSpinner(false); // Hide the spinner in case of an error
        });
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', getApiDataAndSetLink);