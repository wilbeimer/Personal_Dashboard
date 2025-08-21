if (document.getElementById("loginBtn")){
   document.getElementById("loginBtn").addEventListener("click", async () => {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const response = await fetch("http://127.0.0.1:8000/users/login", {
         method: "POST",
         headers: {
             "Content-Type": "application/json"
         },
         body: JSON.stringify({ email, password })
      });
      if (response.ok) {
         const data = await response.json();
         // Save the JWT token in localStorage
         localStorage.setItem("access_token", data["access token"]);
         
         // Redirect to dashboard
         window.location.href = "/home";
      } else {
         const err = await response.json();
         alert(err.detail);
      }
   });
}

if (document.getElementById("registerBtn")){
   document.getElementById("registerBtn").addEventListener("click", async () => {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const response = await fetch("http://127.0.0.1:8000/users/register", {
         method: "POST",
         headers: {
            "Content-Type": "application/json"
         },
         body: JSON.stringify({ email, password })
      });

      if (response.ok) {
         // Redirect to login page
         window.location.href = "/static/login.html";
       } else {
           const err = await response.json();
           alert(err.detail);
       }
   });
}
