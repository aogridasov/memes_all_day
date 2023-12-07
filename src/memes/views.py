from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import MemeUploadForm, SignUpForm
from .models import MemeLike, MemePost


class BaseMemeListView(ListView):
    """Абстрактный вью для наследования"""

    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return MemePost.objects.all()

        user_liked = MemeLike.objects.filter(
            meme=OuterRef('id'),
            user=self.request.user,
        )

        queryset = MemePost.objects.annotate(
            current_user_liked=Exists(user_liked)
        ).annotate(likes_count=Count('likes'))
        return queryset.order_by('-created_at')


class IndexView(BaseMemeListView):
    """Отображает главную страницу"""

    template_name = 'index.html'


class FavoritesView(BaseMemeListView):
    """Отображает страницу c лайкнутыми мемами"""

    template_name = 'favorites.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_user_liked=True)


class MyUploadsView(BaseMemeListView):
    """Отображает страницу c загружеными юзерами мемами"""

    template_name = 'my_memes.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class SearchView(BaseMemeListView):
    """Отображает cтраницу поиска"""

    template_name = 'search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        return queryset.filter(
            Q(description__icontains=query) | Q(author__username__icontains=query)
        )


class SignUp(CreateView):
    """Базовая вью для регистрации"""

    form_class = SignUpForm
    success_url = reverse_lazy('memes:index')
    template_name = 'users/signup.html'


@login_required
def like_meme(request, id):
    """Лайкаем мем"""

    meme = get_object_or_404(MemePost, id=id)
    MemeLike.objects.get_or_create(
        user=request.user,
        meme=meme,
    )
    return redirect('memes:index')


@login_required
def unlike_meme(request, id):
    """Убираем лайк с мема"""

    meme = get_object_or_404(MemePost, id=id)
    MemeLike.objects.filter(user=request.user, meme=meme).delete()
    return redirect('memes:index')


class MemeUploadView(LoginRequiredMixin, CreateView):
    """Вью для загрузки мема"""

    form_class = MemeUploadForm
    success_url = reverse_lazy('memes:my_memes')
    template_name = 'upload_meme.html'


@login_required
def meme_create(request):
    form = MemeUploadForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        meme = form.save(commit=False)
        meme.author = request.user
        meme.save()
        return redirect('memes:index')

    return render(request, 'upload_meme.html', {'form': form})


@login_required
def meme_delete(request, id):
    MemePost.objects.filter(id=id).delete()
    return redirect('memes:my_memes')
