# AI-Powered Job Description & Interview Questionnaire Generator 🤖📄❓

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![AI](https://img.shields.io/badge/Powered_by-Gemini_AI-orange.svg)

An intelligent tool that generates professional job descriptions and customized technical interview questionnaires using Google's Gemini AI.

## 🌟 Key Features

### Job Description Generator
- 🏷️ **Position-Specific JDs** - Tailored to exact job titles and levels
- 🛠️ **Tech Stack Integration** - Automatically incorporates specified technologies
- 📈 **Experience Matching** - Adjusts language based on required experience level
- 🏭 **Industry Adaptation** - Customizes terminology for different industries

### Technical Questionnaire Generator
- 🎚️ **Difficulty Levels** - Easy/Medium/Advanced questions
- 🔢 **Custom Quantity** - Generate 5-20 technical questions
- 💡 **Scenario-Based** - Includes practical problem-solving questions
- 🛠️ **Tool-Specific** - Questions about required technologies and tools

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/yourusername/jd-questionnaire-generator.git
cd jd-questionnaire-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Google API key to .env
