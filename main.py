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
from db import get_all_investment_summary_data
 
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
 
class LoanTotal(BaseModel):
    loan_amount: str
    outstanding: str
    EMI: str
 
class LoanResponse(BaseModel):
    loans: List[LoanDetail]
    total: LoanTotal

class AssetAllocation(BaseModel):
    debt: str
    equity: str
    others: str
    
class Client(BaseModel):
    name: str
    risk_profile: str
    current_value: str
    investment_value: str
    weightage: str
    total_gain_loss: str
    current_asset_allocation: AssetAllocation
    target_asset_allocation: AssetAllocation

from pydantic import BaseModel
from typing import List


class InvestmentItem(BaseModel):
    particulars: str
    holdings_cost: str
    current_value: str
    holdings: str
    gain_or_lose_realized: str
    devident_or_interest: str
    gain_or_lose_unrealized: str
    irr_since_interception: str


class InvestmentData(BaseModel):
    category: str
    holdings_cost: str
    current_value: str
    holdings: str
    gain_or_lose_realized: str
    devident_or_interest: str
    gain_or_lose_unrealized: str
    irr_since_interception: str

    subcategories: List[InvestmentItem]


class PortfolioPageData(BaseModel):
    investment_data: List[InvestmentData]

class DebtAnalysisItem(BaseModel):
    particulars: str
    holdings_cost: str
    current_value: str
    holdings: str
    gain_or_lose_realized: str
    devident_or_interest: str
    gain_or_lose_unrealized: str
    irr: str
 
class TwenteethPageData(BaseModel):
    debt_analysis_response: List[DebtAnalysisItem]

class InvestmentSummaryReportRequest(BaseModel):
    first_page_data: InvestmentSummaryPageData
    second_page_data: InvestmentSummaryPageData
    third_page_data: ExecutiveSummaryPageData
    fourth_page_data: AssetsAndLiabilitiesPageData
    fifth_page_data: DebtMutualFundInstrumentLevelSummary
    sixth_page_data: EquityMutualFundsInstrumentLevelSummary
    seventh_page_data: HybridMutualFundInstrumentLevelSummary
    eighth_page_data: List[EquityPMS]
    ninth_page_data: EquityAIFInstrumentLevelSummary
    tenth_page_data: List[StockHolding]
    eleventh_page_data: List[FundHolding]
    twelfth_page_data: LifeInsuranceResponse
    thirteenth_page_data: List[BankAccount]
    fourteenth_page_data: CreditCardResponse
    fifteenth_page_data: LoanResponse
    eighteenth_page_data: List[Client]
    nineteenth_page_data: PortfolioPageData
    twenteeth_page_data: TwenteethPageData
 
