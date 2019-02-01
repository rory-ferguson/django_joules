from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from .EmptyTrackingMegaMenu import Main, run_script

live = [['https://www.joules.com'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def sresponse(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            env = request.POST.get('env')
            uk = run_script(env=live[0])
            us = run_script(env=live[1])
            de = run_script(env=live[2])
            lst['uk'] = uk
            lst['us'] = us
            lst['de'] = de
            print(lst)
            return JsonResponse(lst)

            # form = SubmitButtonWidget()
            # return render(request, 'missing_categories/post.html', {'form': form, 'uk': uk, 'us': us, 'de': de})
            

    else:
        form = SubmitButtonWidget()

    return render(request, 'missing_categories/post.html', {'form': form})