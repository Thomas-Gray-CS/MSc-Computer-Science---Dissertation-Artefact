// useState is imported to allow component state to be managed.
// Applicable CSS is imported.

import React, { useState, useEffect } from 'react';
import '../css/AssignQuizzes.css';


// Function to allow teachers to assigned quizzes is made.
// Constants for the subject and whether completed are initialised as
// empty, ready to be populated as the component renders.

function AssignQuizzes({ teacherUserId }) {
  const [subject, setSubject] = useState('');
  const [completed, setCompleted] = useState('');


  // Subject that the teacher teaches is fetched from the api.
  // The url is read and the applicable data for that teacher id is extracted.
  // This JSON is parsed and then the subject within it is set to the subject const.

  useEffect(() => {
    // Fetch students from the quiz viewset's getStudents endpoint, filtered by teacher_id
    const getStudents = async () => {
      const res = await fetch(`/api/quiz/getStudents/?teacher_id=${teacherUserId}`);
      const data = await res.json();
      setSubject(data.subject_id);
    };
    getStudents();
  }, [teacherUserId]);

  // Function that assigns a quiz is defined.
  // It has a POST method, sending a JSON block that contains the
  // Teacher ID and the Subject ID. This is currently setting the quiz for
  // all students with that subject. This would be modified if deployed to a live 
  // environment.

  const createQuiz = async () => {
    await fetch('/api/quiz/createQuiz/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        teacher_id: teacherUserId,
        subject_id: subject
      })
    });

    setCompleted('Quiz Assigned Successfully');
    // Log or use the teacher_id from the backend response
    setTimeout(() => setCompleted(''), 3000);
  };


  // The buttons and text are returned to the frontend, with the applicable 
  // functions being called by different buttons. Assign Quiz button opens 
  // another button to confirm this, which in turn calls the function.
  // Once complete is set, the success message is displayed.

  return (
    <div className="assignQuizzesContainer">
      <h2 className="assignQuizzesHeader">Assign Quiz</h2>
      <div className="assignQuizzesBody">
        <p className="assignQuizzesTextSpacing">Click to assign quiz.</p>
        <button 
          className="assignQuizzesButton" 
          onClick={createQuiz}
          disabled={!subject}
        >
          Assign Quiz to All Students
        </button>
        {completed && (
          <div className="assignQuizzesSuccessMessage">
            {completed}
          </div>
        )}
      </div>
    </div>
  );
}


// Component is exported to allow for use with other components.

export default AssignQuizzes;
