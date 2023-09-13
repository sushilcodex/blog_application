from blog.models import Blog

class FilterBlogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        filtered_blogs = Blog.objects.exclude(author__id=1)
        request.filtered_blogs = filtered_blogs
        response = self.get_response(request)
        return response
 