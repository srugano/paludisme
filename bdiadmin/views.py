from bdiadmin.models import District, Province, ProfileUser
from bdiadmin.serializers import ProvinceSerializer, DistrictSerializer, CDSSerializer
from django.shortcuts import HttpResponseRedirect
from rest_framework import viewsets
from bdiadmin.forms import *
from django.views.generic import ListView, CreateView
import django_filters.rest_framework


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('code', 'name')


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('code', 'name', 'province')


class CDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = CDS.objects.all()
    serializer_class = CDSSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('code', 'name', 'district')


# @login_required
# def edit_user(request, pk):
#     user = User.objects.get(pk=pk)
#     user_form = ProfileUserForm(instance=user)

#     ProfileInlineFormset = inlineformset_factory(User, ProfileUser, fields=('telephone', 'level'))
#     formset = ProfileInlineFormset(instance=user)

#     if request.user.is_authenticated() and request.user.id == user.id:
#         if request.method == "POST":
#             user_form = ProfileUserForm(request.POST, instance=user)
#             formset = ProfileInlineFormset(request.POST, instance=user)

#             if user_form.is_valid():
#                 created_user = user_form.save(commit=False)
#                 formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

#                 if formset.is_valid():
#                     created_user.save()
#                     formset.save()
#                     return HttpResponseRedirect('/bdiadmin/profile/')

#         return render(request, "bdiadmin/account_update.html", {
#             "noodle": pk,
#             "noodle_form": user_form,
#             "formset": formset,
#         })
#     else:
#         return HttpResponseRedirect('/bdiadmin/profile/')


class ProfileUserListView(ListView):
    model = ProfileUser
    paginate_by = 25


class ProfileUserCreateView(CreateView):
    model = ProfileUser
    form_class = ProfileUserForm

    def get_success_url(self):
        return HttpResponseRedirect('/bdiadmin/profile/')

    def form_valid(self, form, **kwargs):
        user_form = UserCreateForm(self.request.POST)
        if user_form.is_valid:
            new_user = user_form.save()
            profile = ProfileUser.objects.get(user=new_user)
            profile.telephone = form.cleaned_data['telephone']
            profile.level = form.cleaned_data['level']
            profile.save()
            form.send_email(self.request)
            return self.get_success_url()
        else:
            return HttpResponseRedirect('/bdiadmin/profile/')

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
