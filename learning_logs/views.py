from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Домашняя страница приложения Learning Log"""
    try:
        updates = Entry.objects.filter(topic=19).order_by('-date_added')[:5]
        topic_id = 19
    except:
        updates = Entry.objects.filter(topic=7).order_by('-date_added')[:5]
        topic_id = 7
    context = {'updates': updates, 'topic_id': topic_id}
    return render(request, 'learning_logs/index.html', context)
    

#@login_required
def topics(request):
    """Вывод всех тем, созданных пользователями"""
    
    topics_public = Topic.objects.filter(public=True).order_by('-date_added') # темы public
    
    if request.user.is_authenticated:
        topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
        context = {'topics': topics,'topics_public': topics_public}
        return render(request, 'learning_logs/topics.html', context)
    else:
        context = {'topics_public': topics_public}
        return render(request, 'learning_logs/topics.html', context)
        
#@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Проверка того, что тема принадлежит текущему пользователю.
    if not topic.public:
        check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404

@login_required
def new_topic(request):
    """Определяет новую тему"""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные
        form = TopicForm(request.POST)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # for key in request.POST:
            #     if key == 'public':
            #         new_topic.public = True
            if 'public' in request.POST:
                new_topic.public = True

            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id = topic_id)
    check_topic_owner(request, topic)

    topic.delete()
    return HttpResponseRedirect(reverse('topics'))

@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)    
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
    # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
    # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id = entry_id)
    check_topic_owner(request, entry.topic)

    entry.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    
@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id = topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        form = TopicForm(instance=topic)
        public = form.save(commit = False).public # true / false
        if public:
            form.fields['public'].initial = True # поставить галочку
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            if 'public' in request.POST:
                new_topic.public = True
            else:
                new_topic.public = False

            new_topic.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)
