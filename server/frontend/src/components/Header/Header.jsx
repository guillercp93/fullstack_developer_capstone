import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = ({ home_page_items }) => {
  const logout = async (e) => {
    e.preventDefault();
    let logout_url = window.location.origin + "/djangoapp/logout";
    const res = await fetch(logout_url, {
      method: "GET",
    });

    const json = await res.json();
    if (json) {
      let username = sessionStorage.getItem('username');
      sessionStorage.removeItem('username');
      window.location.href = window.location.origin;
      window.location.reload();
      alert("Logging out " + username + "...")
    }
    else {
      alert("The user could not be logged out.")
    }
  };

  //Gets the username in the current session
  let curr_user = sessionStorage.getItem('username')

  //If the user is logged in, show the username and logout option on home page
  if (curr_user !== null && curr_user !== "") {
    home_page_items = <div className="input_panel">
      <text className='username'>{sessionStorage.getItem("username")}</text>
      <a className="nav_item" href="/djangoapp/logout" onClick={logout}>Logout</a>
    </div>
  }
  return (
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm sticky-top">
        <div class="container-fluid">
          <a class="navbar-brand d-flex align-items-center" href="/">
            <i class="fas fa-car me-2"></i>
            <span class="fw-bold">Best Cars Dealership</span>
          </a>
          <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarText">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <a class="nav-link px-3" href="/" aria-current="page"><i class="fas fa-home me-1"></i>Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link px-3" href="/about"><i class="fas fa-info-circle me-1"></i>About Us</a>
              </li>
              <li class="nav-item">
                <a class="nav-link px-3" href="/contact"><i class="fas fa-envelope me-1"></i>Contact</a>
              </li>
            </ul>
            <span class="navbar-text">
              <div class="loginlink" id="loginlogout">
                {home_page_items}
              </div>
            </span>
          </div>
        </div>
      </nav>
    </div>
  )
}

export default Header
