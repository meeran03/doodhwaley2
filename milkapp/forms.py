# from .models import *
# from django import forms

# class AreaForm(forms.ModelForm):
#     city_id = forms.ChoiceField(choices=((x.id,x.name) for x in City.objects.all()))
#     class Meta:
#         model = Area
#         fields = ['city_id','area_name']

#     def save(self):
#         cleaned_data = super(AreaForm, self).clean()
#         name = cleaned_data.get('area_name')
#         city_id = cleaned_data.get('city_id')
#        # city_id = city._id
#         if not name and not city_id:
#             raise forms.ValidationError('You have to write something!')
#         form = Area(area_name=name,city_id=city_id)
#         form.save()

# class AdminForm(forms.ModelForm):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = Admin
#         fields = ['email','password']
    
    
        
    