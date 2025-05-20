from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from utils import ReportGenerator
import asyncio
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfMerger

# Create necessary directories
TEMPLATES_DIR = Path("templates")
STATIC_DIR = Path("static")
OUTPUT_DIR = Path("output")

# Ensure directories exist
for directory in [TEMPLATES_DIR, STATIC_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

app = FastAPI(
    title="Report Generation API",
    description="API for generating PDF reports with dynamic content",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize report generator
report_generator = ReportGenerator()

# Create thread pool for CPU-bound tasks
thread_pool = ThreadPoolExecutor(max_workers=4)

class ReportData(BaseModel):
    title: str
    summary: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    chart_data: Optional[List[float]] = None
    chart_type: Optional[str] = "line"
    chart_title: Optional[str] = "Chart"

class InvestmentSubcategory(BaseModel):
    particular: str
    investment_amount: str
    holding_cost: str
    current_value: str
    irr: str

class InvestmentSection(BaseModel):
    category: str
    investment_amount: str
    holding_cost: str
    current_value: str
    irr: str
    subcategories: List[InvestmentSubcategory]

class Assets(BaseModel):
    particular: str
    holding_cost: Optional[str] = None
    current_value: Optional[str] = None
    irr: Optional[str] = None

class Liability(BaseModel):
    particular: str
    loan_credit_limit: Optional[str] = None
    outstanding_amount: Optional[str] = None

class AssetsClass(BaseModel):
    particular: str
    premium_account: str
    sum_assured: str
    valuation: str
    due_date: str

class LiabilitiesClass(BaseModel):
    credit_cards : List
    loans: List
    
class ExecutiveSummaryPageData(BaseModel):
    assets: List[Assets]
    liabilities: List[Liability]
    
class InvestmentSummaryPageRow(BaseModel):
    category: str
    investment_amount: str
    holding_cost: str
    current_value: str
    irr: str
    subcategories: List[InvestmentSubcategory]
    
class InvestmentSummaryPageData(BaseModel):
    investment_data: List[InvestmentSummaryPageRow]

class AssetsAndLiabilitiesPageData(BaseModel):
    assets: List[AssetsClass]
    liabilities: LiabilitiesClass
    bank_balance: List
    
class FundsClass(BaseModel):
    scheme_name: str
    folio_no: str
    date_of_investment: str
    Invested_amout: str
    devident_or_received: str
    number_of_units: str
    last_updated_NAV: str
    current_market_value: str
    unrealized_gain_or_lose: str
    realized_gain_or_lose: str
    IRR_since_interception: str
    IRR_FYTD: str
    
class EquityMutualFundsInstrumentLevelSummary(BaseModel):
    client_name: str
    mid_cap_fund: List[FundsClass]
    small_cap_fund: List[FundsClass]
    large_cap_fund : List[FundsClass]

    
class EquityPMS(BaseModel):
    particular: str
    reference_no: str 
    investment_date: str
    investment_amount: str
    valuation_date: str
    current_value: str
    unrealized_gain_loss: str
    amount_or_capital_redeemed: str
    XIRR: str

class StockHolding(BaseModel):
    stock_name: str
    date: str
    ISIN: str
    no_of_units: str
    market_price_per_share: str
    current_market_value: str

class FundHolding(BaseModel):
    fund_name: str
    asset_class: str
    ISIN: str
    reference_no: str
    no_of_units: str
    market_price_per_share: str
    investment_amont: str 

class BankAccount(BaseModel):
    account_holder_name: str
    balance_as_on: str
    account_number: str
    account_type: str
    balance: str
    
class InvestmentSummaryReportRequest(BaseModel):
    first_page_data: InvestmentSummaryPageData
    second_page_data: InvestmentSummaryPageData
    third_page_data: ExecutiveSummaryPageData
    fourth_page_data: AssetsAndLiabilitiesPageData
    fourth_page_data: AssetsAndLiabilitiesPageData
    sixth_page_data: EquityMutualFundsInstrumentLevelSummary
    eighth_page_data: List[EquityPMS]
    tenth_page_data: List[StockHolding]
    eleventh_page_data: List[FundHolding]
    twelveth_page_data: List[BankAccount]
    

@app.post("/generate-investment-summary-report")
async def generate_investment_summary_report(
    data: InvestmentSummaryReportRequest,
    background_tasks: BackgroundTasks
):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        first_page_filename = f"investment_summary_first_page_{timestamp}.pdf"
        second_page_filename = f"investment_summary_second_page_{timestamp}.pdf"
        fourth_page_filename = f"assets_and_liabilities{timestamp}.pdf"
        third_page_filename = f"executive_summary_page_{timestamp}.pdf"
        sixth_page_filename = f"equity_mutual_fund_instrument_level_summary_{timestamp}.pdf"
        eighth_page_filename = f"equity_PMS_{timestamp}.pdf"
        tenth_page_filename = f"demat_stocks_{timestamp}.pdf"
        eleventh_page_filename = f"demat_MF_{timestamp}.pdf"
        tewlveth_page_filename = f"bank_account_balance_{timestamp}.pdf"
        merged_filename = f"investment_summary_report_{timestamp}.pdf"

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=16) as pool:
            # Generate both PDFs in parallel
            first_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "investment_summary_first_page.html",
                    {"investment_data": data.first_page_data.investment_data},
                    first_page_filename
                )
            )
            second_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "investment_summary_second_page.html",
                    {"investment_data": data.second_page_data.investment_data},
                    second_page_filename
                )
            )
            fourth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "assets_and_liabilities.html",
                    {"assets": data.fourth_page_data.assets, "liabilities": data.fourth_page_data.liabilities, "bank_balance": data.fourth_page_data.bank_balance},
                    fourth_page_filename
                )   
            )
            third_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "executive_summary_page.html",
                    {"assets": data.third_page_data.assets, "liabilities": data.third_page_data.liabilities},
                    third_page_filename
                )   
            )
            sixth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "equity_mutual_fund_instrument_level_summary.html",
                    {"data": data.sixth_page_data },
                    sixth_page_filename
                )   
            )
            eighth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "equity_PMS.html",
                    {"data": data.eighth_page_data },
                    eighth_page_filename
                )   
            )
            tenth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "demat_stocks.html",
                    {"data": data.tenth_page_data },
                    tenth_page_filename
                )   
            )
            eleventh_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "demat_MF.html",
                    {"data": data.eleventh_page_data },
                    eleventh_page_filename
                )   
            )
            twelveth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "bank_account_balance.html",
                    {"data": data.twelveth_page_data },
                    tewlveth_page_filename
                )   
            )
            
            first_page_path, second_page_path, fourth_page_path, third_page_path, six_page_path, eighth_page_path , tenthth_page_path, eleventh_page_path, twelveth_page_path  = await asyncio.gather(first_page_future, second_page_future, fourth_page_future, third_page_future, sixth_page_future, eighth_page_future, tenth_page_future, eleventh_page_future, twelveth_page_future)
        
        # Merge PDFs
        merger = PdfMerger()
        merger.append(str(first_page_path))
        merger.append(str(second_page_path))
        merger.append(str(fourth_page_path))
        merger.append(str(third_page_path))
        merger.append(str(six_page_path))
        merger.append(str(eighth_page_path))
        merger.append(str(tenthth_page_path))
        merger.append(str(eleventh_page_path))
        merger.append(str(twelveth_page_path))
        merged_path = OUTPUT_DIR / merged_filename
        with open(merged_path, "wb") as fout:
            merger.write(fout)
        merger.close()

        # Schedule cleanup
        background_tasks.add_task(report_generator.cleanup_old_files)
        # Optionally, also cleanup the intermediate PDFs
        background_tasks.add_task(lambda: Path(first_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(second_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(fourth_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(third_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(six_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(eighth_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(tenthth_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(eleventh_page_path).unlink(missing_ok=True))
        background_tasks.add_task(lambda: Path(twelveth_page_path).unlink(missing_ok=True))

        return FileResponse(
            merged_path,
            media_type="application/pdf",
            filename=merged_filename,
            background=background_tasks
        )
    except Exception as e:
        print(f"Error generating merged investment summary report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

