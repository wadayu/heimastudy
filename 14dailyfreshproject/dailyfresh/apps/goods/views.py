from django.shortcuts import render
from django.views.generic import View

# Create your views here.

# /index
class IndexView(View):
    # 首页
    def get(self,request):
        return render(request,'index.html')
