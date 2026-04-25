# Project Name: Chithara - AI music generation

## Project Overview:
The **Chitara AI Music Generator** is a standalone web-based system that allows users to generate, play, download, and share music through a web browser. The system relies on an external AI music generation service to process user prompts and return generated music content.

## Project Structure:
### Structure Diagram
**chithara** <br>  
 ├── mysite/ <br>
 ├── accounts/ <br>
 ├── media/ <br>
 ├── templates/ <br>
 ├── musics/ <br>
 │   ├── enums/ <br>
 │   ├── migrations/ <br>
 │   ├── models/ <br>
 │   ├── services/ <br>
 │   ├── templates/ <br>
 │   └── utilities/ <br>
 └── manage.py <br>
 
### Directory Responsibility
- **mysite/** : Main Django configuration, project-level URL routing, and global settings.
- **accounts/** : Handles user authentication. Intentionally kept lightweight as it relies heavily on Django's built-in auth system.
- **media/** : Stores local media files, such as the `WIN.mp3` default landing page track and mock audio files.
- **templates/** : Project-level global HTML templates (`base.html`, `index.html`, and global auth overrides).
- **musics/** : The core application handling music generation, playback, and library management. It uses a highly modular architecture:
  - `models/`: Database schemas explicitly separated into `music_model.py`, `genre_model.py`, and `mood_model.py`.
  - `enums/`: Reusable database choices (`generate_state_enum.py`, `generate_strategy_enum.py`).
  - `services/generators/`: Strategy Design Pattern implementation for hot-swapping APIs (`mock_generator.py`, `suno_generator.py`).
  - `utilities/`: Extracted helper logic (`music_form.py`, `polling_task.py`, `visual_suno_quota.py`, `create_default_music.py`).
  - `templates/`: App-specific frontend components (`library.html`, `detail.html`, etc.) that inherit from the global base layout.

## Basic setup instructions:
Assume you already have a working GitHub account.
#### 0. Go to any directory/folder you want to contain the file

#### 1. Clone  this repository to your local machine
```
git clone https://github.com/PannawitMahacharoensiri/Chithara.git 
```
#### 2. Create and activate a virtual environment (optional)   
You may replace **venv_name** with any name that follows standard naming conventions (e.g., snake_case or camelCase).

(Window) command prompt :
```
# Create python vitual environment (only for the first time) 
python -m venv venv_name
# Run vitual environment 
venv_name\Scripts\activate
```
 (Mac/Linux) Terminal :
```
python3 -m venv venv_name 
source venv_name/bin/activate
```

#### 3. Install dependencies
```
cd Chithara
pip install -r requirements.txt
```

#### 4. Set up the Key
Create a `.env` file inside the `chithara/` directory (the same folder that contains `manage.py`) and add the following variables:

```env
# --- Suno AI ---
SUNO_API_KEY=your_suno_api_key_here

# --- Google OAuth ---
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

You can follow these guides on the project Wiki to obtain each key:
- **SUNO_API_KEY** → [Suno API Key Setup](https://github.com/PannawitMahacharoensiri/Chithara/wiki/Suno-API-Key-Setup)
- **GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET** → [Google Cloud OAuth Setup](https://github.com/PannawitMahacharoensiri/Chithara/wiki/Google-Cloud-OAuth-Setup)

> Never commit your `.env` file to version control. Make sure `.env` is always listed in `.gitignore`.

#### 5. Apply database migrations
```
python manage.py migrate
```

#### 6. Run the development server
```
python manage.py runserver
```
Then open your browser at:
http://127.0.0.1:8000/

## How to select Generate Strategy (Mock or Suno).
You can select the generation strategy directly on the **Generate page** it is one of the input fields in the generation form. Simply choose **Mock** (instant, no API key needed) or **Suno** (real AI generation) from the dropdown before submitting.

See the [Demonstration Video](https://youtu.be/NthGzOtg60w) below for a live walkthrough.

## Demonstration Video:
- [CRUD demonstrate video ](https://youtu.be/Py9o0Sbzmw4)
- [generate strategy demonstrate video](https://youtu.be/NthGzOtg60w)

## Project Wiki:
- [Chithara Wiki](https://github.com/PannawitMahacharoensiri/Chithara/wiki)
> All of the Analyzed Diagram are kept in the GitHub Wiki. These includes : class diagram (MVC), domain modeling, sequence diagram, Use Case Diagram.

## License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

© 2026 Pannawit Maharoensiri. All rights reserved.
