from django.shortcuts import render, get_object_or_404, redirect
from .form import ImageForm
from .models import Image
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Create your views here.

def index(request):
    if 'delete_image' in request.POST:
        image_id = request.POST.get('delete_image')
        try:
            image_to_delete = Image.objects.get(id=image_id)
            image_to_delete.delete()
            return HttpResponseRedirect(reverse('index'))
        except Image.DoesNotExist:
            pass
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, 'index.html', {'obj': obj})
        else:
            image = Image.objects.all()
            return render(request, 'index.html', {'image': image, 'form': form})
            pass
    else:
        form = ImageForm()
        image = Image.objects.all()
    return render(request, 'index.html', {'image': image, 'form': form})


def edit_caption(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, "Caption updated successfully.")
            return redirect('index')
        else:
            messages.error(request, "There was an error updating the caption.")
    else:
        form = ImageForm(instance=image)
    return render(request, 'edit_image.html', {'form': form})