# Browser Testing with Playwright MCP

## Objetivo

Esta skill define padrões para testes automatizados em navegador usando o **Playwright MCP** (Model Context Protocol). Quando o usuário solicitar testes ou validações de funcionalidades que abrem no navegador, os agentes **DEVEM** usar o Playwright MCP para:

- Abrir a aplicação no navegador
- Verificar console do navegador (erros JavaScript)
- Verificar logs de rede (network requests)
- Capturar screenshots para validação visual
- Verificar elementos na tela
- Testar interações (cliques, formulários, etc.)

---

## Quando Usar

**SEMPRE** usar Playwright MCP quando:

1. ✅ O usuário solicitar testes de funcionalidades frontend
2. ✅ O usuário pedir para "verificar se está funcionando no navegador"
3. ✅ O usuário pedir para "testar a interface"
4. ✅ O usuário pedir para "verificar erros no console"
5. ✅ O usuário pedir para "validar visualmente"
6. ✅ O usuário pedir para "verificar logs de rede"
7. ✅ O usuário pedir para "testar interações" (cliques, formulários, etc.)

**NÃO** usar Playwright MCP quando:

- ❌ Testes unitários de código backend
- ❌ Testes de API (usar ferramentas como Postman, curl, etc.)
- ❌ Validações que não requerem navegador

---

## Ferramentas Disponíveis

O Playwright MCP está disponível através do servidor MCP `cursor-browser-extension`. As principais ferramentas são:

### Navegação

- `browser_navigate` - Navegar para uma URL
- `browser_navigate_back` - Voltar para página anterior
- `browser_resize` - Redimensionar janela do navegador

### Inspeção

- `browser_snapshot` - Capturar snapshot de acessibilidade (melhor que screenshot)
- `browser_take_screenshot` - Capturar screenshot da página ou elemento
- `browser_console_messages` - Obter mensagens do console
- `browser_network_requests` - Obter requisições de rede

### Interação

- `browser_click` - Clicar em elemento
- `browser_type` - Digitar texto em campo
- `browser_select_option` - Selecionar opção em dropdown
- `browser_drag` - Arrastar e soltar
- `browser_hover` - Passar mouse sobre elemento
- `browser_press_key` - Pressionar tecla

### Utilitários

- `browser_wait_for` - Aguardar texto aparecer/desaparecer ou tempo passar
- `browser_evaluate` - Executar JavaScript na página
- `browser_fill_form` - Preencher múltiplos campos de formulário
- `browser_handle_dialog` - Lidar com diálogos (alert, confirm, prompt)
- `browser_tabs` - Gerenciar abas do navegador

---

## Fluxo de Teste Padrão

### 1. Preparação

```python
# 1. Navegar para a URL da aplicação
browser_navigate(url="http://localhost:3000")

# 2. Aguardar página carregar
browser_wait_for(text="Loading...", textGone="Loading...")
```

### 2. Verificação de Console

```python
# 3. Verificar console para erros JavaScript
console_messages = browser_console_messages()

# Filtrar apenas erros
errors = [msg for msg in console_messages if msg.get("level") == "error"]

if errors:
    # Reportar erros encontrados
    print(f"❌ Erros no console: {len(errors)}")
    for error in errors:
        print(f"  - {error.get('text')}")
else:
    print("✅ Console sem erros")
```

### 3. Verificação de Rede

```python
# 4. Verificar requisições de rede
network_requests = browser_network_requests()

# Filtrar requisições com erro
failed_requests = [
    req for req in network_requests 
    if req.get("status") and req.get("status") >= 400
]

if failed_requests:
    print(f"❌ Requisições com erro: {len(failed_requests)}")
    for req in failed_requests:
        print(f"  - {req.get('url')}: {req.get('status')}")
else:
    print("✅ Todas as requisições bem-sucedidas")
```

### 4. Validação Visual

```python
# 5. Capturar screenshot para validação
browser_take_screenshot(
    filename="test-result.png",
    fullPage=True
)

# 6. Capturar snapshot de acessibilidade (melhor para análise)
snapshot = browser_snapshot()
```

### 5. Interação e Teste

```python
# 7. Testar interações
# Exemplo: Clicar em botão
browser_click(
    element="Login button",
    ref="button[type='submit']"
)

# 8. Aguardar resultado
browser_wait_for(text="Welcome")

# 9. Verificar resultado
snapshot = browser_snapshot()
if "Welcome" in snapshot:
    print("✅ Login bem-sucedido")
else:
    print("❌ Login falhou")
```

---

## Padrões de Validação

### Validação de Console

**SEMPRE** verificar console após carregar página:

```python
console_messages = browser_console_messages()
errors = [msg for msg in console_messages if msg.get("level") == "error"]

if errors:
    # Reportar TODOS os erros encontrados
    for error in errors:
        print(f"❌ Console Error: {error.get('text')}")
        print(f"   Source: {error.get('source')}")
        print(f"   Line: {error.get('line')}")
```

### Validação de Rede

**SEMPRE** verificar requisições de rede após ações:

```python
network_requests = browser_network_requests()

# Verificar requisições falhadas
failed = [r for r in network_requests if r.get("status") >= 400]

# Verificar requisições lentas (> 2s)
slow = [r for r in network_requests if r.get("duration", 0) > 2000]
```

### Validação Visual

**SEMPRE** capturar screenshot quando:

- Página carrega pela primeira vez
- Após interações importantes
- Quando o usuário solicitar validação visual

