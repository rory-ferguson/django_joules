from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from .site_scrape_plp.main_ import run_script
from multiprocessing import Process, Pool
from pathlib import Path
import os.path

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook


live = [['https://www.joules.com']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def main(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            r = run_environment(live)
            
            # write list to csv
            # with open('file.csv', 'w') as file:
            #     for item in my_list:
            #         file.write("%s\n" % item)

            content = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('txt.txt')
            with open(content, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=txt.txt'
                return response

            # file = Path(os.path.abspath(os.path.dirname(__file__))).joinpath('test.xlsx')
            # with open(file, 'rb') as fh:
            #     response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            #     response['Content-Disposition'] = 'attachment; filename=' + str(file)
            #     return response

    else:
        form = SubmitButtonWidget()

    return render(request, 'badges/content.html', {'form': form})

def run_environment(env):
    with Pool(processes=1) as pool:
        p1 = pool.apply_async(run_script, (env[0], ))

        return p1.get()