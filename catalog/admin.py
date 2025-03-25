from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.TabularInline):
  model = Book

  extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

  """
  You can change the order of declaration, which fields are displayed (or excluded), 
  whether sections are used to organize the information, whether fields are displayed 
  horizontally or vertically, and even what edit widgets are used in the admin forms.
  """
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

  inlines = [BookInline]

class BooksInstanceInline(admin.TabularInline):
  model = BookInstance

  extra = 0


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'display_genre')

  inlines = [BooksInstanceInline]



# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book', 'status', 'borrower', 'due_back', 'id')
  list_filter = ('status', 'due_back')

  fieldsets = (
    (None, {
      'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
      'fields': ('status', 'due_back', 'borrower')
    }),
    )
  


