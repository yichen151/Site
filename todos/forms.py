from django.forms import ModelForm
from django.forms import widgets as wid


from .models import Grouping, Todo

class GroupForm(ModelForm):
	class Meta:
		model = Grouping
		fields = ['text']
		labels = {'text': ''}

class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['text', 'complete']
		widgets = {
			"text":wid.Textarea(attrs = {'cols': 80}),
			"complete":wid.Select(choices = (("uncomplete", "uncomplete"), ("complete", "complete"))),
		}