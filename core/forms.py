from django import forms
from .models import Soporte,Cita,RegistroMedico
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date


class SoporteForm(forms.ModelForm):

    class Meta:
        model = Soporte
        fields = ['nombre', 'correo', 'whatsapp', 'area', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu nombre completo'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu correo electrónico'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu número de WhatsApp'
            }),
            'area': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe tu problema o consulta',
                'rows': 4
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        correo = cleaned_data.get('correo')
        whatsapp = cleaned_data.get('whatsapp')
        area = cleaned_data.get('area')
        descripcion = cleaned_data.get('descripcion')

        if nombre and correo and nombre.lower() == correo.lower():
            raise forms.ValidationError("El nombre no puede ser igual al correo electrónico.")
        
        if area == 6 and (not descripcion or len(descripcion) < 50):
            raise forms.ValidationError("Si seleccionas 'Otros', la descripción debe tener al menos 50 caracteres.")

        if whatsapp and whatsapp.startswith('9') and len(whatsapp) != 9:
            raise forms.ValidationError("Si el número de WhatsApp comienza con '9', debe tener exactamente 9 caracteres.")

        return cleaned_data
    
    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not whatsapp.isdigit():
            raise ValidationError("El número de WhatsApp debe contener solo dígitos.")
        if len(whatsapp) != 10:
            raise ValidationError("El número de WhatsApp debe tener 10 dígitos.")
        return whatsapp
    
class CitaForm(forms.ModelForm):

    class Meta:
        model = Cita
        fields = ['nombre', 'rut', 'correo', 'telefono', 'fecha_cita', 'hora_cita', 'especialidadMedico', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu rut'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu teléfono'}),
            'fecha_cita': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'hora_cita': forms.Select(attrs={'class': 'form-control'}),
            'especialidadMedico': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tu problema', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_cita = cleaned_data.get('fecha_cita')
        telefono = cleaned_data.get('telefono')
        rut = cleaned_data.get('rut')

        if fecha_cita and fecha_cita < date.today():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")

        if telefono and (not telefono.isdigit() or len(telefono) < 8 or len(telefono) > 15):
            raise forms.ValidationError("El teléfono debe contener solo números y tener entre 8 y 15 caracteres.")

        if rut and len(rut) < 9:
            raise forms.ValidationError("El RUT debe tener al menos 9 caracteres.")

        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de usuario",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apellido",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico",
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirma tu contraseña",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")

        if password1 and (len(password1) < 8 or not any(char.isdigit() for char in password1) or not any(char.isalpha() for char in password1)):
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, incluir números y letras.")

        return cleaned_data

class RegistroMedicoForm(forms.ModelForm):

    class Meta:
        model = RegistroMedico
        fields = ['paciente', 'cita','especialidad', 'diagnostico', 'prescripcion']
        widgets = {
            'paciente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del paciente'
            }),
            'cita': forms.Select(attrs={
                'class': 'form-control'
            }),
            'especialidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el diagnóstico',
                'rows': 4
            }),
            'prescripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Indique las prescripciones médicas',
                'rows': 4
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        diagnostico = cleaned_data.get('diagnostico')
        paciente = cleaned_data.get('paciente')
        cita = cleaned_data.get('cita')

        if diagnostico and len(diagnostico) < 10:
            raise forms.ValidationError("El diagnóstico debe tener al menos 10 caracteres.")

        if not paciente:
            raise forms.ValidationError("El nombre del paciente no puede estar vacío.")

        if not cita:
            raise forms.ValidationError("Debes seleccionar una cita válida.")

        return cleaned_data
