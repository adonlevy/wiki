from django import forms

# define a form for search


class NewSearch(forms.Form):
    query = forms.CharField(label="Search Wiki", widget=forms.TextInput(
        attrs={'placeholder': 'Search', 'class': 'form-control col-md-10 col-lg-14'}))


class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Title of Entry',
               'class': 'form-control col-md-8 col-lg-8'}
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Page content...',
               'class': 'form-control col-md-8 col-lg-8', 'rows': 10}
    ))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)
