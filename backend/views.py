# Repsonse is imported from DRF to handle returning data.
# Viewserts helps create the API views
# Action allows for custom actions to be created to enhance functionality
# Random is used to shuffle questions and quizzes

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
import random


# All backend models are imported so that they can be accessed.

from backend.models import (
    Teacher,
    Student, 
    BKT, 
    Subject, 
    Subtopic, 
    User, 
    Question, 
    Quiz
)


# Serialisers are imported for the required models where data needs to be sent to the frontend.

from backend.serializers import (
    UserSerializer, 
    TeacherSerializer, 
    BKTSerializer, 
    QuizSerializer
    
)


# Standard viewset for login in made, triggered by the frontend when login is attempted.
# This handles the authentication and checks if the user is valid.

class Login(viewsets.ViewSet): 
    @action(detail=False, methods=['post'])
    def checkLogin(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        # If the user is a teacher, add teacher_id to the user data
        if user.user_type == 'teacher':
            teacher = Teacher.objects.get(user_id=user.user_id)
            user_data['teacher_id'] = teacher.teacher_id

        # If the user is a student, add student_id to the user data (optional, for symmetry)
        elif user.user_type == 'student':
            student = Student.objects.get(user_id=user.user_id)
            user_data['student_id'] = student.student_id

        return Response({'user': user_data})




# View for the BKT values is made, with all BKT data being made available as serialised in the view.

class BKTViewSet(viewsets.ModelViewSet):
    queryset = BKT.objects.all()
    serializer_class = BKTSerializer
    

    # Function to update the p_known value is made, which runs when a student answers a question.
    # Variables are set using data made available from the frontend request.

    @action(detail=False, methods=['post'])
    def updateBKT(self, request):
        student_id = request.data.get('student_id')
        question_id = request.data.get('question_id')
        selected_answer = request.data.get('selected_answer')

        question = Question.objects.get(question_id=question_id)
        subtopic = question.subtopic
        student = Student.objects.get(student_id=student_id)
        bkt = BKT.objects.get(student=student, subtopic=subtopic)
        
    
        # Correct is set where the selected answer from the frontend directly matches the correct answer
        # From the backend.

        correct = (selected_answer == question.correct_answer)
        

        # If the value is correct, the BKT formula (taken from the dissertation) is used for a correct answer.

        if correct:
            top_value = bkt.p_known * (1 - bkt.p_slip)
            bottom_value = top_value + (1 - bkt.p_known) * bkt.p_guess


        # If the answer is incorrect, the formula for incorrect answers is used.
           
        else:
            top_value = bkt.p_known * bkt.p_slip
            bottom_value = top_value + (1 - bkt.p_known) * (1 - bkt.p_guess)



        # The "learned" value is taken by dividing value 1 by value 2.
        # The new p_known value is then calculated using the final part of the formula with the calculated 
        # p_learned value. 

        p_learned = top_value / bottom_value
        bkt.p_known = round(min(1.0, max(0.0, p_learned + (1 - p_learned) * bkt.p_will_learn)), 2)
        bkt.save()
        
        
        # The calculated values are then returned in the response for the frontend.

        return Response({
            'correct': correct,
            'correct_answer': question.correct_answer,
            'p_known': round(bkt.p_known, 3)
        })


# Viewset for quizzes is created, with all data being made available in the queryset.

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    # Quiz generator is created, using the data retrieved from the frontend request.
# It can only get quizzes that have been assigned, so there will always be a quiz id.

    @action(detail=False, methods=['get'])
    def generateQuiz(self, request):
        student_id = request.query_params.get('student_id')
        quiz_id = request.query_params.get('quiz_id')

        student = Student.objects.get(student_id=student_id)
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        subject = quiz.subject
        

        # All relevant subtopics for the particular subject are filtered.
        # A blank array for the question list is initialised, ready to be populated.

        subtopics = Subtopic.objects.filter(subject=subject)
        questionList = []
        

        # Loop through each subtopic is completed, retrieving all BKT_known values for a student.
        # For this prototype, there will be six subtopics.
        # The value of p_known is then used to determine how many questions from each subtopic
        # are needed.

        for subtopic in subtopics:
            subtopic_bkt_values = BKT.objects.get(student=student, subtopic=subtopic)
            p_known = subtopic_bkt_values.p_known
            
            if p_known <= 0.4:
                question_amount = 3
            elif p_known > 0.4 and p_known < 0.8:
                question_amount = 2
            else:
                question_amount = 1

        # The current subtopic is filtered in the questions and the questions are randomised.
        # Then the required number of questions (if available) are added to the question list.

            subtopic_questions = list(Question.objects.filter(subject=subject, subtopic=subtopic))
            random.shuffle(subtopic_questions)
            questionList.extend(subtopic_questions[:question_amount])


# The generated list of questions is shuffled to ensure it is random (so that students
# cannot just memorise answers). 

        random.shuffle(questionList)


        # dictionary is created to hold the question data, taking all of them in order. This makes the quiz
        # ready to pass to the frontend.

        question_data = [
            {
                'question_id': question.question_id, 
                'question_text': question.question_text, 
                'answer_1': question.answer_1, 
                'answer_2': question.answer_2, 
                'answer_3': question.answer_3, 
                'answer_4': question.answer_4
            } for question in questionList
        ]
        

        # The response to be sent to the frontend is created, containing the quiz data,
        # The amount of questions and the subject.

        return Response(
            {
                'questions': question_data,
                'total_questions': len(question_data),
                'subject_name': subject.subject_name,
                'quiz_type': 'assigned'
            }
        )


    # teacher data function is created, retrieving all subjects and the classes from 
    # the frontend (should always be one).

    @action(detail=False, methods=['get'])
    def getStudents(self, request):
        teacher_id = request.query_params.get('teacher_id')
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        # Only return the subject and students for this teacher's form
        subject = teacher.subject
        students_in_class = Student.objects.filter(form=teacher.form)
        class_data = {
            'class_id': subject.subject_id,
            'subject_id': subject.subject_id,
            'subject_name': subject.subject_name,
            'students': [
                {
                    'student_id': student.student_id,
                    'student_name': f"{student.user_id.first_name} {student.user_id.surname}"
                }
                for student in students_in_class
            ]
        }
        return Response(class_data)

    # Function to assign quizzes is created, taking the teacher id and subject id from the frontend request.

    @action(detail=False, methods=['post'])
    def createQuiz(self, request):
        teacher_id = request.data.get('teacher_id')
        subject_id = request.data.get('subject_id')
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        subject = Subject.objects.get(subject_id=subject_id)
        students = Student.objects.filter(form=teacher.form)
        created_assignments = []

        for student in students:
            quiz = Quiz.objects.create(
                teacher=teacher,
                student=student,
                subject=subject
            )
            created_assignments.append(quiz.quiz_id)

        return Response({
            'quiz_ids': created_assignments,
            'teacher_id': teacher.teacher_id
        })
    

    # Function that retrieves all of the quizzes assigned to a student is made.
    # Student ID is taken from the frontend request.

    @action(detail=False, methods=['get'])
    def getQuizzes(self, request):
        student_id = request.query_params.get('student_id')
        student = Student.objects.get(student_id=student_id)
        quizzes = Quiz.objects.filter(
            student=student,
            completed=False
        )

        quiz_data = []
        for quiz in quizzes:
            quiz_data.append({
                'quiz_id': quiz.quiz_id,
                'subject_id': quiz.subject.subject_id,
                'subject_name': quiz.subject.subject_name,
                'teacher_id': quiz.teacher.teacher_id,
                'teacher_name': f"{quiz.teacher.user_id.first_name} {quiz.teacher.user_id.surname}"
            })

        return Response({
            'assigned_quizzes': quiz_data,
            'total_count': len(quiz_data)
        })
    

    # Function to mark each quiz as completed is created. This takes frontend values in the post request.

    @action(detail=False, methods=['post'])
    def markCompleted(self, request):
        quiz_id = request.data.get('assigned_quiz_id')  # Keep old parameter name for frontend compatibility
        score = request.data.get('score')
        total_questions = request.data.get('total_questions')
        

        # The quiz is obtained where the quiz id matches the one provided. Each parameter
        # is then updated using the previously received values.

        quiz = Quiz.objects.get(quiz_id=quiz_id)
        quiz.completed = True
        quiz.score = score
        quiz.total_questions = total_questions
        quiz.save()
        
        
        # Response block is set to be sent to the frontend.

        return Response({
            'quiz_id': quiz_id,
            'score': score,
            'total_questions': total_questions
        })


# Teach viewset is created and all teacher data is made available.

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


    # Teacherdata function is created, where all subjects are taken for the teacher and an empty
    # array for the results is made.

    @action(detail=False, methods=['get'])
    def getProgressData(self, request):
        subjects = Subject.objects.all()
        result = []


        # Loop through students is completed, where all student values are retrieved for the subject.

        for subject in subjects:
            students = Student.objects.all()
            student_data = []
            class_p_known = 0

            for student in students:
                bkt_values = BKT.objects.filter(student=student)
                mean_known_score = sum([bkt.p_known for bkt in bkt_values]) / len(bkt_values) if bkt_values else 0
                class_p_known += mean_known_score
                student_data.append(
                    {
                        'student_id': student.student_id,
                        'student_name': f"{student.user_id.first_name} {student.user_id.surname}",
                        'average_p_known': round(mean_known_score * 100, 2)
                    }
                )

            class_avg_p_known = round((class_p_known / len(students)) * 100, 2) if students else 0

            subtopics = Subtopic.objects.filter(subject=subject)
            subtopic_data = []

            for subtopic in subtopics:
                subtopic_p_known = []
                for student in students:
                    bkt = BKT.objects.filter(student=student, subtopic=subtopic).first()
                    if bkt:
                        subtopic_p_known.append(bkt.p_known)

                mean_p_known = sum(subtopic_p_known) / len(subtopic_p_known) if subtopic_p_known else 0
                subtopic_data.append({
                    'subtopic_id': subtopic.subtopic_id,
                    'subtopic_name': subtopic.subtopic_name,
                    'mean_p_known': round(mean_p_known * 100, 2)
                })

            class_info = {
                'class_id': subject.subject_id,
                'class_name': subject.subject_name, 
                'subject': {
                    'subject_id': subject.subject_id, 
                    'subject_name': subject.subject_name, 
                    'students': student_data,
                    'class_average_p_known': class_avg_p_known, 
                    'subtopics': subtopic_data
                }
            }
            result.append(class_info)
        return Response(result)
