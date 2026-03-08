from django.contrib import admin
from .models import *

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']

@admin.register(Rasi)
class RasiAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Nachathiram)
class NachathiramAdmin(admin.ModelAdmin):
    list_display = ['name', 'rasi']
    list_filter = ['rasi']

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Jathagam)
class JathagamAdmin(admin.ModelAdmin):
    list_display = ['name']

class CandidatePhotoInline(admin.TabularInline):
    model = CandidatePhoto
    extra = 1
    max_num = 3

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name', 'gender', 'age', 'rasi', 'status', 'is_paid', 'created_at']
    list_filter = ['gender', 'status', 'is_paid', 'rasi']
    search_fields = ['name', 'uid']
    inlines = [CandidatePhotoInline]

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone']

@admin.register(ShadowCandidate)
class ShadowCandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'notes']
