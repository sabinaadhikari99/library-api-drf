from django.db import models
from django.utils import timezone
from datetime import timedelta


# =========================
# BOOK MODEL
# =========================
class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)

    published_date = models.DateField()
    genre = models.CharField(max_length=50)

    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# =========================
# MEMBER MODEL
# =========================
class Member(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


# =========================
# LOAN MODEL
# =========================
class Loan(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set due date only if not provided
        if not self.due_date:
            self.due_date = (timezone.now() + timedelta(days=14)).date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"