from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404 
from .models import Image
from django.http import HttpResponse 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required
def image_create(request):
    """
    View for creating an Image using the JavaScript Bookmarklet.
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            #如果这个表单是合法的，我们将新建一个 Image 实例
            new_item = form.save(commit=False)
            # assign current user to the item
            #我们将绑定当前用户（user）到一个新的 iamge 对象。这样我们就可以知道是谁上传了每一张图片
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            #使用 Django 的信息框架创建了一条上传成功的消息然后重定向用户到新图像的规范URL
            #我们没有在 Image 模型中实现 get_absolute_url() 方法，我们等会儿将编写它
            return redirect(new_item.get_absolute_url())
    else:
            # build form with data provided by the bookmarklet via GET
            form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images','form': form})
    
def image_detail(request, id, slug): 
    image = get_object_or_404(Image, id=id, slug=slug) 
    return render(request, 'images/image/detail.html', {'section': 'images','image': image})


@login_required 
def image_list(request): 
    images = Image.objects.all() 
    paginator = Paginator(images, 8) 
    page = request.GET.get('page') 
    try: 
        images = paginator.page(page) 
    except PageNotAnInteger: 
        # If page is not an integer deliver the first page 
        images = paginator.page(1) 
    except EmptyPage: 
        if request.is_ajax(): 
            # If the request is AJAX and the page is out of range return an empty page 
            return HttpResponse('') 
        # If page is out of range deliver last page of results 
        images = paginator.page(paginator.num_pages) 
    #ajax has bug can not display  need debug
    #images = Image.objects.all() 
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images}) 
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})






#Django 同样也提供了 require_POST 装饰器来只允许 POST 请求
#一个可让你传递一组请求方法作为参数的 require_http_methods 装饰器
#使用 Django 提供的 JsonResponse 类来将给你定的对象转换为一个 JSON 输出
#这个类返回一个带有 application/json 内容类型的 HTTP 响应
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})







