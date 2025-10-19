"""
Ollama LLM Integration
Simple integration with Ollama for local LLM models
No compilation required - uses Ollama API
"""

import logging
import requests
import json
from typing import Optional, List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaLLM:
    """
    A simple wrapper for Ollama LLM integration
    Uses Ollama API instead of direct model loading
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "gemma3:12b"):
        """
        Initialize the Ollama LLM
        
        Args:
            base_url: Ollama server URL
            model_name: Name of the model to use
        """
        self.base_url = base_url
        self.model_name = model_name
        self.is_loaded = False
        
        logger.info(f"Ollama LLM initialized with model: {model_name}")
    
    def check_ollama_running(self) -> bool:
        """
        Check if Ollama is running
        
        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def load_model(self, model_name: Optional[str] = None) -> None:
        """
        Load the model in Ollama (this will download if not present)
        
        Args:
            model_name: Name of the model to load
        """
        if model_name:
            self.model_name = model_name
        
        # Check if Ollama is running
        if not self.check_ollama_running():
            raise RuntimeError(
                "Ollama is not running. Please start Ollama first:\n"
                "1. Install Ollama: https://ollama.ai/download\n"
                "2. Start Ollama: ollama serve\n"
                "3. Pull a model: ollama pull gemma2:12b"
            )
        
        # Check if model is available
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if self.model_name not in model_names:
                logger.info(f"Model {self.model_name} not found. Available models: {model_names}")
                logger.info(f"Please run: ollama pull {self.model_name}")
                raise RuntimeError(f"Model {self.model_name} not found. Please run: ollama pull {self.model_name}")
            
            self.is_loaded = True
            logger.info(f"Model {self.model_name} is ready")
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to check Ollama models: {e}")
    
    def generate(self, prompt: str, max_tokens: Optional[int] = None, **kwargs) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: Input prompt for generation
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Prepare the request
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        # Add optional parameters
        if max_tokens:
            data["options"] = {"num_predict": max_tokens}
        
        # Add other parameters
        if "temperature" in kwargs:
            if "options" not in data:
                data["options"] = {}
            data["options"]["temperature"] = kwargs["temperature"]
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("response", "")
            
            logger.debug(f"Generated text: {generated_text[:100]}...")
            return generated_text.strip()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Text generation failed: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Chat with the model using a conversation format
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional generation parameters
            
        Returns:
            Model's response
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Format messages for Ollama
        formatted_prompt = self._format_messages(messages)
        
        # Generate response
        return self.generate(formatted_prompt, **kwargs)
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Format conversation messages into a single prompt
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Formatted prompt string
        """
        formatted_prompt = ""
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                formatted_prompt += f"System: {content}\n\n"
            elif role == "user":
                formatted_prompt += f"Human: {content}\n\n"
            elif role == "assistant":
                formatted_prompt += f"Assistant: {content}\n\n"
        
        # Add a prompt for the assistant to respond
        formatted_prompt += "Assistant:"
        
        return formatted_prompt
    
    def is_loaded(self) -> bool:
        """
        Check if the model is loaded
        
        Returns:
            True if model is loaded, False otherwise
        """
        return self.is_loaded
    
    def unload(self) -> None:
        """
        Unload the model (Ollama keeps models in memory)
        """
        logger.info("Ollama model remains loaded in Ollama server")


# Example usage and testing
if __name__ == "__main__":
    # Create an instance of the Ollama LLM
    ollama_llm = OllamaLLM()
    
    try:
        # Load a model
        print("Loading model...")
        ollama_llm.load_model("gemma3:12b")
        
        # Test simple generation
        print("\nTesting simple generation:")
        prompt = "What is artificial intelligence?"
        response = ollama_llm.generate(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        # Test chat format
        print("\nTesting chat format:")
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Explain machine learning in simple terms."}
        ]
        chat_response = ollama_llm.chat(messages)
        print(f"Chat response: {chat_response}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed: https://ollama.ai/download")
        print("2. Start Ollama: ollama serve")
        print("3. Pull a model: ollama pull gemma2:12b")
