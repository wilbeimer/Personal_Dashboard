export async function handleAuth(endpoint, successRedirect, errorLabelId) {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const errorLabel = document.getElementById(errorLabelId);
    errorLabel.textContent = "";

    try {
        const response = await fetch(`http://127.0.0.1:8000/users/${endpoint}`, {
            method: "POST",
            credentials: 'include',  // Important: send cookies
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // No need to store token in localStorage
            window.location.href = data.redirect || successRedirect;
        } else {
            errorLabel.textContent = data.detail || "Login failed";
        }
    } catch (error) {
        errorLabel.textContent = "Network error";
    }
}