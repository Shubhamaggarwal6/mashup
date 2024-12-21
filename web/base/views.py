from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.conf import settings
#import numpy as np
#import io
# import csv
from django.core.files.storage import default_storage

def home(request):
    context = {'message': "Nothing to see here."}
    if request.method == 'POST':
        try:
            input_file = request.FILES.get('input_file')
            weights = request.POST.get('weights')
            impacts = request.POST.get('impacts')
            email = request.POST.get('email')


            email_message = EmailMultiAlternatives(
                'Song Mashup Result',
                "Please find the attached audio file.",
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            email_message.attach('topsis_results.csv', "hi,low", 'text/csv')
            email_message.send()

            context['message'] = 'Mashup has been sent to your email.'
        except ValueError as ve:
            context['error'] = f"ValueError: {ve}"
        except Exception as e:
            context['error'] = f"An unexpected error occurred: {e}"

        return redirect('home')

    return render(request, "index.html", context)
