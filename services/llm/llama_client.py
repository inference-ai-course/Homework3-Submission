"""
Llama LLM Service Implementation
"""
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import List, Optional
import torch
from huggingface_hub import HfFolder
from services.llm.base import LLMService, LLMResult
from services.llm.prompts import build_prompt
from config.settings import settings
from utils.logger import logger


class LlamaLLMService(LLMService):
    """Llama 3.2 LLM implementation using HuggingFace"""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize Llama LLM service
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to use (cpu, cuda)
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name or settings.llm_model
        self.device = device or settings.llm_device
        self.max_tokens = max_tokens or settings.llm_max_tokens
        
        logger.info(f"Loading LLM model: {self.model_name} on {self.device}")
        
        # Get Hugging Face token for gated models
        hf_token = HfFolder.get_token()
        token_kwargs = {}
        if hf_token:
            token_kwargs["token"] = hf_token
            logger.info("Using Hugging Face token for model access")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            **token_kwargs
        )
        
        # Set pad token if not set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model with appropriate dtype
        model_kwargs = {}
        if self.device == "cpu":
            model_kwargs["dtype"] = torch.float32
        else:
            model_kwargs["dtype"] = torch.float16
        
        # Add token to model kwargs
        model_kwargs.update(token_kwargs)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            **model_kwargs
        )
        
        # Move model to device
        if self.device == "cuda" and torch.cuda.is_available():
            self.model = self.model.to("cuda")
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" and torch.cuda.is_available() else -1
        )
        
        logger.info("LLM model loaded successfully")
    
    def generate(
        self,
        user_message: str,
        conversation_history: Optional[List[dict]] = None
    ) -> LLMResult:
        """
        Generate response to user message
        
        Args:
            user_message: Current user message
            conversation_history: Previous conversation turns
            
        Returns:
            LLMResult with generated response
        """
        try:
            # Build prompt
            prompt = build_prompt(user_message, conversation_history)
            
            logger.debug(f"Generating response for: {user_message[:50]}...")
            
            # Generate response
            outputs = self.pipeline(
                prompt,
                max_new_tokens=self.max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                return_full_text=False
            )
            
            # Extract response
            response_text = outputs[0]["generated_text"].strip()
            
            # Count tokens (approximate)
            tokens_used = len(self.tokenizer.encode(prompt + response_text))
            
            logger.info(f"Generated response: {len(response_text)} chars, ~{tokens_used} tokens")
            
            return LLMResult(
                response=response_text,
                tokens_used=tokens_used,
                model_name=self.model_name
            )
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise


# Global Llama LLM instance
llama_llm = LlamaLLMService()
