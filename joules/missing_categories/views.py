from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from .EmptyTrackingMegaMenu import run_script
from multiprocessing import Process, Pool

live = [['https://www.joules.com'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def sresponse(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            env = request.POST.get('env')

            with Pool(processes=3) as pool:
                p1 = pool.apply_async(run_script, (live[0], ))
                p2 = pool.apply_async(run_script, (live[1], ))
                p3 = pool.apply_async(run_script, (live[2], ))

                lst['uk'] = p1.get()
                lst['us'] = p2.get()
                lst['de'] = p3.get()

                return JsonResponse(lst)
        if 'staging' in request.POST.get('env'):
            env = request.POST.get('env')

            with Pool(processes=3) as pool:
                p1 = pool.apply_async(run_script, (staging[0], ))
                p2 = pool.apply_async(run_script, (staging[1], ))
                p3 = pool.apply_async(run_script, (staging[2], ))

                lst['uk'] = p1.get()
                lst['us'] = p2.get()
                lst['de'] = p3.get()

                return JsonResponse(lst)

    else:
        form = SubmitButtonWidget()

    return render(request, 'missing_categories/post.html', {'form': form})