from django.shortcuts import render
from .entities.user import User
#from .entities.work_order import WorkOrder
#from .entities.work_order_history import WorkOrderHistory
#from .entities.log import Log

def index(request):
    # Obtiene la pestaña seleccionada (por defecto 'user')
    active_tab = request.GET.get('tab', 'user')
    
    context = {
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

def login(request):
    #autenticacion de usuario
    return render(request, 'hello/login.html')
