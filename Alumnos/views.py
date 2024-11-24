from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .forms import LoginForm, ReestablecerForm, ResetearForm
from .models import Alumno, Proyecto, Proyecto_Alumno, Tramite, Carta_Acceso, Semestre
from Jurados.models import Asignacion
from .utils import generar_pdf_alumno
import json
import os
from django.conf import settings

# Create your views here.
def alumno_login(request):
    mensaje = ""
    mostrar_modal = False 

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                alumno = Alumno.objects.get(codMatricula=username)
                
                if check_password(password, alumno.password):
                    request.session['alumno_id'] = alumno.id
                    return redirect('dashboard_alumno')
                
                else:
                    mensaje = "Contraseña incorrecta."
                    mostrar_modal = True

            except Alumno.DoesNotExist:
                mensaje = "El usuario no existe."
                mostrar_modal = True
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True  
    else:
        form = LoginForm()

    return render(request, 'alumno_login.html', {'form': form, 'mensaje': mensaje, 'mostrar_modal': mostrar_modal})

def dashboard_alumno(request):
    if 'alumno_id' not in request.session:
        return redirect('alumno_login')
    
    alumno_id = request.session['alumno_id']

    try:
        alumno = Alumno.objects.get(id=alumno_id)
        return render(request, 'dashboard_alumno.html', {'alumno': alumno})
    except Alumno.DoesNotExist:
        del request.session['alumno_id']
        return redirect('alumno_login')
    
def datosPersonales_alumno(request):
    if 'alumno_id' not in request.session:
        return redirect('alumno_login')

    alumno_id = request.session['alumno_id']

    try:
        alumno = Alumno.objects.get(id=alumno_id)
        return render(request, 'datosPersonales_alumno.html', {'alumno': alumno})
    except Alumno.DoesNotExist:
        del request.session['alumno_id']
        return redirect('alumno_login')
    
