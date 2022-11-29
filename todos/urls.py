"""定义 todos 的 URL 模式。"""

from django.urls import path

from . import views

app_name = 'todos'
urlpatterns = [
	# 主页
	path('', views.index, name = 'index'),
	# 显示所有分组
	path('groupings/', views.groupings, name = 'groupings'),
	# 特定分组的详细页面
	path('groupings/<int:grouping_id>/', views.grouping, name = 'grouping'),
	# 用于新建分组的页面
	path('new_grouping/', views.new_grouping, name = 'new_grouping'),
	# 用于新建 todo 的页面
	path('new_todo/<int:grouping_id>/', views.new_todo, name = 'new_todo'),
	# 用于编辑条目的页面
	path('edit_todo/<int:todo_id>/', views.edit_todo, name = 'edit_todo'),
	# 用于编辑分组的页面
	path('edit_grouping/<int:grouping_id>/', views.edit_grouping, name = 'edit_grouping'),
	# 删除 todo
	path('edit_todo/<int:todo_id>/delete/', views.delete_todo, name = 'delete_todo'),
	# 删除分组
	path('edit_grouping/<int:grouping_id>/delete/', views.delete_grouping, name = 'delete_grouping'),
	]