```python
# Screenshot completo da página
browser_take_screenshot(
    filename="dashboard-complete.png",
    fullPage=True
)

# Screenshot de elemento específico
browser_take_screenshot(
    element="KPI Chart",
    ref="[data-testid='kpi-chart']",
    filename="kpi-chart.png"
)
```

---

## Exemplos de Uso

### Exemplo 1: Teste de Login

```python
# 1. Navegar para página de login
browser_navigate(url="http://localhost:3000/login")

# 2. Aguardar página carregar
browser_wait_for(text="Login")

# 3. Verificar console
console = browser_console_messages()
errors = [m for m in console if m.get("level") == "error"]
assert len(errors) == 0, f"Erros no console: {errors}"

# 4. Preencher formulário
browser_fill_form(fields=[
    {"name": "Email", "ref": "input[name='email']", "type": "textbox", "value": "user@example.com"},
    {"name": "Password", "ref": "input[name='password']", "type": "textbox", "value": "password123"}
])

# 5. Clicar em submit
browser_click(element="Login button", ref="button[type='submit']")

# 6. Aguardar redirecionamento
browser_wait_for(text="Dashboard")

# 7. Verificar resultado
snapshot = browser_snapshot()
assert "Dashboard" in snapshot, "Login falhou"

# 8. Capturar screenshot
browser_take_screenshot(filename="login-success.png")
```

### Exemplo 2: Validação de Dashboard

```python
# 1. Navegar para dashboard
browser_navigate(url="http://localhost:3000/dashboard")

# 2. Aguardar carregamento
browser_wait_for(textGone="Loading...")

# 3. Verificar console
console = browser_console_messages()
errors = [m for m in console if m.get("level") == "error"]
if errors:
    print(f"❌ Erros encontrados: {len(errors)}")
    for error in errors:
        print(f"  - {error.get('text')}")

# 4. Verificar requisições de rede
network = browser_network_requests()
failed = [r for r in network if r.get("status") >= 400]
if failed:
    print(f"❌ Requisições falhadas: {len(failed)}")

# 5. Verificar elementos na tela
snapshot = browser_snapshot()
assert "KPIs" in snapshot, "Seção de KPIs não encontrada"
assert "Charts" in snapshot, "Gráficos não encontrados"

# 6. Capturar screenshot completo
browser_take_screenshot(filename="dashboard-validation.png", fullPage=True)
```

### Exemplo 3: Teste de Formulário

```python
# 1. Navegar para formulário
browser_navigate(url="http://localhost:3000/form")

# 2. Preencher campos
browser_fill_form(fields=[
    {"name": "Name", "ref": "input[name='name']", "type": "textbox", "value": "Test User"},
    {"name": "Email", "ref": "input[name='email']", "type": "textbox", "value": "test@example.com"},
    {"name": "Agree", "ref": "input[name='agree']", "type": "checkbox", "value": "true"}
])

# 3. Selecionar dropdown
browser_select_option(
    element="Country dropdown",
    ref="select[name='country']",
    values=["Brazil"]
)

# 4. Submeter
browser_click(element="Submit button", ref="button[type='submit']")

# 5. Aguardar sucesso
browser_wait_for(text="Success")

# 6. Verificar resultado
snapshot = browser_snapshot()
assert "Success" in snapshot
```

---

## Checklist de Validação

Ao realizar testes no navegador, **SEMPRE** verificar:

- [ ] Console sem erros JavaScript
- [ ] Requisições de rede bem-sucedidas (status < 400)
- [ ] Elementos esperados presentes na tela
- [ ] Interações funcionando corretamente
- [ ] Screenshots capturados para documentação
- [ ] Performance aceitável (requisições < 2s)

---

## Armazenamento de Screenshots

Screenshots devem ser salvos em:

- **Projetos de estudo:** `Projetos/Estudos/.playwright-mcp/`
- **Projetos de trabalho:** `Projetos/Trabalho/[PROJETO]/.playwright-mcp/`
- **Projetos pessoais:** `Projetos/Projetos/[PROJETO]/.playwright-mcp/`

**Nomenclatura:**
- `test-[funcionalidade]-[status].png` (ex: `test-login-success.png`)
- `[página]-[descrição].png` (ex: `dashboard-kpis-complete.png`)
- `[correção]-[descrição].png` (ex: `fix-chart-rendering.png`)

---

## Referências

- **MCP Server:** `cursor-browser-extension`
- **Documentação:** Ver ferramentas disponíveis via `list_mcp_resources`
- **Exemplos:** Ver screenshots em `Projetos/Estudos/.playwright-mcp/`

---

## Notas Importantes

1. **Sempre aguardar carregamento:** Use `browser_wait_for` antes de interagir
2. **Verificar console primeiro:** Erros JavaScript podem indicar problemas sérios
3. **Capturar screenshots:** Facilita validação visual e documentação
4. **Usar snapshot para análise:** `browser_snapshot` é melhor que screenshot para análise programática
5. **Verificar rede:** Requisições falhadas podem indicar problemas de backend

---

## Integração com Agentes

Agentes de programação **DEVEM**:

1. **Reconhecer** quando o usuário solicita testes no navegador
2. **Usar** Playwright MCP automaticamente
3. **Reportar** erros encontrados no console e rede
4. **Capturar** screenshots para validação
5. **Documentar** resultados dos testes

**Exemplo de resposta do agente:**

```
✅ Teste de login realizado com sucesso!

📊 Validações:
- Console: ✅ Sem erros
- Rede: ✅ Todas as requisições bem-sucedidas
- Visual: ✅ Login funcionando corretamente

📸 Screenshot salvo em: .playwright-mcp/test-login-success.png
```

