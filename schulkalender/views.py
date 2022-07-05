from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views.generic.edit import DeleteView, FormView, UpdateView
from .forms import FilterForm, EventForm
from .models import Event


class EventCreate(FormView):
    template_name = "event_create.html"
    form_class = EventForm
    success_url = "/kalender/"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            event = form.save()
            event.author = self.request.user.get_username()
            event.save()
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


def create(request):
    pass


class EventDelete(DeleteView):
    template_name = "event_delete.html"
    model = Event
    success_url = "/kalender/"

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.object.author == self.request.user.get_username() or self.request.user.is_superuser):
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


def delete(request, pk):
    pass


class EventUpdate(UpdateView):
    template_name = "event_update.html"
    model = Event
    fields = ["title", "location", "recipients", "start_date", "start_period", "start_time",
              "end_date", "end_period", "end_time", "all_day", "description"]
    success_url = "/kalender/"

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.object.author == self.request.user.get_username() or self.request.user.is_superuser):
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


def update(request, pk):
    pass


def detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "detail.html", {"event": event})


def filter(request, query, username):
    eventlist = Event.objects.filter(recipients__icontains=query) if (query or query == "") else Event.objects.order_by("start_date")
    user = request.user
    if username:
        eventlist = eventlist.filter(author__exact=username)
    filterform = FilterForm(request.POST, initial={"query": ""})
    context = {
        "eventlist": eventlist,
        "user": user,
        "query": query,
        "filterform": filterform,
    }
    if filterform.is_valid():
        query = filterform.cleaned_data["query"]
        if query == "":
            return render(request, "index.html", context)
        else:
            return HttpResponseRedirect(f"/kalender/filter={query}")
    else:
        return render(request, "index.html", context)


def recipientfilter(request, query):
    return filter(request, query, None)


def ownfilter(request):
    return filter(request, None, request.user.username)


def index(request):
    return filter(request, None, None)
