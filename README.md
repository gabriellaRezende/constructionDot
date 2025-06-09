# 🏗️ constructionDot

Projeto Django com Django Oscar para gerenciamento de loja virtual.


## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:

- [Python 3.10 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- (Opcional) Um editor como [VS Code](https://code.visualstudio.com/)


## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```
git clone https://github.com/gabriellaRezende/constructionDot.git
cd seu-repositorio/constructionDot
```

### 2. Criar ambiente virtual

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar Dependências

Se o arquivo `requirements.txt` estiver presente:

```
pip install -r requirements.txt
```

Se não estiver, instale manualmente os principais pacotes:

```
pip install django==5.2.1
pip install django-oscar
pip install django-widget-tweaks
pip install django-haystack
pip install django-treebeard
pip install sorl-thumbnail
pip install django-tables2
pip install djangorestframework
pip install django-oscar-api
```

Depois, gere o arquivo `requirements.txt` com:

```
pip freeze > requirements.txt
```

### 4. Rodar o projeto

```
python manage.py migrate
python manage.py runserver
```

### ✅ Verificação Pós-Instalação

Após `python manage.py runserver`, abra no navegador:

- http://127.0.0.1:8000/  
  Deve exibir a página inicial padrão do Django Oscar.

- http://127.0.0.1:8000/dashboard/  
  Deve carregar o dashboard (login pode ser necessário).

- http://127.0.0.1:8000/api/  
  Deve apresentar a interface “Browsable API” do Django REST Framework, sem erro 500.

Se qualquer uma dessas URLs retornar erro, revise as configurações de `INSTALLED_APPS` e migrações.

## 👩‍💻 Autora
Gabriella Rezende • gabriella.rzende@...
Thales Pires •  
