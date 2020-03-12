import django_tables2 as tables
from .models import Jobs

class JobsTable(tables.Table):
    class Meta:
        model = Jobs
        attrs = {"class": "table"}