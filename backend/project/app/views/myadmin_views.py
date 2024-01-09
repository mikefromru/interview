from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404

from django.views import View
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Subject, Question

from django.contrib.auth.mixins import UserPassesTestMixin

from ..forms import SubjectCreateForm


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SubjectListView(SuperuserRequiredMixin, ListView):
    model = Subject
    template_name = 'myadmin/subject_list.html'


class SubjectDetailView(SuperuserRequiredMixin, View):

    template_name = 'myadmin/subject_detail_list.html'

    def get(self, request, id, lang='en_lang'):
        print(lang, ' <<<<<<')
        queryset = Question.objects.filter(name__id=id).all().values('id', lang)
        print(queryset[:3], ' <<<<<<<<<<<<<<<<<<<<')
        return render(request, self.template_name, {'object': queryset})


# class NewSubject(SuperuserRequiredMixin, View):

#     template_name = 'myadmin/subject_detail_list.html'

#     def get(self, reuest):
#         return HttpResponse('This is GET method')
    


class SubjectDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Subject
    success_url = '/myadmin'
    template_name = 'myadmin/subject-confirm-delete.html'


class SubjectUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Subject


class SubjectCreateView(SuperuserRequiredMixin, CreateView):
    # model = Subject
    template_name = 'myadmin/create-subject.html'

    def get(self, request, *args, **kwargs):
        context = {'form': SubjectCreateForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SubjectCreateForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save()
            subject.save()
            # return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
            return redirect('/myadmin')
        return render(request, self.template_name, {'form': form})