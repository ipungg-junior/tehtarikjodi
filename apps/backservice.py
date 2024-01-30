from .models import *
import json, random, string,datetime

totalVisitor = VisitorCollection.objects.all()[0]

def generate_random_string():
    # Karakter yang akan digunakan untuk pembuatan string acak
    characters = string.ascii_letters + string.digits  # Huruf besar, huruf kecil, dan angka
    # Menggunakan random.choice() untuk memilih karakter acak 4 kali
    random_string = ''.join(random.choice(characters) for _ in range(4))
    return random_string

def add_visitor():
    try:
        newIdCookie = generate_random_string()
        newVisitor = VisitorRecord(idCookie=newIdCookie)
        newVisitor.save()
        totalVisitor.total += 1
        totalVisitor.save()
        return newIdCookie
    except:
        return 0
 
def auth_login(data):
    if (data['user_id'] == 'scAsDm3'):
        if (data['user_pass'] == 'fxjs7pq'):
            return True
        else:
            return False
    else:
        return False

def checkSession(data):
    try:
        data = data.COOKIES['is_saved']
        return True
    except:
        return False

def get_total_visitor():
    totalVisitor = VisitorCollection.objects.all()[0].total
    return totalVisitor

def get_visitor_today():
    today = datetime.date.today()
    visitor = VisitorRecord.objects.filter(datetime__day=today.day)
    data = 0
    for v in visitor:
        if (v.datetime.day == today.day):
            data += 1
    return data 

def get_visittor_by_date(date):
    visitor = VisitorRecord.objects.filter(datetime__year=date.year, datetime__month=date.month, datetime__day=date.day)
    return visitor