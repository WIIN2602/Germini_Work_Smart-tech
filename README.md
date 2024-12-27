This project is used for submitting the work WEEK5:Smart Agriculture part 2 of the subject 89036264-64 Artificial Intelligence in Smart Technology by Mr. Weeradech Taengon 65160283.

# Germini: Plant Disease Detection System

This project provides a system for detecting plant diseases, pests, and suggesting remedies using the **Gemini AI**. The app is built with **FastAPI** and integrates AI for advanced image processing and analysis.

## Features

- Upload an image of a plant leaf to detect diseases and pests.
- Get remedies and suggestions for treatment.
- Responsive web interface.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

## Setup Instructions

Follow these steps to set up and run the application:

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/WIIN2602/Germini_Work_Smart-tech.git
```

2. Navigate to the Project Directory
Change into the project directory:
```bash
cd Germini_Work_Smart-tech
```

3. Create and Activate a Virtual Environment
Create a virtual environment for the project:
```bash
python -m venv venv
```
Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install Required Packages
Install all the dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

5. Set Up the Environment Variables
The application requires a Gemini API key. Set the GOOGLE_API_KEY environment variable with your API key:

On Windows (Command Prompt):
```bash
set GOOGLE_API_KEY=your_api_key
```
On macOS/Linux:
```bash
export GOOGLE_API_KEY=your_api_key
```

6. Run the Application
Start the application using:

```bash
python app.py
```

7. Access the Application
Open your browser and navigate to:

```arduino
http://127.0.0.1:8000
```
You will see the web interface where you can upload an image for analysis.

Project Structure
```php
Germini_Work_Smart-tech/
│
├── app.py               # Main FastAPI application
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates for the web interface
│   └── upload.html
├── static/              # Static files (CSS, JS, images)
└── README.md            # Project documentation
```
Usage
Open the web interface.
Upload an image of a plant leaf.
Click "เริ่มการวิเคราะห์" to get disease detection results and remedies.

Troubleshooting
Favicon Not Showing: Ensure the favicon.ico file is located in the static/ or templates/ directory and linked properly in the HTML.
Environment Variable Issues: Double-check the API key and ensure it is exported correctly.
