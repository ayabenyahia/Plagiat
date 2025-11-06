document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMsg = document.getElementById("error-msg");

  // Identifiants valides
  const validUsername = "admin";
  const validPassword = "1234";

  if (username === validUsername && password === validPassword) {
    localStorage.setItem("loggedIn", "true");
    window.location.href = "index.html";
  } else {
    errorMsg.textContent = "Nom d'utilisateur ou mot de passe incorrect.";
  }
});
