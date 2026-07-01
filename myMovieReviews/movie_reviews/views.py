from django.shortcuts import render, redirect, get_object_or_404
from .models import Review


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'movie_reviews/review_list.html', {'reviews': reviews})


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'movie_reviews/review_detail.html', {'review': review})


def review_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        release_year = request.POST.get('release_year')
        genre = request.POST.get('genre')
        rating = request.POST.get('rating')
        director = request.POST.get('director')
        main_actor = request.POST.get('main_actor')
        running_time = request.POST.get('running_time')
        content = request.POST.get('content')

        Review.objects.create(
            title=title,
            release_year=release_year,
            genre=genre,
            rating=rating,
            director=director,
            main_actor=main_actor,
            running_time=running_time,
            content=content,
        )
        return redirect('review_list')
    return render(request, 'movie_reviews/review_form.html')


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.release_year = request.POST.get('release_year')
        review.genre = request.POST.get('genre')
        review.rating = request.POST.get('rating')
        review.director = request.POST.get('director')
        review.main_actor = request.POST.get('main_actor')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        review.save()
        return redirect('review_detail', pk=review.pk)
    return render(request, 'movie_reviews/review_form.html', {'review': review})


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'movie_reviews/review_delete.html', {'review': review})