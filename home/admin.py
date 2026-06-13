from django.contrib import admin
from .models import Book, Member, Loan


# =========================
# LOAN INLINE
# =========================
class LoanInline(admin.TabularInline):
    model = Loan
    extra = 0
    fields = ("member", "borrowed_date", "due_date", "is_returned")
    readonly_fields = ("borrowed_date", "due_date")


# =========================
# BOOK ADMIN
# =========================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "genre",
        "available_copies",
    )

    search_fields = ("title", "isbn", "author")
    list_filter = ("genre",)
    readonly_fields = ("id",)
    inlines = [LoanInline]
    ordering = ("id",)


# =========================
# MEMBER ADMIN
# =========================
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    readonly_fields = ("id",)
    ordering = ("id",)


# =========================
# LOAN ADMIN
# =========================
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "member",
        "borrowed_date",
        "due_date",
        "is_returned",
    )

    search_fields = ("book__title", "member__name")
    list_filter = ("is_returned", "borrowed_date", "due_date")
    readonly_fields = ("borrowed_date", "due_date")
    ordering = ("-borrowed_date",)