# The Pitch Visualizer

The Pitch Visualizer is a Flask-based web application that magically transforms a simple narrative into a rich, visual storyboard. Aimed at supercharging sales and pitch teams, it converts 3-5 sentences of text into beautifully generated images mapped to their respective scenes using the power of structural segmentation and AI image generation.

## Capabilities
- **Intelligent Narrative Segmentation**: Uses the NLTK (Natural Language Toolkit) to logically break paragraphs down into discrete scenes.
- **LLM-Powered Prompt Refinement**: Utilizes OpenAI's Chat Completion (`gpt-3.5-turbo`) to upscale simple sentences into dense, highly imaginative, and hyper-detailed prompts suitable for modern image generators.
- **Generative AI Storyboarding**: Integrates seamlessly with DALL-E 3 to physically visualize each segmented idea depending on a selected aesthetic.
- **Dynamic Visual Styles**: Grants absolute control over the artistic direction (e.g., Cinematic, Cyberpunk, Anime/Ghibli, Fantasy Concept Art).
- **Responsive Dynamic UI**: Asynchronous JavaScript fetching renders the storyboard panel-by-panel, ensuring the user is never stuck looking at a stalled loading screen and timeouts are completely bypassed.

## Setup Instructions

### 1. Prerequisites
- **Python 3.10+**
- An active **OpenAI API Key** with credits available for DALL-E 3 and GPT-3.5-Turbo models.

### 2. Environment Setup
1. Open up your terminal or command prompt and navigate to the project directory:
   ```bash
   cd challenge2
   ```
2. Set up a Python Virtual Environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the Virtual Environment:
   - **Windows:** `.venv\Scripts\activate`
   - **MacOS/Linux:** `source .venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. API Key Management
You need to authenticate with OpenAI to use the generative models. Set your API Key securely as an environment variable before running the application:

- **Windows (PowerShell):**
  ```powershell
  $env:OPENAI_API_KEY="your-api-key-here"
  ```
- **Windows (Command Prompt):**
  ```cmd
  set OPENAI_API_KEY=your-api-key-here
  ```
- **MacOS/Linux (Bash/Zsh):**
  ```bash
  export OPENAI_API_KEY="your-api-key-here"
  ```

*(Alternatively, you can create a `.env` file in the root folder with `OPENAI_API_KEY=your-api-key-here` to use the installed `python-dotenv` package manually.)*

### 5. Execution
Run the application using the following command:
```bash
python app.py
```
Open a web browser and navigate to `http://127.0.0.1:5000/`. Type your story in the text area, select your preferred Visual Style, and click **Generate Storyboard**!

## Design Choices & Engineering Methodology

- **Component Decoupling**: Rather than bundling text segmentation and image generation into a bloated monolithic POST route, the application's backend logic is broken out into granular REST JSON endpoints (`/api/segment` and `/api/generate_panel`). This improves fault tolerance and lets the frontend scale dynamically.
- **Asynchronous Front-End (Panel-By-Panel Generation)**: Generating multiple highly complex DALL-E 3 sequences sequentially in a single synchronous server thread is very risky, as it inevitably exceeds standard HTTP timeout limits for longer inputs. By leaning on an asynchronous Javascript fetch loop, we handle long generations elegantly and keep the user engaged by watching the panels progressively populate one-by-one.
- **LLM Refinement Workflow**: To conquer the hurdle of "blank slate" or uninspiring AI image generation, a secondary reasoning LLM pipeline was designed. `gpt-3.5-turbo` catches the tokenized sentence. Through careful system prompting, it refines the bare-bones text into an art-focused descriptive template uniquely compatible with DALL-E 3's strict constraints (such as inherently suppressing rogue text/dialog generation and enforcing specific cinematic lighting mechanics).
- **Graceful NLTK Implementation**: The NLTK segmentation model downloads (`punkt` and `punkt_tab`) run entirely on a separate background thread upon boot. This prevents the initial server start command from hanging aggressively for upwards of 10-15 seconds and failing silently in restricted network environments.

