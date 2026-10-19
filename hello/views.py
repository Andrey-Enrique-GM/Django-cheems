from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from .entities.user import User
from .enums.profile import Profile
from .enums.work_order_status import WorkOrderStatus
from .entities.work_order import WorkOrder
from .entities.work_order_history import WorkOrderHistory
from .entities.log import Log



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


    return render(request, 'hello/login.html')


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
        pass
    elif active_tab == 'work_order_history':
        context['work_order_histories'] = WorkOrderHistory.get_all()
        pass
    elif active_tab == 'log':
        context['logs'] = Log.get_all()
        pass

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
        try:
            status = WorkOrderStatus(int(
                request.POST.get('status', str(WorkOrderStatus.PENDING.value))
            ))
        except (TypeError, ValueError):
            return HttpResponseBadRequest('Estado de orden de trabajo inválido.')

        WorkOrder.create(title=title, description=description, status=status)
        
        return redirect('/?tab=work_order')

    return redirect('index')
