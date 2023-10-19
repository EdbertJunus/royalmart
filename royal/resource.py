from import_export import resources
from .models import SalesDetail

class SalesResource(resources.ModelResource):
    class Meta:
        model = SalesDetail