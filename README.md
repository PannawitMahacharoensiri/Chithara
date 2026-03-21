# Project Name: Chithara - AI music generation

## Project Overview:
The **Chitara AI Music Generator** is a standalone web-based system that allows users to generate, play, download, and share music through a web browser. The system relies on an external AI music generation service to process user prompts and return generated music content.

## Project Structure:
### Structure Diagram
**chithara**  
 |___ mysite/ <br>
 |___ accounts/ <br>
 |___ musics/ <br>
 |___ manage.py <br>
 |___ . . .
### Direction Responsibility
- **mysite/** : main configuration and entry point of the whole project.
- **accounts/** : handle user data, perform simple CRUD of the user data and Account Authentication
- **musics/** : handle all music data, perform a simple CRUD of the music data with Music Generation, Music Playback, Music Library, Music Sharing and Download feature.

## Basic setup instructions:
Assume you already have a working GitHub account.
#### 1. Clone  this repository to your local machine
```
git clone <your-repo-url> 
cd <your-project-folder>
```
#### 2. Create and activate a virtual environment (optional)   

(Window) command prompt :
```
# Create python vitual environment (only for the first time) 
python -m venv <venv_name>
# Run vitual environment 
<venv_name>\Scripts\activate

```
 (Mac/Linux) Terminal :
```
python3 -m venv <venv_name> 
source <venv_name>/bin/activate
```

#### 3. Apply database migrations
```
python manage.py migrate
```

#### 4. Run the development server
```
python manage.py runserver
```
Then open your browser at:
http://127.0.0.1:8000/

## Demonstration Video:
[CRUD demonstrate video ](https://youtu.be/8lFgBuS0Oc8)
