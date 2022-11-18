from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect   

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
        # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                if  Article.objects.filter(title = form['title']).exists():
                        form['errors'] = u"Статья с таким именем уже есть"
                        return render(request, 'new.html', {'form': form})
                else:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('archive')
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'new.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'new.html', {})
    else:
        raise Http404
