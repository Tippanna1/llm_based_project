import requests
import logging
import openai
import os
from transformers import pipeline
from flask import jsonify
import datetime
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)

tokens = os.getenv('HUGGINGFACE_API_KEY')
headers = {
    'Authorization': f'Bearer {tokens}'
}

generator = pipeline('text-generation', model='gpt2', use_auth_token=tokens)

# After other imports and before logging setup
HISTORY_FILE = "history.json"

def load_history():
    """Load history from JSON file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading history: {e}")
    return []

def save_history(history):
    """Save history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving history: {e}")

# Initialize history from file
_history = load_history()

def get_history():
    """Return the processing history"""
    return _history

def process_data(prompt):
    # Use a more focused prompt template
    formatted_prompt = f"""Analyze the following text:
    "{prompt}"

    Please provide:
    1. Summary: 
    2. Keywords: 
    3. Sentiment: 

    Analysis:"""

    response = generator(
        formatted_prompt,
        max_length=200,
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        pad_token_id=50256  
    )
    
    # Extract only the generated analysis, removing the prompt
    generated_text = response[0]['generated_text']
    analysis_start = generated_text.find("Analysis:")
    if analysis_start != -1:
        analysis = generated_text[analysis_start + 9:].strip()
    else:
        analysis = generated_text
        
    # Create result and store in history
    result = {
        "original_text": prompt,
        "analysis": analysis,
        "timestamp": datetime.datetime.now().isoformat()
    }
    _history.append(result)
    save_history(_history)  # Save after each update
    
    return result

def validate_post_data(data):
    if not isinstance(data, dict):
        return (False, 'Invalid data format')
    if not data.get('text'):
        return (False, 'Text is required')
    if not data['text'].strip():
        return (False, 'Text cannot be empty')
    return (True, 'Valid data')

def error_response(message):
    return jsonify({'error': message, 'status': 400, 'success': False}), 400

def success_response(message, data={}):
    return jsonify({'message': message, 'status': 200, 'success': True, 'data': data}), 200