from django.shortcuts import render, redirect
from .forms import Support1, Admin
from django.core.mail import send_mail
from django.urls import reverse


def support12(request):
    form1 = Support1(request.POST or None, request.FILES or None)
    if form1.is_valid():
        subject = form1.cleaned_data['subject']
        message = form1.cleaned_data['message']
        form1.save()

        send_mail(
            subject,
            message,
            'gonderen@example.com',
            ['efecnkose@gmail.com'],
            fail_silently=False,
        )

        return redirect(reverse('home'))  # Anasayfaya yönlendirme işlemi

    context = {
        'form': form1,
    }

    return render(request, "contact.html", context)



