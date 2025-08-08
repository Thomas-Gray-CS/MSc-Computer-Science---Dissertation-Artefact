// useState is imported to manage the state of each component
// CSS is imported from the applicable file

import React, { useState, useEffect } from 'react';
import '../css/Quiz.css';


// Quiz function is defined with user and onComplete set as parameters.
// A number of useStats are set to either empty or default values (used to intialise their 
// data types), which are updated throughout the function.

function Quiz({ user, onComplete }) {
  const [assignedQuizzes, setAssignedQuizzes] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState('');
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isQuizDisplayed, setIsQuizDisplayed] = useState(false);
  const [userScore, setUserScore] = useState(0);
  const [isQuizCompleted, setIsQuizCompleted] = useState(false);


  // useEffect is used to fetch all assigned quizzes for the applicable user, obtaining
  // this as JSON and then updating the quiz const to hold the array of quizzes.

  useEffect(() => {
    const getQuizzes = async () => {
      const response = await fetch(`/api/quiz/getQuizzes/?student_id=${user.student_id}`);
      const responseData = await response.json();
      setAssignedQuizzes(responseData.assigned_quizzes || []);
    };
    getQuizzes();
  }, [user.student_id]);


  // Function to start the quiz is defined, taking the selected quiz for the applicable user from the url.
  // The question data is retrieved and stored in the questions const as an array.
  // The number for the current question is set to 0 and boolean for the display quiz is set to true.

  const generateQuiz = async () => {
    const response = await fetch(`/api/quiz/generateQuiz/?quiz_id=${selectedQuizId}&student_id=${user.student_id}`);
    const quizData = await response.json();
    setQuizQuestions(quizData.questions || []);
    setCurrentQuestionIndex(0);
    setIsQuizDisplayed(true);
  };


  // Answer handler takes the answer selected and gets the question from the current index.
  // With question 1 being index 0 and this incrementing as needed.

  const handleQuestionAnswer = async (selectedAnswer) => {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    

    // Response is set to post each of the answers to the api to update the p_known.

    const updateBKT = await fetch('/api/bktvalues/updateBKT/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: user.student_id,
        question_id: currentQuestion.question_id,
        selected_answer: selectedAnswer,
      })
    });
    

    // result (check if correct or not) is set from the JSON response from the API

    const answerChecker = await updateBKT.json();
    

    // If the result is correct, 1 is added to the score. If not, nothing happens.
    let updatedScore = userScore;
    if (answerChecker.correct) {
      updatedScore = userScore + 1;
      setUserScore(updatedScore);
    }

    
    // Checks whether any questions are left, using current + 1 to get the real number.

    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      await fetch('/api/quiz/markCompleted/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assigned_quiz_id: selectedQuizId,
          score: updatedScore,
          total_questions: quizQuestions.length
        })
      });
      setIsQuizCompleted(true);
    }
  };

  const handleReturnToHomepage = async () => {

    // Reset all states to the defaults as needed

    setIsQuizCompleted(false);
    setIsQuizDisplayed(false);
    setUserScore(0);
    setCurrentQuestionIndex(0);
    setSelectedQuizId('');
    setQuizQuestions([]);
    

    // Once the quiz is completed, the list of assigned quizzes is set again (incase there
    // are multiple quizzes assigned).

    const response = await fetch(`/api/quiz/getQuizzes/?student_id=${user.student_id}`);
    const refreshedData = await response.json();
    setAssignedQuizzes(refreshedData.assigned_quizzes || []);
    

    // Return to homepage

    onComplete();
  };

  
  // If the quiz has been completed, a screen to say that it has been completed is displayed.
  // A button calls the return to homepage function, taking the user there are resetting quiz values.

  if (isQuizCompleted) {
    return (
      <div className="quizContainer">
        <div className="quizCompletionScreen">
          <h2>Well done!</h2>
          <p>You scored {userScore} out of {quizQuestions.length}</p>
          <button onClick={handleReturnToHomepage} className="quizButton">
            Return to Homepage
          </button>
        </div>
      </div>
    );
  }


  // If display quiz is false, the screen to select a quiz is provided to the user.


  // When there is more than 0 quizzes (so at least one is assigned), a dropdown is displayed
  // with each quiz being available for selected. Once a quiz is selected, the applicable quiz id
  // is set so that the correct one is there when the function is called (using setSelectedQuiz).

  // When a user clicks start quiz, the start assigned quiz function is called, else a message stating
  // that there are no quizzes is displayed.

  if (!isQuizDisplayed) {
    return (
      <div className="quizContainer">
        <h3 className="quizHeading">Assigned Quizzes</h3>
        {assignedQuizzes.length > 0 ? (
          <div className="quizBody">
            <p>Complete quizzes </p>
            <select className="quizSelect" value={selectedQuizId} onChange={event => setSelectedQuizId(event.target.value)}>
              <option value="">Select Quiz</option>
              {assignedQuizzes.map(quizItem => (
                <option key={quizItem.quiz_id} value={quizItem.quiz_id}>
                  {quizItem.subject_name} 
                </option>
              ))}
            </select>
            <button className="quizButton" onClick={generateQuiz} disabled={!selectedQuizId}>
              Start Quiz
            </button>
          </div>
        ) : (
          <div className="quizBodyEmpty">
            <p>You have no quizzes to complete.</p>
          </div>
        )}
      </div>
    );
  }


  // currentQuestion is set to the current question as per the index incrementing.

  const currentQuestion = quizQuestions[currentQuestionIndex];
  

  // Array is set with each of the answers.

  const getQuestionAnswers = (questionData) => [
    questionData.answer_1, 
    questionData.answer_2, 
    questionData.answer_3, 
    questionData.answer_4
  ];


  // Question is returned to the frontend with the number of the question, the question text and the 
  // answers mapped to button, with all buttons able to call the handleAnswer function and 
  // pass the answer text to it.

  return (
    <div className="quizContainer">
      <h3 className="quizHeading">Question {currentQuestionIndex + 1} of {quizQuestions.length}</h3>
      <div className="quizQuestion">{currentQuestion.question_text}</div>
      <div className="quizAnswers">
        {getQuestionAnswers(currentQuestion).map((answerText, answerIndex) => (
          <button key={answerIndex} className="quizAnswerButton" onClick={() => handleQuestionAnswer(answerText)}>
            {answerText}
          </button>
        ))}
      </div>
    </div>
  );
}


// Quiz component is exported to be used by other components, such as on button clicks.

export default Quiz;
