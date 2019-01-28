from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
import bs4
import logging
import json

from .run_script import NewIn
from .forms import NameForm


def get_name(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        run_script = NewIn()
        run_script.build_url(sku)
        run_script.get_request()
        product = run_script.scrape()

        return JsonResponse(product)

    else:
        form = NameForm()

    return render(request, 'post.html', {'form': form})