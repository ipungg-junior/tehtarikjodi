from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import json, random, string

def generate_random_string():
    # Karakter yang akan digunakan untuk pembuatan string acak
    characters = string.ascii_letters + string.digits  # Huruf besar, huruf kecil, dan angka
    # Menggunakan random.choice() untuk memilih karakter acak 4 kali
    random_string = ''.join(random.choice(characters) for _ in range(4))
    return random_string

@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class LandingPage(View):
    context = ""

    def get(self, request):
        try:
            # Ambil cookie sesi dari landing page, lacak di DB, buat baru jika tidak ada
            idCookie = request.COOKIES['idCookie']
            return render(request, 'landing.html', content_type='text/html', context={'idCookie': idCookie})
        except KeyError:
            newIdCookie = generate_random_string()
            response = render(request, 'landing.html', content_type='text/html', context={'idCookie': newIdCookie})
            response.set_cookie('idCookie', newIdCookie, max_age=180)
            return response

    def post(self, request):
        pass


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class Simulation(View):
    context = ""

    def get(self, request):
        if (self.context == "simulation"):
            try:
                # Ambil cookie sesi dari landing page, lacak di DB, buat baru jika tidak ada
                idCookie = request.COOKIES['idCookie']
                return render(request, 'form.html', content_type='text/html', context={'idCookie': idCookie})
            except KeyError:
                newIdCookie = generate_random_string()
                response = render(request, 'form.html', content_type='text/html', context={'idCookie': newIdCookie})
                response.set_cookie('idCookie', newIdCookie, max_age=180)
                return response
            
        if (self.context == "report-simulation"):
            idCookie = request.COOKIES['idCookie']
            # Ambil data form dari DB masukan ke context
            ctx = {
                'idCookie': idCookie,
                'no_hp': ''
                }
            return render(request, 'propose-roi.html', context=ctx, content_type='text/html')
    
    def post(self, request):
        if (self.context == 'post-calculate'):
            # Mengambil data JSON dari permintaan
            data = json.loads(request.body)
            idCookie = request.COOKIES['idCookie']
            # Lakukan save database
            return redirect(f'/simulasi-investasi/report/{idCookie}')