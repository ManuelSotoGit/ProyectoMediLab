from django.db import models

# Create your models here.
class MedicosEspecialidad(models.Model):
    especialidad = models.CharField(max_length=50)
    def __str__(self):
        return self.especialidad

opciones_horarios = [
    [0,"09:00"],[1,"10:00"],[2,"11:00"],[3,"12:00"],[4,"13:00"],
    [5,"14:00"],[6,"15:00"],[7,"16:00"],[8,"17:00"],[9,"18:00"],
    [10,"19:00"],[11,"20:00"],[12,"21:00"]
]

class Cita(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.CharField(max_length=12)
    fecha_cita = models.DateField()
    hora_cita = models.IntegerField(choices=opciones_horarios)
    especialidadMedico= models.ForeignKey(MedicosEspecialidad,on_delete=models.PROTECT)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.rut}"

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre completo del paciente
    correo = models.EmailField(unique=True)  # Correo electrónico único
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono opcional
    direccion = models.TextField(blank=True, null=True)  # Dirección opcional

    def __str__(self):
        return self.nombre

class RegistroMedico(models.Model):
    paciente = models.CharField(max_length=100) 
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)  
    especialidad = models.ForeignKey(MedicosEspecialidad, on_delete=models.PROTECT)  
    diagnostico = models.TextField(blank=True, null=True)  
    prescripcion = models.TextField(blank=True, null=True)  
    fecha_registro = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Registro de {self.paciente} - {self.fecha_registro.strftime('%Y-%m-%d')}"


opcion_area=[
    [0,"Falta de seguimiento"],[1,"Tiempos de espera prolongados"],[2,"Fallos en el servicio"],
    [3,"Cambio de términos y condiciones"],[4,"Mala atención al cliente"],[5,"Devoluciones"],[6,"Desabasto"],[7,"Otros"]
]

class Soporte(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    whatsapp = models.CharField(max_length=12)
    area = models.IntegerField(choices=opcion_area)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
