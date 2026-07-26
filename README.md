# 🛡️ Abuse Word Detector
 
A Django web application that detects abusive and offensive words in text input — helping moderate content and keep online spaces clean.
 
---
 
## 🚀 Features
 
- Detects abusive/offensive words in user-submitted text
- Clean and simple web interface
- Built with Django (Python) and HTML templates
- Lightweight SQLite database
- PDF report generation support
 
---
 
## 🛠️ Tech Stack
 
| Layer      | Technology        |
|------------|-------------------|
| Backend    | Python, Django    |
| Frontend   | HTML (Templates)  |
| Database   | SQLite3           |
| PDF Export | `generate_pdf.py` |
 
---
 
## 📁 Project Structure
 
```
abuseworddetector/
├── content_moderator/      # Django project settings & URL configuration
├── detector/               # Core app — views, models, logic
├── templates/
│   └── detector/           # HTML templates for the UI
├── main.py                 # Entry point / standalone detection script
├── generate_pdf.py         # PDF report generation utility
├── manage.py               # Django management CLI
├── db.sqlite3              # SQLite database
├── pyproject.toml          # Project dependencies
└── .replit                 # Replit configuration
```
 
---
 
## ⚙️ Installation & Setup
 
### Prerequisites
 
- Python 3.8+
- pip
 
### Steps
 
1. **Clone the repository**
 
   ```bash
   git clone https://github.com/sauravkumar106/abuseworddetector.git
   cd abuseworddetector
   ```
 
2. **Install dependencies**
 
   ```bash
   pip install -r requirements.txt
   ```
 
   > If using `pyproject.toml` with `uv`:
   > ```bash
   > uv sync
   > ```
 
3. **Apply migrations**
 
   ```bash
   python manage.py migrate
   ```
 
4. **Run the development server**
 
   ```bash
   python manage.py runserver
   ```
 
5. **Open in your browser**
 
   ```
   http://127.0.0.1:8000/
   ```
 
---
 
## 🖥️ Usage
 
1. Navigate to the web app in your browser.
2. Enter or paste the text you want to check.
3. Submit the form — the app will analyze the text and highlight any detected abusive or offensive words.
4. Optionally generate a PDF report of the results using the export feature.
 
---
 
## 🧪 Running Standalone Detection
 
You can also run the detector directly from the command line:
 
```bash
python main.py
```
 
---
 
## 📄 Generating PDF Reports
 
```bash
python generate_pdf.py
```
 
---
 
## 🤝 Contributing
 
Contributions are welcome! To get started:
 
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes and commit (`git commit -m "Add your feature"`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request
 
---
 
## 📜 License
 
This project is open source. Feel free to use, modify, and distribute it.
 
---
 
## 👤 Author

1. **Saurav Kumar**
GitHub: [@sauravkumar106](https://github.com/sauravkumar106)


2. **Pralav Jha**
GitHub: [@Pralav14](https://github.com/pralav14)
 
