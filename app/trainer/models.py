from django.db import models
from django.contrib.auth.models import User

class Regulation(models.Model):
	title = models.CharField(max_length=50,verbose_name='Назва правіла')
	content = models.TextField(null=True, blank=True,verbose_name='Тэкст')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural='Правілы'
		verbose_name='Правіла'


class Quiz(models.Model):
    rule = models.ForeignKey(Regulation, on_delete=models.PROTECT,verbose_name='Правіла')
    explanation = models.TextField(blank=True, verbose_name='Агульнае заданне')
    name = models.CharField(max_length=255)
    
    def __str__(self):
    	return self.explanation

    class Meta:
        verbose_name='Заданне для практыкавання'

class Task(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT, verbose_name='Пытанне да задання',
                             related_name='questions')
    question = models.TextField(verbose_name='Тэкст заданія', blank=True)


    def __str__(self):
    	return self.question
        
    class Meta:
        verbose_name_plural='Заданні'
        verbose_name='Заданне'


class Answer(models.Model):
    question = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Адказ', max_length=255)
    is_correct = models.BooleanField('Правільны адказ', default=False)

    def __str__(self):
        return self.text




class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    # through Kласс модели, которая представляет связующую таблицу (связующая модель) 
    # либо в виде ссьmки на него, либо в виде имени, представленном стро­кой.

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz, taken_quiz=None) \
            .values_list('answer__question__pk', flat=True) # получаем объекты через таблицу studentAnswer по ключу answer, 
                                                            # далее из таббл Answer по ключу question получаем сам запрос
                                                            # массив из ключей отвеченных вопросов
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('question')
        return questions

    

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    taken_quiz = models.ForeignKey(TakenQuiz, on_delete=models.CASCADE, 
                                   related_name='taken_quiz_answers', 
                                   null=True)