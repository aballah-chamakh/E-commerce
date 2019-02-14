from django.contrib import admin
from .models import Product,ParaCustomProduct,ClientCustomProduct

product_models = [Product,ParaCustomProduct,ClientCustomProduct]

for model in product_models :
    admin.site.register(model)
