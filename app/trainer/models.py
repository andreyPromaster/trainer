from django.db import models

class Task(models.Model):
	title = models.CharField(max_length=50,verbose_name='Назва правіла')
	content = models.TextField(null=True, blank=True,verbose_name='Тэкст')
	class Meta:
		verbose_name_plural='Правілы'
		verbose_name='Правіла'
 #надо определится с названиями классов
         

