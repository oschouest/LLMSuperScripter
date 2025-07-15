"""
LLM Interface Module

Handles communication with various LLM providers (OpenAI, local models, etc.)
with built-in safety validation and prompt engineering.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

# Will be implemented with actual LLM libraries
# import openai
# import ollama  # For local models

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def validate_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate a command before execution"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        # self.client = openai.OpenAI(api_key=api_key)
        
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using OpenAI API"""
        # Implementation will use actual OpenAI client
        return "Mock response - implement with actual OpenAI API"
    
    def validate_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate command safety using OpenAI"""
        # Implementation will analyze command safety
        return {
            "safe": True,
            "confidence": 0.95,
            "risks": [],
            "recommendations": []
        }

class LocalLLMProvider(LLMProvider):
    """Local LLM provider (Ollama, etc.)"""
    
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name
        
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using local LLM"""
        # Implementation will use local LLM
        return "Mock response - implement with local LLM"
    
    def validate_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate command safety using local LLM"""
        return {
            "safe": True,
            "confidence": 0.90,
            "risks": [],
            "recommendations": []
        }

class LLMInterface:
    """Main interface for LLM operations"""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.logger = logging.getLogger(__name__)
        
    def parse_natural_language_command(self, user_input: str) -> Dict[str, Any]:
        """Parse natural language into structured commands"""
        prompt = f"""
        Parse the following user request into a structured command:
        
        User Input: "{user_input}"
        
        Return a JSON structure with:
        - action: The main action to perform
        - target: What to modify/configure
        - parameters: Any specific parameters
        - safety_level: risk assessment (low/medium/high)
        - requires_backup: whether backup is needed
        - admin_required: whether admin privileges needed
        
        Example:
        {{
            "action": "install",
            "target": "development_environment",
            "parameters": {{"languages": ["python", "nodejs"]}},
            "safety_level": "low",
            "requires_backup": false,
            "admin_required": true
        }}
        """
        
        response = self.provider.generate_response(prompt)
        
        try:
            # Parse JSON response
            parsed = json.loads(response)
            self.logger.info(f"Parsed command: {parsed}")
            return parsed
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse LLM response: {response}")
            return {"error": "Failed to parse command"}
    
    def generate_execution_plan(self, command: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate step-by-step execution plan"""
        prompt = f"""
        Create a detailed execution plan for this command:
        {json.dumps(command, indent=2)}
        
        Return a JSON array of steps, each with:
        - step_number: Sequential step number
        - description: Human-readable description
        - command: Actual command to execute
        - estimated_time: Estimated duration
        - reversible: Whether this step can be undone
        - backup_required: Whether backup is needed before this step
        """
        
        response = self.provider.generate_response(prompt)
        
        try:
            steps = json.loads(response)
            self.logger.info(f"Generated {len(steps)} execution steps")
            return steps
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse execution plan: {response}")
            return []
    
    def validate_safety(self, command: str) -> Dict[str, Any]:
        """Validate command safety before execution"""
        return self.provider.validate_command(command)

# Factory function for creating LLM interfaces
def create_llm_interface(provider_type: str = "local", **kwargs) -> LLMInterface:
    """Create LLM interface with specified provider"""
    
    if provider_type == "openai":
        api_key = kwargs.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key required")
        provider = OpenAIProvider(api_key, kwargs.get("model", "gpt-4"))
    elif provider_type == "local":
        provider = LocalLLMProvider(kwargs.get("model", "llama2"))
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return LLMInterface(provider)
