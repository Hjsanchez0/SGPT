from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from collections import defaultdict
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import LoginForm, ReestablecerForm, ResetearForm
from .models import Administrativo
from Alumnos.models import Carta_Acceso, Proyecto_Alumno, Semestre
from Jurados.models import Jurado, Asignacion
from .utils import generar_carta_alumno
from datetime import date
import json, os

# Create your views here.
def administrativo_login(request):
    mensaje = ""
    mostrar_modal = False 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                administrativo = Administrativo.objects.get(dni=username)

                if check_password(password, administrativo.password):
                    request.session['administrativo_id'] = administrativo.id
                    return redirect('dashboard_administrativo')
                else:
                    mensaje = "Contraseña incorrecta."
                    mostrar_modal = True

            except Administrativo.DoesNotExist:
                mensaje = "El usuario no existe."
                mostrar_modal = True
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True
    else:
        form = LoginForm()

    return render(request, 'administrativo_login.html', {'form': form, 'mensaje': mensaje, 'mostrar_modal': mostrar_modal})

def dashboard_administrativo(request):
    if 'administrativo_id' not in request.session:
        return redirect('administrativo_login')

    administrativo_id = request.session['administrativo_id'] 

    try:
        administrativo = Administrativo.objects.get(id=administrativo_id)
        return render(request, 'dashboard_administrativo.html', {'administrativo': administrativo})
    except Administrativo.DoesNotExist:
        del request.session['administrativo_id']
        return redirect('administrativo_login')

def datosPersonales_admin(request):
    if 'administrativo_id' not in request.session:
        return redirect('administrativo_login')

    administrativo_id = request.session['administrativo_id']

    try:
        administrativo = Administrativo.objects.get(id=administrativo_id)
        return render(request, 'datosPersonales_admin.html', {'administrativo': administrativo})
    except Administrativo.DoesNotExist:
        del request.session['administrativo_id']
        return redirect('administrativo_login')

def actualizarDatos_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        administrativo_id = data.get('administrativo_id')
        email = data.get('email')
        domicilio = data.get('domicilio')
        celular = data.get('celular')
        fecha_nacimiento = data.get('fechaNacimiento')
        sexo = data.get('sexo')

        try:
            administrativo = Administrativo.objects.get(id=administrativo_id)
            administrativo.email = email
            administrativo.domicilio = domicilio
            administrativo.celular = celular
            administrativo.fechaNacimiento = fecha_nacimiento
            administrativo.sexo = sexo
            administrativo.save()

            return JsonResponse({'status': 'success', 'message': 'Datos actualizados correctamente.'})
        except Administrativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Administrativo not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def changePassword_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        administrativo_id = data.get('administrativo_id')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        try:
            administrativo = Administrativo.objects.get(id=administrativo_id)

            if not check_password(current_password, administrativo.password):
                return JsonResponse({'status': 'error', 'message': 'La contraseña no actual no es correcta.'}) 
            
            administrativo.password = make_password(new_password)
            administrativo.save()

            return JsonResponse({'status': 'success', 'message': 'Contraseña actualizada exitosamente.'})
        
        except Administrativo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Administrative not found.'})
        
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})            

def tramites_admin(request):
    if 'administrativo_id' not in request.session:
        return redirect('administrativo_login')

    administrativo_id = request.session['administrativo_id']

    try:
        administrativo = Administrativo.objects.get(id=administrativo_id)

        proyectos_alumnos = Proyecto_Alumno.objects.select_related('alumno', 'carta_acceso', 'semestre').all()

        carta_dni_dict = defaultdict(list)
        for proyecto_alumno in proyectos_alumnos:
            if proyecto_alumno.carta_acceso: 
                carta_dni_dict[proyecto_alumno.carta_acceso].append((
                    proyecto_alumno.alumno.dni,
                    proyecto_alumno.alumno.nombres,
                    proyecto_alumno.alumno.apellidoPat,
                    proyecto_alumno.alumno.apellidoMat,
                    proyecto_alumno.semestre.id,
                    proyecto_alumno.semestre.semestreAcademico, 
                ))

        semestres = Semestre.objects.all()

        return render(request, 'tramites_admin.html', {
            'administrativo': administrativo,
            'semestres': semestres,
            'carta_dni_dict': carta_dni_dict.items(), 
        })
    except Administrativo.DoesNotExist:
        del request.session['administrativo_id']
        return redirect('administrativo_login')

