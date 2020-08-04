from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = []
    visiters = Visit.objects.filter(leaved_at=None)
    for one_visiter in visiters:
      non_closed_visits.append({
        "who_entered": one_visiter.passcard.owner_name,
        "entered_at": one_visiter.entered_at,
        "duration": one_visiter.format_duration(),
        "is_strange": one_visiter.is_strange(),
      })
    
    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
