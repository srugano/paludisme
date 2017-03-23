from jsonview.decorators import json_view
from bdiadmin.models import District, Province, ProfileUser
from bdiadmin.serializers import ProvinceSerializer, DistrictSerializer, CDSSerializer
from django.http import JsonResponse
import json
from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets
from bdiadmin.forms import *
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, CreateView
from cmam_app.utils import get_adminqueryset
from django.contrib.auth.models import User


@json_view
def get_district(request, pk):
    districts = get_adminqueryset(request, District.objects.filter(province=pk).values('id', 'name'))
    district = []
    for i in districts:
        district.append({i['id']: i['name']})
    return JsonResponse(json.dumps(district), safe=False)


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class CDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = CDS.objects.all()
    serializer_class = CDSSerializer

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = ProfileUserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, ProfileUser, fields=('telephone', 'level'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = ProfileUserForm(request.POST, instance=user)
            formset = ProfileInlineFormset(request.POST, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/bdiadmin/profile/')

        return render(request, "bdiadmin/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        return HttpResponseRedirect('/bdiadmin/profile/')


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
