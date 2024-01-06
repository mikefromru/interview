from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404


from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Subject

from django.contrib.auth.mixins import UserPassesTestMixin


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SubjectListView(SuperuserRequiredMixin, ListView):
    model = Subject


class SubjectDetailView(SuperuserRequiredMixin, DetailView):
    model = Subject


class SubjectDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Subject


class SubjectUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Subject


class SubjectCreateView(SuperuserRequiredMixin, CreateView):
    model = Subject

