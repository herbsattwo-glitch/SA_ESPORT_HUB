from django.contrib import admin
from django.contrib.auth.models import User
from django.template.response import TemplateResponse


class XboxAdminSite(admin.AdminSite):
    """Custom Xbox admin site with dashboard stats."""

    site_header = 'SA Esports Admin'
    site_title = 'SA Esports Admin'
    index_title = 'Dashboard'

    def index(self, request, extra_context=None):
        from leagues.models import League
        from players.models import Player, ScoutingReport

        extra_context = extra_context or {}
        extra_context.update({
            'league_count': League.objects.count(),
            'player_count': Player.objects.count(),
            'user_count': User.objects.count(),
            'report_count': ScoutingReport.objects.count(),
        })
        return super().index(request, extra_context)


# Override the default admin index method directly
_original_index = admin.site.index

def custom_index(request, extra_context=None):
    from leagues.models import League
    from players.models import Player, ScoutingReport

    extra_context = extra_context or {}
    extra_context.update({
        'league_count': League.objects.count(),
        'player_count': Player.objects.count(),
        'user_count': User.objects.count(),
        'report_count': ScoutingReport.objects.count(),
    })
    return _original_index(request, extra_context)

admin.site.index = custom_index