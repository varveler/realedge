from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from .models import UpGapper
from .serializers import GapperSerializer

# Create your views here.
def homepage(request):
    return render(request, '_next/out/index.html')


@csrf_exempt
def gappers(request):
    if request.method == 'GET':
        gappers = UpGapper.objects.all()
        serializer = GapperSerializer(gappers, many=True)
        return JsonResponse(serializer.data, safe=False)


def gapper_detail_view(request, _id):
   return render(request, '_next/out/gappers/[id].html', {'id': _id})


@csrf_exempt
def gapper_detail(request, _id):
    if request.method == 'GET':
        ticker = _id.split('-')[0]
        date = _id.split('-')[1]
        gapper = UpGapper.objects.filter(ticker=ticker, date__year=date[0:4], date__month=date[4:6], date__day=date[6:8])
        if not gapper:
            return
        gapper = gapper[0]
        serializer = GapperSerializer(gapper)
        return JsonResponse(serializer.data)
