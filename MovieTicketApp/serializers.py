from rest_framework import serializers
from django.contrib.auth.models import User
from MovieTicketApp.models import MovieDb,ShowDb,BookingDb



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieDb
        fields = '__all__'


class ShowSerializers(serializers.ModelSerializer):

    movie_title = serializers.CharField(
        source='movie.title',
        read_only=True
    )

    class Meta:
        model = ShowDb
        fields = [
            'id',
            'movie',
            'movie_title',
            'show_date',
            'show_time',
            'theatre',
            'ticket_price',
            'total_seats'
        ]


class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingDb
        fields = '__all__'
        read_only_fields = ['id', 'user', 'total_amount', 'booking_date', 'status']

