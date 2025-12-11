# Regras para Arquivos CSS

**Última Atualização:** 2025-12-08

---

## estrutura de pastas

**sempre usar pasta `styles/` com arquivos separados por tipo:**

```
styles/
├── app.css
├── componentes.css
├── dashboard.css
├── table.css
├── menu.css
└── ...
```

**organização:**
- `app.css` - estilos gerais da aplicação
- `componentes.css` - estilos de componentes reutilizáveis
- `dashboard.css` - estilos específicos do dashboard
- `table.css` - estilos de tabelas
- `menu.css` - estilos de menus/navegação
- outros arquivos conforme necessário

---

## versões minificadas obrigatórias

**sempre criar versão `.min.css` de cada arquivo:**
- `app.css` → `app.min.css`
- `componentes.css` → `componentes.min.css`
- etc.

**processo:**
1. criar arquivo legível (`.css`)
2. minificar para produção (`.min.css`)
3. carregar apenas `.min.css` em produção

---

## carregamento

**regra crítica:**
- **produção:** carregar apenas versões `.min.css`
- **desenvolvimento:** pode carregar versões legíveis (opcional)

**nunca carregar versão legível em produção:**
- impacto negativo no carregamento
- arquivos maiores
- performance reduzida

---

## carregamento por página

**carregar apenas os arquivos necessários em cada página:**

**exemplo:**
```html
<!-- Página de dashboard -->
<link rel="stylesheet" href="/styles/app.min.css">
<link rel="stylesheet" href="/styles/dashboard.min.css">

<!-- Página de tabela -->
<link rel="stylesheet" href="/styles/app.min.css">
<link rel="stylesheet" href="/styles/table.min.css">
```

**não carregar todos os arquivos em todas as páginas.**

---

## django: static files

**desenvolvimento:**
- servir arquivos estáticos via Django URLs
- adicionar em `urls.py` principal:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**produção:**
- usar `collectstatic` para coletar arquivos
- servir via nginx (Django não serve estáticos em produção)
- configurar nginx para servir arquivos estáticos

**comando:**
```bash
python manage.py collectstatic
```

---

## minificação

**ferramentas recomendadas:**
- `cssnano` (via postcss)
- `clean-css`
- `csso`

**processo:**
1. manter arquivos legíveis no repositório
2. minificar durante build/deploy
3. commitar apenas arquivos legíveis (`.min.css` pode ser gerado)

---

## organização

**cada arquivo deve ter responsabilidade única:**
- `app.css` - reset, variáveis, tipografia, layout geral
- `componentes.css` - botões, cards, modais, etc.
- `dashboard.css` - layout específico do dashboard
- `table.css` - estilos de tabelas e listagens
- `menu.css` - navegação, sidebar, header

---

## referências

- regras gerais: `core/agents/programming.mdc`
- django static: `core/docs/programming/DJANGO_RULES.md`

---

**estas regras são obrigatórias para todos os projetos frontend.**


