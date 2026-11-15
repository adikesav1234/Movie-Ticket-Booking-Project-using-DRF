from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MovieDb(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    release_date = models.DateField()

    def __str__(self):
        return self.title


class ShowDb(models.Model):
    movie = models.ForeignKey(MovieDb, on_delete=models.CASCADE, related_name='movie_shows')
    show_date = models.DateField()
    show_time = models.TimeField()
    theatre = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.theatre}"


class BookingDb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookings')
    show = models.ForeignKey(ShowDb, on_delete=models.CASCADE, related_name='show_bookings')
    number_of_seats = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f"{self.user.username} - {self.show.movie.title}"