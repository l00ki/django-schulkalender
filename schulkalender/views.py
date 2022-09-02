from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.utils import timezone
from .forms import FilterForm, EventForm, DatePickerInput, TimePickerInput
from .models import Event
from .settings import base_url

from copy import deepcopy
from datetime import date, datetime, time, timedelta
import locale


locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


def event_to_day(event, day, user):
    newday = deepcopy(day)
    newday["recipients"] = event.recipients
    newday["title"] = event.title
    if event.all_day:
        newday["start_time"] = "-/-"
        newday["end_time"] = "-/-"
    else:
        newday["start_time"] = event.start_time
        if type(event.start_time) == time:
            newday["start_time"] = event.start_time.strftime("%H:%M")
        newday["end_time"] = event.end_time
        if type(event.end_time) == time:
            newday["end_time"] = event.end_time.strftime("%H:%M")
    newday["author"] = event.author
    newday["description"] = event.description
    newday["id"] = event.id
    newday["owned"] = user.username == newday["author"] or user.is_superuser
    return newday
    


class EventCreate(FormView):
    template_name = "event_create.html"
    form_class = EventForm
    success_url = f"{base_url}"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            event = form.save()
            event.author = self.request.user.get_username()
            event.save()
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


class EventDelete(DeleteView):
    template_name = "event_delete.html"
    model = Event
    success_url = f"{base_url}"

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.object.author == self.request.user.get_username() or self.request.user.is_superuser):
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


class EventUpdate(UpdateView):
    template_name = "event_update.html"
    form_class = EventForm
    model = Event
    success_url = f"{base_url}"

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated and (self.object.author == user.get_username() or user.is_superuser):
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("nicht authentifiziert")


def detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user 
    owned = event.author == user.username or user.is_superuser
    return render(request, "detail.html", {"event": event, "owned": owned, "user": user})


def filter(request, query, username):
    today = date.today()
    user = request.user
    eventlist = Event.objects.filter(Q(start_date__gte=today))
    if query or query == "":
        q = Q(recipients__icontains=query) | Q(recipients__exact=None)
        eventlist = Event.objects.filter(q)
    if not user.is_authenticated:
        eventlist = eventlist.exclude(teacher_only=True)
    eventlist = eventlist.order_by("start_date")
    if username:
        eventlist = eventlist.filter(author__exact=username)
    if not username and (not query or query == ""):
        eventlist = dayslist(eventlist, user, pad=True)
    else:
        eventlist = dayslist(eventlist, user, pad=False)
    filterform = FilterForm(request.POST, initial={"query": ""})
    context = {
        "eventlist": eventlist,
        "user": user,
        "query": query,
        "filterform": filterform,
    }
    if filterform.is_valid():
        newquery = filterform.cleaned_data["query"]
        if newquery == "" or not newquery:
            context["query"] = query
            return render(request, "index.html", context)
        else:
            return HttpResponseRedirect(f"{base_url}filter={newquery}")
    else:
        return render(request, "index.html", context)


def dayslist(events, user, pad):
    oneday = timedelta(days=1)
    for event in events:
        if not event.recipients:
            event.recipients = "-/-"
        if event.start_time:
            pass
        elif event.start_period:
            event.start_time = str(event.start_period) + ". Std."
        else:
            event.start_time = "-/-"
        if event.end_time:
            pass
        elif event.end_period:
            event.end_time = str(event.end_period) + ". Std."
        else:
            event.end_time = "-/-"
        if not event.description:
            event.description = "-/-"
    today = timezone.localdate()
    dayslist = []
    if pad:
        currentdate = today
        if currentdate.month == 8 and currentdate.day == 1:
            currentdate += oneday
        eventsiter = iter(events)
        event = next(eventsiter, None)
        ongoing = []
        while not (currentdate.month == 8 and currentdate.day == 1):
            days = []
            weekend = currentdate.weekday() >= 5
            daytmp = {"start_date": currentdate.strftime("%a %d.%m.%y"), "weekend": weekend}
            if ongoing:
                for onevent in ongoing:
                    day = event_to_day(onevent, daytmp, user)
                    day["start_time"] = "-/-"
                    day["end_time"] = "-/-"
                    if onevent.end_date < currentdate:
                        day["end_time"] = onevent.end_time
                        if type(onevent.end_time) == time:
                            day["end_time"] = onevent.end_time.strftime("%H:%M")
                    if days:
                        day["start_date"] = ""
                    day["weekend"] = weekend
                    days += [deepcopy(day)]
                    if onevent.end_date < currentdate:
                        ongoing.remove(onevent)
            while event and (event.start_date == currentdate):
                day = event_to_day(event, daytmp, user)
                if len(days) >= 1:
                    day["start_date"] = ""
                if event.end_date and event.end_date != event.start_date:
                    ongoing += [deepcopy(event)]
                    day["end_time"] = "-/-"
                day["weekend"] = weekend
                days += [deepcopy(day)]
                event = next(eventsiter, None)
            if days == [] :
                days += [deepcopy(daytmp)]
            dayslist += days
            currentdate += oneday
            if len(dayslist) > 370: break
    else:
        currentdate = events[0].start_date.min
        for event in events:
            day = {"start_date": "",
                   "recipients": event.recipients,
                   "title": event.title,
                   "start_time": event.start_time,
                   "end_time": event.end_time,
                   "author": event.author,
                   "description": event.description,
                   "id": event.id,
                   "owned": user.username == event.author or user.is_superuser,
                   "weekend": False}
            if type(day["start_time"]) == time:
                day["start_time"] = day["start_time"].strftime("%H:%M")
            if type(day["end_time"]) == time:
                day["end_time"] = day["end_time"].strftime("%H:%M")
            if event.start_date != currentdate:
                currentdate = event.start_date
                day["start_date"] = event.start_date.strftime("%a %d.%m.%y")
                if event.end_date and event.end_date != event.start_date:
                    day["start_date"] += " - " + event.end_date.strftime("%a %d.%m.%y")
            dayslist += [day]
    return dayslist
    

def recipientfilter(request, query):
    return filter(request, query, None)


def ownfilter(request):
    return filter(request, None, request.user.username)


def index(request):
    return filter(request, None, None)
