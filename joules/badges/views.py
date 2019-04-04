from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from multiprocessing import Process, Pool
import csv
from .site_scrape_plp.main import run_script

live = [['https://www.joules.com']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def main(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            lst = run_environment(live)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            writer = csv.writer(response)
            for i in lst:
                writer.writerow(i)

            return response

    else:
        form = SubmitButtonWidget()

    return render(request, 'badges/content.html', {'form': form})


def run_environment(env):
    with Pool(processes=1) as pool:
        p1 = pool.apply_async(run_script, (env[0], ))

        return p1.get()