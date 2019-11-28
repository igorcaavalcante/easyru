from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class OperatorManager(BaseUserManager):
    def create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError(_('CPF não pode ser Nulo!'))

        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(cpf, password, **extra_fields)
