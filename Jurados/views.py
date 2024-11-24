from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password,  make_password
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import LoginForm, ReestablecerForm, ResetearForm
from .models import Jurado, Asignacion
from Alumnos.models import Semestre, Proyecto_Alumno
from datetime import date
from .utils import generar_observacion
import json, os


# Create your views here.
def jurado_login(request):
    mensaje = ""
    mostrar_modal = False 

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                jurado = Jurado.objects.get(dni=username)

                if check_password(password, jurado.password):
                    request.session['jurado_id'] = jurado.id
                    return redirect('dashboard_jurado')
                else:
                    mensaje = "Contraseña incorrecta."
                    mostrar_modal = True

            except Jurado.DoesNotExist:
                mensaje = "El usuario no existe."
                mostrar_modal = True
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True  

    else:
        form = LoginForm()

    return render(request, 'jurado_login.html', {
        'form': form,
        'mensaje': mensaje,
        'mostrar_modal': mostrar_modal 
    })

def dashboard_jurado(request):
    if 'jurado_id' not in request.session:
        return redirect('jurado_login')

    jurado_id = request.session['jurado_id'] 

    try:
        jurado = Jurado.objects.get(id=jurado_id)
        return render(request, 'dashboard_jurado.html', {'jurado': jurado})
    except Jurado.DoesNotExist:
        del request.session['jurado_id']
        return redirect('jurado_login')

def datosPersonales_jurado(request):
    if 'jurado_id' not in request.session:
        return redirect('jurado_login')

    jurado_id = request.session['jurado_id']

    try:
        jurado = Jurado.objects.get(id=jurado_id)
        return render(request, 'datosPersonales_jurado.html', {'jurado': jurado})
    except Jurado.DoesNotExist:
        del request.session['jurado_id']
        return redirect('jurado_login')

