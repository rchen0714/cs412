from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result, Voter
import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    '''View to list voter records.'''

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        
        # start with entire queryset
        voters = super().get_queryset().order_by('last_name', 'first_name')
 
 
        # Filtering fields 

        # filter by party affiliation
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(party_affiliation__iexact=party)

        # filter by minimum date of birth (year)
        if 'min_year' in self.request.GET:
            min_year = self.request.GET['min_year']
            if min_year:
                voters = voters.filter(date_of_birth__year__gte=min_year)

        # filter by maximum date of birth (year)
        if 'max_year' in self.request.GET:
            max_year = self.request.GET['max_year']
            if max_year:
                voters = voters.filter(date_of_birth__year__lte=max_year)
                
        # filter by voter score
        if 'score' in self.request.GET:
            score = self.request.GET['score']
            if score:
                voters = voters.filter(voter_score=score)


        # filter by election participation
        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town=True)

        return voters
    
 
class ResultDetailView(DetailView):
    '''View to show detail page for one result.'''
 
 
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'
 
 
    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        r = context['r']
 
        # create graph of first half/second half as pie chart:
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds , second_half_seconds]
        
        # generate the Pie chart
        fig = go.Pie(labels=x, values=y) 
        title_text = f"Half Marathon Splits"
        # obtain the graph as an HTML div"
        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['graph_div_splits'] = graph_div_splits
 
		# create graph of runners who passed/passed by
        x= [f'Runners Passed by {r.first_name}', f'Runners who Passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",               
                                         ) 
        context['graph_div_passed'] = graph_div_passed
        return context