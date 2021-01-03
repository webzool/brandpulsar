from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView, TemplateView

from main.models import Domain
from users.views import RegisterView
from main.models import Industry
from marketplace.forms import DomainCreateForm

User = get_user_model()


class BecomeASellerView(RegisterView):
    template_name = 'marketplace/become-a-seller.html'

    def form_valid(self, form):
        user = form.instance
        user.user_type=2 # User becomes seller
        user.set_password(form.cleaned_data.get("password1"))
        user.save()
        self.generate_mail(user=user)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            # Meta Tags
            'title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'meta_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'og_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/become-a-seller',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        })
        return context


class DomainCreateView(CreateView):
    model = Domain
    form_class = DomainCreateForm
    # TODO : Create 'Domain Accepted Page' for success_url 
    template_name = 'marketplace/domain/create.html'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request # appends request object to the form
        return kw
    
    def get_success_url(self):
        return reverse_lazy('marketplace:setup-domain', kwargs={'pk' : self.object.pk}) 

    def form_valid(self, form):
        form.owner = self.request.user.pk
        form.save()
        return super().form_valid(form)


class DomainUpdateView(FormView):
    form_class = DomainCreateForm
    template_name = 'marketplace/domain/update.html'

    def get_object(self):
        return get_object_or_404(
            Domain.objects.all(),
            owner=self.request.user, pk=self.kwargs.get("pk")
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = self.get_object()
        return context

    def form_valid(self, form):
        instance = self.get_object()
        name = form.cleaned_data.get("name")
        if name:
            instance.name = name
        length = form.cleaned_data.get("length")
        if length:
            instance.length = length
        extension = form.cleaned_data.get("extension")
        if extension:
            instance.extension = extension
        price = form.cleaned_data.get("price")
        if price:
            instance.price = price
        thumbnail_image = form.cleaned_data.get("thumbnail_image")
        if thumbnail_image:
            instance.thumbnail_image = thumbnail_image
        purpose = form.cleaned_data.get("purpose")
        tags = form.cleaned_data.get("tags")
        if tags:
            for obj in tags:
                instance.tags.add(obj)
        industry = form.cleaned_data.get("industry")
        if industry:
            for obj in industry:
                instance.industry.add(obj)
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:dashboard')


class DomainDeleteView(DeleteView):
    model = Domain
    template_name = 'marketplace/domain/delete.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model.objects.all(),
            owner=self.request.user, pk=self.kwargs.get("pk")
        )
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.status == 'sold':
            return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('users:dashboard')


class DomainSetupView(TemplateView):
    template_name = 'marketplace/domain/setup.html'

    def get_object(self):
        return get_object_or_404(
            Domain.objects.all(),
            owner=self.request.user, pk=self.kwargs.get('pk')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = self.get_object()
        return context


class BrainStormingView(TemplateView):
    template_name = 'marketplace/brainstorming.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'industries': Industry.objects.all(),
            # Meta Tags
            'title': 'Brandpulsar - Brainstorming Tool',
            'meta_description': 'Use domain brainstorming tool of Brand Pulsar to choose among the available domains and get ideas to form your own domain.',
            'og_title': 'Brandpulsar - Brainstorming Tool',
            'og_description': 'Use domain brainstorming tool of Brand Pulsar to choose among the available domains and get ideas to form your own domain.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/marketplace/brainstorming/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }
        
        return context