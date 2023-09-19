from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class LandingPage(View):
    context = ""

    def get(self, request):
        return render(request, 'landing.html', context={}, content_type='text/html')

    def post(self, request):
        pass


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class Simulation(View):
    context = ""

    def get(self, request):
        return render(request, 'form.html', context={}, content_type='text/html')
    
    def post(self, request):
        if (self.context == 'post-calculate'):
            body_json = request.bodya
            pass
        
        pass