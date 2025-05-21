from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from contextlib import contextmanager

# Database connection parameters - these should be moved to environment variables
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "your_db_name"),
    "user": os.getenv("DB_USER", "your_db_user"),
    "password": os.getenv("DB_PASSWORD", "your_db_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)
        yield conn
    finally:
        if conn is not None:
            conn.close()

def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """Execute a query and return results as a list of dictionaries"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

def get_investment_summary_first_page() -> List[Dict[str, Any]]:
    """Execute the investment summary first page query"""
    query = """
        WITH category_totals AS (
            SELECT 
                CASE 
                    WHEN asset_class = 'Mutual Fund' THEN 'Mutual Fund'
                    ELSE 'Other'
                END as category,
                COALESCE(sub_asset_class, 'Mutual Fund') as particular,
                COALESCE(SUM(investment_amount), 0)::text as investment_amount,
                COALESCE(SUM(investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(market_value) - SUM(investment_amount)) / NULLIF(SUM(investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active
            GROUP BY 
                CASE 
                    WHEN asset_class = 'Mutual Fund' THEN 'Mutual Fund'
                    ELSE 'Other'
                END,
                COALESCE(sub_asset_class, 'Mutual Fund')
        )
        SELECT 
            category,
            COALESCE(SUM(investment_amount::numeric), 0)::text as investment_amount,
            COALESCE(SUM(holding_cost::numeric), 0)::text as holding_cost,
            COALESCE(SUM(current_value::numeric), 0)::text as current_value,
            COALESCE(SUM(irr::numeric), 0)::text as irr,
            COALESCE(json_agg(
                json_build_object(
                    'particular', particular,
                    'investment_amount', investment_amount,
                    'holding_cost', holding_cost,
                    'current_value', current_value,
                    'irr', irr
                )
            ), '[]'::json) as subcategories
        FROM category_totals
        GROUP BY category
        ORDER BY category;
    """
    return execute_query(query)

def get_investment_summary_second_page() -> List[Dict[str, Any]]:
    second_page_query = """
        WITH category_totals AS (
            SELECT 
                CASE 
                    WHEN asset_class != 'Mutual Fund' THEN asset_class
                    ELSE 'Other'
                END as category,
                COALESCE(sub_asset_class, asset_class) as particular,
                COALESCE(SUM(investment_amount), 0)::text as investment_amount,
                COALESCE(SUM(investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(market_value) - SUM(investment_amount)) / NULLIF(SUM(investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active
            WHERE asset_class != 'Mutual Fund'
            GROUP BY 
                CASE 
                    WHEN asset_class != 'Mutual Fund' THEN asset_class
                    ELSE 'Other'
                END,
                COALESCE(sub_asset_class, asset_class)
        )
        SELECT 
            category,
            COALESCE(SUM(investment_amount::numeric), 0)::text as investment_amount,
            COALESCE(SUM(holding_cost::numeric), 0)::text as holding_cost,
            COALESCE(SUM(current_value::numeric), 0)::text as current_value,
            COALESCE(SUM(irr::numeric), 0)::text as irr,
            COALESCE(json_agg(
                json_build_object(
                    'particular', particular,
                    'investment_amount', investment_amount,
                    'holding_cost', holding_cost,
                    'current_value', current_value,
                    'irr', irr
                )
            ), '[]'::json) as subcategories
        FROM category_totals
        GROUP BY category
        ORDER BY category;
    """
    return execute_query(second_page_query)

def get_investment_summary_third_page() -> List[Dict[str, Any]]:
    third_page_query = """
        WITH asset_totals AS (
            SELECT 
                asset_class as particular,
                COALESCE(SUM(investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(market_value) - SUM(investment_amount)) / NULLIF(SUM(investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active
            GROUP BY asset_class
            UNION ALL
            SELECT 
                'Total Assets' as particular,
                COALESCE(SUM(investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(market_value) - SUM(investment_amount)) / NULLIF(SUM(investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active
        )
        SELECT 
            particular,
            holding_cost,
            current_value,
            irr
        FROM asset_totals
        ORDER BY 
            CASE WHEN particular = 'Total Assets' THEN 2 ELSE 1 END,
            particular;
        """
    return execute_query(third_page_query)

def get_all_investment_summary_data() -> dict:
    """Fetch all data required for the investment summary report"""
    try:
        # Get data for each page
        first_page_data = get_investment_summary_first_page()
        second_page_data = get_investment_summary_second_page()
        third_page_data = get_investment_summary_third_page()
        
        # Create the complete data structure
        complete_data = {
            "first_page_data": {
                "investment_data": first_page_data
            },
            "second_page_data": {
                "investment_data": second_page_data
            },
            "third_page_data": {
                "assets": third_page_data,
                "liabilities": []  # Add your liabilities query here
            },
            "fourth_page_data": {
                "assets": [],
                "liabilities": {
                    "credit_cards": [],
                    "loans": []
                },
                "bank_balance": []
            },
            "fifth_page_data": {
                "investment_details": [],
                "total_investment": {
                    "invested_amount": "0",
                    "dividends_received": "0",
                    "current_market_value": "0",
                    "unrealized_gain_loss": "0",
                    "irr_since_inception": "0",
                    "irr_ytd": "0"
                }
            },
            "sixth_page_data": {
                "client_name": "",
                "mid_cap_fund": [],
                "small_cap_fund": [],
                "large_cap_fund": []
            },
            "seventh_page_data": {
                "client_name": "",
                "multi_asset_allocation": []
            },
            "eighth_page_data": [],
            "ninth_page_data": {
                "summary": []
            },
            "tenth_page_data": [],
            "eleventh_page_data": [],
            "twelfth_page_data": {
                "policies": []
            },
            "thirteenth_page_data": [],
            "fourteenth_page_data": {
                "credit_cards": [],
                "total": {
                    "credit_limit": "0",
                    "available_credit_limit": "0",
                    "minimum_amount_due": "0",
                    "total_amount_due": "0"
                }
            },
            "fifteenth_page_data": {
                "loans": [],
                "total": {
                    "loan_amount": "0",
                    "outstanding": "0",
                    "EMI": "0"
                }
            },
            "eighteenth_page_data": [],
            "nineteenth_page_data": {
                "investment_data": []
            },
            "twenteeth_page_data": {
                "debt_analysis_response": []
            }
        }
        
        print("Debug - Complete data keys:", list(complete_data.keys()))  # Debug log
        print("Debug - Nineteenth page data:", complete_data.get("nineteenth_page_data"))  # Debug log
        print("Debug - Twenteeth page data:", complete_data.get("twenteeth_page_data"))  # Debug log
        
        return complete_data
    except Exception as e:
        print(f"Error fetching investment summary data: {str(e)}")
        raise