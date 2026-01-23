"""
Prompt Chainer - Encadeamento de prompts para fluxos complexos.

Permite criar sequências de prompts onde a saída de um prompt
é usada como entrada para o próximo.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass


@dataclass
class PromptStep:
    """Representa um passo no encadeamento de prompts."""
    
    name: str
    prompt_template: str
    input_variables: List[str]
    output_processor: Optional[Callable[[str], Any]] = None
    
    def render(self, context: Dict[str, Any]) -> str:
        """Renderiza o prompt com o contexto fornecido."""
        try:
            return self.prompt_template.format(**context)
        except KeyError as e:
            raise ValueError(f"Variável faltando no contexto: {e}")
    
    def process_output(self, output: str) -> Any:
        """Processa a saída do prompt."""
        if self.output_processor:
            return self.output_processor(output)
        return output


class PromptChainer:
    """
    Encadeador de prompts para criar fluxos complexos.
    
    Exemplo:
        chainer = PromptChainer()
        chainer.add_step("analyze", "Analise o algoritmo {algorithm}")
        chainer.add_step("visualize", "Crie um diagrama baseado em: {analyze_output}")
        result = chainer.execute({"algorithm": "Bubble Sort"})
    """
    
    def __init__(self):
        self.steps: List[PromptStep] = []
        self.execution_history: List[Dict[str, Any]] = []
    
    def add_step(
        self,
        name: str,
        prompt_template: str,
        input_variables: Optional[List[str]] = None,
        output_processor: Optional[Callable[[str], Any]] = None
    ) -> "PromptChainer":
        """
        Adiciona um passo ao encadeamento.
        
        Args:
            name: Nome único do passo
            prompt_template: Template do prompt (pode usar {variavel} para variáveis)
            input_variables: Lista de variáveis necessárias (auto-detectado se None)
            output_processor: Função para processar a saída do passo
        
        Returns:
            Self para encadeamento de métodos
        """
        if input_variables is None:
            # Auto-detectar variáveis no template
            import re
            input_variables = re.findall(r'\{(\w+)\}', prompt_template)
        
        step = PromptStep(
            name=name,
            prompt_template=prompt_template,
            input_variables=input_variables,
            output_processor=output_processor
        )
        self.steps.append(step)
        return self
    
    def execute(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o encadeamento de prompts.
        
        Args:
            initial_context: Contexto inicial com variáveis de entrada
        
        Returns:
            Dicionário com todas as saídas dos passos
        """
        context = initial_context.copy()
        self.execution_history = []
        
        for step in self.steps:
            # Verificar se todas as variáveis necessárias estão disponíveis
            missing_vars = [var for var in step.input_variables if var not in context]
            if missing_vars:
                raise ValueError(
                    f"Passo '{step.name}' requer variáveis faltando: {missing_vars}"
                )
            
            # Renderizar prompt
            prompt = step.render(context)
            
            # Executar prompt (deve ser implementado pelo chamador)
            # Por enquanto, apenas armazena o prompt
            execution_record = {
                "step": step.name,
                "prompt": prompt,
                "input_context": context.copy()
            }
            
            # Adicionar placeholder para saída
            output_key = f"{step.name}_output"
            context[output_key] = f"[Output of {step.name}]"
            
            execution_record["output"] = context[output_key]
            self.execution_history.append(execution_record)
        
        return context
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de execução."""
        return self.execution_history
    
    def clear(self):
        """Limpa todos os passos do encadeamento."""
        self.steps = []
        self.execution_history = []

