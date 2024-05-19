from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")

def questions(request):
    return render(request, "questions.html")
def materials(request):
    return render(request, "materials.html")
def test(request):
    return render(request, "test.html")
def add_term(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_add.html", context={"terms": terms})
def test_result(request):
    test_results = terms_work.get_test()
    return render(request, "test_result.html", context={"test_results": test_results})
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
def send_test(request):
    if request.method == "POST":
        cache.clear()
        answer1 = request.POST.get("example1")
        answer2 = request.POST.get("example2")
        answer3 = request.POST.get("example3")
        answer4 = request.POST.get("example4")

        answer = [answer1, answer2, answer3, answer4]
        context = {"questions": answer}
        new_line = f"{answer1};{answer2};{answer3};{answer4}"
        with open("./data/test.csv", "r", encoding="utf-8") as f:
            existing_terms = [l.strip("\n") for l in f.readlines()]
            title = existing_terms[0]
            old_terms = existing_terms[1:]
        terms_sorted = old_terms + [new_line]
        new_terms = [title] + terms_sorted
        with open("./data/test.csv", "w", encoding="utf-8") as f:
            f.write("\n".join(new_terms))
        context = {"term": new_line}
        return render(request, "test_request.html", context)
    else:
        test(request)
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