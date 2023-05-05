# from django.forms import ValidationError
# from products.models import Product


# class StockValidate:
#     def __init__(self, pk):
#         self.pk = pk

#     def __call__(self, value):
#         product = Product.objects.get(pk=self.pk)
#         amount = product.stock
#         if value > amount:
#             raise ValidationError("Quantity exceeds the stock")
