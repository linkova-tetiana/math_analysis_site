from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")

def questions(request):
    return render(request, "questions.html")

def add_term(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_add.html", context={"terms": terms})
def add_term_anon(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_anon.html", context={"terms": terms})


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(user_name, new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)
def send_term_anon(request):
    if request.method == "POST":
        cache.clear()
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"term": new_term}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term("Аноним", new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_anon_request.html", context)
    else:
        add_term(request)