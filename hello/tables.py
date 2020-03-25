import django_tables2 as tables
# from .models import Jobs
from django_tables2.utils import A  
from .models import Job_Results

# class JobsTable(tables.Table):
#     class Meta:
#         model = Jobs
#         attrs = {"class": "table"}

class Job_ResultsTable(tables.Table):
    id = tables.LinkColumn("job_detail", args=[A("id")])
    class Meta:
        model = Job_Results
        attrs = {"class": "table"}