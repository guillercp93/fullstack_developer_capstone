import React from 'react';
import "../assets/style.css";

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
    home_page_items = <>
      <text className="nav-link"><i className="fas fa-user me-1"></i>{curr_user}</text>
      <a className="nav-link" onClick={logout} href="/djangoapp/logout"><i className="fas fa-sign-out-alt me-1"></i>Logout</a>
    </>
  }
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm sticky-top">
        <div className="container-fluid">
          <a className="navbar-brand d-flex align-items-center" href="/">
            <i className="fas fa-car me-2"></i>
            <span className="fw-bold">Best Cars Dealership</span>
          </a>
          <button className="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarText">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="nav-link px-3" href="/" aria-current="page"><i className="fas fa-home me-1"></i>Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link px-3" href="/about"><i className="fas fa-info-circle me-1"></i>About Us</a>
              </li>
              <li className="nav-item">
                <a className="nav-link px-3" href="/contact"><i className="fas fa-envelope me-1"></i>Contact</a>
              </li>
            </ul>
            <div className="navbar-nav" id="loginlogout">
              {home_page_items}
            </div>
          </div>
        </div>
      </nav>
    </div>
  )
}

export default Header
