from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from . models import Voter
from datetime import date
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
        all_voters = super().get_queryset().order_by('last_name', 'first_name')
 
        # Filtering fields 

        party = self.request.GET.get('party')

        if party:
            all_voters = all_voters.filter(party_affiliation__iexact=party)
        
        min_year = self.request.GET.get('min_year')
        if min_year:
            all_voters = all_voters.filter(date_of_birth__year__gte=min_year)

        max_year = self.request.GET.get('max_year')
        if max_year:
            all_voters = all_voters.filter(date_of_birth__year__lte=max_year)
        
        score = self.request.GET.get('score')
        if score:
            all_voters = all_voters.filter(voter_score=score)
        
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                all_voters = all_voters.filter(**{field: True})
        
        return all_voters
    
    def get_context_data(self, **kwargs):
        """Provide year list for dropdowns and persist selected filters."""
        context = super().get_context_data(**kwargs)

        current_year = date.today().year
        context['years'] = list(range(current_year, 1919, -1))
        context['scores'] = range(1, 6)

        context['selected_party'] = self.request.GET.get('party')
        context['selected_min_year'] = self.request.GET.get('min_year')
        context['selected_max_year'] = self.request.GET.get('max_year')
        context['selected_score'] = self.request.GET.get('score')

        context['form_action'] = 'voter_list'

        return context
    

class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''
 
 
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs):
        """Add Google Maps link to context."""
        
        context = super().get_context_data(**kwargs)
        v = context['v']

        address = f"{v.residential_street_number} {v.residential_street_name}, Newton, MA {v.residential_zip_code}"
        g_map = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
        context['maps_link'] = g_map
        
        return context

class VoterGraphsView(TemplateView):
    '''View to show various graphs about voters.'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'v'

    def get_queryset(self):
        
        all_voters = Voter.objects.all()

        party = self.request.GET.get('party')

        if party:
            all_voters = all_voters.filter(party_affiliation__iexact=party)
        
        min_year = self.request.GET.get('min_year')
        if min_year:
            all_voters = all_voters.filter(date_of_birth__year__gte=min_year)

        max_year = self.request.GET.get('max_year')
        if max_year:
            all_voters = all_voters.filter(date_of_birth__year__lte=max_year)
        
        score = self.request.GET.get('score')
        if score:
            all_voters = all_voters.filter(voter_score=score)
        
        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field):
                all_voters = all_voters.filter(**{field: True})
        
        return all_voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_voters = self.get_queryset()

        # All Plotly Graphs 

        # Historgram Chart: Distribution of Voters by their year of birth

        birth_years = [voter.date_of_birth.year for voter in filtered_voters]

        fig1 = go.Histogram(x=birth_years, nbinsx=100)
        title_text1 = f"Voter Distribution by Year of Birth (n={len(birth_years)})"

        layout1 = go.Layout(
            bargap=0.2,  
            xaxis=dict(title='Year of Birth'),
            yaxis=dict(title='Count')
        )
        
        graph_div_birth = plotly.offline.plot({"data": [fig1], 
                                               "layout": layout1,
                                               "layout_title_text": title_text1,
                                              }, auto_open=False, output_type="div"
                                              )
        context['graph_div_birth'] = graph_div_birth


        # Pie Chart: Distrubution of Voters by their party affiliation
    
        party_counts = {}
        for voter in filtered_voters:
            party = voter.party_affiliation
            party_counts[party] = party_counts.get(party, 0) + 1

        labels = list(party_counts.keys())
        values = list(party_counts.values())

        fig2 = go.Pie(labels=labels, values=values)
        title_text2 = f"Voter Distribution by Party Affiliation (n={len(filtered_voters)})"
        graph_div_party = plotly.offline.plot({"data": [fig2], 
                                               "layout_title_text": title_text2,
                                              }, auto_open=False, output_type="div"
                                              )
        context['graph_div_party'] = graph_div_party

        # Bar Chart: Distribution of Voters by their participation in each of the 5 elections

        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        vote_counts = []

        for election in elections:
            count = filtered_voters.filter(**{election: True}).count()
            vote_counts.append(count)

        fig3 = go.Bar(x=elections, y=vote_counts)
        title_text3 = f"Vote Count by Election (n={Voter.objects.count()})"
        graph_div_elections = plotly.offline.plot({"data": [fig3], 
                                                   "layout_title_text": title_text3,
                                                  }, auto_open=False, output_type="div"
                                                  )
        context['graph_div_elections'] = graph_div_elections

        current_year = date.today().year
        context['years'] = list(range(current_year, 1899, -1))
        context['scores'] = range(1, 6)
        context['selected_party'] = self.request.GET.get('party')
        context['selected_min_year'] = self.request.GET.get('min_year')
        context['selected_max_year'] = self.request.GET.get('max_year')
        context['selected_score'] = self.request.GET.get('score')
        context['form_action'] = 'voter_graphs'


        return context
 

        