def actualizar_observacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carta_id = data.get('carta_id')
        observacion = data.get('observacion')

        try:
            carta = Carta_Acceso.objects.get(id=carta_id)
            carta.estadoFut = 'Observado' 
            carta.observacionFut = observacion
            carta.save() 
            return JsonResponse({'message': 'Observación actualizada con éxito.'})
        except Carta_Acceso.DoesNotExist:
            return JsonResponse({'message': 'Carta no encontrada.'}, status=404)
    return JsonResponse({'message': 'Método no permitido.'}, status=405)

def enviar_respuesta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carta_ids = data.get('carta_ids', [])
            
            for carta_id in carta_ids:
                carta = Carta_Acceso.objects.get(id=carta_id)

                proyectos_alumnos = Proyecto_Alumno.objects.filter(carta_acceso=carta)

                if proyectos_alumnos.exists():
                    all_alumnos_data = []

                    for proyecto_alumno in proyectos_alumnos:
                        alumno = proyecto_alumno.alumno
                        proyecto = proyecto_alumno.proyecto

                        alumno_data = {
                            'dni': alumno.dni,
                            'codMatricula': alumno.codMatricula,
                            'nombre': f"{alumno.nombres} {alumno.apellidoPat} {alumno.apellidoMat}",
                        }

                        proyecto_data = {
                            'titulo': proyecto.titulo,
                            'institucion': proyecto.institucion,
                            'director': proyecto.director,
                            'cargo': proyecto.cargo,
                        }

                        all_alumnos_data.append({
                            'alumno': alumno_data,
                            'proyecto': proyecto_data,
                        })

                    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdfCarta', f'carta_acceso_{carta_id}.pdf')
                    generar_carta_alumno(pdf_file_path, {'carta': carta, 'alumnos': all_alumnos_data})

                    carta.estadoFut = 'Aceptado'
                    carta.observacionFut = 'Ninguna'
                    carta.fechaCarta = date.today()

                    carta.pdfCarta = os.path.join('pdfCarta', f'carta_acceso_{carta_id}.pdf')
                    carta.save()

            return JsonResponse({'status': 'success', 'message': 'Respuesta enviada correctamente.'}, status=200)

        except Exception as e:
            print('Error:', str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

def asignacionJurado_admin(request):
    if 'administrativo_id' not in request.session:
        return redirect('administrativo_login')

    administrativo_id = request.session['administrativo_id']

    try:
        administrativo = Administrativo.objects.get(id=administrativo_id)

        jurados_filtrados = Jurado.objects.filter(rol__ocupacion__in=['PRESIDENTE', 'VOCAL', 'SECRETARIO'])

        asignaciones = Asignacion.objects.select_related('proyecto', 'semestre', 'jurado').all()

        proyectos = {}
        
        for asignacion in asignaciones:
            proyecto_id = asignacion.proyecto.id

            proyecto_alumno = Proyecto_Alumno.objects.filter(proyecto_id=proyecto_id).first()

            if proyecto_id not in proyectos:
                proyectos[proyecto_id] = {
                    'id': proyecto_id,
                    'titulo': asignacion.proyecto.titulo,
                    'semestre': asignacion.semestre.semestreAcademico,
                    'fecha': asignacion.fechaAsignacion,
                    'jurados': {
                        'presidente': {'id': None, 'nombre_completo': None},
                        'vocal': {'id': None, 'nombre_completo': None},
                        'secretario': {'id': None, 'nombre_completo': None}
                    },
                    'resolucion_pdf': proyecto_alumno.resolucionPdf
                    
                }

            if asignacion.jurado:
                nombre_completo = f"{asignacion.jurado.apellidoPat} {asignacion.jurado.apellidoMat} {asignacion.jurado.nombres}"
                jurado_data = {'id': asignacion.jurado.id, 'nombre_completo': nombre_completo}
                
                if asignacion.jurado.rol.ocupacion == 'PRESIDENTE':
                    proyectos[proyecto_id]['jurados']['presidente'] = jurado_data
                elif asignacion.jurado.rol.ocupacion == 'VOCAL':
                    proyectos[proyecto_id]['jurados']['vocal'] = jurado_data
                elif asignacion.jurado.rol.ocupacion == 'SECRETARIO':
                    proyectos[proyecto_id]['jurados']['secretario'] = jurado_data

        semestres = Semestre.objects.all()

        return render(request, 'asignacionJurado_admin.html', {
            'administrativo': administrativo,
            'semestres': semestres,
            'proyectos': proyectos.values(),  
            'jurados': jurados_filtrados, 
        })
    except Administrativo.DoesNotExist:
        del request.session['administrativo_id']
        return redirect('administrativo_login')

def actualizar_jurados(request):
    if request.method == 'POST':
        presidente_id = request.POST.get('presidenteId')
        vocal_id = request.POST.get('vocalId')
        secretario_id = request.POST.get('secretarioId')
        proyecto_id = request.POST.get('proyectoId')
        administrativo_id = request.POST.get('administrativoId')
        resolucion_pdf = request.FILES.get('resolucionPdf')

        try:
            proyecto_alumnos = Proyecto_Alumno.objects.filter(proyecto_id=proyecto_id)

            if resolucion_pdf:
                for proyecto_alumno in proyecto_alumnos:
                    if proyecto_alumno.resolucionPdf != 'Pendiente':
                        return JsonResponse({'success': False, 'error': 'Ya existe una resolucion asociado a este proyecto.'})

                archivo_path = default_storage.save(f'pdfResolucion/{resolucion_pdf.name}', resolucion_pdf)

                for proyecto_alumno in proyecto_alumnos:
                    proyecto_alumno.resolucionPdf = archivo_path
                    proyecto_alumno.save()
            
            asignaciones = Asignacion.objects.filter(proyecto_id=proyecto_id, jurado__isnull=True)[:3]
            if len(asignaciones) < 3:
                return JsonResponse({'success': False, 'error': 'No hay suficientes asignaciones disponibles.'})

            fecha_actual = date.today()

            asignaciones[0].jurado_id = presidente_id
            asignaciones[0].fechaAsignacion = fecha_actual
            asignaciones[0].administrativo_id = administrativo_id

            asignaciones[1].jurado_id = vocal_id
            asignaciones[1].fechaAsignacion = fecha_actual
            asignaciones[1].administrativo_id = administrativo_id

            asignaciones[2].jurado_id = secretario_id
            asignaciones[2].fechaAsignacion = fecha_actual
            asignaciones[2].administrativo_id = administrativo_id

            for asignacion in asignaciones:
                asignacion.save()

            return JsonResponse({'success': True})
        except Proyecto_Alumno.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El proyecto no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})

