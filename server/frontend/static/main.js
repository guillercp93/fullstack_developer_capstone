const logout = async (e) => {
  //Include the code for logout here.
  const logout_url = window.location.origin + "/djangoapp/logout";
  const res = await fetch(logout_url, { method: "GET" });
  const json = await res.json();
  if (json) {
    let curr_user = sessionStorage.getItem("username");
    sessionStorage.removeItem("username");
    window.location.href = window.location.origin;
    window.location.reload();
    alert("Logging out " + curr_user + "...")
  }
  else {
    alert("The user could not be logged out.")
  }
};

const checkSession = () => {
  let curr_user = sessionStorage.getItem("username");

  if (curr_user && curr_user !== "") {
    document.getElementById("loginlogout").innerHTML =
      '<span class="nav-link"><i class="fas fa-user me-1"></i>' + curr_user + '</span>' +
      '<a class="nav-link" onclick="logout()" href="/"><i class="fas fa-sign-out-alt me-1"></i>Logout</a>'
  } else {
    document.getElementById("loginlogout").innerHTML =
      '<a class="nav-link" href="/login"><i class="fas fa-sign-in-alt me-1"></i>Login</a>' +
      '<a class="nav-link" href="/register"><i class="fas fa-user-plus me-1"></i>Register</a>'
  }
}