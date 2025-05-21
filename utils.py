from pathlib import Path
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
import pdfkit
from jinja2 import Environment, FileSystemLoader
import io
import base64
import os
from functools import lru_cache
import hashlib
from concurrent.futures import ThreadPoolExecutor
import tempfile

class ReportGenerator:
    def __init__(self):
        self.template_dir = Path("templates")
        self.output_dir = Path("output")
        self.static_dir = Path("static")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # Configure pdfkit options with max settings
        self.max_pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': True,
            'disable-smart-shrinking': None,
            'quiet': None,
            'print-media-type': None,
            'dpi': 300,  # High DPI for max quality
            'image-quality': 100,  # Maximum image quality
            'enable-javascript': None,
            'javascript-delay': '500',  # Longer delay for better rendering
            'no-stop-slow-scripts': None,
            'debug-javascript': True,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore'
        }

        # Configure pdfkit options with min settings
        self.min_pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': True,
            'disable-smart-shrinking': None,
            'quiet': None,
            'print-media-type': None,
            'dpi': 72,  # Minimum DPI
            'image-quality': 30,  # Minimum image quality
            'enable-javascript': True,
            'javascript-delay': '50',  # Minimum delay
            'no-stop-slow-scripts': None,
            'debug-javascript': None,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore',
            'lowquality': None  # Use low quality mode
        }
        
        # Original optimized settings (keeping for backward compatibility)
        self.pdf_options = {
            'page-size': 'A4',
            'orientation': 'Landscape',
            # 'zoom': '0.75',  # Scale down content
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': True,
            'disable-smart-shrinking': None,
            'quiet': None,
            'print-media-type': None,
            'dpi': 100,
            'image-quality': 60,
            'enable-javascript': True,
            'javascript-delay': '100',
            'no-stop-slow-scripts': None,
            'debug-javascript': None,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore',
            'lowquality': None
        }

        # Explicitly set wkhtmltopdf path
        # self.config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        # self.config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf") # macOS/Linux path
        self.config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")

        
        # Create thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
        
        # Pre-compile templates
        self._precompile_templates()

    def _precompile_templates(self):
        """Pre-compile commonly used templates"""
        self.template_cache = {}
        for template_file in self.template_dir.glob("*.html"):
            template = self.env.get_template(template_file.name)
            self.template_cache[template_file.name] = template

    @lru_cache(maxsize=64)
    def _generate_chart_image(self, data_tuple, chart_type, title):
        """Cached chart generation for repeated data"""
        plt.style.use('bmh')
        plt.figure(figsize=(8, 5), dpi=100)  # Further reduced DPI
        plt.gca().set_facecolor('white')
        
        if chart_type == "line":
            plt.plot(data_tuple, linewidth=2, marker='o', markersize=4)
            plt.grid(True, linestyle='--', alpha=0.7)
        elif chart_type == "bar":
            bars = plt.bar(range(len(data_tuple)), data_tuple, width=0.6)
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,.0f}',
                        ha='center', va='bottom')
            plt.grid(True, linestyle='--', alpha=0.7)
        elif chart_type == "pie":
            plt.pie(data_tuple, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
        
        plt.title(title, pad=20, fontsize=12, fontweight='bold')
        plt.xlabel('Time Period', labelpad=10)
        plt.ylabel('Value', labelpad=10)
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, 
                   format='png', 
                   dpi=100,  # Further reduced DPI
                   bbox_inches='tight',
                   facecolor='white',
                   edgecolor='none',
                   pad_inches=0.2)
        img.seek(0)
        plt.close('all')  # Close all figures to prevent memory leaks
        return img.getvalue()

    def create_chart(self, data, chart_type="line", title="Chart", filename=None):
        """
        Create a chart using matplotlib and save it as an image
        """
        # Convert data to tuple for caching
        data_tuple = tuple(data)
        
        # Generate chart image
        img_data = self._generate_chart_image(data_tuple, chart_type, title)
        
        if filename:
            chart_path = self.static_dir / filename
            with open(chart_path, 'wb') as f:
                f.write(img_data)
            abs_path = os.path.abspath(chart_path)
            return f"file:///{abs_path.replace(os.sep, '/')}"
        else:
            return f"data:image/png;base64,{base64.b64encode(img_data).decode()}"

    def generate_pdf(self, template_name, data, output_filename, pdf_options=None):
        """
        Generate a PDF report using the specified template and data
        """
        # Use cached template if available
        template = self.template_cache.get(template_name, self.env.get_template(template_name))
        data['generated_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Render the template
        html_content = template.render(**data)
        
        # Save HTML content to a unique temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", dir=self.output_dir, mode="w", encoding="utf-8") as tmpfile:
            tmpfile.write(html_content)
            temp_html_path = Path(tmpfile.name)
        
        print(temp_html_path)
        try:
            # Generate PDF
            output_path = self.output_dir / output_filename
            pdfkit.from_file(
                str(temp_html_path.resolve()), 
                str(output_path.resolve()), 
                options=pdf_options or self.pdf_options,
                configuration=self.config
            )
        except Exception as e:
            if temp_html_path.exists():
                temp_html_path.unlink()
            raise e
        
        # Clean up temporary HTML file
        if temp_html_path.exists():
            temp_html_path.unlink()
        
        return output_path

    def cleanup_old_files(self, max_age_hours=24):
        """
        Clean up old generated files
        """
        current_time = datetime.now()
        for file in self.output_dir.glob("*"):
            if file.is_file():
                file_age = current_time - datetime.fromtimestamp(file.stat().st_mtime)
                if file_age.total_seconds() > (max_age_hours * 3600):
                    file.unlink() 