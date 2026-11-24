from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from MovieTicketApp.models import MovieDb, ShowDb, BookingDb
from MovieTicketApp.serializers import UserSerializer,MovieSerializers,ShowSerializers,BookingSerializers
from django.db.models import Sum

# Create your views here.

#Calculate Available Seats
def get_available_seats(show):

    booked_seats=BookingDb.objects.filter(
        show=show,
        status='Confirmed'
    ).aggregate(total=Sum('number_of_seats'))['total'] or 0
    return show.total_seats-booked_seats

#Display Show Details With Available Seats
def get_show_details(show):
    serializer_instance = ShowSerializers(show)
    show_data=dict(serializer_instance.data)
    show_data['available_seats']=get_available_seats(show)
    return show_data

class RegisterView(APIView):
    def post(self, request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                {"Message": "User Registered Successfully"},status=201)
        else:
            return Response(serializer_instance.errors, status=400)

class UserListView(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer_instance=UserSerializer(user,many=True)
        return Response(serializer_instance.data)
    
class UserDetailView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer_instance = UserSerializer(request.user)
        return Response(serializer_instance.data)

class MovieListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        movies = MovieDb.objects.all()

        search=request.query_params.get('search')
        if search:
            movies=movies.filter(title__icontains=search)
        genre=request.query_params.get('genre')
        if genre:
            movies = movies.filter(genre__icontains=genre)

        serializer_instance = MovieSerializers(movies, many=True)
        return Response(serializer_instance.data)

    def post(self, request):
        movie = request.data
        serializer_instance = MovieSerializers(data=movie)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Movie Added Successfully",
                "Movie Details": serializer_instance.data
            }, status=201)
        else:
            return Response(serializer_instance.errors, status=400)

class MovieRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        movie_object = get_object_or_404(MovieDb, id=pk)
        serializer_instance = MovieSerializers(movie_object)
        return Response(serializer_instance.data)

    def put(self, request, pk):
        movie_object = get_object_or_404(MovieDb, id=pk)
        serializer_instance = MovieSerializers(data=request.data,instance=movie_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Movie Updated Successfully",
                "Updated Details": serializer_instance.data
            })
        else:
            return Response(serializer_instance.errors, status=400)

    def delete(self, request, pk):
        movie_object = get_object_or_404(MovieDb, id=pk)
        movie_object.delete()
        return Response({"Message": "Movie Deleted Successfully"})

class ShowListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        shows = ShowDb.objects.all()
        serializer_instance = ShowSerializers(shows, many=True)
        return Response({
            "Show Details": serializer_instance.data
        })

    def post(self, request):
        show = request.data
        serializer_instance = ShowSerializers(data=show)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                {"Message": "Show Created Successfully",
                 "Show Details": serializer_instance.data},status=201)
        else:
            return Response(serializer_instance.errors, status=400)

class ShowRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        show_object = get_object_or_404(ShowDb, id=pk)
        serializer_instance = ShowSerializers(show_object)
        return Response({
            "Show Details" : serializer_instance.data,
            "Available Seats" : get_available_seats(show_object)
        })

    def put(self, request, pk):
        show_object = get_object_or_404(ShowDb, id=pk)
        serializer_instance = ShowSerializers(data=request.data,instance=show_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Show Updated Successfully",
                "Updated Details": serializer_instance.data})
        else:
            return Response(serializer_instance.errors, status=400)

    def delete(self, request, pk):
        show_object = get_object_or_404(ShowDb, id=pk)
        show_object.delete()
        return Response({"Message": "Show Deleted Successfully"})

class BookingListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        bookings=BookingDb.objects.filter(user=request.user)
        serializer_intance=BookingSerializers(bookings,many=True)
        return Response(serializer_intance.data)

    def post(self,request):
        serializer_instance=BookingSerializers(data=request.data)
        if serializer_instance.is_valid():
            show=serializer_instance.validated_data['show']
            seats=serializer_instance.validated_data['number_of_seats']
            available_seats=get_available_seats(show)
            if seats <= 0:
                return Response({"Error":"Please select at least one seat."},status=400)
            if seats>available_seats:
                return Response({
                    "Error":"Not enough seats available",
                    "Available Seats": available_seats
                },status=400)
            
            total_amount = show.ticket_price * seats
            serializer_instance.save(user=request.user,total_amount=total_amount)
            return Response({
                "Message": "Tickets Booked Successfully",
                "Booking Details": serializer_instance.data
            },status=201)
        else:
            return Response(serializer_instance.errors,status=400)

class BookingRetrieveDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        booking_object = get_object_or_404(BookingDb,id=pk,user=request.user)
        serializer_instance = BookingSerializers(booking_object)
        return Response(serializer_instance.data)
    def delete(self, request, pk):
        booking_object = get_object_or_404(BookingDb, id=pk, user=request.user)
        if booking_object.status=='Cancelled':
            return Response({"Message":"Booking is already cancelled."},status=400)
        booking_object.status='Cancelled'
        booking_object.save()
        
        return Response({
            "Message": "Booking Cancelled Successfully",
            "Available Seats" : get_available_seats(booking_object.show)
            })

