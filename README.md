Now say anything naturally:

"shut down chrome" → understands = close_window
"put on some music" → understands = open_spotify
"look up the weather in Ghana" → understands = search_web with query
"take me to the nearest hospital" → understands = open_maps_dest
"make it louder" → understands = volume_up
"what is the speed of light" → understands = conversation

Here is a clean, rewritten version of your notes.

# Voice Assistant Project Setup Guide

## 1. Create the project folder

```bash
mkdir VoiceAssistant
cd VoiceAssistant
```

## 2. Create a virtual environment

```bash
python -m venv voice-env
```

## 3. Activate the virtual environment

**Windows**

```bash
voice-env\Scripts\activate
```

## 4. Install the required packages

Install all the Python packages your project needs.

Example:

```bash
pip install package_name
```

## 5. Create your project files

Create all the Python files and folders needed for your project.

## 6. Create `requirements.txt`

Run:

```bash
pip freeze > requirements.txt
```

## 7. Create a `.gitignore` file

Add files and folders that should not be uploaded to GitHub (such as `voice-env`).

## 8. Test your project

Run:

```bash
python main.py
```

## 9. Initialize Git

```bash
git init
```

## 10. Add your project files

```bash
git add .
```

## 11. Commit your changes

```bash
git commit -m "Initial commit"
```

## 12. Create a repository on GitHub

Create a new repository named **VoiceAssistant** (or your preferred project name).

## 13. Connect your local project to GitHub

Example:

```bash
git remote add origin https://github.com/your-username/VoiceAssistant.git
```

## 14. Push the project to GitHub

```bash
git push -u origin main
```

---

# How Someone Else Can Run the Project

## 15. Clone the repository

```bash
git clone https://github.com/your-username/VoiceAssistant.git
cd VoiceAssistant
```

## 16. Create a virtual environment

```bash
python -m venv voice-env
```

## 17. Activate the virtual environment

```bash
voice-env\Scripts\activate
```

## 18. Install all dependencies

```bash
pip install -r requirements.txt
```

## 19. Run the project

```bash
python main.py
```
What Amaghana can now do in conversation
About herself:

"Who built you?"
"Nicholas built me — he's a software developer studying computer science in Ghana. Pretty talented guy if you ask me, haha!"

Funny failed command:

"Make me a sandwich"
"Ha, I wish I had hands for that! But I can open a recipe search if that helps?"

Natural search help:

"I need to find something about machine learning"
"Sure! Want me to search Google or YouTube for that?"

Banter:

"You're not very smart"
"Ha! Fair enough, I'm still learning. But I bet I can open Chrome faster than you can."

Coding help:

"How do I center a div in CSS?"
"Classic question! Use flexbox — set the parent to display flex, justify-content center and align-items center. Want me to search for more details?"



Say "Hey Amaghana" then try:

"Who made you?"
"Tell me a joke"
"Make me fly"
"Search for the best Python frameworks"
"Open chrome"