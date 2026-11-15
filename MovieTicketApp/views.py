from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from MovieTicketApp.models import MovieDb, ShowDb, BookingDb
from MovieTicketApp.serializers import UserSerializer,MovieSerializers,ShowSerializers,BookingSerializers

# Create your views here.
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

class MovieListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        movies = MovieDb.objects.all()
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
        return Response(serializer_instance.data)

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
        return Response(serializer_instance.data)

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
        booking_object.delete()
        return Response({"Message": "Booking Cancelled Successfully"})

        