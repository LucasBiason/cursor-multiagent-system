# Como Clonar o Repositório com Submodule Privado

## ✅ Status do Submodule

O repositório privado **ESTÁ** configurado como submodule corretamente.

## Como Funciona

### 1. Clone do Repositório Público

```bash
git clone https://github.com/LucasBiason/cursor-multiagent-system.git
cd cursor-multiagent-system
```

**Resultado:** A pasta `config/` virá **VAZIA** (apenas o arquivo `.git`)

### 2. Inicializar o Submodule (Repositório Privado)

```bash
git submodule update --init --recursive
```

**Comportamento:**
- ✅ Se você **TEM ACESSO** ao repositório privado:
  - O Git tentará clonar `https://github.com/LucasBiason/cursor-multiagent-private.git`
  - Se estiver autenticado no GitHub, vai clonar normalmente
  - A pasta `config/` será preenchida com todo o conteúdo

- ❌ Se você **NÃO TEM ACESSO** ao repositório privado:
  - Vai dar erro de autenticação/permissão
  - A pasta `config/` continuará vazia

### 3. Autenticação Necessária

Para clonar o submodule privado, você precisa:

1. **Estar autenticado no GitHub:**
   ```bash
   gh auth login
   # ou
   git config --global credential.helper store
   ```

2. **Ter acesso ao repositório privado:**
   - O repositório `cursor-multiagent-private` deve estar na sua lista de repositórios
   - Ou você deve ser colaborador do repositório

## Verificação do Submodule

### Status Atual
```bash
git submodule status
```

**Saída esperada:**
```
+0b59f65... config (heads/main)
```

O `+` indica que há uma nova versão disponível no remote.

### Sincronizar com Remote
```bash
git submodule update --remote config
```

## Estrutura Após Clone Completo

```
cursor-multiagent-system/
├── .gitmodules          # Configuração do submodule
├── config/              # Submodule (repositório privado)
│   ├── .git            # Link para o repositório privado
│   ├── CONTEXTO_COMPLETO_ATUAL.md
│   ├── PROJETOS_DETALHADOS.md
│   ├── README.md
│   └── ... (todos os arquivos privados)
└── ... (outros arquivos públicos)
```

## Comandos Úteis

### Atualizar Submodule
```bash
cd config
git pull origin main
cd ..
git add config
git commit -m "Atualizar submodule"
```

### Clonar com Submodules de Uma Vez
```bash
git clone --recurse-submodules https://github.com/LucasBiason/cursor-multiagent-system.git
```

### Verificar URL do Submodule
```bash
cat .gitmodules
```

**Saída:**
```
[submodule "config"]
	path = config
	url = https://github.com/LucasBiason/cursor-multiagent-private.git
```

## Troubleshooting

### Erro: "Permission denied"
- Verifique se está autenticado no GitHub
- Verifique se tem acesso ao repositório privado

### Erro: "Repository not found"
- O repositório privado não existe ou você não tem acesso
- Verifique a URL em `.gitmodules`

### Submodule vazio após clone
- Execute: `git submodule update --init --recursive`
- Verifique autenticação: `gh auth status`

---

**Última Atualização:** 04/12/2025

