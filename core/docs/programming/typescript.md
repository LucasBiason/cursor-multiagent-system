# typescript e react - padrões e boas práticas

**última atualização:** 2025-12-08  
**aplicável a:** todos os projetos frontend (react, next.js, typescript)

---

## regras gerais

### typescript obrigatório
- **sempre usar typescript** (nunca javascript)
- **type hints obrigatórios** em props, parâmetros, retornos
- **preferir `type`** ao invés de `interface` (exceto para apis públicas)
- **optional chaining** (`?.`) e nullish coalescing (`??`) quando apropriado

### código
- **sem emojis** em código typescript/javascript
- **comentários em inglês**
- **código limpo** e profissional

---

## imports

### absolute imports obrigatório

```typescript
// ❌ errado - imports relativos
import { Button } from '../../../components/Button'
import { useAuth } from '../../hooks/useAuth'

// ✅ correto - absolute imports
import { Button } from '@/components/Button'
import { useAuth } from '@/hooks/useAuth'
```

### aliases padrão

```typescript
// vite.config.ts ou tsconfig.json
{
  "@/": "./src/",
  "@components/": "./src/components/",
  "@hooks/": "./src/hooks/",
  "@utils/": "./src/utils/",
  "@services/": "./src/services/",
  "@types/": "./src/types/"
}
```

---

## componentes react

### function components obrigatório

```typescript
// ❌ errado - class component
class MyComponent extends React.Component {
  render() {
    return <div>Hello</div>
  }
}

// ✅ correto - function component
const MyComponent = () => {
  return <div>Hello</div>
}
```

### react.memo para performance

```typescript
import { memo } from 'react'

export const ProjectCard = memo(({ project }: ProjectCardProps) => {
  return <div>{project.title}</div>
})

ProjectCard.displayName = 'ProjectCard'
```

**quando usar:**
- componentes que recebem props que não mudam frequentemente
- componentes renderizados frequentemente em listas
- componentes sem estado interno complexo

**quando não usar:**
- componentes que mudam props frequentemente
- componentes com muitas dependências
- componentes muito simples (overhead não vale)

### named exports obrigatório

```typescript
// ❌ errado
export default MyComponent

// ✅ correto
export const MyComponent = () => { ... }
```

### displayname para debugging

```typescript
export const MyComponent = memo(() => { ... })
MyComponent.displayName = 'MyComponent'
```

---

## hooks

### usecallback para handlers

```typescript
import { useCallback } from 'react'

const MyComponent = ({ onAction }: Props) => {
  const handleClick = useCallback(() => {
    if (onAction) {
      onAction('id')
    }
  }, [onAction])
  
  return <button onClick={handleClick}>Click</button>
}
```

### usecallback em hooks customizados

```typescript
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

### tratamento de erros

```typescript
try {
  setLoading(true)
  setError(null) // resetar erro antes de nova tentativa
  const data = await fetchData()
  setData(data)
} catch (err) {
  console.error('Erro descritivo:', err)
  setError('Mensagem amigável ao usuário')
} finally {
  setLoading(false)
}
```

### usememo para cálculos pesados

```typescript
import { useMemo } from 'react'

const seoData = useMemo(() => ({
  title: `${user.name} - Portfolio`,
  description: user.bio,
  keywords: user.skills.join(', ')
}), [user.name, user.bio, user.skills])
```

---

## nomenclatura

### handlers

```typescript
// ✅ correto - prefixo handle
const handleClick = () => { ... }
const handleSubmit = () => { ... }
const handleChange = () => { ... }
const handleMenuToggle = () => { ... }
```

### variáveis e funções

```typescript
// camelCase
const userName = 'John'
const fetchUserData = async () => { ... }

// booleanos com prefixo
const isLoaded = true
const hasError = false
const canEdit = true
```

### componentes e types

```typescript
// PascalCase
type ProjectCardProps = { ... }
interface User { ... }
const MyComponent = () => { ... }
```

---

## performance

### code splitting (lazy loading)

```typescript
import { lazy, Suspense } from 'react'

