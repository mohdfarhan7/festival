# Major Indian Festivals Web Application

An interactive web application that teaches users about major Indian festivals (Diwali, Harvest Festival, and Holi) through engaging content and quizzes.

## Features

- Interactive learning experience
- Step-by-step content presentation
- Quiz for each festival
- Combined quiz for all festivals
- 10-minute timer for the learning session
- Responsive design using Bootstrap
- Beautiful UI with images and videos

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Name: major-festivals
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Click "Create Web Service"

The application will be automatically deployed and you'll get a URL where your application is hosted.

## Project Structure

```
major-festivals/
├── app.py                 # Main Flask application
├── templates/            # HTML templates
├── static/              # Static files
│   ├── css/            # CSS styles
│   ├── js/             # JavaScript files
│   ├── images/         # Festival images
│   └── videos/         # Festival videos
├── data/               # JSON data files
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── Procfile           # Process file for deployment
└── .gitignore         # Git ignore file
```

## Features in Detail

1. **Start Page**
   - Simple start button to begin the learning journey
   - Timer starts when user enters the home page

2. **Home Page**
   - Festival cards with images and descriptions
   - Navigation to individual festival learning sections
   - Access to the combined quiz

3. **Learning Section**
   - Step-by-step content presentation
   - Progress tracking
   - Interactive elements
   - Media integration (images and videos)

4. **Quiz Section**
   - Multiple choice questions
   - Immediate feedback
   - Score tracking
   - Review of incorrect answers

5. **Timer**
   - 10-minute countdown
   - Visible on all pages
   - Redirects to start page when time expires

## Technologies Used

- Flask (Python web framework)
- Bootstrap 5 (Frontend framework)
- JavaScript (Timer and interactivity)
- HTML5 & CSS3
- JSON (Data storage)
- Gunicorn (Production server)

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## License

This project is licensed under the MIT License. 