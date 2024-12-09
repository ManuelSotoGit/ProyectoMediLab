from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import SoporteForm,CitaForm,CustomUserCreationForm,RegistroMedicoForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from .models import Cita,MedicosEspecialidad



# ruta nav
def index(request):
    return render(request, 'core/index.html')
def servicios(request):
    return render(request, 'core/servicios.html')
def sobrenosotros(request):
    return render(request, 'core/sobrenosotros.html')

# comienzo del crud de registro_cita
@permission_required('core.add_citas')
def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recepcionista')  # Redirige al panel del recepcionista
    else:
        form = CitaForm()
    return render(request, 'core/trabajos/registrar_cita.html', {'form': form})
@permission_required('core.change_citas')
def editar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)  # Obtener la cita específica
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)  # Prellenar el formulario con los datos existentes
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('recepcionista')  # Redirigir al panel del recepcionista
    else:
        form = CitaForm(instance=cita)  # Mostrar los datos actuales en el formulario
    return render(request, 'core/trabajos/editar_cita.html', {'form': form, 'cita': cita})
@permission_required('core.delete_citas')
def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        cita.delete()
        return redirect('recepcionista')
    return render(request, 'core/trabajos/eliminar_cita.html', {'cita': cita})

# view de tablas importantes
def recepcionista(request):
    # Obtiene todas las citas
    citas = Cita.objects.all()
    especialidades = MedicosEspecialidad.objects.all()

    # Manejo del formulario
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recepcionista')
    else:
        form = CitaForm()

    # Obtener las opciones de horarios desde el modelo
    opciones_horas = Cita._meta.get_field('hora_cita').choices

    # Contexto para pasar a la plantilla
    data = {
        'citas': citas,
        'form': form,
        'opciones_horas': opciones_horas,  # Incluye las opciones en el contexto
        'especialidades': especialidades,  # Pasa las especialidades al contexto
    }

    return render(request, 'core/trabajos/recepcionista.html', data)

def medico1(request):
    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Diagnostico registrado!')
            return redirect('medico1')  # Cambia 'home' por la ruta adecuada
        else:   
            messages.error(request, 'Hubo un error al registrar el diagnostico del paciente.')
    else:
        form = RegistroMedicoForm()
    return render(request, 'core/trabajos/medico1.html', {'form': form})
    
def citas(request):
    data={
        'form': CitaForm()
    }
    if request.method == 'POST':
        formulario = CitaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Tu cita ha sido reservada con éxito!')
            return redirect(to='citas')
        else:
            messages.error(request, 'Hubo un error al reservar tu cita. Por favor, revisa el formulario.')
            
    return render(request, 'core/citas.html',data)
@login_required
def soporte(request):
    data={
        'form': SoporteForm()
    }

    if request.method == 'POST':
        formulario = SoporteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else:
            data["form"] = formulario
            
    return render(request, 'core/soporte.html',data)

# registro de usuario "registration/"
def soporte_view(request):
    if request.method == 'POST':
        form = SoporteForm(request.POST)
        if form.is_valid():
            soporte = form.save()
            # Enviar correo
            send_mail(
                subject="Nueva solicitud de soporte",
                message=f"Nombre: {soporte.nombre}\nCorreo: {soporte.correo}\nÁrea: {soporte.get_area_display()}\nDescripción: {soporte.descripcion}",
                from_email="manuel.e.soto.n.2012@gmail.com",
                recipient_list=["manuel.e.soto.n.2012@gmail.com"],  # Correo del administrador
            )
            messages.success(request, "Tu solicitud de soporte ha sido enviada con éxito.")
            return redirect('soporte')
    else:
        form = SoporteForm()
    return render(request, 'soporte.html', {'form': form})

def registro(request):
    data={'form':CustomUserCreationForm(data=request.POST)}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request,"Te has registrado correctamente ")
            return redirect(to="index")
    return render(request, 'registration/registro.html',data)

