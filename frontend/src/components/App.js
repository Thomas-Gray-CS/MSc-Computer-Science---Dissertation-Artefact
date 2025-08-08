// Required imports are placed, along with loginform and homepage.

import React, { useState } from 'react';
import '../css/App.css';
import LoginForm from './LoginForm';
import Homepage from './Homepage';

// Function intially sets a const as user and sets this as null (no one logged in as of yet).

function App() {
  const [user, setUser] = useState(null);

  // User data is provided from the login form and is set to userData.
  // This is then assigned to the user state,
  const handleLogin = (userData) => {
    setUser(userData);
  };


  // When the logout button is clicked, the user state is emptied to show no current user.
  // The function is designed to return to the login form.

  const handleLogout = () => {
    setUser(null);
  };

  // App css is returned and the homepage is displayed if the user is logged in.
  // If not, the login form is maintained on the screen.

  return (
    <div className="App">
      {!user ? (
        <LoginForm onLogin={handleLogin} />
      ) : (
        <Homepage user={user} onLogout={handleLogout} />
      )}
    </div>
  );
}

// App component is exported to be used in the other components.

export default App;
