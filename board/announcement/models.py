from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

tanks = 'Танки'
hils = 'Хилы'
dd = 'ДД'
merchants = 'Торговцы'
guild_masters = 'Гилдмастеры'
quest_givers = 'Квестгиверы'
blacksmiths = 'Кузнецы'
tanners = 'Кожевники'
potion_makers = 'Зельевары'
spell_masters = 'Мастера заклинаний'

CATEGORY = [
    (tanks, 'Танки'),
    (hils, 'Хилы'),
    (dd, 'ДД'),
    (merchants, 'Торговцы'),
    (guild_masters, 'Гилдмастеры'),
    (quest_givers, 'Квестгиверы'),
    (blacksmiths, 'Кузнецы'),
    (tanners, 'Кожевники'),
    (potion_makers, 'Зельевары'),
    (spell_masters, 'Мастера заклинаний'),
]


class Post(models.Model):
    objects = None
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default=tanks)
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        authors_email = self.author.email
        authors_name = self.author.username
        return f'{self.head_name}: {authors_name} : {authors_email}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="1")
    # post = models.ManyToManyField(Post, blank=True, null=True, related_name="author")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('com_detail', args=[str(self.id)])

    def __str__(self):
        user_email = self.user.email
        author_post = self.post.author
        return f'{self.user}: {author_post}: {self.post.head_name}: {user_email}'


class Agree(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default="1")
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('agree', args=[str(self.id)])

    def __str__(self):
        user_email = self.comment.user.email
        return f"{user_email}"


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
