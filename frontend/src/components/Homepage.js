// UseState is imported to manage component states
// The applicable CSS is imported
// The required components to be used on this page are imported

import React, { useState } from 'react';
import '../css/Homepage.css';
import Quiz from './Quiz';
import TeacherData from './TeacherData';
import AssignQuizzes from './AssignQuizzes';


// HomePage function is defined, which defines what the homepage should displayed
// depending on the user type.

function HomePage({ user, onLogout }) {
  const [view, setView] = useState('home');



  // Sets the buttons on the homepage if user type = student
  // oncomplete sets the view to home once a quiz is done, as is the default.
  // Checks the view value and renders the component needed depending on what is selected.

  if (user.user_type === 'student') {
    return (
      <div className="homepageContainer">
        <h2 className="homepageHeading">Welcome {user.first_name}!</h2>
        <button className="homepageButton" onClick={() => setView('quiz')}>View Quizzes</button>
        {view === 'quiz' && (<Quiz user={{ student_id: user.student_id }} onComplete={() => setView('home')} />)}
        <button className="homepageButton" onClick={onLogout}>Logout</button>
      </div>
    );
  }


  // Sets the buttons on the homepage if user type = teacher.
  // Checks the view value and renders the component needed depending on what is selected.

  if (user.user_type === 'teacher') {
    return (
      <div className="homepageContainer">
        <h2 className="homepageHeading">Welcome {user.first_name}</h2>
        <button className="homepageButton" onClick={() => setView('progress')}>View Student Data</button>
        {view === 'progress' && <TeacherData teacherUserId={user.teacher_id} />}
        <button className="homepageButton" onClick={() => setView('assign')}>Assign Quizzes</button>
        {view === 'assign' && <AssignQuizzes teacherUserId={user.teacher_id} />}
        <button className="homepageButton" onClick={onLogout}>Logout</button>
      </div>
    );
  }
}

// HomePage component is exported so that other components can use it

export default HomePage;
