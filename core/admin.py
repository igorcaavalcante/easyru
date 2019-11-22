from django.contrib import admin
from .models import Funcionario
from .models import Usuario
from .models import Consumidor
from .models import Gru
from .models import Transacao

# Register your models here.
admin.site.register(Operator)
admin.site.register(User)
admin.site.register(Consumer)
admin.site.register(Gru)
admin.site.register(Transaction)
