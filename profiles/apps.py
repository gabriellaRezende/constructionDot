from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        # Importando os sinais aqui para garantir que sejam carregados quando o app for iniciado
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group

        def create_default_groups(sender, **kwargs):
            # Cria grupos padrão se não existirem
            for group_name in ['Fornecedor', 'Cliente']:
                Group.objects.get_or_create(name=group_name)

        # Conecta o sinal post_migrate ao método create_default_groups
        post_migrate.connect(create_default_groups, sender=self)