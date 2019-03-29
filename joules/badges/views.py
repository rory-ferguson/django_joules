from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from .site_scrape_plp.main_ import run_script
from multiprocessing import Process, Pool
from pathlib import Path
import os.path

from django.views.static import serve

live = [['https://www.joules.com']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def main(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            # run_environment(live)

            file = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('test.xlsx')
            
            return serve(request, file)

    else:
        form = SubmitButtonWidget()

    return render(request, 'badges/content.html', {'form': form})

def run_environment(env):
    with Pool(processes=1) as pool:
        p1 = pool.apply_async(run_script, (env[0], ))


