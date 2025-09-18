from django.shortcuts import render

# Create your views here.


def show_form(request):
    ''' Show the form to the user '''

    template_name = "formdata/form.html"

    return render(request, template_name)

def submit(request):
    ''' Process the form submission '''

    template_name = "formdata/confirmation.html"

    if request.POST:

        name = request.POST['name']
        color = request.POST['color']

        context = {
            "name": name,
            "color": color
        }

    return render(request, template_name=template_name, context=context)