from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from .entities.user import User
from .entities.work_order import WorkOrder
from .entities.work_order_history import WorkOrderHistory
from .entities.log import Log
from .enums.profile import Profile
from .enums.work_order_status import WorkOrderStatus
from .enums.system_module import SystemModule
from django.db import connection



def login(request):
    """Vista de Login rudimentaria con manejo de sesión"""
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        user = User.login(account, password)
        if user:
            # Guardamos los datos básicos en la sesión
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_profile'] = int(user.profile)
            
            # log de inicio de sesión
            try:
                Log.create(
                    description=f"El usuario {user.name} ha iniciado sesión",
                    id_user=user.id,
                    module=1 # Usa el 1 (Módulo de Autenticación / Login)
                )
            except Exception as e:
                # imprimir error en consola si falla el log pero permite el acceso
                print(f"Error al guardar log de login: {e}")

            return redirect('index')
        else:
            return render(request, 'hello/login.html', {
                'error': 'Correo o contraseña incorrectos'
            })

    return render(request, 'hello/login.html')


def register(request):
    """Vista básica para registrar un nuevo usuario desde el login"""
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        profile = request.POST.get('profile', 1)

        try:
            user = User.create(name, account, password, int(profile))
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_profile'] = int(user.profile)
            return redirect('index')
        except Exception:
            return render(request, 'hello/login.html', {
                'error': 'No se pudo registrar (la cuenta ya existe o datos inválidos)'
            })

    return redirect('login')


def logout(request):
    """Cierra la sesión borrando los datos guardados"""
    request.session.flush()
    return redirect('login')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        profile = request.POST.get('profile', 1)

        try:
            user = User.create(name, account, password, int(profile))
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_profile'] = int(user.profile)
            return redirect('index')
        except Exception:
            return render(request, 'hello/login.html', {
                'error': 'No se pudo registrar (la cuenta ya existe o datos inválidos)'
            })

    return redirect('login')


def logout(request):
    """Cierra la sesión borrando los datos guardados"""
    request.session.flush()
    return redirect('login')


def get_current_user(request):
    """
    Función auxiliar para obtener el usuario autenticado.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return User.get_by_id(user_id)


def index(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect('login')
    
    # Verifica si el usuario actual es ADMINISTRADOR
    is_admin = (current_user is not None and current_user.profile == Profile.ADMINISTRADOR)

    # Obteniene la pestaña seleccionada (por defecto 'user')
    active_tab = request.GET.get('tab', 'user')

    # Obteniene el ID de la orden de trabajo si se proporciona
    work_order_id = request.GET.get('work_order_id')
    
    context = {
        'current_user': current_user,
        'is_admin': is_admin,
        'active_tab': active_tab,
        'users': None,
        'work_orders': None,
        'work_order_histories': None,
        'logs': None,
    }

    # Carga los datos según la pestaña activa
    if active_tab == 'user':
        context['users'] = User.get_all()
    elif active_tab == 'work_order':
        context['work_orders'] = WorkOrder.get_all()
    elif active_tab == 'work_order_history':
        # Si se recibe un ID de orden de trabajo, filtra solo esa
        if work_order_id:
            context['work_order_histories'] = WorkOrderHistory.get_by_work_order(int(work_order_id))
        else:
            context['work_order_histories'] = WorkOrderHistory.get_all()
    elif active_tab == 'log':
        context['logs'] = Log.get_all()

    return render(request, 'hello/index.html', context)


def create_work_order(request):
    """
    Vista/Endpoint para procesar la creación de una orden de trabajo.
    """
    current_user = get_current_user(request)
    
    # Solo administradores pueden crear órdenes
    if not current_user or current_user.profile != Profile.ADMINISTRADOR:
        # Redirigir o retornar un error si no tiene permisos
        return redirect('index')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Se crea la orden de trabajo en la base de datos
        status = WorkOrderStatus.PENDING
        new_order = WorkOrder.create(title=title, description=description)
        
        # Registra en el Historial (Work Order History)
        try:
            WorkOrderHistory.create(
                id_user=current_user.id,
                action=status.value,
                id_work_order=new_order.id  # Obteniene el ID directamente del objeto creado
            )
        except Exception as e:
            print(f"Error al guardar historial de creación: {e}")

        # log general
        try:
            Log.create(
                description=f"El administrador {current_user.name} creó la orden: '{title}'",
                id_user=current_user.id,
                module=SystemModule.WORK_ORDER.value # Usa el 2 (Módulo de Órdenes de Trabajo)
            )
        except Exception as e:
            print(f"Error al guardar log: {e}")

        return redirect('/?tab=work_order')

    return redirect('index')


def update_work_order_status(request, order_id):
    current_user = get_current_user(request)
    if not current_user or current_user.profile != Profile.ADMINISTRADOR:
        return redirect('index')

    if request.method != 'POST':
        return redirect('index')

    try:
        status = WorkOrderStatus(int(request.POST.get('status')))
    except (TypeError, ValueError):
        return HttpResponseBadRequest('Estado de orden de trabajo inválido.')

    WorkOrder.update_status(order_id=order_id, status=status)

    try:
        WorkOrderHistory.create(
            id_user=current_user.id,
            action=status.value,
            id_work_order=order_id,
        )
    except Exception as e:
        print(f"Error al guardar historial de actualización: {e}")

    try:
        Log.create(
            description=f"El administrador {current_user.name} cambió el estado de la orden ID: {order_id}",
            id_user=current_user.id,
            module=SystemModule.WORK_ORDER.value,
        )
    except Exception as e:
        print(f"Error al guardar log: {e}")

    return redirect('/?tab=work_order')


def update_work_order(request, order_id):
    """
    Vista/Endpoint para procesar la actualización de una orden de trabajo existente.
    """
    current_user = get_current_user(request)
    
    # Solo administradores pueden editar órdenes
    if not current_user or current_user.profile != Profile.ADMINISTRADOR:
        return redirect('index')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            status = WorkOrderStatus(int(
                request.POST.get('status', str(WorkOrderStatus.PENDING.value))
            ))
        except (TypeError, ValueError):
            return HttpResponseBadRequest('Estado de orden de trabajo inválido.')

        # Se actualiza la orden de trabajo en la base de datos
        WorkOrder.update(order_id=order_id, title=title, description=description, status=status)
        
        # Registra el cambio en el Historial (Work Order History)
        try:
            WorkOrderHistory.create(
                id_user=current_user.id,
                action=status.value,
                id_work_order=order_id
            )
        except Exception as e:
            print(f"Error al guardar historial de actualización: {e}")

        # log general
        try:
            Log.create(
                description=f"El administrador {current_user.name} actualizó la orden ID: {order_id}",
                id_user=current_user.id,
                module=SystemModule.WORK_ORDER.value # Usa el 2 (Módulo de Órdenes de Trabajo)
            )
        except Exception as e:
            print(f"Error al guardar log: {e}")

        return redirect('/?tab=work_order')

    return redirect('index')
