from django.contrib import admin
from django import forms
from .models import ProductCategory, ProductBrand, Product, PriceFilter, ProductTag,ProductGallery,ProductQuestionsAnswers,ProductComment
import json

# Custom form for Product model
class ProductAdminForm(forms.ModelForm):
    features_json = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        label="Features"
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # If the instance exists
            self.fields['features_json'].initial = json.dumps(self.instance.get_features(), ensure_ascii=False, indent=4)

    def clean_features_json(self):
        data = self.cleaned_data['features_json']
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON data")

    def save(self, commit=True):
        instance = super(ProductAdminForm, self).save(commit=False)
        instance.set_features(self.cleaned_data['features_json'])
        if commit:
            instance.save()
        return instance

# Custom form for ProductTag model
class ProductTagForm(forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductTagForm, self).__init__(*args, **kwargs)
        # Filter the parent field to show only tags where is_parent = True
        self.fields['parent'].queryset = ProductTag.objects.filter(is_parent=True)

# Registering ProductTagAdmin
@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    form = ProductTagForm  # Use the custom form here
    list_display = ('caption', 'parent')
    search_fields = ('caption', 'parent__caption')

# Registering ProductAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    
    list_display = ('title', 'price', 'category', 'brand', 'is_active')
    search_fields = ('title', 'slug')
    list_filter = ('is_active', 'brand', 'category', 'tags')
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ['brand', 'category', 'tags']  # This requires ProductTag to be registered
    
    # This will show tags in a more accessible way.
    filter_horizontal = ('tags',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'brand', 'short_description','description','colors','rate','satisfaction','image','price','discount_percent','discount_expiry', 'tags', 'is_active')
        }),
        ('Features', {
            'fields': ('features_json',),
            'classes': ('collapse',),
        }),
    )

# Registering other models
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_title', 'is_active', 'icon_name')
    search_fields = ('title', 'url_title')
    list_filter = ('is_active',)
    prepopulated_fields = {"url_title": ("title",)}
    
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_title', 'is_active')
    search_fields = ('title', 'url_title')
    list_filter = ('is_active',)
    prepopulated_fields = {"url_title": ("title",)}
    filter_horizontal = ('category',)
    
@admin.register(PriceFilter)
class PriceFilterAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_price')
    search_fields = ('title',)
    list_filter = ('max_price',)


@admin.register(ProductQuestionsAnswers)
class ProductQuestionsAnswersAdmin(admin.ModelAdmin):
    list_display = ('text','parent')

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('comment','user','rate','buyer')

admin.site.register(ProductGallery)