def actualizarDatos_jurado(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        jurado_id = data.get('jurado_id')
        email = data.get('email')
        domicilio = data.get('domicilio')
        celular = data.get('celular')
        fecha_nacimiento = data.get('fechaNacimiento')
        sexo = data.get('sexo')

        try:
            jurado = Jurado.objects.get(id=jurado_id)
            jurado.email = email
            jurado.domicilio = domicilio
            jurado.celular = celular
            jurado.fechaNacimiento = fecha_nacimiento
            jurado.sexo = sexo
            jurado.save()

            return JsonResponse({'status': 'success', 'message': 'Datos actualizados correctamente.'})
        except Jurado.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Jurado not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def changePassword_jurado(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        jurado_id = data.get('jurado_id')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        try:
            jurado = Jurado.objects.get(id=jurado_id)

            if not check_password(current_password, jurado.password):
                return JsonResponse({'status': 'error', 'message': 'La contraseña no actual no es correcta.'}) 
            
            jurado.password = make_password(new_password)
            jurado.save()

            return JsonResponse({'status': 'success', 'message': 'Contraseña actualizada exitosamente.'})
        
        except Jurado.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Jurado not found.'})
        
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def evaluacion_jurado(request):
    if 'jurado_id' not in request.session:
        return redirect('jurado_login')

    jurado_id = request.session['jurado_id']
    try:
        jurado = Jurado.objects.get(id=jurado_id)

        semestres = Semestre.objects.all()

        asignaciones = Asignacion.objects.filter(jurado=jurado)

        proyectos_data = []
        for asignacion in asignaciones:

            proyecto = asignacion.proyecto

            try:
                proyecto_alumno = Proyecto_Alumno.objects.filter(proyecto_id=proyecto.id).first()
                dictamen_pdf = proyecto_alumno.dictamenPdf
                
            except Proyecto_Alumno.DoesNotExist:
                dictamen_pdf = None 
        
            proyectos_data.append({
                'asignacion': asignacion,
                'semestre': asignacion.semestre,
                'proyecto': asignacion.proyecto,
                'dictamen_pdf': dictamen_pdf
            })
        
        return render(request, 'evaluacion_jurado.html', {'jurado': jurado, 'semestres': semestres, 'proyectos_data': proyectos_data,})
         
    except Jurado.DoesNotExist:
        del request.session['jurado_id']
        return redirect('jurado_login')

def evaluacion_jurado_proyecto(request, asignacion_id):
    if 'jurado_id' not in request.session:
        return redirect('jurado_login')

    jurado_id = request.session['jurado_id']
    try:
        jurado = Jurado.objects.get(id=jurado_id)

        asignacion = Asignacion.objects.get(id=asignacion_id)

        return render(request, 'evaluacion_jurado_proyecto.html', {'jurado': jurado,'asignacion': asignacion})

    except Jurado.DoesNotExist:
        del request.session['jurado_id']
        return redirect('jurado_login')
    
    except Asignacion.DoesNotExist:
        return redirect('evaluacion_jurado')
    
def guardar_evaluacion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            asignacion_id = data.get("asignacionId")
            calificacionIntroduccion = int(data.get("calificacion_introduccion", 0))
            calificacionAntecedentes = int(data.get("calificacion_antecedentes", 0))
            calificacionMarcoTeorico = int(data.get("calificacion_marco_teorico", 0))
            calificacionHipotesis = int(data.get("calificacion_hipotesis", 0))
            calificacionMetodologia = int(data.get("calificacion_metodologia", 0))
            calificacionAspectosAdministrativos = int(data.get("calificacion_aspectos_administrativos", 0))
            calificacionRedaccion = int(data.get("calificacion_redaccion", 0))
            calificacionCitaReferencia = int(data.get("calificacion_citayreferencia", 0))

            suma = (calificacionIntroduccion + calificacionAntecedentes +
                    calificacionMarcoTeorico + calificacionHipotesis +
                    calificacionMetodologia + calificacionAspectosAdministrativos +
                    calificacionRedaccion + calificacionCitaReferencia)

            asignacion = Asignacion.objects.get(id=asignacion_id)
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdfObservacion', f'observacion_{asignacion_id}.pdf')

            generar_observacion(pdf_file_path, data)

            asignacion.estadoRevision = 'Revisado'
            asignacion.fechaRevision = date.today()
            asignacion.observacionPdf = os.path.join('pdfObservacion', f'observacion_{asignacion_id}.pdf')
            asignacion.notaFinal = suma
            asignacion.save()

            return JsonResponse({"status": "success", "message": "Evaluación guardada correctamente"})

        except Asignacion.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Asignación no encontrada"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Error en el formato de los datos"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
    
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def reestablecerPassword_jurado(request):
    mensaje = ""
    mostrar_modal = False

    if request.method == 'POST':
        form = ReestablecerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                jurado = Jurado.objects.get(email=email)
                
                token = get_random_string(32)

                jurado.reset_token = token
                jurado.save()
                
                ruta = 'http://127.0.0.1:8000/jurados/resetear-password/'
                enlace = f"{ruta}?token={token}"

                asunto = 'Restablecimiento de Contraseña'
                mensaje_correo = f"""
                Hola {jurado.nombres},

                Hemos recibido una solicitud para restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:
                {enlace}

                Si no solicitaste el restablecimiento de tu contraseña, ignora este mensaje.
                """

                send_mail(
                    asunto,
                    mensaje_correo,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                
                mensaje = "Correo de restablecimiento de contraseña enviado correctamente."
                mostrar_modal = True

            except Jurado.DoesNotExist:
                mensaje = "El correo no está registrado en el sistema."
                mostrar_modal = True

    else:
        form = ReestablecerForm()

    return render(request, 'reestablecerPassword_jurado.html', {
        'form': form,
        'mensaje': mensaje,
        'mostrar_modal': mostrar_modal
    })

def resetear_contrasena(request):
    mensaje = ""
    mostrar_modal = False 
    
    if request.method == 'POST':
        form = ResetearForm(request.POST)
        token = request.POST.get('token')

        if form.is_valid():
            nueva_contrasena = form.cleaned_data['password']
            confirmar_contrasena = form.cleaned_data['confirm_password']

            if nueva_contrasena != confirmar_contrasena:
                mensaje = "Las contraseñas no coinciden."
                mostrar_modal = True  
            else:
                try:
                    jurado = Jurado.objects.get(reset_token=token)
                    jurado.password = make_password(nueva_contrasena)
                    jurado.reset_token = None 
                    jurado.save()

                    mensaje = "Tu contraseña ha sido restablecida correctamente."
                    mostrar_modal = True  
                    return render(request, 'reseteoPassword_jurado.html', {
                        'form': form,
                        'mensaje': mensaje,
                        'token': token,
                        'mostrar_modal': mostrar_modal
                    })
                except Jurado.DoesNotExist:
                    mensaje = "Token de restablecimiento inválido."
                    mostrar_modal = True 
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True  

    else:
        form = ResetearForm()

    return render(request, 'reseteoPassword_jurado.html', {
        'form': form,
        'mensaje': mensaje,
        'token': request.GET.get('token'), 
        'mostrar_modal': mostrar_modal 
    })