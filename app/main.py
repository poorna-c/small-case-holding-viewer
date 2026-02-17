# import os
# import shutil
# from datetime import datetime
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import HTMLResponse
# from app.data_loader import process_portfolio
# from app.services import generate_dashboard, generate_timeline_chart

# app = FastAPI()

# DATA_FOLDER = "data"
# os.makedirs(DATA_FOLDER, exist_ok=True)

# def get_latest_file():
#     files = [
#         os.path.join(DATA_FOLDER, f)
#         for f in os.listdir(DATA_FOLDER)
#         if f.endswith(".xlsx")
#     ]
#     if not files:
#         return None
#     return max(files, key=os.path.getctime)


# @app.get("/", response_class=HTMLResponse)
# def home():
#     return """
#     <html>
#     <head>
#         <title>Upload Portfolio Excel</title>
#         <style>
#             body {
#                 font-family: Arial;
#                 background: #f4f6f9;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 height: 100vh;
#             }
#             .box {
#                 background: white;
#                 padding: 40px;
#                 border-radius: 10px;
#                 box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#                 text-align: center;
#             }
#             input {
#                 margin: 20px 0;
#             }
#             button {
#                 padding: 10px 20px;
#                 background: #2c3e50;
#                 color: white;
#                 border: none;
#                 border-radius: 5px;
#                 cursor: pointer;
#             }
#             a {
#                 display: block;
#                 margin-top: 20px;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="box">
#             <h2>Upload Portfolio Excel File</h2>
#             <form action="/upload" enctype="multipart/form-data" method="post">
#                 <input name="file" type="file" accept=".xlsx" required>
#                 <br>
#                 <button type="submit">Upload</button>
#             </form>
#             <a href="/dashboard">Go to Dashboard</a>
#             <a href="/timeline">Go to Timeline</a>
#         </div>
#     </body>
#     </html>
#     """


# @app.post("/upload", response_class=HTMLResponse)
# async def upload_file(file: UploadFile = File(...)):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = file.filename.replace(".xlsx", "")
#     new_filename = f"{filename}_{timestamp}.xlsx"
#     file_path = os.path.join(DATA_FOLDER, new_filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return f"""
#     <html>
#         <body style="font-family: Arial; text-align:center; margin-top:50px;">
#             <h3>File uploaded successfully!</h3>
#             <p>Saved as: {new_filename}</p>
#             <a href="/dashboard">Go to Dashboard</a><br><br>
#             <a href="/">Upload Another File</a>
#         </body>
#     </html>
#     """


# @app.get("/dashboard", response_class=HTMLResponse)
# def dashboard():
#     latest_file = get_latest_file()
#     if not latest_file:
#         return "<h3>No Excel file uploaded yet. Please upload first.</h3>"

#     df = process_portfolio(latest_file)
#     return generate_dashboard(df)


# @app.get("/timeline", response_class=HTMLResponse)
# def timeline():
#     latest_file = get_latest_file()
#     if not latest_file:
#         return "<h3>No Excel file uploaded yet. Please upload first.</h3>"

#     df = process_portfolio(latest_file)
#     return generate_timeline_chart(df)


import os
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.data_loader import process_portfolio
from app.services import generate_dashboard, generate_timeline_chart

app = FastAPI()

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)


def get_latest_file():
    files = [
        os.path.join(DATA_FOLDER, f)
        for f in os.listdir(DATA_FOLDER)
        if f.endswith(".xlsx")
    ]
    if not files:
        return None
    return max(files, key=os.path.getctime)


