from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    """Тема, которую изучает пользователь"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    
    def calculateVotes(self):
        return Entry.objects.filter(topic = self.id).count()

    count_entries = property(calculateVotes)

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.text
        

class Entry(models.Model):
    """Информация, изученная пользователем по теме"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries' 

    def __str__(self):
        """Возвращает строковое представление модели."""
        if len(self.text) > 70:
            return self.text[:70] + '...'
        else:
            return self.text[:70]