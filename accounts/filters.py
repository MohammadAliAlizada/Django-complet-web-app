#import django_filters
from django_filters import rest_framework as filters
from .models import *


class OrderFilter(filters.FilterSet):
	class Meta:
		model = Order
		fields = '__ali__'