def base_template(content: str, current_file: str = None, error_message: str = None):
    file_label = current_file if current_file else "Upload Portfolio"
    error_html = f'<div class="alert alert-danger text-center">{current_file}</div>' if current_file and "does not contain required columns" in current_file else ""
    # error_html = f'<div class="container mt-3"><div class="alert alert-danger text-center">{error_message}</div></div>' if error_message else ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smallcase Portfolio Analytics</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f8f9fa;
            }}
            .navbar-brand {{
                font-weight: 600;
            }}
            .hero {{
                background: linear-gradient(90deg, #1f2937, #111827);
                color: white;
                padding: 60px 0;
                text-align: center;
            }}
            .card {{
                border: none;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }}
            footer {{
                margin-top: 60px;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: gray;
            }}
        </style>
    </head>
    <body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">📊 Smallcase Portfolio Analytics</a>
        <div class="d-flex align-items-center">
            <span class="text-light me-3 small">
                📁 {file_label}
            </span>
            <a class="btn btn-outline-light btn-sm me-2" href="/dashboard">Dashboard</a>
            <a class="btn btn-outline-light btn-sm" href="/timeline">Timeline</a>
        </div>

      </div>
    </nav>

    {error_html}
    {content}

    <footer>
        Smallcase Portfolio Analytics Dashboard • Built with FastAPI & Plotly
    </footer>

    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    content = """
    <div class="hero">
        <div class="container">
            <h1 class="display-5 fw-bold">Smallcase Portfolio Holding Analyzer</h1>
            <p class="lead mt-3">Upload your smallcase portfolio review Excel and visualize holding patterns beautifully.</p>
        </div>
    </div>

    <div class="container mt-5">
        <div class="card p-5 text-center">
            <h4 class="mb-4">Upload Excel File</h4>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input class="form-control mb-3" name="file" type="file" accept=".xlsx" required>
                <button class="btn btn-dark px-4" type="submit">Upload & Analyze</button>
            </form>
        </div>
    </div>
    """
    return HTMLResponse(base_template(home_content(), current_file=None))

from fastapi import Request

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = file.filename.replace(".xlsx", "")
    new_filename = f"{filename}_{timestamp}.xlsx"
    file_path = os.path.join(DATA_FOLDER, new_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        

        # Test if Excel has proper sheet
        from app.data_loader import process_portfolio
        _ = process_portfolio(file_path)  # will raise ValueError if bad

    except ValueError as ve:
        file.file.close()
        # remove invalid file to avoid clutter
        if os.path.exists(file_path):
            os.remove(file_path)
        return HTMLResponse(base_template(
            content=home_content(),  # reuse home content
            current_file=None,
            error_message="Uploaded Excel file is not supported. Please use correct format."
        ))

    content = f"""
    <div class="container mt-5 text-center">
        <div class="card p-5">
            <h3 class="text-success">✔ File Uploaded Successfully</h3>
            <p class="mt-3">Saved as: <strong>{new_filename}</strong></p>
            <a class="btn btn-dark mt-3" href="/dashboard">Go to Dashboard</a>
        </div>
    </div>
    """

    return HTMLResponse(base_template(content, current_file=new_filename))


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    latest_file = get_latest_file()
    if not latest_file:
        return HTMLResponse(base_template("<div class='container mt-5'><h4>No Excel file uploaded yet.</h4></div>"))

    df = process_portfolio(latest_file)
    content = generate_dashboard(df)
    return HTMLResponse(base_template(content, os.path.basename(latest_file)))


@app.get("/timeline", response_class=HTMLResponse)
def timeline():
    latest_file = get_latest_file()
    if not latest_file:
        return HTMLResponse(base_template("<div class='container mt-5'><h4>No Excel file uploaded yet.</h4></div>"))

    df = process_portfolio(latest_file)
    chart = generate_timeline_chart(df)
    content = f"""
    <div class="container mt-5">
        <div class="card p-4">
            <h4 class="mb-4">Smallcase Portfolio Timeline View</h4>
            {chart}
        </div>
    </div>
    """
    return HTMLResponse(base_template(content, os.path.basename(latest_file)))


def home_content():
    return """
    <div class="hero">
        <div class="container">
            <h1 class="display-5 fw-bold">Portfolio Holding Analyzer</h1>
            <p class="lead mt-3">Upload your portfolio review Excel and visualize holding patterns beautifully.</p>
        </div>
    </div>

    <div class="container mt-5">
        <div class="card p-5 text-center">
            <h4 class="mb-4">Upload Excel File</h4>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input class="form-control mb-3" name="file" type="file" accept=".xlsx" required>
                <button class="btn btn-dark px-4" type="submit">Upload & Analyze</button>
            </form>
        </div>
    </div>
    """
