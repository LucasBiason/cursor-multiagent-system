"""
Few-Shot Examples - Gerenciamento de exemplos few-shot para prompts.

Permite criar e gerenciar exemplos few-shot para melhorar
a qualidade e consistência dos prompts.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class FewShotExample:
    """Representa um exemplo few-shot."""
    
    input_text: str
    output_text: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def format(self, input_format: str = "{input}", output_format: str = "{output}") -> str:
        """Formata o exemplo conforme os templates fornecidos."""
        return f"{input_format.format(input=self.input_text)}\n{output_format.format(output=self.output_text)}"


class FewShotExamples:
    """
    Gerenciador de exemplos few-shot.
    
    Exemplo:
        examples = FewShotExamples()
        examples.add(
            input_text="Crie um diagrama para Bubble Sort",
            output_text="[Diagrama mostrando comparação e troca de elementos]"
        )
        prompt = f"{examples.format_all()}\n\nCrie um diagrama para Quick Sort"
    """
    
    def __init__(self):
        self.examples: List[FewShotExample] = []
    
    def add(
        self,
        input_text: str,
        output_text: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "FewShotExamples":
        """
        Adiciona um exemplo few-shot.
        
        Args:
            input_text: Texto de entrada do exemplo
            output_text: Texto de saída esperado
            description: Descrição opcional do exemplo
            metadata: Metadados adicionais
        
        Returns:
            Self para encadeamento de métodos
        """
        example = FewShotExample(
            input_text=input_text,
            output_text=output_text,
            description=description,
            metadata=metadata or {}
        )
        self.examples.append(example)
        return self
    
    def add_batch(self, examples: List[Dict[str, str]]) -> "FewShotExamples":
        """
        Adiciona múltiplos exemplos de uma vez.
        
        Args:
            examples: Lista de dicionários com 'input' e 'output'
        
        Returns:
            Self para encadeamento de métodos
        """
        for ex in examples:
            self.add(
                input_text=ex.get("input", ""),
                output_text=ex.get("output", ""),
                description=ex.get("description"),
                metadata=ex.get("metadata", {})
            )
        return self
    
    def format_all(
        self,
        input_format: str = "Input: {input}",
        output_format: str = "Output: {output}",
        separator: str = "\n\n"
    ) -> str:
        """
        Formata todos os exemplos em uma string.
        
        Args:
            input_format: Template para formatação do input
            output_format: Template para formatação do output
            separator: Separador entre exemplos
        
        Returns:
            String formatada com todos os exemplos
        """
        formatted = []
        for example in self.examples:
            formatted.append(example.format(input_format, output_format))
        return separator.join(formatted)
    
    def get_n_examples(self, n: int) -> List[FewShotExample]:
        """
        Retorna os primeiros N exemplos.
        
        Args:
            n: Número de exemplos a retornar
        
        Returns:
            Lista com os N primeiros exemplos
        """
        return self.examples[:n]
    
    def filter_by_metadata(self, key: str, value: Any) -> List[FewShotExample]:
        """
        Filtra exemplos por metadados.
        
        Args:
            key: Chave do metadado
            value: Valor esperado
        
        Returns:
            Lista de exemplos que correspondem ao filtro
        """
        return [ex for ex in self.examples if ex.metadata.get(key) == value]
    
    def clear(self):
        """Limpa todos os exemplos."""
        self.examples = []
    
    def count(self) -> int:
        """Retorna o número de exemplos."""
        return len(self.examples)