const ExperienceSection = lazy(() => import('@/components/ExperienceSection'))

const App = () => (
  <Suspense fallback={<div>Carregando...</div>}>
    <ExperienceSection />
  </Suspense>
)
```

**componentes candidatos:**
- seções grandes (experience, services, etc.)
- formulários complexos
- modais e dialogs
- componentes de rotas

---

## error boundaries

### implementação obrigatória

```typescript
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

### integração no entry point

```typescript
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

## typescript

### types vs interfaces

```typescript
// ✅ correto - type para uso interno
type ProjectCardProps = {
  project: Project
  onSelect?: (id: string) => void
}

// ✅ correto - interface para apis públicas
export interface User {
  id: string
  name: string
}
```

### type hints obrigatórios

```typescript
// ✅ correto
const MyComponent = ({ title, count }: { title: string; count: number }): JSX.Element => {
  const [data, setData] = useState<string[]>([])
  // ...
}
```

### optional chaining e nullish coalescing

```typescript
// ✅ correto
const userName = user?.name ?? 'Usuário'
const projectCount = projects?.length ?? 0
```

---

## estrutura de diretórios

### organização padrão

```
src/
├── components/        # componentes react
│   ├── common/       # componentes reutilizáveis
│   └── layouts/     # layouts e containers
├── hooks/            # custom hooks
├── utils/            # funções utilitárias
├── services/         # api calls e serviços
├── types/             # typescript types
└── assets/           # imagens, fonts, etc.
```

### separação de responsabilidades

```typescript
// ✅ correto - lógica no hook
const { projects, loading } = useProjects()

// ✅ correto - apresentação no componente
return <ProjectGallery projects={projects} />
```

---

## estilização

### tailwind css obrigatório

```typescript
// ❌ errado
<div style={{ color: 'red' }}>Text</div>
<style>{`.my-class { color: red; }`}</style>

// ✅ correto
<div className="text-red-500">Text</div>
```

**nunca usar:**
- css inline (`<style>` tags)
- arquivos css separados (exceto configurações globais)
- css modules (a menos que explicitamente solicitado)

### classes condicionais

```typescript
import { clsx } from 'clsx'

<div className={clsx('base-class', {
  'active-class': isActive,
  'disabled-class': isDisabled
})}>
```

---

## acessibilidade (a11y)

### atributos obrigatórios

```typescript
// ✅ correto
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

## padrões de código

### early returns

```typescript
// ✅ correto
const MyComponent = ({ data }: Props) => {
  if (!data) return null
  if (data.length === 0) return <EmptyState />

  return <DataList data={data} />
}
```

### async/await

```typescript
// ❌ errado
fetchData().then(data => setData(data))

// ✅ correto
const loadData = async () => {
  const data = await fetchData()
  setData(data)
}
```

### const vs function

```typescript
// ❌ errado
function myFunction() { ... }

// ✅ correto
const myFunction = () => { ... }
```

---

## ecossistema frontend - práticas avançadas

### react avançado

**componentes funcionais - sempre:**
- class components são legado
- function components são mais simples, mais fáceis de testar
- melhor suporte a hooks

**react.memo - quando usar:**
- componentes renderizados em listas grandes
- componentes que recebem props que raramente mudam
- componentes pesados (muitos cálculos, muitos elementos DOM)

**quando não usar memo:**
- componentes simples (overhead não vale)
- componentes com props que mudam frequentemente
- componentes com muitas dependências

**usecallback - evitar re-criação de funções:**
- memoiza funções, evitando que componentes filhos re-renderizem
- use em handlers passados como props
- use em hooks customizados para funções assíncronas

**usememo - cálculos pesados:**
- memoiza resultados de cálculos
- use para transformações de dados complexas
- use para objetos/arrays que são passados como props

### typescript avançado

**types vs interfaces - quando usar cada um:**
- type: para uso interno, unions, intersections
- interface: para apis públicas, extensão

**type guards - validação em runtime:**
```typescript
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'email' in obj
  )
}
```

