#!/usr/bin/env python3
"""
Setup script for Llama model download
This script helps download the Llama model with proper authentication
"""
import os
import sys
from huggingface_hub import HfFolder, login
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def check_access():
    """Check if user has access to the model"""
    print("Checking Hugging Face authentication...")
    token = HfFolder.get_token()
    if not token:
        print("❌ No Hugging Face token found!")
        print("Please run: huggingface-cli login")
        return False
    
    print(f"✅ Token found: {token[:10]}...")
    return True

def request_access():
    """Guide user to request access"""
    print("\n" + "="*60)
    print("⚠️  ACCESS REQUIRED")
    print("="*60)
    print("\nThe model 'meta-llama/Llama-3.2-1B' requires access approval.")
    print("\nPlease follow these steps:")
    print("1. Visit: https://huggingface.co/meta-llama/Llama-3.2-1B")
    print("2. Click 'Agree and access repository'")
    print("3. Wait for approval (usually instant or a few minutes)")
    print("4. Run this script again after approval")
    print("\n" + "="*60 + "\n")
    return False

def download_model():
    """Download the Llama model"""
    model_name = "meta-llama/Llama-3.2-1B"
    token = HfFolder.get_token()
    
    print(f"\n📥 Downloading model: {model_name}")
    print("This may take several minutes depending on your internet speed...\n")
    
    try:
        # Download tokenizer
        print("1/2 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=token
        )
        print("   ✅ Tokenizer downloaded successfully!")
        
        # Download model
        print("2/2 Downloading model (this is the large file)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=token,
            dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        print("   ✅ Model downloaded successfully!")
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Llama model is now ready to use.")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "gated" in error_str.lower() or "not in the authorized list" in error_str:
            print("\n❌ Access denied. You need to request access first.")
            return request_access()
        else:
            print(f"\n❌ Error: {e}")
            return False

def main():
    """Main function"""
    print("="*60)
    print("Llama Model Setup Script")
    print("="*60)
    
    # Check authentication
    if not check_access():
        sys.exit(1)
    
    # Try to download
    if download_model():
        print("Setup complete! You can now use the Llama model.")
    else:
        print("\nSetup incomplete. Please follow the instructions above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

