from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Book, Member, Loan
from .serializers import BookSerializer, MemberSerializer, LoanSerializer


# =========================
# BOOK VIEWSET
# =========================
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


# =========================
# MEMBER VIEWSET
# =========================
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


# =========================
# LOAN VIEWSET (BORROW LOGIC)
# =========================
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        data = request.data

        # =========================
        # VALIDATION
        # =========================
        book_id = data.get("book")
        member_id = data.get("member")
        
        if not book_id:
            return Response(
                {"error": "book field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not member_id:
            return Response(
                {"error": "member field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================
        # SAFE OBJECT FETCHING
        # =========================
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": f"Book with id {book_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response(
                {"error": f"Member with id {member_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================
        # CHECK AVAILABILITY
        # =========================
        if book.available_copies <= 0:
            return Response(
                {"error": "No copies available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================
        # DUE DATE HANDLING
        # =========================
        due_date = data.get("due_date")
        if not due_date:
            due_date = now().date() + timedelta(days=14)

        # =========================
        # CREATE LOAN
        # =========================
        loan = Loan.objects.create(
            book=book,
            member=member,
            borrowed_date=now().date(),
            due_date=due_date,
            is_returned=data.get("is_returned", False)
        )

        # reduce book stock
        book.available_copies -= 1
        book.save()

        # =========================
        # EMAIL (SAFE)
        # =========================
        try:
            if member.email:
                send_mail(
                    subject="📚 Book Borrowed Successfully",
                    message=f"""
Hello {member.name},

You borrowed: {book.title}
Due date: {loan.due_date}

Please return on time.

Library System
""",
                    from_email="adhikarysabu098@gmail.com",
                    recipient_list=[member.email],
                    fail_silently=False
                )
                print(f"✅ Email sent successfully to {member.email}")
            else:
                print(f"⚠️ Member {member.name} has no email address")
        except Exception as e:
            print(f"❌ Email error: {type(e).__name__}: {e}")

        # =========================
        # RESPONSE
        # =========================
        return Response(
            LoanSerializer(loan).data,
            status=status.HTTP_201_CREATED
        )