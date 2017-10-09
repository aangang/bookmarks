from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

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