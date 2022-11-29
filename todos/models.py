from django.db import models

from django.contrib.auth.models import User


class Grouping(models.Model):
    """todo 的分组"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串展示。"""
        return self.text


class Todo(models.Model):
    """要完成的 todo"""
    grouping = models.ForeignKey(Grouping, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    complete = models.CharField(choices=(("complete", "complete"), ("uncomplete", "uncomplete")),
                                default="uncomplete", max_length=20)

    def __str__(self):
        """返回模型的字符串展示。"""
        if len(self.text) <= 50:
            return f"{self.text}"
        else:
            return f"{self.text[:50]}..."