@app.post("/generate-investment-summary-report", response_model=None)
async def generate_investment_summary_report(
    background_tasks: BackgroundTasks
):
    try:
        # Get all data from database
        data = get_all_investment_summary_data()
        print("Debug - Raw data structure:", data.keys())
        
        # Convert to Pydantic model
        try:
            report_data = InvestmentSummaryReportRequest(**data)
        except Exception as model_error:
            print("Debug - Model validation error:", str(model_error))
            print("Debug - Data structure:", {k: type(v) for k, v in data.items()})
            raise
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        first_page_filename = f"investment_summary_first_page_{timestamp}.pdf"
        second_page_filename = f"investment_summary_second_page_{timestamp}.pdf"
        fourth_page_filename = f"assets_and_liabilities{timestamp}.pdf"
        third_page_filename = f"executive_summary_page_{timestamp}.pdf"
        fifth_page_filename = f"debt_mutual_fund_summary_{timestamp}.pdf"
        sixth_page_filename = f"equity_mutual_fund_instrument_level_summary_{timestamp}.pdf"
        seventh_page_filename = f"hybrid_mutual_fund_summary_{timestamp}.pdf"
        eighth_page_filename = f"equity_PMS_{timestamp}.pdf"
        tenth_page_filename = f"demat_stocks_{timestamp}.pdf"
        ninth_page_filename = f"equity_aif_summary_{timestamp}.pdf"
        eleventh_page_filename = f"demat_MF_{timestamp}.pdf"
        twelfth_page_filename = f"life_insurance_summary_{timestamp}.pdf"
        thirteenth_page_filename = f"bank_account_balance_{timestamp}.pdf"
        fourteenth_page_filename = f"credit_card_summary_{timestamp}.pdf"
        fifteenth_page_filename = f"loan_summary_{timestamp}.pdf"
        eighteenth_page_filename = f"client_code_level_summary_{timestamp}.pdf"
        nineteenth_page_filename = f"portfolio_analysis_{timestamp}.pdf"
        twentieth_page_filename = f"debt_analysis_summary_{timestamp}.pdf"
        merged_filename = f"investment_summary_report_{timestamp}.pdf"

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=16) as pool:
            # Generate both PDFs in parallel
            first_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "investment_summary_first_page.html",
                    {"investment_data": report_data.first_page_data.investment_data},
                    first_page_filename
                )
            )
            second_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "investment_summary_second_page.html",
                    {"investment_data": report_data.second_page_data.investment_data},
                    second_page_filename
                )
            )
            fourth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "assets_and_liabilities.html",
                    {"assets": report_data.fourth_page_data.assets, "liabilities": report_data.fourth_page_data.liabilities, "bank_balance": report_data.fourth_page_data.bank_balance},
                    fourth_page_filename
                )  
            )
            third_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "executive_summary_page.html",
                    {"assets": report_data.third_page_data.assets, "liabilities": report_data.third_page_data.liabilities},
                    third_page_filename
                )  
            )
            fifth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "debt_mutual_fund_instrument_level_summary.html",
                {
                    "investment_details": report_data.fifth_page_data.investment_details,
                    "total_investment": report_data.fifth_page_data.total_investment
                },
                fifth_page_filename
            ))
            sixth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "equity_mutual_fund_instrument_level_summary.html",
                    {"data": report_data.sixth_page_data },
                    sixth_page_filename
                )  
            )
            seventh_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "hybrid_mutual_fund_instrument_level_summary.html",
                {
                    "client_name": report_data.seventh_page_data.client_name,
                    "multi_asset_allocation": report_data.seventh_page_data.multi_asset_allocation
                },
                seventh_page_filename
            ))
            eighth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "equity_PMS.html",
                    {"data": report_data.eighth_page_data },
                    eighth_page_filename
                )  
            )
            ninth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "equity_aif_instrumental_level_summary.html",
                {
                    "summary": report_data.ninth_page_data.summary
                },
                ninth_page_filename
            ))
            tenth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "demat_stocks.html",
                    {"data": report_data.tenth_page_data },
                    tenth_page_filename
                )  
            )
            eleventh_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "demat_MF.html",
                    {"data": report_data.eleventh_page_data },
                    eleventh_page_filename
                )  
            )
            twelfth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "life_insurance.html",
                {
                    "policies": report_data.twelfth_page_data.policies
                },
                twelfth_page_filename
            ))
            thirteenth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "bank_account_balance.html",
                    {"data": report_data.thirteenth_page_data },
                    thirteenth_page_filename
                )  
            )
            fourteenth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
               "credit_card_summary.html",
                {
              "credit_cards": report_data.fourteenth_page_data.credit_cards,
               "total": report_data.fourteenth_page_data.total
             },
                fourteenth_page_filename
            ))
            fifteenth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "loans_summary.html",
                {
                "loans": report_data.fifteenth_page_data.loans,
                "total": report_data.fifteenth_page_data.total
                },
                fifteenth_page_filename
            ))
            eighteenth_page_future = loop.run_in_executor(pool, lambda: report_generator.generate_pdf(
                "code_break_down_template.html",
                {
                    "clients": report_data.eighteenth_page_data,
                    "total": {
                        "current_value": sum(float(client.current_value) for client in report_data.eighteenth_page_data),
                        "investment_value": sum(float(client.investment_value) for client in report_data.eighteenth_page_data),
                        "weightage": sum(float(client.weightage) for client in report_data.eighteenth_page_data),
                        "total_gain_loss": sum(float(client.total_gain_loss) for client in report_data.eighteenth_page_data)
                    }
                },
                eighteenth_page_filename
            ))
            nineteenth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "portfolio_analysis.html",
                    {"investment_data": report_data.nineteenth_page_data.investment_data},
                    nineteenth_page_filename
                )
            )
            twentieth_page_future = loop.run_in_executor(
                pool,
                lambda: report_generator.generate_pdf(
                    "debt_analysis_summary.html",
                    {"debt_analysis_response": report_data.twenteeth_page_data.debt_analysis_response},
                    twentieth_page_filename
                )
            )
            first_page_path, second_page_path, fourth_page_path, third_page_path, sixth_page_path, eighth_page_path, tenth_page_path, eleventh_page_path, thirteenth_page_path, fifth_page_path, seventh_page_path, ninth_page_path, twelfth_page_path, fourteenth_page_path, fifteenth_page_path, eighteenth_page_path, nineteenth_page_path, twentieth_page_path = await asyncio.gather(first_page_future, second_page_future, fourth_page_future, third_page_future, sixth_page_future, eighth_page_future, tenth_page_future, eleventh_page_future, thirteenth_page_future, fifth_page_future, seventh_page_future, ninth_page_future, twelfth_page_future, fourteenth_page_future, fifteenth_page_future, eighteenth_page_future, nineteenth_page_future, twentieth_page_future)
       
        # Merge PDFs
        merger = PdfMerger()
        merger.append(str(first_page_path))
        merger.append(str(second_page_path))
        merger.append(str(fourth_page_path))
        merger.append(str(third_page_path))
        merger.append(str(fifth_page_path))
        merger.append(str(sixth_page_path))
        merger.append(str(seventh_page_path))
        merger.append(str(eighth_page_path))
        merger.append(str(ninth_page_path))
        merger.append(str(tenth_page_path))
        merger.append(str(eleventh_page_path))
        merger.append(str(twelfth_page_path))
        merger.append(str(thirteenth_page_path))
        merger.append(str(fourteenth_page_path))
        merger.append(str(fifteenth_page_path))
        merger.append(str(eighteenth_page_path))
        merger.append(str(nineteenth_page_path))
        merger.append(str(twentieth_page_path))
        merged_path = OUTPUT_DIR / merged_filename
        with open(merged_path, "wb") as fout:
            merger.write(fout)
        merger.close()
 
        # Schedule cleanup
        background_tasks.add_task(report_generator.cleanup_old_files)
        # Cleanup intermediate PDFs
        for path in [first_page_path, second_page_path, fourth_page_path, third_page_path,
                    fifth_page_path, sixth_page_path, seventh_page_path, eighth_page_path,
                    ninth_page_path, tenth_page_path, eleventh_page_path, twelfth_page_path,
                    thirteenth_page_path, fourteenth_page_path, fifteenth_page_path,
                    eighteenth_page_path, nineteenth_page_path, twentieth_page_path]:
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
 
@app.get("/investment-summary")
def investment_summary_first_page():
    try:
        data = get_all_investment_summary_data()
        return {"data": data}
    except Exception as e:
        print(f"Error fetching investment summary first page: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
 