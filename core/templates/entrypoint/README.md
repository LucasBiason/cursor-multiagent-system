# Entrypoint Scripts Templates

**Templates de `entrypoint.sh` para copiar e colar.**

---

## 📁 Templates Disponíveis

- `django-entrypoint.sh` - Para aplicações Django
- `fastapi-entrypoint.sh` - Para aplicações FastAPI
- `nodejs-entrypoint.sh` - Para aplicações Node.js (backend)
- `react-entrypoint.sh` - Para aplicações React (frontend)

---

## 🚀 Como Usar

```bash
# Copiar template
cp core/templates/entrypoint/fastapi-entrypoint.sh entrypoint.sh

# Tornar executável
chmod +x entrypoint.sh

# Integrar no Dockerfile
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]
```

---

## 📖 Documentação

**Para instruções completas sobre entrypoints, consulte:**
- **Docker Entrypoint Skill:** `skills/infrastructure/docker-entrypoint/SKILL.md`

---

**Última Atualização:** 2026-01-22
