from typing import List, Optional
from ninja import NinjaAPI, Schema
from .models import Author, Genre, Language, Book, BookInstance
from django.shortcuts import get_object_or_404
from datetime import date
from ninja.security import django_auth

api = NinjaAPI()


class UserSchema(Schema):
    id: int
    username: str
    password: str

    class Config:
        extra = "forbid"

  
class AuthorSchema(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None

    class Config:
        extra = "forbid"

class GenreSchema(Schema):
    id: int
    name: str

    class Config:
        extra = "forbid"

class LanguageSchema(Schema):
    id: int
    name: str

    class Config:
        extra = "forbid"

class BookSchema(Schema):
    id: int
    title: str
    author: AuthorSchema = None
    summary: str
    isbn: str
    genre: GenreSchema

    class Config:
        extra = "forbid"

class BookInstanceSchema(Schema):
    id: int
    book: BookSchema = None
    imprint: str
    due_back: date = None

    language: LanguageSchema = None
    borrower: UserSchema = None
    status: str

    class Config:
        extra = "forbid"



@api.get("/authors", response=List[AuthorSchema])
def get_all_authors(request):
    return Author.objects.all()

@api.get("/authors/{author_id}", response=AuthorSchema)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id)
    return author

@api.get("/genres", response=List[GenreSchema])
def get_all_genres(request):
    return Genre.objects.all()

@api.get("/languages", response=List[LanguageSchema])
def get_all_languages(request):
    return Language.objects.all()

@api.get("/genres/{genre_id}", response=GenreSchema)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, pk=genre_id)
    return genre

@api.get("/languages/{language_id}", response=LanguageSchema)
def get_language(request, language_id: int):
    language = get_object_or_404(Language, pk=language_id)
    return language

@api.post('/authors', auth=django_auth)
def create_author(request, payload: AuthorSchema):
    author = Author.objects.create(**payload.dict())
    return {"id": author.id}

@api.post("/genres", auth=django_auth)
def create_genre(request, payload: GenreSchema):
    genre = Genre.objects.create(**payload.dict())
    return {"id": genre.id}

@api.post("/languages", auth=django_auth)
def create_language(request, payload: LanguageSchema):
    language = Language.objects.create(**payload.dict())
    return {"id": language.id}

@api.put('/authors/{author_id}', auth=django_auth)
def update_author(request, author_id: int, payload: AuthorSchema):
    author = get_object_or_404(Author, pk=author_id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.put("/genres/{genre_id}", auth=django_auth)
def update_genre(request, genre_id: int, payload: GenreSchema):
    genre = get_object_or_404(Genre, pk=genre_id)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

@api.put("/languages/{language_id}", auth=django_auth)
def update_language(request, language_id: int, payload: LanguageSchema):
    language = get_object_or_404(Language, pk=language_id)
    for attr, value in payload.dict().items():
        setattr(language, attr, value)
    language.save()
    return {"success": True}

@api.delete('/authors/{author_id}', auth=django_auth)
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id)
    author.delete()
    return {"success": True}

@api.delete("/genres/{genre_id}", auth=django_auth)
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, pk=genre_id)
    genre.delete()
    return {"success": True}

@api.delete("/languages/{language_id}", auth=django_auth)
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, pk=language_id)
    language.delete()
    return {"success": True}


@api.get("/books", response=List[BookSchema])
def get_all_books(request):
    return Book.objects.all()

@api.get("/books/{book_id}", response=List[BookInstanceSchema])
def get_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    BookInstance.objects.select_related('book').filter(book=book)
    return book