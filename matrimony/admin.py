from django.contrib import admin
from .models import (State, District, Rasi, Nachathiram, Profession,
                     JathagamType, Planet, Sevadosham, CandidateStatus,
                     TamilYear, TamilMonth, TamilKizhamai, TamilDate, OwnHouse, BirthOrder, RaguKethu, PremiumType,
                     Complexion, Caste, SubCaste, Height, Relation, MaritalStatus,
                     FamilyMember, MaleCandidate, FemaleCandidate, CandidatePhoto,
                     AdminProfile)

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

@admin.register(Complexion)
class ComplexionAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(Height)
class HeightAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(Caste)
class CasteAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(SubCaste)
class SubCasteAdmin(admin.ModelAdmin):
    list_display = ['caste', 'name']
    list_filter = ['caste']

@admin.register(BirthOrder)
class BirthOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(TamilYear)
class TamilYearAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(TamilMonth)
class TamilMonthAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(TamilKizhamai)
class TamilKizhAmaiAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(TamilDate)
class TamilDateAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(OwnHouse)
class OwnHouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order']

@admin.register(RaguKethu)
class RaguKethuAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order']

@admin.register(PremiumType)
class PremiumTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order']

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone', 'alternate_phone']
    fields = ['user', 'location', 'address_line1', 'address_line2', 'address_line3', 'phone', 'alternate_phone', 'email']

admin.site.register(AdminProfile, AdminProfileAdmin)


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['order', 'name']

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['candidate_gender', 'candidate_id', 'name', 'relation', 'marital_status', 'job_info']
