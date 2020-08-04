from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for one_visit in visits:
      this_passcard_visits.append({
            "entered_at": one_visit.entered_at,
            "duration": one_visit.format_duration(),
            "is_strange": one_visit.is_strange(),
      })

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
