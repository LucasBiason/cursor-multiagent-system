# Configuration Reference

Este diretório (`core/config/`) guarda apenas **templates públicos**. O conteúdo real fica no submódulo privado montado em `config/`.

## Estrutura atual

```
core/config/
├── README.md                # Este arquivo
├── .env.example             # Template público de variáveis
├── config.template.json     # Template do arquivo principal
└── (outros templates no futuro)

config/  (submódulo privado `cursor-multiagent-private`)
├── work/
├── studies/
├── personal/
├── ...
└── config.json, .env, indices, etc.
```

## Como usar

1. **Atualize o submódulo privado**
   ```bash
   git submodule update --init --recursive
   ```

2. **Crie seus arquivos reais dentro de `config/`**
   - Copie `core/config/.env.example` para `config/.env`.
   - Copie `core/config/config.template.json` para `config/config.json`.
   - Ajuste os valores (tokens, caminhos, horários, etc.).

3. **Organize por frentes/projetos**
   - `config/work/<projeto>/...`
   - `config/studies/<projeto>/...`
   - `config/logs/<frente>/<YYYY-MM-DD>_<assunto>.md`
   - Índices (`INDEX.md` ou `metadata.json`) em cada pasta para facilitar RAG.

4. **Faça commit no repositório privado**
   ```bash
   cd config
   git status
   git add .
   git commit -m "Atualiza contextos"
   git push origin main
   ```

5. **Arquivos grandes**
   - Guarde-os no repositório `big_files` (privado).
   - Em `config/`, mantenha apenas um índice apontando para o local/ID do arquivo grande.

## Validação

Os scripts `scripts/setup.sh` e `scripts/validate.sh` continuam verificando se `config/config.json` existe e possui JSON válido (rodando dentro do submódulo).

Antes de subir os agentes:

```bash
./scripts/validate.sh
```

Isso garante que:
- `config/config.json` existe
- `config/.env` está presente (ou você definiu as env vars no shell)
- Não há arquivos sensíveis no repositório público (`core/`)

---

Última atualização: 2025-11-14


