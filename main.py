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

for directory in [TEMPLATES_DIR, STATIC_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

app = FastAPI(
    title="Report Generation API",
    description="API for generating PDF reports with dynamic content",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

report_generator = ReportGenerator()
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

class ExecutiveSummaryPageData(BaseModel):
    assets: List[Assets]
    liabilities: List[Liability]

class InvestmenDetail(BaseModel):
    accounts: str
    types: str
    scheme_name: str
    folio_no: str
    date_of_investment: str
    invested_amount: str
    dividends_received: str
    last_updated_nav: str
    no_of_units: str
    current_market_value: str
    unrealized_gain_loss: str
    irr_since_inception: str
    irr_ytd: str

class TotalInvestmenDetail(BaseModel):
    invested_amount: str
    dividends_received: str
    current_market_value: str
    unrealized_gain_loss: str
    irr_since_inception: str
    irr_ytd: str

class DebtMutualFundInstrumentLevelSummary(BaseModel):
    investment_details: List[InvestmenDetail]
    total_investment: TotalInvestmenDetail

class InvestmentSummaryPageRow(BaseModel):
    category: str
    investment_amount: str
    holding_cost: str
    current_value: str
    irr: str
    subcategories: List[InvestmentSubcategory]

class InvestmentSummaryPageData(BaseModel):
    investment_data: List[InvestmentSummaryPageRow]

class HybridMutualFund(BaseModel):
    scheme_name: str
    folio_no: str
    date_of_investment: str
    invested_amount: str
    dividends_received: str
    no_of_units: str
    last_updated_nav: str
    current_market_value: str
    unrealized_gain_loss: str
    realized_gain_loss: str
    irr_since_inception: str
    irr_fytd: str

class HybridMutualFundInstrumentLevelSummary(BaseModel):
    client_name: str
    multi_asset_allocation: List[HybridMutualFund]

class EquityAIFInstrument(BaseModel):
    instument_name: str
    fund_name: Optional[str]
    instument_name: Optional[str]
    reference_no: str
    investment_date: str
    investment_amount: str
    return_of_capital: str
    valuation_date: str
    current_value: str
    unrealized_gain_loss: str
    realized_gain_loss: str
    xirr: str

class EquityAIFInstrumentLevelSummary(BaseModel):
    summary: List[EquityAIFInstrument]

class LifeInsurancePolicy(BaseModel):
    policy_name: str
    policy_type: str
    premimum_due_date: str 
    policy_no: str
    premium_account: str
    sum_assured: str
    valuation: str

class LifeInsuranceResponse(BaseModel):
    policies: List[LifeInsurancePolicy]

class CreditCardDetail(BaseModel):
    card_type:str
    payment_due_date: str
    credit_card_number:str
    credit_limit:str
    cash_limit: str
    available_credit_limit: str
    minimum_amount_due:str
    total_amount_due:str
    
class CreditCardTotal(BaseModel):
    credit_limit: str
    available_credit_limit: str
    minimum_amount_due: str
    total_amount_due: str

class CreditCardResponse(BaseModel):
    credit_cards: List[CreditCardDetail]
    total: CreditCardTotal

class LoanDetail(BaseModel):
    loan_type: str
    loan_account: str
    loan_amount: str
    tenure: str
    maturity:str
    outstanding: str
    EMI: str
    composition:str


class LoanDetail(BaseModel):
    loan_type: str
    loan_account: str
    loan_amount: str
    tenure: str
    maturity:str
    outstanding: str
    EMI: str
    composition:str

class LoanTotal(BaseModel):
    loan_amount: str
    outstanding: str
    EMI: str

class LoanResponse(BaseModel):
    loans: List[LoanDetail]
    total: LoanTotal


class InvestmentSummaryReportRequest(BaseModel):
    first_page_data: InvestmentSummaryPageData
    second_page_data: InvestmentSummaryPageData
    third_page_data: ExecutiveSummaryPageData
    fifth_page_data: DebtMutualFundInstrumentLevelSummary
    seventh_page_data: HybridMutualFundInstrumentLevelSummary
    ninth_page_data: EquityAIFInstrumentLevelSummary
    twelfth_page_data: LifeInsuranceResponse 
    fourteenth_page_data: CreditCardResponse  
    fifteenth_page_data: LoanResponse 


# ---- Endpoint ----

@app.post("/generate-investment-summary-report")
async def generate_investment_summary_report(
    data: InvestmentSummaryReportRequest,
    background_tasks: BackgroundTasks
):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        first_page_filename = f"investment_summary_first_page_{timestamp}.pdf"
        second_page_filename = f"investment_summary_second_page_{timestamp}.pdf"
        third_page_filename = f"executive_summary_page_{timestamp}.pdf"
        fifth_page_filename = f"debt_mutual_fund_summary_{timestamp}.pdf"
        seventh_page_filename = f"hybrid_mutual_fund_summary_{timestamp}.pdf"
        ninth_page_filename = f"equity_aif_summary_{timestamp}.pdf"
        twelfth_page_filename = f"life_insurance_summary_{timestamp}.pdf"
        fourteenth_page_filename = f"credit_card_summary_{timestamp}.pdf"
        fifteenth_page_filename = f"loan_summary_{timestamp}.pdf"
        merged_filename = f"investment_summary_report_{timestamp}.pdf"

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=16) as pool:
            first_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "investment_summary_first_page.html",
                {"investment_data": data.first_page_data.investment_data},
                first_page_filename
            ))
            second_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "investment_summary_second_page.html",
                {"investment_data": data.second_page_data.investment_data},
                second_page_filename
            ))
            third_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "executive_summary_page.html",
                {
                    "assets": data.third_page_data.assets,
                    "liabilities": data.third_page_data.liabilities
                },
                third_page_filename
            ))
            fifth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "debt_mutual_fund_instrument_level_summary.html",
                {
                    "investment_details": data.fifth_page_data.investment_details,
                    "total_investment": data.fifth_page_data.total_investment
                },
                fifth_page_filename
            ))
            seventh_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "hybrid_mutual_fund_instrument_level_summary.html",
                {
                    "client_name": data.seventh_page_data.client_name,
                    "multi_asset_allocation": data.seventh_page_data.multi_asset_allocation
                },
                seventh_page_filename
            ))
            ninth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "equity_aif_instrumental_level_summary.html",
                {
                    "summary": data.ninth_page_data.summary
                },
                ninth_page_filename
            ))
            twelfth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "life_insurance.html",
                {
                    "policies": data.twelfth_page_data.policies
                },
                twelfth_page_filename
            ))
            fourteenth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
               "credit_card_summary.html",
                {
              "credit_cards": data.fourteenth_page_data.credit_cards,
               "total": data.fourteenth_page_data.total
             },
                fourteenth_page_filename
              ))
            
            fifteenth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "loans_summary.html",
             {
            "loans": data.fifteenth_page_data.loans,
            "total": data.fifteenth_page_data.total 
             },
              fifteenth_page_filename
             ))
            
            first_page_path, second_page_path, third_page_path, fifth_page_path, seventh_page_path, ninth_page_path, twelfth_page_path, fourteenth_page_path, fifteenth_page_path= await asyncio.gather(
                first_page_future,
                second_page_future,
                third_page_future,
                fifth_page_future,
                seventh_page_future,
                ninth_page_future,
                twelfth_page_future,
                fourteenth_page_future,
                fifteenth_page_future


            )

        # Merge PDFs
        merger = PdfMerger()
        for path in [first_page_path, second_page_path, third_page_path, fifth_page_path, seventh_page_path, ninth_page_path, twelfth_page_path, fourteenth_page_path, fifteenth_page_path]:
            merger.append(str(path))

        merged_path = OUTPUT_DIR / merged_filename
        with open(merged_path, "wb") as fout:
            merger.write(fout)
        merger.close()

        # Cleanup
        background_tasks.add_task(report_generator.cleanup_old_files)
        for path in [first_page_path, second_page_path, third_page_path, fifth_page_path, seventh_page_path, ninth_page_path, twelfth_page_path, fourteenth_page_path, fifteenth_page_path]:
            background_tasks.add_task(lambda p=path: Path(p).unlink(missing_ok=True))

        return FileResponse(
            merged_path,
            media_type="application/pdf",
            filename=merged_filename,
            background=background_tasks
        )

    except Exception as e:
        print(f"Error generating merged investment summary report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ---- Run ----

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
