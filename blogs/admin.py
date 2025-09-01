from django.contrib import admin
from .models import Category, Blogs, Comment

# CATEGORY ADMIN
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# BLOG ADMIN
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'blog_image', 'status', 'is_featured', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Superuser can delete any blog
        if request.user.is_superuser:
            return True
        # Regular users can only delete their own blogs
        if obj is not None and obj.author == request.user:
            return True
        return False

# COMMENT ADMIN
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'comment', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# REGISTER MODELS
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blogs, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
