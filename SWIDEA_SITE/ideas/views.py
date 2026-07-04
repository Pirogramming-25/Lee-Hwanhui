from django.shortcuts import render, redirect, get_object_or_404 
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm
from django.db import models  




def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})


def devtool_create(request):
    if request.method == 'POST':        
        form = DevToolForm(request.POST)       
        if form.is_valid():            
            devtool = form.save()    
            return redirect('ideas:devtool_detail', pk=devtool.pk)  
        form = DevToolForm()           
    return render(request, 'ideas/devtool_form.html', {'form': form})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)  
    ideas = devtool.ideas.all()             
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool, 'ideas': ideas})

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)  
        if form.is_valid():
            devtool = form.save()
            return redirect('ideas:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)     
    return render(request, 'ideas/devtool_form.html', {'form': form})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()                                
    return redirect('ideas:devtool_list')




def idea_list(request):
    sort = request.GET.get('sort', 'latest')   

    ideas = Idea.objects.all()            

    if sort == 'latest':
        ideas = ideas.order_by('-created_at')  
    elif sort == 'oldest':
        ideas = ideas.order_by('created_at')     
    elif sort == 'name':
        ideas = ideas.order_by('title')          
    elif sort == 'star':
        ideas = ideas.annotate(star_count=models.Count('stars')).order_by('-star_count')

    starred_ids = []                             
    if request.user.is_authenticated:
        starred_ids = IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True)

    return render(request, 'ideas/idea_list.html', {
        'ideas': ideas,
        'sort': sort,
        'starred_ids': starred_ids,  
    })
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES) 
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    is_starred = False                             
    if request.user.is_authenticated:             
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    return render(request, 'ideas/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)       
    return render(request, 'ideas/idea_form.html', {'form': form})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('ideas:idea_list')

def idea_star_toggle(request, pk):
    idea = get_object_or_404(Idea, pk=pk)          
    if request.user.is_authenticated:         
        star = IdeaStar.objects.filter(user=request.user, idea=idea)
        if star.exists():
            star.delete()                        
        else:
            IdeaStar.objects.create(user=request.user, idea=idea)  

    next_page = request.GET.get('next')             
    if next_page == 'list':
        return redirect('ideas:idea_list')          
    return redirect('ideas:idea_detail', pk=pk)       


def idea_interest_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.GET.get('action')              

    if action == 'increase':
        idea.interest += 1                          
    elif action == 'decrease':
        idea.interest -= 1                          

    idea.save()                                  
    return redirect('ideas:idea_detail', pk=pk)      