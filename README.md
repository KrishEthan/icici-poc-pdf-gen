# Investment Summary Report Generator

A FastAPI-based application that generates PDF reports for investment summaries. The application creates multi-page PDF reports with dynamic content, including investment data, charts, and executive summaries.

## Features

- Generates multi-page PDF reports
- Supports dynamic content rendering
- Handles investment data, assets, and liabilities
- Asynchronous PDF generation
- Automatic PDF merging
- Background task cleanup

## Project Structure

```
project/
├── main.py              # Main FastAPI application
├── templates/           # HTML templates for PDF generation
├── static/             # Static assets (CSS, images)
├── output/             # Generated PDF files
└── utils.py            # Utility functions and report generator
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install fastapi uvicorn pydantic PyPDF2
```

3. Run the application:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Generate Investment Summary Report
- **Endpoint**: `/generate-investment-summary-report`
- **Method**: POST
- **Request Body**: JSON with the following structure:

```json
{
  "first_page_data": {
    "investment_data": [
      {
        "category": "string",
        "investment_amount": "string",
        "holding_cost": "string",
        "current_value": "string",
        "irr": "string",
        "subcategories": [
          {
            "particular": "string",
            "investment_amount": "string",
            "holding_cost": "string",
            "current_value": "string",
            "irr": "string"
          }
        ]
      }
    ]
  },
  "second_page_data": {
    "investment_data": [...]
  },
  "third_page_data": {
    "assets": [
      {
        "particular": "string",
        "holding_cost": "string",
        "current_value": "string",
        "irr": "string"
      }
    ],
    "liabilities": [
      {
        "particular": "string",
        "loan_credit_limit": "string",
        "outstanding_amount": "string"
      }
    ]
  }
}
```

## How It Works

1. **PDF Generation Process**:
   - The application receives data through the API endpoint
   - Creates separate PDFs for each page using HTML templates
   - Merges the PDFs into a single document
   - Returns the final PDF file

2. **Page Structure**:
   - First Page: Investment Summary (First Section)
   - Second Page: Investment Summary (Second Section)
   - Third Page: Executive Summary (Assets and Liabilities)

## Adding New Pages

To add a new page to the report:

1. Create a new HTML template in the `templates/` directory
2. Define a new Pydantic model for the page data in `main.py`
3. Add the new page generation to the `generate_investment_summary_report` function:

```python
# Add new page generation
new_page_future = loop.run_in_executor(
    pool,
    lambda: report_generator.generate_pdf(
        "new_page_template.html",
        {"data": data.new_page_data},
        new_page_filename
    )
)

# Add to PDF merger
merger.append(str(new_page_path))
```

## Testing

1. **API Testing**:
```python
import requests
import json

# Test data
test_data = {
    "first_page_data": {
        "investment_data": [...]
    },
    "second_page_data": {
        "investment_data": [...]
    },
    "third_page_data": {
        "assets": [...],
        "liabilities": [...]
    }
}

# Send request
response = requests.post(
    "http://localhost:8000/generate-investment-summary-report",
    json=test_data
)

# Save PDF
if response.status_code == 200:
    with open("test_report.pdf", "wb") as f:
        f.write(response.content)
```

2. **Unit Testing**:
Create test files in a `tests/` directory to test individual components:
- Model validation
- PDF generation
- Data processing

## Error Handling

The application includes error handling for:
- Invalid data formats
- PDF generation failures
- File system operations
- API request validation

## Performance Considerations

- Uses ThreadPoolExecutor for CPU-bound tasks
- Implements background tasks for cleanup
- Asynchronous PDF generation
- Parallel processing of multiple pages

## Security

- CORS middleware enabled
- Input validation through Pydantic models
- Secure file handling
- Temporary file cleanup
