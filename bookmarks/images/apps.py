from django.apps import AppConfig


class ImagesConfig(AppConfig):
    #name 属性定义该应用完整的 Python 路径。verbose_name 属性设置了这个应用可读的名字。它
    #会在管理站点中显示。 ready() 方法就是我们为这个应用导入信号的地方
    name = 'images'
    verbose_name = 'Image bookmarks'
    def ready(self):
        # import signal handlers
        import images.signals