# Project Name: Chithara - AI music generation

## Project Overview:
The **Chitara AI Music Generator** is a standalone web-based system that allows users to generate, play, download, and share music through a web browser. The system relies on an external AI music generation service to process user prompts and return generated music content.

## Project Structure:
### Structure Diagram
**chithara**  
 |___ mysite/ <br>
 |___ accounts/ <br>
 |___ musics/ <br>
 |___ manage.py
### Direction Responsibility
- **mysite/** : main configuration and entry point of the whole project.
- **accounts/** : handle user data, perform simple CRUD of the user data and Account Authentication
- **musics/** : handle all music data, perform a simple CRUD of the music data with Music Generation, Music Playback, Music Library, Music Sharing and Download feature.

## Basic setup instructions:
assume user has working GITHUB account
1. Clone  this repository to your local machine
2. (optional) create and run python vitual environment before excute the project file  
> *run this code inside the project directory with your command prompt(Window)*
```
# Create python vitual environment (only for the first time) 
...> python -m venv venv_name
# Run vitual environment 
...> venv_name\Scripts\activate

```
3. Run the program via this command 
> *run this code inside the project directory with your command prompt(Window)*
```
(venv_name)...> python manage.py runserver
```

## Demonstration Video:
[CRUD demonstrate video ](https://youtu.be/8lFgBuS0Oc8)
