// UseState is imported to manage states of components
// The applicable CSS is imported

import React, { useState } from 'react';
import '../css/LoginForm.css';


// LoginForm function is defined, which handles login.
// email and password are initialised as empty strings to be populated using
// the applicable set functions.

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');


  // handleSubmit function is defined, using the submission of the form
  // as the event. 
  // preventDefault stops a default form submission and stops the 
  // page from reloading.
  // POST requested to the APi is sent with the entered email and password as JSON.

  const checkLogin = async (event) => {
    event.preventDefault();
    const response = await fetch('/api/login/checkLogin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    // data constant is set to take the response from the API as JSON.
    // onLogin is called with the user data from the response passed to it.
    // No error handling is done due to it being a managed prototype.

    const data = await response.json();
    onLogin(data.user);
  };

  // The login form is returned to the frontend, so that the login details can be entered.
  // The onSubmit property triggers the handleSubmit function when required (when
  // the login button is pressed).
  return (
    <div className="loginFormContainer">
      <form className="loginForm" onSubmit={checkLogin}>
        <h2 className="loginFormHeading">Login</h2>
        <input 
          className="loginFormInput"
          type="email" 
          placeholder="Please enter your Email" 
          value={email} 
          onChange={event => setEmail(event.target.value)} 
          required 
        />
        <input 
          className="loginFormInput"
          type="password" 
          placeholder="Please enter your Password" 
          value={password} 
          onChange={event => setPassword(event.target.value)} 
          required 
        />
        <button className="loginFormButton" type="submit">Login</button>
      </form>
    </div>
  );
}


// Component is exported to be used elsewhere in the application.

export default LoginForm;
