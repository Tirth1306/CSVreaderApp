from django.shortcuts import render, redirect
from .forms import uploadfile
from django.contrib import messages
import pandas as pd

# Create your views here.
def upload(request):
    if request.method == 'POST':
        form = uploadfile(request.POST, request.FILES)
        if form.is_valid():
            dt = request.FILES['file']
            df = pd.read_csv(dt, header = None, index_col = 0)
            try:
                count = df.apply(lambda x : x.value_counts() , axis = 1)[['p','a']]
                count.columns = ['Present Days','Absent Days']

                count['Total Days'] = len(df.columns)

                count['Percentage'] = count['Present Days']/count['Total Days'] * 100
                del count['Absent Days']
                count = count.round(2)
                data = []
                for index, row in count.iterrows():
                    data.append([index,row['Total Days'],row['Present Days'],row['Percentage']])

                stats = {
                    'data': data,
                    'm80' : len(count[count['Percentage'] >= 80]),
                    'm50' : len(count[count['Percentage'] >= 50]) - len(count[count['Percentage'] >= 80]),
                    'l50' : len(count[count['Percentage'] < 50])
                }
                return render(request, 'CSVreaderApp/report.html', stats)
            except:
                messages.warning(request, 'Not in proper format. Please check info page for more information')
                return redirect('upload')
    else:
        form = uploadfile()
    return render(request, 'CSVreaderApp/upload.html', {'form': form})

def info(request):
    return render(request, 'CSVreaderApp/info.html')