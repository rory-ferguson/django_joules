from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
# from .site_scrape_plp import main
from multiprocessing import Process, Pool

live = [['https://www.joules.com'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def main(request):
    if request.method == 'POST':
        pass


    else:
        form = SubmitButtonWidget()

    return render(request, 'badges/content.html', {'form': form})
