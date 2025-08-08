from django.db import models # The Models module is imported, so that data models can be defined.


# Model for Users is created, which stores login data and type of account.

class User(models.Model):
    user_id = models.CharField(max_length=5, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)

    # Two choices for users, which impact what is rendered after login in the frontend.

    user_type = models.CharField(max_length=7, choices=[
        ('student', 'Student'), 
        ('teacher', 'Teacher')])
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.surname}" 
    
#Teacher model links from teacher user type in User model in a 1 to 1 relationship (one teacher only has one account)


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=5, primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    form = models.CharField(max_length=3)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return f"Teacher user {self.user_id.first_name} {self.user_id.surname}"
    
    
#Student model links from Student user type in User model in a 1 to 1 relationship (one Student only has one account)
    
class Student(models.Model):
    student_id = models.CharField(max_length=5, primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    form = models.CharField(max_length=3)



    def __str__(self):
        return f"Student user {self.user_id.first_name} {self.user_id.surname}"
    

# Question model is used to store each potential quiz quesiton, with the subject and subtopic being brought 
# in via foreign keys. Four answers are present as well as the correct answer.
    
class Question(models.Model):
    question_id = models.CharField(max_length=30, primary_key=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    subtopic = models.ForeignKey('Subtopic', on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_1 = models.CharField(max_length=100)
    answer_2 = models.CharField(max_length=100)
    answer_3 = models.CharField(max_length=100)
    answer_4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f"Question {self.question_id} - {self.question_text}"


    #Each subject has a model with the subject name and id to be referenced elsewhere.
    
class Subject(models.Model):
    subject_id = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=20, unique=True) 

    def __str__(self):
        return f"{self.subject_name}"
    
    
    # Subtopics are used to be assigned to each question, and sit under each subject as a whole.
    
class Subtopic(models.Model):
    subtopic_id = models.CharField(max_length=20, primary_key=True)
    subtopic_name = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f" Subtopic {self.subtopic_name} in subject {self.subject.subject_name}"
    
    # The model for the BKT model stores the subject and subtopic (as these are done for each student by subtopic
    # and not by subject as a whole). The five parameters for the calculations for this are stored also.

class BKT(models.Model):
    bkt_id = models.CharField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    p_initial_knowledge = models.FloatField()
    p_will_learn = models.FloatField()
    p_slip = models.FloatField()
    p_guess = models.FloatField()
    p_known = models.FloatField()

    def __str__(self):
        return f"BKT model for {self.student} for subtopic {self.subtopic.subtopic_name} in {self.subject.subject_name}"
    

# Assigned quizzes are stored so that students can retreive these once teachers have assigned them.

class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    total_questions = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Quiz {self.quiz_id} assigned by Miss {self.teacher.user_id.surname} to {self.student.user_id.first_name} {self.student.user_id.surname} for {self.subject.subject_name}"

