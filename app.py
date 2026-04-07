import os
import ssl
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import nltk
from openai import OpenAI
import threading

app = Flask(__name__)
app.secret_key = 'super_secret_pitch_key'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
)

def setup_nltk():
    """Download NLTK tokenizer models if they don't exist."""
    try:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
            
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading NLTK punkt_tab...")
        nltk.download('punkt_tab')
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt...")
        nltk.download('punkt')

threading.Thread(target=setup_nltk).start()


def enhance_prompt_with_llm(sentence, style):
    """
    Use OpenAI's Chat API to refine the base sentence into a highly 
    descriptive and imaginative visual prompt for DALL-E.
    """
    system_prompt = (
        "You are an expert AI prompt engineer. Your job is to take a simple narrative sentence "
        "and expand it into a highly detailed, descriptive, and visually imaginative prompt for an image generation model like DALL-E 3. "
        "Focus on lighting, framing, composition, and visual elements. Do not include any text, letters, or words in the prompt unless absolutely necessary. "
        "Deliver ONLY the final enhanced prompt without any introductory text."
    )
    
    user_prompt = f"Sentence: {sentence}\n\nRequired Style: {style}\n\nPlease transform this into a visual prompt."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    return response.choices[0].message.content.strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/segment', methods=['POST'])
def segment_text():
    data = request.json
    text = data.get('narrative_text', '').strip()
    
    if not text:
        return jsonify({"error": "No text provided."}), 400
        
    try:
        sentences = nltk.tokenize.sent_tokenize(text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        return jsonify({"sentences": sentences})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate_panel', methods=['POST'])
def generate_panel():
    data = request.json
    sentence = data.get('sentence', '').strip()
    style = data.get('style', 'Cinematic, ultra-detailed').strip()
    
    if not sentence:
        return jsonify({"error": "No sentence provided."}), 400
        
    try:
        enhanced_prompt = enhance_prompt_with_llm(sentence, style)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        return jsonify({
            "sentence": sentence,
            "enhanced_prompt": enhanced_prompt,
            "image_url": image_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
