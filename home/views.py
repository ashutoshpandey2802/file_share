# views.py

import os
import zipfile
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def handle_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'status': 400, 'message': 'No files uploaded'})

        folder_name = 'uploads'
        upload_path = os.path.join(settings.MEDIA_ROOT, folder_name)
        os.makedirs(upload_path, exist_ok=True)

        for file in files:
            with open(os.path.join(upload_path, file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        zip_path = os.path.join(settings.MEDIA_ROOT, 'downloads', f'{folder_name}.zip')
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                zipf.write(os.path.join(upload_path, file.name), file.name)

        return JsonResponse({'status': 200, 'message': 'Files uploaded successfully', 'data': {'folder': folder_name}})
    else:
        return JsonResponse({'status': 405, 'message': 'Method not allowed'})

def home(request):
    return render(request, 'home.html')
