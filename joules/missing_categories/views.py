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
                r1 = pool.apply_async(run_script, (live[0], ))
                r2 = pool.apply_async(run_script, (live[1], ))
                r3 = pool.apply_async(run_script, (live[2], ))

                lst['uk'] = r1.get()
                lst['us'] = r2.get()
                lst['de'] = r3.get()
            # uk = Process(target=run_script, args=(live[0],))
            # us = Process(target=run_script, args=(live[1],))
            # de = Process(target=run_script, args=(live[2],))
            # uk.start()
            # us.start()
            # de.start()
            # uk.join()
            # us.join()
            # de.join()

            # lst['uk'] = uk
            # lst['us'] = us
            # lst['de'] = de

                print(lst)
                return JsonResponse(lst)
            

    else:
        form = SubmitButtonWidget()

    return render(request, 'missing_categories/post.html', {'form': form})