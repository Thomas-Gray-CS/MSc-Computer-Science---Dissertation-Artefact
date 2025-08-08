import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/App';


// The root is rendered, which for this application is the app component. This triggers either the login form
// or the homepage, depending on whether the user is logged in or not.


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