**generics - reutilização de código:**
```typescript
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  // ...
}
```

### gerenciamento de estado

**usestate - estado local simples:**
- use para estado simples (strings, numbers, booleans)
- evite objetos complexos (use useReducer)

**usereducer - estado complexo:**
- use quando estado tem lógica complexa
- use quando há múltiplas ações relacionadas
- use quando estado precisa ser atualizado de forma previsível

**context api - estado global simples:**
- use para estado global simples (tema, autenticação)
- não use para estado que muda frequentemente
- não use para estado complexo (use zustand/redux)

**zustand/redux - estado global complexo:**
- use para estado global complexo
- use quando precisa de middleware
- use quando precisa de time-travel debugging

### performance - otimizações reais

**code splitting - lazy loading:**
- lazy load de rotas
- lazy load de componentes grandes
- use suspense para fallback

**virtual scrolling - listas grandes:**
- use para listas com milhares de itens
- bibliotecas: @tanstack/react-virtual
- melhora performance drasticamente

**debounce e throttle - inputs e scroll:**
- use debounce para inputs de busca
- use throttle para scroll events
- use useMemo para memoizar funções debounced

### testes - frontend testing

**testing library - testes de componentes:**
- teste comportamento, não implementação
- use queries acessíveis (getByRole, getByLabelText)
- teste interações do usuário

**mocks - apis e hooks:**
- mock de apis para testes isolados
- mock de hooks para testes de componentes
- use jest.mock para mocks globais

### estrutura de projeto - organização que escala

**estrutura recomendada:**
```
src/
├── components/          # Componentes React
│   ├── common/         # Componentes reutilizáveis
│   ├── features/       # Componentes específicos de features
│   └── layouts/        # Layouts
├── hooks/              # Custom hooks
├── services/           # API calls e serviços externos
├── stores/             # State management
├── utils/              # Funções utilitárias
├── types/              # TypeScript types
├── pages/              # Páginas/rotas
└── assets/             # Imagens, fonts, etc.
```

**barrel exports - organização de imports:**
```typescript
// components/common/index.ts
export { Button } from './Button'
export { Input } from './Input'

// Uso
import { Button, Input } from '@/components/common'
```

### acessibilidade (a11y) - não é opcional

**aria labels - sempre que necessário:**
- botões com ícone precisam aria-label
- inputs precisam labels associados
- listas precisam roles apropriados

**navegação por teclado:**
- suporte a tab navigation
- suporte a escape key para modais
- suporte a enter/space para botões

### build e deploy - otimizações

**bundle analysis - identificar problemas:**
- use source-map-explorer
- identifique bundles grandes
- otimize imports desnecessários

**environment variables - configuração:**
- use .env.local para desenvolvimento
- use variáveis prefixadas (VITE_, NEXT_PUBLIC_)
- nunca commite .env files

**error tracking - produção:**
- use error boundaries com tracking
- envie erros para serviço de tracking
- capture contexto útil

---

## checklist de implementação

ao criar ou modificar componentes react, sempre verificar:

- [ ] usa absolute imports (`@/components`, `@/hooks`, etc.)
- [ ] é um function component (não class)
- [ ] usa `react.memo` se apropriado
- [ ] tem `displayname` se memoizado
- [ ] handlers usam `usecallback`
- [ ] hooks customizados usam `usecallback` para funções assíncronas
- [ ] tratamento de erros adequado
- [ ] types typescript completos
- [ ] usa `usememo` para cálculos pesados
- [ ] considera lazy loading para componentes grandes
- [ ] atributos de acessibilidade (aria-label, tabindex, etc.)
- [ ] classes tailwind (não css inline)
- [ ] early returns quando apropriado
- [ ] async/await ao invés de .then()
- [ ] named exports

---

## referências

- frontend ecosystem → seção "ecossistema frontend - práticas avançadas" acima
- python best practices → `python.md`
- api rest → `api-rest.md`
- architecture → `architecture.md`

---

**estas regras são obrigatórias em todos os projetos typescript/react.**

