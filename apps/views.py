from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from .models import *
from .backservice import *
import json, datetime
from django.core.serializers import serialize


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class LandingPage(View):
    context = ""

    def get(self, request):
        article = Article.objects.all()
        try:
            # Ambil cookie sesi dari landing page, lacak di DB, buat baru jika tidak ada
            idCookie = request.COOKIES['idCookie']
            return render(request, 'landing.html', content_type='text/html', context={'idCookie': idCookie, 'article_list': article})
        except KeyError:
            newIdCookie = add_visitor()
            response = render(request, 'landing.html', content_type='text/html', context={'idCookie': newIdCookie, 'article_list': article})
            response.set_cookie('idCookie', newIdCookie, max_age=1800)
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
                newIdCookie = add_visitor()
                response = render(request, 'form.html', content_type='text/html', context={'idCookie': newIdCookie})
                response.set_cookie('idCookie', newIdCookie, max_age=180)
                return response
            
        if (self.context == "report-simulation"):
            # Check cookie exist or not
            try:
                idCookie = request.COOKIES['idCookie']
                print(idCookie)
                try:
                    # Ambil data form dari DB masukan ke context
                    form = FormCollection.objects.get(idCookie=idCookie)
                    ctx = {
                        'idCookie': idCookie,
                        'no_hp': form.no_hp,
                        'jumlah_cup': form.jumlah_cup,
                        'omset_kotor': form.omset_kotor,
                        'hpp': form.hpp,
                        'laba_kotor': form.laba_kotor,
                        'laba_bersih': form.laba_bersih,
                        'sewa_bangunan': form.sewa_bangunan,
                        'bep': form.bep
                        }
                    return render(request, 'propose-roi.html', context=ctx, content_type='text/html')
                except ObjectDoesNotExist:
                    print("Tidak ada model form tersebut.")
                    return redirect(f'/simulasi-investasi/')
            except:
                print("Cookie tidak ditemukan.")
                return redirect(f'/simulasi-investasi/')
                
    def post(self, request):
        if (self.context == 'post-calculate'):
            # Mengambil data JSON dari permintaan
            try:                
                idCookie = request.COOKIES['idCookie']                
                dataJson = json.loads(request.body)
                # Cek apakah data sudah ada dengan id cookie tersebut
                try:
                    latForm = FormCollection.objects.get(idCookie=idCookie)
                    resp = {}
                    resp['status'] = '400'
                    return JsonResponse(resp)
                except:
                    form = FormCollection()
                    form.idCookie = idCookie
                    form.no_hp = str(dataJson['no_hp'])
                    form.jumlah_cup = str(dataJson['jumlah_cup'])
                    form.omset_kotor = str(dataJson['omset_kotor'])
                    form.hpp = str(dataJson['hpp'])
                    form.karyawan = str(dataJson['karyawan'])
                    form.laba_kotor = str(dataJson['laba_kotor'])
                    form.listrik = str(dataJson['listrik'])
                    form.lain = str(dataJson['biaya_lain'])
                    form.operasional = str(dataJson['operasional'])
                    form.sewa_bangunan = str(dataJson['sewa_bangunan'])
                    form.laba_bersih = str(dataJson['laba_bersih'])
                    form.bep = str(dataJson['bep'])
                    form.save()
                    resp = {}
                    resp['status'] = '200'
                    return JsonResponse(resp)
            except:
                resp = {}
                resp['status'] = '401'
                return JsonResponse(resp)
        

class DashboardAdmin(View):
    context = ""

    def get(self, request, id=0):
        stateUser = checkSession(request)
        if (self.context == "login"):
            if (stateUser == False):
                return render(request, "sign-in.html", context={})
            else:
                return redirect('/insight/')
        if (self.context == "insight"):
            if (stateUser):
                now = datetime.date.today()
                formCollection = FormCollection.objects.all().order_by('-created_at')[:20]
                totalVisitor = get_total_visitor()
                visitorToday = get_visittor_by_date(now)
                visitor_with_datenow = get_visittor_by_date(now)
                article = Article.objects.all()
                count_today = 0
                for i in visitorToday:
                    if (now.day == i.datetime.day):
                        count_today += 1
                return render(request, "insight-dev.html", context={'collections': formCollection, 'total_visitor':totalVisitor, 'visitor_today': count_today, 'visitor_data': visitor_with_datenow, 'article_list': article})
            else:
                return redirect('/login/')
            
        if (self.context == "detail"):
            if (stateUser):
                article = Article.objects.get(id=id)
                return render(request, "insight-detail.html", context={'article': article})
            else:
                return redirect('/login/')

    def post(self, request, id=0):
        if (self.context == 'detail'):
            article = Article(id=request.POST.get('id'))
            if (article is not None):
                if (request.FILES.get('image', None) is not None):
                    article.setTitle(request.POST.get('title', None))
                    article.setReferense(request.POST.get('reference', None))
                    article.img = (request.FILES.get('image'))
                    article.save()
                else:
                    article.setTitle(request.POST.get('title', None))
                    article.setReferense(request.POST.get('reference', None))
                    article.save(update_fields=['article_title', 'reference_link'])
                status = JsonResponse({'info': 'success'})
            else:
                status = JsonResponse({'info': 'Internal Server Error (500) , DB object not found!'})
                
            return status
        if (self.context == "login"):
            auth = auth_login(json.loads(request.body))
            if (auth):
                response = HttpResponse()
                response.set_cookie('is_saved', 'true', max_age=5200)
                return response
            else:
                return redirect('/login/')
        if (self.context == "logout"):
            return redirect('')

        if (self.context == "filter-visitor-by-date"):
            search_date = json.loads(request.body)
            search_date = datetime.datetime.strptime(search_date, "%d-%m-%Y")
            visitor_with_date = get_visittor_by_date(search_date)
            jsonDump = {}
            count_idx = 1
            for idx, i in enumerate(visitor_with_date):
                if (search_date.day == i.datetime.day):
                    jsonItem = {}  
                    jsonItem['idCookie'] = i.idCookie
                    jsonItem['datetime'] = (f'{i.datetime.day}/{i.datetime.month}/{i.datetime.year}')
                    jsonDump[count_idx] = jsonItem
                    count_idx += 1
            ret = JsonResponse(jsonDump, safe=False)
            return ret


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class NotFoundPage(View):
    context = ""

    def get(self, request):
        try:
            # Ambil cookie sesi dari landing page, lacak di DB, buat baru jika tidak ada
            idCookie = request.COOKIES['idCookie']
            return render(request, '404.html', content_type='text/html', context={'idCookie': idCookie})
        except KeyError:
            newIdCookie = generate_random_string()
            response = render(request, '404.html', content_type='text/html', context={'idCookie': newIdCookie})
            response.set_cookie('idCookie', newIdCookie, max_age=180)
            return response

    def post(self, request):
        pass