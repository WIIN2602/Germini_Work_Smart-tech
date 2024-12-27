import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from PIL import Image
import google.generativeai as genai
from io import BytesIO

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def configure_genai():
    genai.configure(api_key=os.getenv(
        'AIzaSyAPBQu6gK_tu2ydpwJi31kS7ttCgTGH0Ho'))


def initialize_model():
    return genai.GenerativeModel('gemini-1.5-pro')


async def process_image(model, image):
    prompt = """วิเคราะห์โรคในใบพืช,ต้นเหตุที่คาดว่าน่าจะเป็นเหตุผลให้เกิดโรคนี้,และวิธีการรักษา """

    response = model.generate_content([prompt, image])
    return response.text


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/process-receipt/")
async def process_receipt(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        configure_genai()
        model = initialize_model()

        response_text = await process_image(model, image)

        return {
            "status": "success",
            "text": response_text
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def setup_directories_and_files():
    os.makedirs("templates", exist_ok=True)

    with open("templates/upload.html", "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>วิเคราะห์โรคในใบพืชด้วยGemini</title>
    <style>
        body {
            font-family: 'Sarabun', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(to bottom, #e3f2fd, #f5f5f5);
            color: #34495e;
        }
        .container {
            text-align: center;
            background: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            animation: fadeIn 0.8s ease-in-out;
        }
        .upload-form {
            margin: 30px 0;
            padding: 25px;
            border: 2px dashed #3498db;
            border-radius: 15px;
            background: linear-gradient(to right, #dceefd, #f8f9fa);
            transition: all 0.3s ease-in-out;
        }
        .upload-form:hover {
            border-color: #2980b9;
            background: linear-gradient(to right, #eaf6ff, #ffffff);
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            text-align: left;
            background: #fafafa;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            white-space: pre-line;
            line-height: 1.8;
        }
        #preview {
            max-width: 300px;
            margin: 15px 0;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            display: none;
        }
        button {
            background: linear-gradient(to right, #3498db, #2980b9);
            color: #ffffff;
            padding: 12px 25px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }
        button:hover {
            background: linear-gradient(to right, #2980b9, #1c598a);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .loading {
            color: #7f8c8d;
            font-style: italic;
            font-size: 14px;
        }
        .error {
            color: #e74c3c;
            padding: 12px;
            background: #ffe6e6;
            border-radius: 10px;
            margin-top: 15px;
            border: 1px solid #e5a4a4;
        }
        .text-response {
            text-align: left;
            font-size: 16px;
            color: #2c3e50;
            background: #f1f8ff;
            padding: 20px;
            border-radius: 10px;
            margin-top: 15px;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            line-height: 1.8;
        }
        h1 {
            font-size: 28px;
            color: #2c3e50;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            animation: fadeInDown 0.8s ease-in-out;
        }
        input[type="file"] {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #bdc3c7;
            transition: all 0.3s ease-in-out;
        }
        input[type="file"]:hover {
            border-color: #3498db;
            background: #eaf6ff;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16x16.png">
    <link rel="shortcut icon" href="images/favicon.ico">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>วิเคราะห์โรคในใบพืชด้วยGemini</h1>
        <div class="upload-form">
            <form id="uploadForm">
                <input type="file" id="imageInput" accept="image/*" onchange="previewImage(event)">
                <br><br>
                <img id="preview" style="display: none;">
                <br>
                <button type="submit">เริ่มการวิเคราะห์</button>
            </form>
        </div>
        <div id="result" class="result" style="display: none;"></div>
    </div>

    <script>
        function previewImage(event) {
            const preview = document.getElementById('preview');
            const file = event.target.files[0];
            const reader = new FileReader();

            reader.onload = function() {
                preview.src = reader.result;
                preview.style.display = 'inline';
            }

            if (file) {
                reader.readAsDataURL(file);
            }
        }

        function formatResults(data) {
            if (data.status === 'error') {
                return `<div class="error">เกิดข้อผิดพลาด: ${data.error}</div>`;
            }

            return `<div class="text-response">${data.text}</div>`;
        }

        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            const fileInput = document.getElementById('imageInput');
            const resultDiv = document.getElementById('result');
            
            if (fileInput.files.length === 0) {
                alert('กรุณาเลือกไฟล์ภาพ');
                return;
            }

            formData.append('file', fileInput.files[0]);
            resultDiv.innerHTML = '<div class="loading">กำลังประมวลผล...</div>';
            resultDiv.style.display = 'block';

            try {
                const response = await fetch('/process-receipt/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                resultDiv.innerHTML = formatResults(data);
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">เกิดข้อผิดพลาด: ' + error.message + '</div>';
            }
        });
    </script>
</body>
</html>
""")


if __name__ == "__main__":
    setup_directories_and_files()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
