from django import forms

class ClienteForm(forms.Form):
    cedula = forms.CharField(label='Cedula', max_length=8)
    nombre = forms.CharField(label='Nombres', max_length=200, required=True)
    apellidos = forms.CharField(label='Apellidos', max_length=200, required=True)
    email = forms.EmailField(label='Email', required=True)
    direccion = forms.CharField(label='Direccion', widget=forms.Textarea)
    telefono = forms.CharField(label='Telefono', max_length=12)
    sexo = forms.ChoiceField(label='Sexo', choices=(('M', 'Masculino'), ('F', 'Femenino')))
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}))