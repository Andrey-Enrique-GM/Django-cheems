from django.shortcuts import render, redirect
from .entities.user import User
from .enums.profile import Profile
#from .entities.work_order import WorkOrder
#from .entities.work_order_history import WorkOrderHistory
#from .entities.log import Log



def login(request):
    """Vista temporal de Login"""
    # Por ahora solo redirige al index
    return redirect('index')


def get_current_user(request):
    """
    Función auxiliar para obtener el usuario autenticado.
    Por ahora retorna un usuario simulado con perfil ADMINISTRADOR.
    """
    # CÓDIGO PARA CUANDO EL LOGIN ESTÉ LISTO:
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     return None
    # return User.get_by_id(user_id)

    # SIMULACIÓN TEMPORAL (all ADMINISTRADOR):
    return User(name="Admin Temporal", account="admin_test", profile=Profile.ADMINISTRADOR)


def index(request):
    current_user = get_current_user(request)
    
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
        # context['work_orders'] = WorkOrder.get_all()
        pass
    elif active_tab == 'work_order_history':
        # context['work_order_histories'] = WorkOrderHistory.get_all()
        pass
    elif active_tab == 'log':
        # context['logs'] = Log.get_all()
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

        # CÓDIGO PARA GUARDAR EN LA BASE DE DATOS (cuando este listo WorkOrder):
        # WorkOrder.create(title=title, description=description, status='PENDING')
        
        return redirect('/?tab=work_order')

    return redirect('index')
