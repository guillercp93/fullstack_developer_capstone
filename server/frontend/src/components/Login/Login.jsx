import React, { useState } from 'react';

import "./Login.css";
import Header from '../Header/Header';

const Login = ({ onClose }) => {

  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true)

  let login_url = window.location.origin + "/djangoapp/login";

  const login = async (e) => {
    e.preventDefault();

    const res = await fetch(login_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "userName": userName,
        "password": password
      }),
    });

    const json = await res.json();
    if (json.status != null && json.status === "Authenticated") {
      sessionStorage.setItem('username', json.userName);
      setOpen(false);
    }
    else {
      alert("The user could not be authenticated.")
    }
  };

  if (!open) {
    window.location.href = "/";
  };


  return (
    <div>
      <Header home_page_items={<div></div>}/>
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <form className="card p-4 shadow-sm" style={{ maxWidth: "400px", margin: "2rem auto" }} onSubmit={login}>
            <h3 className="text-center mb-4">Login</h3>
            <div className="mb-3">
              <label className="form-label">Username</label>
              <div className="input-group">
                <span className="input-group-text"><i className="fas fa-user"></i></span>
                <input type="text" name="username" placeholder="Enter username" className="form-control" onChange={(e) => setUserName(e.target.value)} />
              </div>
            </div>
            <div className="mb-3">
              <label className="form-label">Password</label>
              <div className="input-group">
                <span className="input-group-text"><i className="fas fa-lock"></i></span>
                <input name="psw" type="password" placeholder="Enter password" className="form-control" onChange={(e) => setPassword(e.target.value)} />
              </div>
            </div>
            <div className="d-grid gap-2">
              <button type="submit" className="btn btn-primary">
                <i className="fas fa-sign-in-alt me-2"></i>Login
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setOpen(false)}>
                <i className="fas fa-times me-2"></i>Cancel
              </button>
            </div>
            <div className="text-center mt-3">
              <a href="/register" className="text-decoration-none">
                <i className="fas fa-user-plus me-1"></i>Register Now
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
