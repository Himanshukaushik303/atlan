function submitForm(api, apiMethod) {
    // Get form data
    const formData = new FormData(document.querySelector('.myForm'));
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    // Make API call to Django view using fetch
    var url = 'http://127.0.0.1:8000/'.concat(api)
    fetch(url, {
        method: apiMethod,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Set CSRF token
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const responseMessage = document.getElementById('responseMessage');
        responseMessage.innerText = data;
        if (api=="addResponse/") {
            clearFormFields();
        }

    })
    .catch(error => {
        console.error('Error:', error);
    });
    function clearFormFields() {
        // Clear form fields after successful submission
        const form = document.querySelector('.myForm');
        form.reset();
  }
};

// Function to get CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function validate(val) {
v1 = document.getElementById("fname");
v2 = document.getElementById("lname");
v3 = document.getElementById("email");
v4 = document.getElementById("mob");
v5 = document.getElementById("income");
v6 = document.getElementById("saving");

flag1 = true;
flag2 = true;
flag3 = true;
flag4 = true;
flag5 = true;
flag6 = true;

if(val>=1 || val==0) {
if(v1.value == "") {
    v1.style.borderColor = "red";
    flag1 = false;
}
else {
    v1.style.borderColor = "green";
    flag1 = true;
}
}

if(val>=2 || val==0) {
if(v2.value == "") {
    v2.style.borderColor = "red";
    flag2 = false;
}
else {
    v2.style.borderColor = "green";
    flag2 = true;
}
}
if(val>=3 || val==0) {
if(v3.value == "") {
    v3.style.borderColor = "red";
    flag3 = false;
}
else {
    v3.style.borderColor = "green";
    flag3 = true;
}
}
if(val>=4 || val==0) {
if(v4.value == "") {
    v4.style.borderColor = "red";
    flag4 = false;
}
else {
    v4.style.borderColor = "green";
    flag4 = true;
}
}
if(val>=5 || val==0) {
if(v5.value == "") {
    v5.style.borderColor = "red";
    flag5 = false;
}
else {
    v5.style.borderColor = "green";
    flag5 = true;
}
}
if(val>=6 || val==0) {
if(v6.value == "") {
    v6.style.borderColor = "red";
    flag6 = false;
}
else {
    v6.style.borderColor = "green";
    flag6 = true;
}
}

flag = flag1 && flag2 && flag3 && flag4 && flag5 && flag6;

return flag;
}