from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from . import forms
from . import models
# Create your views here.
from django.contrib.auth.models import User

from django.shortcuts import render


@login_required(login_url='login')
def roll_view(request):
    roliklar = models.Rolik.objects.all().order_by('id')
    inroliks_to_update = models.InRolik.objects.filter(
        roliktime__lt=timezone.now(),  # roliktime tugagan
        status='started'  # statusi 'going_on'
    )

    # Har bir rolikni o'zgartirish uchun
    for inrolik in inroliks_to_update:
        inrolik.status = 'finished'  # statusni 'finished' ga o'zgartiramiz
        inrolik.save()
    return render(request, 'cards.html', {'roliklar': roliklar})


@login_required(login_url='login')
def admin_add_roll_view(request):
    rollForm = forms.AddRollForm
    if request.method == 'POST':
        rollForm = forms.AddRollForm(request.POST)
        if rollForm.is_valid():
            rollForm.save()
        else:
            return render(request, 'quiz/admin_add_class.html', {'rollForm': rollForm})
        return HttpResponseRedirect('/admin-view-classes')
    return render(request, 'quiz/admin_add_class.html', {'rollForm': rollForm})


@login_required(login_url='login')
def update_roll(request, roll_id):
    rolik = get_object_or_404(models.Rolik, id=roll_id)
    rolik_s = models.InRolik.objects.all().filter(rolik=rolik).first()
    if request.method == 'POST':
        form = forms.UpdateInRollForm(request.POST, instance=rolik_s)
        if form.is_valid():
            roll_s = form.save(commit=False)
            roll_s.rolik = rolik
            current_time = timezone.now()  # timezone qo'shildi
            roliktime = roll_s.roliktime  # vaqtni offset-aware qilindi
            if roliktime is None:
                roll_s.status = "going_to"
            else:
                if current_time < roliktime:
                    roll_s.status = "started"
                else:
                    roll_s.status = "finished"
            roll_s.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'roll_update.html', {'form': form, 'rolik': rolik})

    else:
        form = forms.UpdateInRollForm(instance=rolik_s)

    return render(request, 'roll_update.html', {'form': form, 'rolik': rolik})
