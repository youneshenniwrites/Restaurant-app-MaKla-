from django.db.models import Q
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import RestaurantLocation
from .forms import RestaurantLocationCreateForm


class RestaurantListView(LoginRequiredMixin, ListView):
    template_name = 'restaurants/restaurant_list.html'

    def get_queryset(self):
        queryset = RestaurantLocation.objects.filter(owner=self.request.user)
        return queryset

    # def get_queryset(self):
    #    slug = self.kwargs.get('slug')
    #    if slug:
    #        queryset = RestaurantLocation.objects.filter(Q(category__iexact=slug) |
    #                                                     Q(category__contains=slug))
    #    else:
    #        queryset = RestaurantLocation.objects.all()
    #    return queryset


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    template_name = 'restaurants/restaurant_detail.html'

    def get_queryset(self):
        queryset = RestaurantLocation.objects.filter(owner=self.request.user)
        return queryset


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'

    def form_valid(self, form):
        '''
        After defining the owner instance in Restaurant model we'll
        override the form_valid method to associate every post data
        to the authenticated user.
        '''
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        '''
        Adds fields to the context data method.
        Makes the template form more flexible.
        '''
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/detail-update.html'

    def get_queryset(self):
        queryset = RestaurantLocation.objects.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = f'Update Restaurant: {name}'
        return context


''' 
function based view to handle model form post data

def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/restaurants/')
    if form.errors:
        print(form.errors)

    context = {'form': form}
    return render(request, 'restaurants/form.html', context)
'''





