from pathlib import Path

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from my_project.models import Book, Store, Buyer, Literature, Publishing
from my_project.forms import StoreForm
from django.contrib.auth import authenticate, login, logout

BASE_DIR = Path(__file__).resolve().parent.parent



def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def show_info(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Покупатели").exists():
            buyer = Buyer.objects.get(id_user_id=user.id)
            literature = list(Literature.objects.filter(buyer_id=buyer.id))
            return render(request, 'buyerView.html', {"literature": literature})
        else:
            book = Book.objects.get(id_user_id=user.id)
            stores = list(Store.objects.filter(book=book))
            return render(request, 'bookInfo.html', {"book": book, "stores": stores})
    else:
        return render(request, 'notAccess.html')


def show_book(request, name_literature, id_publishing, id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Покупатели").exists():
        book = Book.objects.get(id_user_id=id_user)
        stores = list(Store.objects.filter(book=book))
        return render(request, 'bookInfo.html', {"book": book, "stores": stores, "name_literature": name_literature, "id_publishing": id_publishing})
    else:
        return render(request, 'notAccess.html')


def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info" + str(cur_user.id))
        else:
            return render(request, 'index.html')
    else:
        print(request.POST)
        if (request.POST.get("email") != None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return redirect("/info")
            except Exception:
                print("Not correct email or pass ")
                return redirect("/")
        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect("/info")


def add_store(request, name_literature, id_publishing, id_user):
    user = request.user
    if request.method == "GET":
        storeForm = StoreForm()
        return render(request, "templateForm.html", {"form": storeForm, "name_literature": name_literature, "id_publishing": id_publishing})
    else:
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.book = Book.objects.get(id_user_id=id_user)
            store.save()
            return redirect(f"/buyerView/{name_literature}/{id_publishing}/{id_user}")
        else:
            pass


def delete_store(request, name_literature, id_publishing, id_user, number_store):
    book_id = Book.objects.get(id_user_id=id_user)
    store = Store.objects.filter(number=number_store, book_id=book_id).first().delete()
    return redirect(f"/buyerView/{name_literature}/{id_publishing}/{id_user}")


def show_publishing_ofLiterature(request, name_literature):
    literature = Literature.objects.get(name_literature=name_literature)
    publishings = literature.publishing.filter(literature=literature.name_literature)
    return render(request, 'buyerViewPublishing.html', {"publishings": publishings, "name_literature": name_literature})


def show_bookFromPublishing(request, id_publishing, name_literature):
    books = Book.objects.filter(publishing=Publishing.objects.get(id=id_publishing))
    return render(request, 'buyerViewBook.html', {"books": books, "name_literature": name_literature, "id_publishing": id_publishing})


# AJAX view

def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def check_numberStore(request, name_literature):
    number = request.GET.get('number', None)
    if (number == ""):
        number = 0
    literature_obj = Literature.objects.get(name_literature=name_literature)
    response = {
        'exist': Store.objects.filter(number__exact=number, literature=literature_obj).exists()
    }
    return JsonResponse(response)




# Create your views here.