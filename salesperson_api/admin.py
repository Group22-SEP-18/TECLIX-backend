from django.contrib import admin
from .models import SalespersonLocation, Leaderboard, LeaderboardPointSchema

# Register your models here.
admin.site.register(SalespersonLocation)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardPointSchema)