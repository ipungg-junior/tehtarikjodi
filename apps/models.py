from django.db import models
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your models here.
class VisitorCollection(models.Model):
    total = models.IntegerField()
    total_today = models.IntegerField()

class VisitorRecord(models.Model):
    idCookie = models.CharField(max_length=7)
    datetime = models.DateTimeField(auto_now_add=True)

class FormCollection(models.Model):
    idCookie = models.CharField(max_length=7, default='0', null=True)
    no_hp = models.CharField(max_length=14, default='0', null=True)
    jumlah_cup = models.CharField(max_length=21, default='0', null=True)
    omset_kotor = models.CharField(max_length=21, default='0', null=True)
    hpp = models.CharField(max_length=21, default='0', null=True)
    karyawan = models.CharField(max_length=21, default='0', null=True)
    laba_kotor = models.CharField(max_length=21, default='0', null=True)
    listrik = models.CharField(max_length=14, default='0', null=True)
    lain = models.CharField(max_length=14, default='0', null=True)
    operasional = models.CharField(max_length=14, default='0', null=True)
    sewa_bangunan = models.CharField(max_length=14, default='0', null=True)
    laba_bersih = models.CharField(max_length=17, default='0', null=True)
    bep = models.CharField(max_length=14, default='0', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.idCookie} - 0{self.no_hp}'
    

class Article(models.Model):
    article_title = models.CharField(max_length=40, default='', null=True)
    reference_link = models.CharField(max_length=200, default='', null=True)
    img = models.ImageField(upload_to='media/article/', null=True, blank=True)

    def getPathImage(self):
        return self.img.path

    def setTitle(self, name):
        self.article_title = name

    def setPicture(self, picture):
        self.img = picture
        base_name, ext = os.path.splitext(self.img.name)
        self.img.name = str(self.id) + ext

    def setReferense(self, link):
        self.reference_link = link

    def __str__(self):
        return self.article_title