from django.contrib import admin
from django.urls import path
from .views import index,citas,soporte,registro,recepcionista,medico1,registrar_cita,editar_cita,eliminar_cita,servicios,sobrenosotros


urlpatterns = [
    path('',index,name="index"),
    path('servicios/',servicios,name="servicios"),
    path('sobrenosotros/',sobrenosotros,name="sobrenosotros"),
    path('citas/',citas,name="citas"),
    path('soporte/',soporte,name="soporte"),
    path('registro/',registro,name="registro"),
    path('recepcionista/',recepcionista,name="recepcionista"),
    path('medico1/', medico1, name='medico1'),

    path('recepcionista/registrar_cita/', registrar_cita, name="registrar_cita"),
    path('recepcionista/editar_cita/<int:id>/', editar_cita, name="editar_cita"),
    path('recepcionista/eliminar_cita/<int:id>/', eliminar_cita, name="eliminar_cita"),
]