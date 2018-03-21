from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def test_view(request):
    input_string = request.GET.get('units', "")

    # return HttpResponse(input_string)
    return JsonResponse({'units': input_string})
