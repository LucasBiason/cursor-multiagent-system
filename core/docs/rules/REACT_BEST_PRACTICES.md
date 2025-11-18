# Regras e Boas Práticas React.js

## 📚 Referências Base
- [React Architecture Pattern and Best Practices (GeeksforGeeks)](https://www.geeksforgeeks.org/reactjs/react-architecture-pattern-and-best-practices/)
- [React Design Patterns and Best Practices for 2025 (Telerik)](https://www.telerik.com/blogs/react-design-patterns-best-practices)

## 🎯 Objetivo
Este documento estabelece regras e boas práticas que **TODOS OS AGENTES** devem seguir ao trabalhar com projetos React.js, garantindo código de alta qualidade, performance e manutenibilidade.

---

## 1. ESTRUTURA DE IMPORTS

### ✅ OBRIGATÓRIO: Absolute Imports
**SEMPRE** usar absolute imports ao invés de imports relativos.

```typescript
// ❌ ERRADO - Imports relativos
import { Button } from '../../../components/Button'
import { useAuth } from '../../hooks/useAuth'

// ✅ CORRETO - Absolute imports
import { Button } from '@/components/Button'
import { useAuth } from '@/hooks/useAuth'
```

**Configuração necessária:**
- `vite.config.ts`: Configurar path aliases (`@/`, `@components/`, `@hooks/`, etc.)
- `tsconfig.json`: Adicionar `baseUrl` e `paths` correspondentes

**Aliases padrão:**
- `@/` → `./src/`
- `@components/` → `./src/components/`
- `@hooks/` → `./src/hooks/`
- `@utils/` → `./src/utils/`
- `@services/` → `./src/services/`
- `@types/` → `./src/types/`

---

## 2. COMPONENTES

### 2.1 Function Components (Obrigatório)
**SEMPRE** usar Function Components. Classes são proibidas, exceto para Error Boundaries.

```typescript
// ❌ ERRADO - Class Component
class MyComponent extends React.Component {
  render() {
    return <div>Hello</div>
  }
}

// ✅ CORRETO - Function Component
const MyComponent = () => {
  return <div>Hello</div>
}
```

### 2.2 React.memo para Performance
**SEMPRE** usar `React.memo` em componentes que:
- Recebem props que não mudam frequentemente
- São renderizados frequentemente em listas
- Não dependem de estado interno complexo

```typescript
// ✅ CORRETO
import { memo } from 'react'

export const ProjectCard = memo(({ project }: ProjectCardProps) => {
  return <div>{project.title}</div>
})

ProjectCard.displayName = 'ProjectCard'
```

**Exceções:** Componentes que mudam frequentemente ou têm lógica complexa podem não se beneficiar de `memo`.

### 2.3 Named Exports
**SEMPRE** usar named exports para componentes e utilitários.

```typescript
// ❌ ERRADO
export default MyComponent

// ✅ CORRETO
export const MyComponent = () => { ... }
```

### 2.4 displayName para Debugging
**SEMPRE** adicionar `displayName` em componentes memoizados.

```typescript
export const MyComponent = memo(() => { ... })
MyComponent.displayName = 'MyComponent'
```

---

## 3. HOOKS CUSTOMIZADOS

### 3.1 useCallback para Funções Assíncronas
**SEMPRE** usar `useCallback` em hooks customizados que fazem requisições assíncronas.

```typescript
// ✅ CORRETO
export const useUser = () => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const loadUser = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const userData = await fetchUser()
      setUser(userData)
    } catch (err) {
      console.error('Erro ao carregar usuário:', err)
      setError('Não foi possível carregar dados.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadUser()
  }, [loadUser])

  return { user, loading, error }
}
```

### 3.2 Tratamento de Erros
**SEMPRE** incluir tratamento de erros adequado em hooks.

```typescript
// ✅ CORRETO
try {
  setLoading(true)
  setError(null) // Resetar erro antes de nova tentativa
  const data = await fetchData()
  setData(data)
} catch (err) {
  console.error('Erro descritivo:', err)
  setError('Mensagem amigável ao usuário')
} finally {
  setLoading(false)
}
```

---

## 4. HANDLERS E EVENTOS

### 4.1 useCallback para Handlers
**SEMPRE** usar `useCallback` para handlers de eventos passados como props.

```typescript
// ✅ CORRETO
const handleClick = useCallback((id: string) => {
  // lógica
}, [dependencies])

const handleSubmit = useCallback(async (data: FormData) => {
  // lógica assíncrona
}, [dependencies])
```

### 4.2 Nomenclatura de Handlers
**SEMPRE** usar prefixo `handle` para funções de evento.

```typescript
// ✅ CORRETO
const handleClick = () => { ... }
const handleSubmit = () => { ... }
const handleChange = () => { ... }
const handleMenuToggle = () => { ... }
```

---

## 5. PERFORMANCE

### 5.1 useMemo para Cálculos Pesados
**SEMPRE** usar `useMemo` para:
- Cálculos custosos
- Transformações de dados complexas
- Valores derivados que não mudam frequentemente

```typescript
// ✅ CORRETO
const seoData = useMemo(() => ({
  title: `${user.name} - Portfolio`,
  description: user.bio,
  keywords: user.skills.join(', ')
}), [user.name, user.bio, user.skills])
```

### 5.2 Code Splitting (Lazy Loading)
**SEMPRE** usar `React.lazy` e `Suspense` para componentes grandes ou rotas.

```typescript
// ✅ CORRETO
import { lazy, Suspense } from 'react'

const ExperienceSection = lazy(() => import('@/components/ExperienceSection'))

const App = () => (
  <Suspense fallback={<div>Carregando...</div>}>
    <ExperienceSection />
  </Suspense>
)
```

**Componentes candidatos a lazy loading:**
- Seções grandes (Experience, Services, etc.)
- Formulários complexos
- Modais e dialogs
- Componentes de rotas

---

## 6. ERROR BOUNDARIES

### 6.1 Implementação Obrigatória
**SEMPRE** implementar Error Boundary em aplicações React.

```typescript
// ✅ CORRETO
import React, { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children?: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-fallback">
          <h1>Ocorreu um erro!</h1>
          <p>Por favor, recarregue a página.</p>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
```

### 6.2 Integração no Entry Point
**SEMPRE** envolver a aplicação com Error Boundary no `main.tsx` ou `App.tsx`.

```typescript
// ✅ CORRETO
import ErrorBoundary from '@/components/ErrorBoundary'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
)
```

---

## 7. TYPESCRIPT

### 7.1 Types vs Interfaces
**PREFERIR** `type` ao invés de `interface`, exceto para APIs públicas.

```typescript
// ✅ CORRETO - Type para uso interno
type ProjectCardProps = {
  project: Project
  onSelect?: (id: string) => void
}

// ✅ CORRETO - Interface para APIs públicas
export interface User {
  id: string
  name: string
}
```

### 7.2 Type Hints Obrigatórios
**SEMPRE** adicionar type hints em:
- Props de componentes
- Parâmetros de funções
- Retornos de funções assíncronas
- Estados de hooks

```typescript
// ✅ CORRETO
const MyComponent = ({ title, count }: { title: string; count: number }): JSX.Element => {
  const [data, setData] = useState<string[]>([])
  // ...
}
```

### 7.3 Optional Chaining e Nullish Coalescing
**SEMPRE** usar `?.` e `??` quando apropriado.

```typescript
// ✅ CORRETO
const userName = user?.name ?? 'Usuário'
const projectCount = projects?.length ?? 0
```

---

## 8. ESTRUTURA DE DIRETÓRIOS

### 8.1 Organização Padrão
**SEMPRE** seguir esta estrutura:

```
src/
├── components/        # Componentes React
│   ├── common/       # Componentes reutilizáveis
│   └── layouts/     # Layouts e containers
├── hooks/            # Custom hooks
├── utils/            # Funções utilitárias
├── services/         # API calls e serviços
├── types/             # TypeScript types
└── assets/           # Imagens, fonts, etc.
```

### 8.2 Separação de Responsabilidades
**SEMPRE** separar:
- **Lógica de negócio** → Hooks customizados
- **Apresentação** → Componentes
- **Dados** → Services
- **Utilitários** → Utils

```typescript
// ✅ CORRETO - Lógica no hook
const { projects, loading } = useProjects()

// ✅ CORRETO - Apresentação no componente
return <ProjectGallery projects={projects} />
```

---

## 9. ESTILIZAÇÃO

### 9.1 Tailwind CSS (Obrigatório)
**SEMPRE** usar classes Tailwind CSS. **NUNCA** usar:
- CSS inline (`<style>` tags)
- Arquivos CSS separados (exceto para configurações globais)
- CSS Modules (a menos que explicitamente solicitado)

```typescript
// ❌ ERRADO
<div style={{ color: 'red' }}>Text</div>
<style>{`.my-class { color: red; }`}</style>

// ✅ CORRETO
<div className="text-red-500">Text</div>
```

### 9.2 Classes Condicionais
**SEMPRE** usar bibliotecas como `clsx` ou `cn` para classes condicionais.

```typescript
// ✅ CORRETO
import { clsx } from 'clsx'

<div className={clsx('base-class', {
  'active-class': isActive,
  'disabled-class': isDisabled
})}>
```

---

## 10. ACESSIBILIDADE (a11y)

### 10.1 Atributos Obrigatórios
**SEMPRE** adicionar atributos de acessibilidade em elementos interativos.

```typescript
// ✅ CORRETO
<button
  onClick={handleClick}
  aria-label="Fechar menu"
  tabIndex={0}
>
  <i className="bx bx-x" />
</button>

<a
  href={url}
  target="_blank"
  rel="noreferrer"
  aria-label="Abrir em nova aba"
>
  Link
</a>
```

---

## 11. VALIDAÇÃO E REGRAS ESPECÍFICAS

### 11.1 Early Returns
**SEMPRE** usar early returns para melhorar legibilidade.

```typescript
// ✅ CORRETO
const MyComponent = ({ data }: Props) => {
  if (!data) return null
  if (data.length === 0) return <EmptyState />

  return <DataList data={data} />
}
```

### 11.2 Async/Await
**SEMPRE** preferir `async/await` ao invés de `.then()`.

```typescript
// ❌ ERRADO
fetchData().then(data => setData(data))

// ✅ CORRETO
const loadData = async () => {
  const data = await fetchData()
  setData(data)
}
```

### 11.3 Const vs Function
**SEMPRE** usar `const` com arrow functions ao invés de `function`.

```typescript
// ❌ ERRADO
function myFunction() { ... }

// ✅ CORRETO
const myFunction = () => { ... }
```

---

## 12. CHECKLIST DE IMPLEMENTAÇÃO

Ao criar ou modificar componentes React, **SEMPRE** verificar:

- [ ] ✅ Usa absolute imports (`@/components`, `@/hooks`, etc.)
- [ ] ✅ É um Function Component (não class)
- [ ] ✅ Usa `React.memo` se apropriado
- [ ] ✅ Tem `displayName` se memoizado
- [ ] ✅ Handlers usam `useCallback`
- [ ] ✅ Hooks customizados usam `useCallback` para funções assíncronas
- [ ] ✅ Tratamento de erros adequado
- [ ] ✅ Types TypeScript completos
- [ ] ✅ Usa `useMemo` para cálculos pesados
- [ ] ✅ Considera lazy loading para componentes grandes
- [ ] ✅ Atributos de acessibilidade (aria-label, tabindex, etc.)
- [ ] ✅ Classes Tailwind (não CSS inline)
- [ ] ✅ Early returns quando apropriado
- [ ] ✅ Async/await ao invés de .then()
- [ ] ✅ Named exports

---

## 13. EXCEÇÕES E CASOS ESPECIAIS

### 13.1 Quando NÃO usar React.memo
- Componentes que mudam props frequentemente
- Componentes com muitas dependências
- Componentes muito simples (overhead não vale a pena)

### 13.2 Quando NÃO usar useCallback
- Funções que não são passadas como props
- Funções que mudam a cada render (sem dependências estáveis)

### 13.3 Quando NÃO usar Lazy Loading
- Componentes críticos acima da dobra
- Componentes muito pequenos
- Componentes que são sempre necessários

---

## 14. REFERÊNCIAS RÁPIDAS

### Padrão de Componente Completo
```typescript
import { memo, useCallback, useState } from 'react'
import type { ComponentProps } from '@/types'

type MyComponentProps = {
  title: string
  onAction?: (id: string) => void
}

export const MyComponent = memo(({ title, onAction }: MyComponentProps) => {
  const [state, setState] = useState<string>('')

  const handleClick = useCallback(() => {
    if (onAction) {
      onAction('id')
    }
  }, [onAction])

  return (
    <div className="container">
      <h2>{title}</h2>
      <button onClick={handleClick} aria-label="Ação">
        Clique
      </button>
    </div>
  )
})

MyComponent.displayName = 'MyComponent'
```

### Padrão de Hook Customizado
```typescript
import { useEffect, useState, useCallback } from 'react'
import { fetchData } from '@/services/api'
import type { Data } from '@/types'

export const useData = () => {
  const [data, setData] = useState<Data | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const loadData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await fetchData()
      setData(result)
    } catch (err) {
      console.error('Erro ao carregar dados:', err)
      setError('Não foi possível carregar dados.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  return { data, loading, error }
}
```

---

## 15. NOTAS FINAIS

- **SEMPRE** seguir estas regras ao trabalhar com React.js
- **SEMPRE** revisar código antes de finalizar
- **SEMPRE** verificar o checklist de implementação
- Em caso de dúvida, consultar as referências base ou este documento
- Quando necessário, documentar exceções e justificativas

---

**Última atualização:** 2025-11-17  
**Versão:** 1.0.0  
**Aplicável a:** Todos os agentes do sistema