def eliminar_jurados(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        proyecto_id = data.get('proyectoId')

        try:
            asignaciones = Asignacion.objects.filter(proyecto_id=proyecto_id)[:3]
        
            if len(asignaciones) < 3:
                return JsonResponse({'success': False, 'error': 'No hay suficientes asignaciones disponibles.'})

            for asignacion in asignaciones:
                asignacion.jurado_id = None
                asignacion.fechaAsignacion = None
                asignacion.administrativo_id = None
                asignacion.save()

            proyecto_alumnos = Proyecto_Alumno.objects.filter(proyecto_id=proyecto_id)

            for proyecto_alumno in proyecto_alumnos:
                if proyecto_alumno.resolucionPdf:
                    resolucion_pdf_path = proyecto_alumno.resolucionPdf.path
                    if os.path.exists(resolucion_pdf_path):
                        os.remove(resolucion_pdf_path)

                    proyecto_alumno.resolucionPdf = 'Pendiente' 
                    proyecto_alumno.save() 

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def seguimiento_admin(request):
    if 'administrativo_id' not in request.session:
        return redirect('administrativo_login')

    administrativo_id = request.session['administrativo_id']

    try:
        administrativo = Administrativo.objects.get(id=administrativo_id)

        asignaciones = Asignacion.objects.filter(administrativo=administrativo)

        semestres = Semestre.objects.all()

        proyectos_data = []

        for asignacion in asignaciones:
            proyecto = asignacion.proyecto
            semestre = asignacion.semestre.semestreAcademico if asignacion.semestre else None

            proyectos_alumnos = Proyecto_Alumno.objects.filter(proyecto=proyecto)
            alumnos = [
                f"{proyecto_alumno.alumno.nombres} {proyecto_alumno.alumno.apellidoPat} {proyecto_alumno.alumno.apellidoMat}"
                for proyecto_alumno in proyectos_alumnos
            ]
            dnIs = [
                proyecto_alumno.alumno.dni for proyecto_alumno in proyectos_alumnos
            ]

            alumnos_str = ' - '.join(alumnos) 
            dnIs_str = ' - '.join(dnIs)          

            jurados = [asignacion.jurado]  


            proyectos_data.append({
                'jurado': jurados,              
                'titulo': proyecto.titulo,    
                'semestre': semestre,        
                'alumnos': alumnos_str,         
                'dni': dnIs_str,                
                'fechaEnvio': asignacion.fechaEnvio, 
                'estadoEnvio': asignacion.estadoEnvio, 
                'fechaRevision': asignacion.fechaRevision,
                'estadoRevision': asignacion.estadoRevision, 
            })

        return render(request, 'seguimiento_admin.html', {'administrativo': administrativo, 'semestres': semestres, 'proyectos_data': proyectos_data,
        })
    except Administrativo.DoesNotExist:
        del request.session['administrativo_id']
        return redirect('administrativo_login')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def reestablecerPassword_admin(request):
    mensaje = ""
    mostrar_modal = False

    if request.method == 'POST':
        form = ReestablecerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                admin = Administrativo.objects.get(email=email)
                
                token = get_random_string(32)

                admin.reset_token = token
                admin.save()
                
                ruta = 'http://127.0.0.1:8000/administrativos/resetear-password/'
                enlace = f"{ruta}?token={token}"

                asunto = 'Restablecimiento de Contraseña'
                mensaje_correo = f"""
                Hola {admin.nombres},

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

            except Administrativo.DoesNotExist:
                mensaje = "El correo no está registrado en el sistema."
                mostrar_modal = True

    else:
        form = ReestablecerForm()

    return render(request, 'reestablecerPassword_admin.html', {
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
                    admin = Administrativo.objects.get(reset_token=token)
                    admin.password = make_password(nueva_contrasena)
                    admin.reset_token = None 
                    admin.save()

                    mensaje = "Tu contraseña ha sido restablecida correctamente."
                    mostrar_modal = True  
                    return render(request, 'reseteoPassword_admin.html', {
                        'form': form,
                        'mensaje': mensaje,
                        'token': token,
                        'mostrar_modal': mostrar_modal
                    })
                except Administrativo.DoesNotExist:
                    mensaje = "Token de restablecimiento inválido."
                    mostrar_modal = True 
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True  

    else:
        form = ResetearForm()

    return render(request, 'reseteoPassword_admin.html', {
        'form': form,
        'mensaje': mensaje,
        'token': request.GET.get('token'), 
        'mostrar_modal': mostrar_modal 
    })