from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_comments_rating = 0
        posts = Post.objects.filter(author=self)
        for a in posts:
            posts_rating += a.rating
        comments = Comment.objects.filter(user=self.user)
        for b in comments:
            comments_rating += b.rating
        posts_comments = Comment.objects.filter(post__author=self)
        for c in posts_comments:
            comments_rating += c.rating

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'

    CONTENT = [
        (article, 'Статья'),
        (news, 'Новости'),
    ]

    post_name = models.CharField(max_length=255)
    post_text = models.CharField(max_length=10000)
    post_rating = models.IntegerField(default=0)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_content = models.CharField(max_length=2,
                                    choices=CONTENT,
                                    default=article)

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:125] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_text = models.TextField()
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

