from django.http import HttpResponseRedirect
from django.shortcuts import render
from .run_script import NewIn

from .forms import SkuOne


def get_name(request):
    if request.method == 'POST':
        if 'Product_01' in request.POST:
            form = SkuOne(request.POST or None)
            if form.is_valid():
                sku = form.cleaned_data['sku']  # 203531|WHITE
                run = NewIn()
                run.dict(product='Product_01')
                run.build_url(sku)
                run.get_request()
                product = run.scrape()
                print(product)

                return render(request, 'post.html', {'form': form, 'product': product})
    else:
        form = SkuOne()

    return render(request, 'post.html', {'form': form})
