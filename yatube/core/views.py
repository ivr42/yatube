from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, "core/404.html", {"path": request.path}, status=404)


def handler500(request, *args, **kwargs):
    return render(request, "core/500.html", status=500)


def handler403(request, *args, **kwargs):
    return render(request, "core/403.html", status=403)


def csrf_failure(request, reason=""):
    return render(request, "core/403csrf.html")
