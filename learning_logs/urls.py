from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/favicon/favicon.ico')),

    # Домашняя страница
    path('', views.index, name = 'index'),
    
    # Вывод всех тем
    path('topics/', views.topics, name = 'topics'),
    
    # Страница с подробной информацией по отдельной теме
    path('topics/<topic_id>/', views.topic, name='topic'),
    
    # Страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),

    # Страница для добавления новой записи
    path('new_entry/<topic_id>', views.new_entry, name='new_entry'),

    # Страница для редактирования записи
    path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),

    # Страница для редактирования темы
    path('edit_topic/<topic_id>', views.edit_topic, name='edit_topic'),

    # Удаление темы
    path('topics/<topic_id>/delete', views.delete_topic, name='delete_topic'),

    # Удаление записи
    path('delete_entry/<entry_id>', views.delete_entry, name='delete_entry'),
]