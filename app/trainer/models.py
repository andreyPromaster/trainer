from django.db import models

class Regulation(models.Model):
	title = models.CharField(max_length=50,verbose_name='Назва правіла')
	content = models.TextField(null=True, blank=True,verbose_name='Тэкст')
	class Meta:
		verbose_name_plural='Правілы'
		verbose_name='Правіла'

class ExplanationOfTask(models.Model):
    rule = models.ForeignKey(Regulation, on_delete=models.PROTECT)
    explanation = models.CharField(max_length=250,verbose_name='Агульнае заданне', blank=True)
    class Meta:
        verbose_name='Заданне для практыкавання'

class Task(models.Model):
    explanation = models.ForeignKey(ExplanationOfTask, on_delete=models.PROTECT)
    question = models.CharField(max_length=150,verbose_name='Тэкст заданія', blank=True)
    answer = models.CharField(max_length=50,verbose_name='Адказ', blank=True)
    class Meta:
        verbose_name_plural='Заданні'
        verbose_name='Заданне'