def actualizarDatos_alumno(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        alumno_id = data.get('alumno_id')
        email = data.get('email')
        domicilio = data.get('domicilio')
        celular = data.get('celular')
        fecha_nacimiento = data.get('fechaNacimiento')
        sexo = data.get('sexo')
        
        try:
            alumno = Alumno.objects.get(id=alumno_id)
            alumno.email = email
            alumno.domicilio = domicilio
            alumno.celular = celular
            alumno.fechaNacimiento = fecha_nacimiento
            alumno.sexo = sexo
            alumno.save()

            return JsonResponse({'status': 'success', 'message': 'Datos actualizados correctamente.'})
        except Alumno.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Alumno not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def changePassword_alumno(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        alumno_id = data.get('alumno_id')
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        try:
            alumno = Alumno.objects.get(id=alumno_id)

            if not check_password(current_password, alumno.password):
                return JsonResponse({'status': 'error', 'message': 'La contraseña no actual no es correcta.'}) 
            
            alumno.password = make_password(new_password)
            alumno.save()

            return JsonResponse({'status': 'success', 'message': 'Contraseña actualizada exitosamente.'})
        
        except Alumno.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Administrative not found.'})
        
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def datosInvestigacion_alumno(request):
    if 'alumno_id' not in request.session:
        return redirect('alumno_login')

    alumno_id = request.session['alumno_id']

    try:
        alumno = Alumno.objects.get(id=alumno_id)

        proyecto_alumno = Proyecto_Alumno.objects.filter(alumno=alumno).order_by('-proyecto__id').first()

        semestres = Semestre.objects.all()

        if proyecto_alumno:
            proyecto = proyecto_alumno.proyecto

            semestre_actual = proyecto.semestre if hasattr(proyecto, 'semestre') else None

            estudiantes_secundarios = Proyecto_Alumno.objects.filter(proyecto=proyecto).exclude(alumno=alumno).select_related('alumno')

            return render(request, 'datosInvestigacion_alumno.html', {
                'alumno': alumno,
                'proyecto': proyecto,
                'semestre_actual': semestre_actual,
                'semestres': semestres,
                'estudiantes_secundarios': estudiantes_secundarios
            })
        else:
            return render(request, 'datosInvestigacion_alumno.html', {
                'alumno': alumno,
                'semestres': semestres,
                'mensaje': 'No tienes un proyecto asociado.'
            })

    except Alumno.DoesNotExist:
        del request.session['alumno_id']
        return redirect('alumno_login')

def buscar_estudiante(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dni = data.get('dni')
        cod_matricula = data.get('codMatricula')

        alumno_id = request.session.get('alumno_id')

        estudiantes = Alumno.objects.all()
        if dni:
            estudiantes = estudiantes.filter(dni=dni)
        if cod_matricula:
            estudiantes = estudiantes.filter(codMatricula=cod_matricula)

        resultados = []

        for estudiante in estudiantes:
            resultados.append({
                'id': estudiante.id,
                'dni': estudiante.dni,
                'codMatricula': estudiante.codMatricula,
                'nombres': estudiante.nombres,
                'apellidoPat': estudiante.apellidoPat,
                'apellidoMat': estudiante.apellidoMat,
                'email': estudiante.email,
                'omitir_botones': estudiante.id == alumno_id
            })

        return JsonResponse({'resultados': resultados}, safe=False)
    
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def guardarInvestigacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        alumno_id = data.get('alumno_id') 
        semestre_id = data.get('semestre_id')  
        institucion = data.get('institucion')
        ruc = data.get('ruc')
        titulo = data.get('titulo')
        director = data.get('director')
        cargo = data.get('cargo')
        direccion = data.get('direccion')
        selected_ids = data.get('selected_ids', []) 

        try:
            alumno = Alumno.objects.get(id=alumno_id)
            semestre = get_object_or_404(Semestre, id=semestre_id)

            proyecto_alumno = Proyecto_Alumno.objects.filter(alumno=alumno, semestre=semestre).first()

            if proyecto_alumno:
                proyecto = proyecto_alumno.proyecto

                proyecto.institucion = institucion
                proyecto.ruc = ruc
                proyecto.titulo = titulo
                proyecto.director = director
                proyecto.cargo = cargo
                proyecto.direccion = direccion
                proyecto.save()

                estudiantes_actuales = Proyecto_Alumno.objects.filter(proyecto=proyecto).exclude(alumno=alumno).values_list('alumno_id', flat=True)

                for estudiante_id in selected_ids:
                    if estudiante_id not in estudiantes_actuales:
                        estudiante = Alumno.objects.get(id=estudiante_id)
                        Proyecto_Alumno.objects.get_or_create(alumno=estudiante, proyecto=proyecto, semestre=semestre)

                estudiantes_a_eliminar = set(estudiantes_actuales) - set(selected_ids)
                Proyecto_Alumno.objects.filter(alumno_id__in=estudiantes_a_eliminar, proyecto=proyecto).delete()

                return JsonResponse({'status': 'success', 'message': 'Datos del proyecto actualizados y estudiantes asociados/eliminados.'})
            
            else:
                proyecto = Proyecto.objects.create(
                    institucion=institucion,
                    ruc=ruc,
                    titulo=titulo,
                    director=director,
                    cargo=cargo,
                    direccion=direccion
                )

                Proyecto_Alumno.objects.create(
                    alumno=alumno,
                    proyecto=proyecto,
                    semestre=semestre,
                    dictamenPdf='Pendiente'
                )

                for estudiante_id in selected_ids:
                    estudiante = Alumno.objects.get(id=estudiante_id)
                    Proyecto_Alumno.objects.create(alumno=estudiante, proyecto=proyecto, semestre=semestre, dictamenPdf='Pendiente')

                for _ in range(3):
                    Asignacion.objects.create(
                        proyecto=proyecto,
                        semestre_id=semestre.id,
                        fechaEnvio = None,
                        estadoEnvio = 'Pendiente',
                        drivePdf = 'Pendiente',
                        fechaRevision = None,
                        estadoRevision = 'Pendiente',
                        observacionPdf = 'Pendiente'
                    )

                return JsonResponse({'status': 'success', 'message': 'Nuevo proyecto creado y relación establecida con los estudiantes seleccionados, y asignaciones registradas.'})

        except Alumno.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Alumno no encontrado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

def tramites_alumno(request):
    if 'alumno_id' not in request.session:
        return redirect('alumno_login')
    
    alumno_id = request.session['alumno_id']

    try:
        alumno = Alumno.objects.get(id=alumno_id)
        
        if not Proyecto_Alumno.objects.filter(alumno=alumno).exists():
            return redirect('datosInvestigacion_alumno')
        
        proyectos_alumno = Proyecto_Alumno.objects.filter(alumno=alumno)
        proyecto_info = None
        cartas_acceso = []

        for proyecto_alumno in proyectos_alumno:
            proyecto_info = {
                'id': proyecto_alumno.proyecto.id,
                'titulo': proyecto_alumno.proyecto.titulo,
                'institucion': proyecto_alumno.proyecto.institucion,
                'ruc': proyecto_alumno.proyecto.ruc,
                'director': proyecto_alumno.proyecto.director,
                'cargo': proyecto_alumno.proyecto.cargo,
                'direccion': proyecto_alumno.proyecto.direccion,
                'semestre_id': proyecto_alumno.semestre.id if proyecto_alumno.semestre else None, 
            }

            if proyecto_alumno.carta_acceso:
                cartas_acceso.append(proyecto_alumno.carta_acceso)

        tramites = Tramite.objects.all()

        return render(request, 'tramites_alumno.html', {
            'alumno': alumno,
            'tramites': tramites,
            'proyecto_info': proyecto_info,
            'carta_acceso': cartas_acceso, 
        })
    
    except Alumno.DoesNotExist:
        del request.session['alumno_id']
        return redirect('alumno_login')

def generar_pdf(request, proyecto_id, semestre_id):
    if request.method == 'POST':
        try:
            alumnos = Alumno.objects.filter(proyecto_alumno__proyecto_id=proyecto_id, proyecto_alumno__semestre_id=semestre_id)

            if not alumnos.exists():
                return JsonResponse({"status": "error", "message": "No hay otros alumnos relacionados con este proyecto"}, status=404)
            
            contenido = request.POST.get('contenido')
            firma = request.FILES.get('firma')

            response = HttpResponse(content_type='application/pdf')
            generar_pdf_alumno(response, alumnos, contenido, firma)

            return response

        except Alumno.DoesNotExist:
            return JsonResponse({"status": "error", "message": "No se encontraron alumnos para este proyecto"}, status=404)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

def registrar_carta_acceso(request):
    if request.method == 'POST':
        try:
            tramite_id = request.POST.get('tramite')
            proyecto_id = request.POST.get('proyecto_id')
            semestre_id = request.POST.get('semestre_id')

            proyecto_alumnos = Proyecto_Alumno.objects.filter(proyecto_id=proyecto_id, semestre_id=semestre_id)

            if not proyecto_alumnos.exists():
                return JsonResponse({'status': 'error', 'message': 'No se encontró el proyecto.'})

            alumnos = Alumno.objects.filter(proyecto_alumno__proyecto_id=proyecto_id, proyecto_alumno__semestre_id=semestre_id)

            if not alumnos.exists():
                return JsonResponse({'status': 'error', 'message': 'No hay otros alumnos relacionados con este proyecto.'})

            contenido = request.POST.get('contenido')
            firma = request.FILES.get('firma')

            alumno_id = alumnos.first().id
            pdf_file_name = f'semestre-{semestre_id}_proyecto-{proyecto_id}_alumno-{alumno_id}.pdf'
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdfFut', pdf_file_name)

            os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

            carta_acceso_existente = Carta_Acceso.objects.filter(tramite_id=tramite_id, 
                proyecto_alumno__proyecto_id=proyecto_id, 
                proyecto_alumno__semestre_id=semestre_id).first()

            if carta_acceso_existente:
                carta_acceso_existente.contenido = contenido
                carta_acceso_existente.firma = firma 
                carta_acceso_existente.estadoFut = 'Pendiente'
                carta_acceso_existente.fechaFut = timezone.now()
                carta_acceso_existente.save()

                if os.path.exists(pdf_file_path):
                    os.remove(pdf_file_path)

            pdf_response = HttpResponse(content_type='application/pdf')
            generar_pdf_alumno(pdf_response, alumnos, contenido, firma)

            with open(pdf_file_path, 'wb') as f:
                f.write(pdf_response.content)

            if not carta_acceso_existente:
                carta_acceso = Carta_Acceso.objects.create(
                    tramite_id=tramite_id,
                    fechaFut=timezone.now(), 
                    estadoFut='Pendiente',
                    pdfFut=os.path.join('pdfFut', pdf_file_name),
                    observacionFut='Pendiente',
                    pdfCarta='Pendiente'
                )

                proyecto_alumnos.update(carta_acceso=carta_acceso)

            return JsonResponse({'status': 'success', 'message': 'Carta de acceso registrada correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

def evaluacion_alumno(request):
    if 'alumno_id' not in request.session:
        return redirect('alumno_login')

    alumno_id = request.session['alumno_id']
    try:
        alumno = Alumno.objects.get(id=alumno_id)
        
        proyectos_alumno = Proyecto_Alumno.objects.filter(alumno=alumno)
        if not proyectos_alumno.exists():
            return render(request, 'evaluacion_alumno.html', {
                'alumno': alumno,
                'mensaje': 'No hay proyectos registrados.'
            })

        proyectos_data = []
        
        for proyecto_alumno in proyectos_alumno:
            proyecto_id = proyecto_alumno.proyecto.id
            asignaciones = Asignacion.objects.filter(proyecto_id=proyecto_id)
            
            notas_finales = [asignacion.notaFinal for asignacion in asignaciones if asignacion.notaFinal is not None]
            
            if len(notas_finales) == 3:
                nota_promocional = round(sum(notas_finales) / 3, 2)
            else:
                nota_promocional = None

            proyecto_alumno.notaPromocional = nota_promocional
            proyecto_alumno.save()

            proyectos_data.append({
                'proyecto': proyecto_alumno,
                'asignaciones': asignaciones,
                'semestre': proyecto_alumno.semestre,
                'nota_promocional': nota_promocional,
                'dictamenPdf': proyecto_alumno.dictamenPdf
            })
        
        return render(request, 'evaluacion_alumno.html', {
            'alumno': alumno,
            'proyectos_data': proyectos_data,
        })
    except Alumno.DoesNotExist:
        del request.session['alumno_id']
        return redirect('alumno_login')

def actualizar_asignacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        asignacion_id = data.get('asignacionId')
        enlace_drive = data.get('enlace')

        try:
            asignacion = Asignacion.objects.get(id=asignacion_id)
            asignacion.fechaEnvio = timezone.now()
            asignacion.estadoEnvio = 'Enviado'
            asignacion.drivePdf = enlace_drive
            asignacion.fechaRevision = None
            asignacion.estadoRevision = 'Pendiente'
            asignacion.save()

            return JsonResponse({'status': 'success', 'message': 'Datos actualizados correctamente.'})
        except Asignacion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Asignacion not found.'})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'})

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def reestablecerPassword_alumno(request):
    mensaje = ""
    mostrar_modal = False

    if request.method == 'POST':
        form = ReestablecerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                alumno = Alumno.objects.get(email=email)
                
                token = get_random_string(32)

                alumno.reset_token = token
                alumno.save()
                
                ruta = 'http://127.0.0.1:8000/alumnos/resetear-password/'
                enlace = f"{ruta}?token={token}"

                asunto = 'Restablecimiento de Contraseña'
                mensaje_correo = f"""
                Hola {alumno.nombres},

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

            except Alumno.DoesNotExist:
                mensaje = "El correo no está registrado en el sistema."
                mostrar_modal = True

    else:
        form = ReestablecerForm()

    return render(request, 'reestablecerPassword_alumno.html', {
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
                    alumno = Alumno.objects.get(reset_token=token)
                    alumno.password = make_password(nueva_contrasena)
                    alumno.reset_token = None 
                    alumno.save()

                    mensaje = "Tu contraseña ha sido restablecida correctamente."
                    mostrar_modal = True  
                    return render(request, 'reseteoPassword_alumno.html', {
                        'form': form,
                        'mensaje': mensaje,
                        'token': token,
                        'mostrar_modal': mostrar_modal
                    })
                except Alumno.DoesNotExist:
                    mensaje = "Token de restablecimiento inválido."
                    mostrar_modal = True 
        else:
            mensaje = "Por favor corrige los errores en el formulario."
            mostrar_modal = True  

    else:
        form = ResetearForm()

    return render(request, 'reseteoPassword_alumno.html', {
        'form': form,
        'mensaje': mensaje,
        'token': request.GET.get('token'), 
        'mostrar_modal': mostrar_modal 
    })