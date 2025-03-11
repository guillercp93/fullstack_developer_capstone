import React, { useState } from 'react'
import './Register.css'
import Header from '../Header/Header';

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const gohome = () => {
    window.location.href = window.location.origin;
  }

  const register = async (e) => {
    e.preventDefault();
    const register_url = window.location.origin + "/djangoapp/register";
    const res = await fetch(register_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "userName": userName,
        "password": password,
        "email": email,
        "firstName": firstName,
        "lastName": lastName
      }),
    });
    const json = await res.json();
    if (json.status != null && json.status === "Registered") {
      sessionStorage.setItem('username', json.userName);
    } else if (json.error === "User already exists") {
      alert("A user with this username already registered.")
    } else {
      alert("The user could not be registered.")
    }
    gohome();
  };

  return (
    <div className="container-fluid">
      <Header home_page_items={<div></div>} />
      <div className="modalContainer">
        <form onSubmit={register} className="card p-4 shadow-sm needs-validation">
          <h3 className="text-center mb-4">Sign Up</h3>
          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><i className="fas fa-user"></i></span>
              <input type="text" name="username" placeholder="Username" className="form-control" onChange={(e) => setUserName(e.target.value)} />
            </div>
          </div>
          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><i className="fas fa-user"></i></span>
              <input type="text" name="first_name" placeholder="First Name" className="form-control" onChange={(e) => setFirstName(e.target.value)} />
            </div>
          </div>
          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><i className="fas fa-user"></i></span>
              <input type="text" name="last_name" placeholder="Last Name" className="form-control" onChange={(e) => setLastName(e.target.value)} />
            </div>
          </div>
          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><i className="fas fa-envelope"></i></span>
              <input type="email" name="email" placeholder="Email" className="form-control" onChange={(e) => setEmail(e.target.value)} />
            </div>
          </div>
          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><i className="fas fa-lock"></i></span>
              <input name="psw" type="password" placeholder="Password" className="form-control" onChange={(e) => setPassword(e.target.value)} />
            </div>
          </div>
          <div className="d-grid">
            <button type="submit" className="btn btn-primary">Register</button>
          </div>
          <div className="text-center mt-3">
            <p>Already have an account? <a href="/login">Login here</a></p>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Register;
