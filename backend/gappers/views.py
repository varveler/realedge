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
