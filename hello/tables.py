import django_tables2 as tables
from .models import Jobs
from django_tables2.utils import A  
from .models import Job_Results

class JobsTable(tables.Table):
    class Meta:
        model = Jobs
        attrs = {"class": "table"}
        fields = ('id', 'input_text', 'created_date', 'completed_date')

class Job_ResultsTable(tables.Table):
    id = tables.LinkColumn("job_detail", args=[A("id")])
    class Meta:
        model = Job_Results
        attrs = {"class": "table"}
        template_name = "django_tables2/bootstrap.html"

# completed_date, created_date, id, input_text, job_results, notes, user, user_id