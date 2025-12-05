# 📄 TEMPLATES - ORGANIZAÇÃO

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: ALTA

---

## 🎯 REGRA DE OURO

**TODOS os templates em `templates/` na raiz do projeto.**  
**Subpastas por app: `templates/{app_name}/`**

---

## 📁 ESTRUTURA OBRIGATÓRIA

```
project/
├── templates/                    # ✅ Pasta central
│   ├── base.html                # Base template
│   ├── components/              # Componentes compartilhados
│   │   ├── pagination.html
│   │   ├── navbar.html
│   │   └── footer.html
│   ├── authentication/          # Templates de auth
│   │   ├── login.html
│   │   ├── register.html
│   │   └── password_reset.html
│   ├── dashboard/               # Templates de dashboard
│   │   ├── analytics.html
│   │   ├── kpi_financeiro.html
│   │   └── dashboard.html
│   └── kpi/                     # Templates de kpi
│       ├── upload_manager.html
│       └── upload.html
├── dashboard/
│   └── templates/               # ❌ NÃO usar
├── kpi/
│   └── templates/               # ❌ NÃO usar
└── authentication/
    └── templates/               # ❌ NÃO usar
```

---

## ✅ ESTRUTURA CORRETA

### Django Settings
```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Pasta central
        'APP_DIRS': False,  # ❌ Desabilitar busca em apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Views
```python
# ✅ CORRETO - Caminho relativo à templates/
def analytics_view(request):
    return render(request, 'dashboard/analytics.html', context)

def upload_view(request):
    return render(request, 'kpi/upload_manager.html', context)

def login_view(request):
    return render(request, 'authentication/login.html', context)
```

```python
# ❌ ERRADO - Caminho duplicado
def analytics_view(request):
    return render(request, 'dashboard/templates/dashboard/analytics.html', context)
```

---

## 🔄 MIGRAÇÃO DE TEMPLATES

### Passo 1: Criar Estrutura
```bash
mkdir -p templates/authentication
mkdir -p templates/dashboard
mkdir -p templates/kpi
mkdir -p templates/components
```

### Passo 2: Mover Templates
```bash
# Mover templates de apps para central
mv dashboard/templates/dashboard/* templates/dashboard/
mv kpi/templates/kpi/* templates/kpi/
mv authentication/templates/authentication/* templates/authentication/

# Mover componentes compartilhados
mv dashboard/templates/components/* templates/components/
```

### Passo 3: Remover Pastas Vazias
```bash
# Remover pastas templates das apps
rmdir dashboard/templates/dashboard dashboard/templates
rmdir kpi/templates/kpi kpi/templates
rmdir authentication/templates/authentication authentication/templates
```

### Passo 4: Atualizar Views
```python
# Buscar e substituir em todas as views
# ANTES: 'dashboard/templates/dashboard/analytics.html'
# DEPOIS: 'dashboard/analytics.html'
```

---

## 📋 ORGANIZAÇÃO POR TIPO

### Base e Componentes Globais
```
templates/
├── base.html                    # Base template
├── 404.html                     # Error pages
├── 500.html
└── components/                  # Componentes compartilhados
    ├── navbar.html
    ├── footer.html
    ├── pagination.html
    └── breadcrumb.html
```

### Templates por App
```
templates/
├── authentication/              # Auth app
│   ├── login.html
│   ├── register.html
│   ├── password_reset.html
│   └── password_change.html
├── dashboard/                   # Dashboard app
│   ├── analytics.html
│   ├── kpi_financeiro.html
│   ├── dashboard.html
│   └── components/              # Componentes específicos
│       ├── kpi_card.html
│       └── filter_card.html
└── kpi/                         # KPI app
    ├── upload_manager.html
    └── upload.html
```

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Templates Espalhados
```
# ❌ ERRADO
dashboard/templates/dashboard/analytics.html
kpi/templates/kpi/upload.html
authentication/templates/login.html

# ✅ CORRETO
templates/dashboard/analytics.html
templates/kpi/upload.html
templates/authentication/login.html
```

### ❌ Exemplo 2: APP_DIRS = True
```python
# ❌ ERRADO - Busca em apps
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,  # ❌ Permite templates em apps
}]

# ✅ CORRETO - Apenas pasta central
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': False,  # ✅ Força uso da pasta central
}]
```

### ❌ Exemplo 3: Caminhos Duplicados
```python
# ❌ ERRADO
render(request, 'dashboard/templates/dashboard/analytics.html')

# ✅ CORRETO
render(request, 'dashboard/analytics.html')
```

---

## 🔍 CHECKLIST DE ORGANIZAÇÃO

### Estrutura
- [ ] Pasta `templates/` existe na raiz
- [ ] Subpastas por app criadas
- [ ] Pasta `components/` para compartilhados
- [ ] `base.html` na raiz de templates/

### Configuração
- [ ] `TEMPLATES['DIRS']` aponta para `templates/`
- [ ] `APP_DIRS = False` em settings
- [ ] Nenhuma pasta `templates/` dentro de apps

### Views
- [ ] Caminhos relativos à `templates/`
- [ ] Sem duplicação de `templates/` no path
- [ ] Includes usam caminhos corretos

### Limpeza
- [ ] Pastas `app/templates/` removidas
- [ ] Nenhum template órfão
- [ ] Imports de templates atualizados

---

## 📝 TEMPLATE INCLUDES

### Base Template
```django
{# templates/base.html #}
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}KPI Dashboard{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'styles/main.css' %}">
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
</body>
</html>
```

### App Template
```django
{# templates/dashboard/analytics.html #}
{% extends 'base.html' %}

{% block title %}Analytics - KPI Dashboard{% endblock %}

{% block content %}
    <div class="container">
        {% include 'components/breadcrumb.html' %}
        {% include 'dashboard/components/kpi_card.html' %}
    </div>
{% endblock %}
```

---

## 🎯 BENEFÍCIOS

### ✅ Vantagens
1. **Centralização**: Todos os templates em um lugar
2. **Organização**: Estrutura clara por app
3. **Manutenção**: Fácil encontrar e editar
4. **Reutilização**: Componentes compartilhados
5. **Performance**: Busca mais rápida (sem APP_DIRS)

### ❌ Problemas Evitados
1. Templates duplicados em apps
2. Caminhos confusos e inconsistentes
3. Dificuldade de encontrar templates
4. Componentes duplicados
5. Conflitos de nomes

---

**UMA PASTA. SUBPASTAS POR APP. SIMPLES E ORGANIZADO.**

