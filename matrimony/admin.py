from django.contrib import admin
from .models import (State, District, Rasi, Nachathiram, Profession,
                     JathagamType, Planet, Sevadosham, CandidateStatus,
                     MaleCandidate, FemaleCandidate, CandidatePhoto,
                     AdminProfile, ShadowCandidate)

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order']
    ordering = ['order']

@admin.register(Sevadosham)
class SevadoshamAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order']

@admin.register(CandidateStatus)
class CandidateStatusAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order']

@admin.register(JathagamType)
class JathagamTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Rasi)
class RasiAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Nachathiram)
class NachathiramAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rasi']
    list_filter = ['rasi']

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    list_filter = ['state']

@admin.register(MaleCandidate)
class MaleCandidateAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name', 'status', 'created_at']
    search_fields = ['uid', 'name']
    list_filter = ['status', 'rasi']

@admin.register(FemaleCandidate)
class FemaleCandidateAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name', 'status', 'created_at']
    search_fields = ['uid', 'name']
    list_filter = ['status', 'rasi']

@admin.register(CandidatePhoto)
class CandidatePhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'male_candidate', 'female_candidate', 'is_primary']

admin.site.register(AdminProfile)
admin.site.register(ShadowCandidate)
