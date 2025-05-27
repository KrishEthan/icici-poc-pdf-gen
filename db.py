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

def get_investment_summary_all_assets() -> List[Dict[str, Any]]:
    """Get data for all asset classes for the investment summary report (merged first and second page)."""
    query = """
        WITH subcategory_totals AS (
            SELECT 
                p.asset_class,
                p.sub_asset_class,
                COALESCE(SUM(p.investment_amount), 0)::text as investment_amount,
                COALESCE(SUM(p.investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(p.market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(p.investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(p.market_value) - SUM(p.investment_amount)) / NULLIF(SUM(p.investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active p
            WHERE p.sub_asset_class IS NOT NULL
            GROUP BY p.asset_class, p.sub_asset_class
        ),
        category_totals AS (
            SELECT 
                p.asset_class as category,
                COALESCE(SUM(p.investment_amount), 0)::text as investment_amount,
                COALESCE(SUM(p.investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(p.market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(p.investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(p.market_value) - SUM(p.investment_amount)) / NULLIF(SUM(p.investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr,
                (
                    SELECT COALESCE(
                        json_agg(
                            json_build_object(
                                'particular', s.sub_asset_class,
                                'investment_amount', s.investment_amount,
                                'holding_cost', s.holding_cost,
                                'current_value', s.current_value,
                                'irr', s.irr
                            ) ORDER BY s.sub_asset_class
                        ) FILTER (WHERE s.sub_asset_class IS NOT NULL),
                        '[]'::json
                    )
                    FROM subcategory_totals s
                    WHERE s.asset_class = p.asset_class
                ) as subcategories
            FROM position_active p
            GROUP BY p.asset_class
            UNION ALL
            SELECT 
                'Total Assets' as category,
                COALESCE(SUM(p.investment_amount), 0)::text as investment_amount,
                COALESCE(SUM(p.investment_amount) * 0.9, 0)::text as holding_cost,
                COALESCE(SUM(p.market_value), 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(p.investment_amount) > 0 
                        THEN ROUND(
                            ((SUM(p.market_value) - SUM(p.investment_amount)) / NULLIF(SUM(p.investment_amount), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr,
                '[]'::json as subcategories
            FROM position_active p
        )
        SELECT 
            category,
            investment_amount,
            holding_cost,
            current_value,
            irr,
            COALESCE(subcategories, '[]'::json) as subcategories
        FROM category_totals
        ORDER BY 
            CASE WHEN category = 'Total Assets' THEN 2 ELSE 1 END,
            category;
    """
    return execute_query(query)

def get_liabilities_summary() -> List[Dict[str, Any]]:
    """Fetch liabilities data from the position_active table with subcategories."""
    # Debug query to see what's in the table
    debug_query = """
        SELECT DISTINCT asset_class, sub_asset_class, COUNT(*) as count
        FROM position_active
        WHERE asset_class IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability')
        GROUP BY asset_class, sub_asset_class
        ORDER BY asset_class, sub_asset_class;
    """
    debug_results = execute_query(debug_query)
    print("Debug - Actual liability data in position_active:", debug_results)

    # Main query with proper handling of subcategories
    query = """
        WITH liability_subcategories AS (
            SELECT 
                p.asset_class,
                p.sub_asset_class,
                COALESCE(SUM(p.investment_amount), 0)::text as credit_limit,
                COALESCE(SUM(p.market_value), 0)::text as outstanding_amount
            FROM position_active p
            WHERE p.asset_class IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability')
            AND p.sub_asset_class IS NOT NULL
            GROUP BY p.asset_class, p.sub_asset_class
        ),
        ordered_subcategories AS (
            SELECT 
                asset_class,
                json_agg(
                    json_build_object(
                        'particular', sub_asset_class,
                        'credit_limit', credit_limit,
                        'outstanding_amount', outstanding_amount
                    ) ORDER BY sub_asset_class
                ) as subcategories
            FROM liability_subcategories
            GROUP BY asset_class
        ),
        category_totals AS (
            SELECT 
                p.asset_class,
                COALESCE(SUM(p.investment_amount), 0)::text as credit_limit,
                COALESCE(SUM(p.market_value), 0)::text as outstanding_amount
            FROM position_active p
            WHERE p.asset_class IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability')
            GROUP BY p.asset_class
        )
        SELECT 
            c.asset_class as particular,
            c.credit_limit,
            c.outstanding_amount,
            COALESCE(s.subcategories, '[]'::json) as subcategories
        FROM category_totals c
        LEFT JOIN ordered_subcategories s ON c.asset_class = s.asset_class
        ORDER BY c.asset_class;
    """
    return execute_query(query)

def get_asset_class_summary() -> List[Dict[str, Any]]:
    """Get distinct asset classes summary for third page."""
    query = """
        SELECT 
            'Assets' as type,
            array_agg(DISTINCT asset_class ORDER BY asset_class) as classes,
            COUNT(DISTINCT asset_class) as count
        FROM position_active
        WHERE asset_class NOT IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability')
        UNION ALL
        SELECT 
            'Liabilities' as type,
            array_agg(DISTINCT asset_class ORDER BY asset_class) as classes,
            COUNT(DISTINCT asset_class) as count
        FROM position_active
        WHERE asset_class IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability');
    """
    return execute_query(query)

def get_instrument_summary() -> List[Dict[str, Any]]:
    """Get investment data grouped by instrument_name for fourth page, with high-level summary and detailed entries."""
    query = """
        WITH instrument_totals AS (
            SELECT 
                instrument_name,
                COALESCE(SUM(investment_amount::numeric), 0)::text as total_investment_amount,
                COALESCE(SUM(investment_amount::numeric) * 0.9, 0)::text as total_holding_cost,
                COALESCE(SUM(market_value::numeric), 0)::text as total_current_value,
                COALESCE(
                    CASE 
                        WHEN SUM(investment_amount::numeric) > 0 
                        THEN ROUND(
                            ((SUM(market_value::numeric) - SUM(investment_amount::numeric)) / 
                            NULLIF(SUM(investment_amount::numeric), 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as total_irr
            FROM position_active
            WHERE instrument_name IS NOT NULL
            GROUP BY instrument_name
        ),
        instrument_details AS (
            SELECT 
                instrument_name,
                asset_class,
                sub_asset_class,
                COALESCE(investment_amount, 0)::text as investment_amount,
                COALESCE(investment_amount * 0.9, 0)::text as holding_cost,
                COALESCE(market_value, 0)::text as current_value,
                COALESCE(
                    CASE 
                        WHEN investment_amount > 0 
                        THEN ROUND(
                            ((market_value - investment_amount) / NULLIF(investment_amount, 0)) * 100,
                            2
                        )::text
                        ELSE '0' 
                    END,
                    '0'
                ) as irr
            FROM position_active
            WHERE instrument_name IS NOT NULL
        )
        SELECT 
            t.instrument_name,
            json_build_object(
                'summary', json_build_object(
                    'total_investment_amount', t.total_investment_amount,
                    'total_holding_cost', t.total_holding_cost,
                    'total_current_value', t.total_current_value,
                    'total_irr', t.total_irr
                ),
                'details', COALESCE(
                    json_agg(
                        json_build_object(
                            'asset_class', d.asset_class,
                            'sub_asset_class', d.sub_asset_class,
                            'investment_amount', d.investment_amount,
                            'holding_cost', d.holding_cost,
                            'current_value', d.current_value,
                            'irr', d.irr
                        ) ORDER BY d.asset_class, d.sub_asset_class
                    ) FILTER (WHERE d.instrument_name IS NOT NULL),
                    '[]'::json
                )
            ) as instrument_data
        FROM instrument_totals t
        LEFT JOIN instrument_details d ON t.instrument_name = d.instrument_name
        GROUP BY t.instrument_name, t.total_investment_amount, t.total_holding_cost, t.total_current_value, t.total_irr
        ORDER BY t.instrument_name;
    """
    return execute_query(query)

def get_client_code_summary() -> List[Dict[str, Any]]:
    """Get client code level summary with current and model allocations."""
    query = """
        WITH client_summary AS (
            SELECT
                CONCAT(cm.first_name, ' ', COALESCE(cm.middle_name, ''), ' ', COALESCE(cm.last_name, '')) as name,
                cm.segment_desc as risk_profile,
                COALESCE(SUM(pa.market_value::numeric), 0) as current_value,
                COALESCE(SUM(pa.investment_amount::numeric), 0) as investment_value
            FROM position_active pa
            JOIN client_master cm ON pa.invest_id = cm.invest_id
            WHERE pa.invest_id IS NOT NULL
            GROUP BY cm.first_name, cm.middle_name, cm.last_name, cm.segment_desc
        ),
        total_summary AS (
            SELECT COALESCE(SUM(current_value), 0) as total_current_value 
            FROM client_summary
        ),
        allocation_breakdown AS (
            SELECT
                CONCAT(cm.first_name, ' ', COALESCE(cm.middle_name, ''), ' ', COALESCE(cm.last_name, '')) as name,
                CASE 
                    WHEN pa.asset_class = 'Debt' THEN 'Debt'
                    WHEN pa.asset_class IN ('Equity', 'Mutual Fund', 'PMS', 'AIF') THEN 'Equity'
                    ELSE 'Others'
                END as allocation_type,
                COALESCE(SUM(pa.market_value::numeric), 0) as allocation_value
            FROM position_active pa
            JOIN client_master cm ON pa.invest_id = cm.invest_id
            WHERE pa.invest_id IS NOT NULL
            GROUP BY cm.first_name, cm.middle_name, cm.last_name, allocation_type
        ),
        allocation_percentages AS (
            SELECT
                a.name,
                a.allocation_type,
                ROUND(
                    (a.allocation_value::numeric / NULLIF(cs.current_value, 0)) * 100,
                    1
                ) as percentage
            FROM allocation_breakdown a
            JOIN client_summary cs ON cs.name = a.name
        ),
        model_allocations AS (
            SELECT 
                segment_desc as risk_profile,
                CASE 
                    WHEN segment_desc = 'Conservative' THEN json_build_object(
                        'debt', 70,
                        'equity', 20,
                        'others', 10
                    )
                    WHEN segment_desc = 'Moderate' THEN json_build_object(
                        'debt', 50,
                        'equity', 40,
                        'others', 10
                    )
                    WHEN segment_desc = 'Aggressive' THEN json_build_object(
                        'debt', 30,
                        'equity', 60,
                        'others', 10
                    )
                    ELSE json_build_object(
                        'debt', 40,
                        'equity', 50,
                        'others', 10
                    )
                END as model_allocation
            FROM (SELECT DISTINCT segment_desc FROM client_master) cm
        )
        SELECT
            cs.name as client_name,
            cs.risk_profile,
            cs.current_value::text,
            cs.investment_value::text,
            ROUND(
                (cs.current_value::numeric / NULLIF(ts.total_current_value, 0)) * 100,
                1
            )::text as weightage,
            (cs.current_value - cs.investment_value)::text as total_gain_loss,
            json_build_object(
                'current', json_build_object(
                    'debt', COALESCE((
                        SELECT percentage 
                        FROM allocation_percentages 
                        WHERE name = cs.name 
                        AND allocation_type = 'Debt'
                    ), 0),
                    'equity', COALESCE((
                        SELECT percentage 
                        FROM allocation_percentages 
                        WHERE name = cs.name 
                        AND allocation_type = 'Equity'
                    ), 0),
                    'others', COALESCE((
                        SELECT percentage 
                        FROM allocation_percentages 
                        WHERE name = cs.name 
                        AND allocation_type = 'Others'
                    ), 0)
                ),
                'target', ma.model_allocation
            ) as asset_allocation
        FROM client_summary cs
        CROSS JOIN total_summary ts
        LEFT JOIN model_allocations ma ON cs.risk_profile = ma.risk_profile
        ORDER BY (cs.current_value::numeric / NULLIF(ts.total_current_value, 0)) DESC;
    """
    return execute_query(query)

def get_investment_details() -> List[Dict[str, Any]]:
    """Get detailed investment data grouped by asset class only."""
    query = """
        WITH distinct_asset_classes AS (
            SELECT DISTINCT asset_class
            FROM position_active
            WHERE asset_class IS NOT NULL 
            AND asset_class != ''
            AND asset_class NOT IN ('Loan', 'Credit Cards', 'Mortgage', 'Other Liabilities', 'Liability')
        ),
        categorized_investments AS (
            SELECT 
                pa.instrument_name,
                pa.investment_date,
                pa.investment_amount::text,
                COALESCE(pa.dividend, 0)::text as dividend,
                COALESCE(pa.quantity, 0)::text as quantity,
                COALESCE(pa.mtm, 0)::text as mtm,
                COALESCE(pa.market_value, 0)::text as market_value,
                COALESCE(pa.unrealised_pnl, 0)::text as unrealised_pnl,
                COALESCE(pa.realised_pnl, 0)::text as realised_pnl,
                COALESCE(pa.xirr_percent, 0)::text as xirr_percent,
                COALESCE(pa.amount_or_capital_redeemed, 0)::text as amount_or_capital_redeemed,
                pa.valuation_date,
                pa.asset_class,
                pa.sub_asset_class,
                CONCAT_WS(' ', 
                    NULLIF(cm.first_name, ''), 
                    NULLIF(cm.middle_name, ''), 
                    NULLIF(cm.last_name, '')
                ) AS client_name,
                ROW_NUMBER() OVER (
                    PARTITION BY pa.invest_id, pa.instrument_name 
                    ORDER BY COALESCE(pa.valuation_date, pa.investment_date) DESC
                ) as rn
            FROM 
                position_active pa
            LEFT JOIN 
                client_master cm ON pa.invest_id = cm.invest_id
            WHERE 
                pa.instrument_name IS NOT NULL
                AND pa.instrument_name != ''
                AND pa.asset_class IN (SELECT asset_class FROM distinct_asset_classes)
        ),
        grouped_investments AS (
            SELECT 
                asset_class,
                json_agg(
                    json_build_object(
                        'instrument_name', instrument_name,
                        'investment_date', investment_date,
                        'investment_amount', investment_amount,
                        'dividend', dividend,
                        'quantity', quantity,
                        'mtm', mtm,
                        'market_value', market_value,
                        'unrealised_pnl', unrealised_pnl,
                        'realised_pnl', realised_pnl,
                        'xirr_percent', xirr_percent,
                        'amount_or_capital_redeemed', amount_or_capital_redeemed,
                        'valuation_date', valuation_date,
                        'asset_class', asset_class,
                        'sub_asset_class', sub_asset_class,
                        'client_name', client_name
                    ) ORDER BY instrument_name, COALESCE(valuation_date, investment_date) DESC
                ) FILTER (WHERE rn = 1) as investments
            FROM categorized_investments
            GROUP BY asset_class
        )
        SELECT 
            json_object_agg(
                LOWER(asset_class), 
                COALESCE(investments, '[]'::json)
            ) as asset_class_investments
        FROM grouped_investments;
    """
    return execute_query(query)

def get_equity_investments() -> Dict[str, Any]:
    """Get detailed equity investments with summary for pie chart."""
    query = """
        WITH equity_investments AS (
            SELECT 
                pa.instrument_name,
                pa.investment_date,
                pa.investment_amount::text,
                COALESCE(pa.dividend, 0)::text as dividend,
                COALESCE(pa.quantity, 0)::text as quantity,
                COALESCE(pa.mtm, 0)::text as mtm,
                COALESCE(pa.market_value, 0)::text as market_value,
                COALESCE(pa.unrealised_pnl, 0)::text as unrealised_pnl,
                COALESCE(pa.realised_pnl, 0)::text as realised_pnl,
                COALESCE(pa.xirr_percent, 0)::text as xirr_percent,
                COALESCE(pa.amount_or_capital_redeemed, 0)::text as amount_or_capital_redeemed,
                pa.valuation_date,
                pa.asset_class,
                pa.sub_asset_class,
                CONCAT_WS(' ', 
                    NULLIF(cm.first_name, ''), 
                    NULLIF(cm.middle_name, ''), 
                    NULLIF(cm.last_name, '')
                ) AS client_name,
                ROW_NUMBER() OVER (
                    PARTITION BY pa.invest_id, pa.instrument_name 
                    ORDER BY COALESCE(pa.valuation_date, pa.investment_date) DESC
                ) as rn
            FROM 
                position_active pa
            LEFT JOIN 
                client_master cm ON pa.invest_id = cm.invest_id
            WHERE 
                pa.asset_class IN ('Equity', 'Mutual Fund', 'PMS', 'AIF', 'Stocks')
                AND pa.instrument_name IS NOT NULL
                AND pa.instrument_name != ''
        ),
        equity_summary AS (
            SELECT 
                sub_asset_class,
                COUNT(*) as count,
                SUM(market_value::numeric) as total_value,
                SUM(investment_amount::numeric) as total_investment,
                SUM(unrealised_pnl::numeric) as total_unrealised_pnl,
                SUM(realised_pnl::numeric) as total_realised_pnl,
                AVG(xirr_percent::numeric) as avg_xirr
            FROM equity_investments
            WHERE rn = 1
            GROUP BY sub_asset_class
        ),
        total_values AS (
            SELECT SUM(total_value) as grand_total
            FROM equity_summary
        )
        SELECT 
            json_build_object(
                'details', (
                    SELECT json_agg(
                        json_build_object(
                            'instrument_name', instrument_name,
                            'investment_date', investment_date,
                            'investment_amount', investment_amount,
                            'dividend', dividend,
                            'quantity', quantity,
                            'mtm', mtm,
                            'market_value', market_value,
                            'unrealised_pnl', unrealised_pnl,
                            'realised_pnl', realised_pnl,
                            'xirr_percent', xirr_percent,
                            'amount_or_capital_redeemed', amount_or_capital_redeemed,
                            'valuation_date', valuation_date,
                            'asset_class', asset_class,
                            'sub_asset_class', sub_asset_class,
                            'client_name', client_name
                        ) ORDER BY instrument_name, COALESCE(valuation_date, investment_date) DESC
                    ) FILTER (WHERE rn = 1)
                    FROM equity_investments
                ),
                'summary', (
                    SELECT json_agg(
                        json_build_object(
                            'category', s.sub_asset_class,
                            'count', s.count,
                            'total_value', s.total_value::text,
                            'total_investment', s.total_investment::text,
                            'total_unrealised_pnl', s.total_unrealised_pnl::text,
                            'total_realised_pnl', s.total_realised_pnl::text,
                            'avg_xirr', ROUND(s.avg_xirr, 2)::text,
                            'percentage', ROUND((s.total_value::numeric / NULLIF(t.grand_total, 0)) * 100, 2)::text
                        ) ORDER BY s.total_value DESC
                    )
                    FROM equity_summary s
                    CROSS JOIN total_values t
                )
            ) as equity_data;
    """
    return execute_query(query)[0]

def get_debt_investments() -> Dict[str, Any]:
    """Get detailed debt investments with summary for pie chart."""
    query = """
        WITH debt_investments AS (
            SELECT 
                pa.instrument_name,
                pa.investment_date,
                pa.investment_amount::text,
                COALESCE(pa.dividend, 0)::text as dividend,
                COALESCE(pa.quantity, 0)::text as quantity,
                COALESCE(pa.mtm, 0)::text as mtm,
                COALESCE(pa.market_value, 0)::text as market_value,
                COALESCE(pa.unrealised_pnl, 0)::text as unrealised_pnl,
                COALESCE(pa.realised_pnl, 0)::text as realised_pnl,
                COALESCE(pa.xirr_percent, 0)::text as xirr_percent,
                COALESCE(pa.amount_or_capital_redeemed, 0)::text as amount_or_capital_redeemed,
                pa.valuation_date,
                pa.asset_class,
                pa.sub_asset_class,
                CONCAT_WS(' ', 
                    NULLIF(cm.first_name, ''), 
                    NULLIF(cm.middle_name, ''), 
                    NULLIF(cm.last_name, '')
                ) AS client_name,
                ROW_NUMBER() OVER (
                    PARTITION BY pa.invest_id, pa.instrument_name 
                    ORDER BY COALESCE(pa.valuation_date, pa.investment_date) DESC
                ) as rn
            FROM 
                position_active pa
            LEFT JOIN 
                client_master cm ON pa.invest_id = cm.invest_id
            WHERE 
                pa.asset_class IN ('Debt', 'Fixed Income', 'Bonds')
                AND pa.instrument_name IS NOT NULL
                AND pa.instrument_name != ''
        ),
        debt_summary AS (
            SELECT 
                sub_asset_class,
                COUNT(*) as count,
                SUM(market_value::numeric) as total_value,
                SUM(investment_amount::numeric) as total_investment,
                SUM(unrealised_pnl::numeric) as total_unrealised_pnl,
                SUM(realised_pnl::numeric) as total_realised_pnl,
                AVG(xirr_percent::numeric) as avg_xirr
            FROM debt_investments
            WHERE rn = 1
            GROUP BY sub_asset_class
        ),
        total_values AS (
            SELECT SUM(total_value) as grand_total
            FROM debt_summary
        )
        SELECT 
            json_build_object(
                'details', (
                    SELECT json_agg(
                        json_build_object(
                            'instrument_name', instrument_name,
                            'investment_date', investment_date,
                            'investment_amount', investment_amount,
                            'dividend', dividend,
                            'quantity', quantity,
                            'mtm', mtm,
                            'market_value', market_value,
                            'unrealised_pnl', unrealised_pnl,
                            'realised_pnl', realised_pnl,
                            'xirr_percent', xirr_percent,
                            'amount_or_capital_redeemed', amount_or_capital_redeemed,
                            'valuation_date', valuation_date,
                            'asset_class', asset_class,
                            'sub_asset_class', sub_asset_class,
                            'client_name', client_name
                        ) ORDER BY instrument_name, COALESCE(valuation_date, investment_date) DESC
                    ) FILTER (WHERE rn = 1)
                    FROM debt_investments
                ),
                'summary', (
                    SELECT json_agg(
                        json_build_object(
                            'category', s.sub_asset_class,
                            'count', s.count,
                            'total_value', s.total_value::text,
                            'total_investment', s.total_investment::text,
                            'total_unrealised_pnl', s.total_unrealised_pnl::text,
                            'total_realised_pnl', s.total_realised_pnl::text,
                            'avg_xirr', ROUND(s.avg_xirr, 2)::text,
                            'percentage', ROUND((s.total_value::numeric / NULLIF(t.grand_total, 0)) * 100, 2)::text
                        ) ORDER BY s.total_value DESC
                    )
                    FROM debt_summary s
                    CROSS JOIN total_values t
                )
            ) as debt_data;
    """
    return execute_query(query)[0]

def get_hybrid_investments() -> Dict[str, Any]:
    """Get detailed hybrid investments with summary for pie chart."""
    query = """
        WITH hybrid_investments AS (
            SELECT 
                pa.instrument_name,
                pa.investment_date,
                pa.investment_amount::text,
                COALESCE(pa.dividend, 0)::text as dividend,
                COALESCE(pa.quantity, 0)::text as quantity,
                COALESCE(pa.mtm, 0)::text as mtm,
                COALESCE(pa.market_value, 0)::text as market_value,
                COALESCE(pa.unrealised_pnl, 0)::text as unrealised_pnl,
                COALESCE(pa.realised_pnl, 0)::text as realised_pnl,
                COALESCE(pa.xirr_percent, 0)::text as xirr_percent,
                COALESCE(pa.amount_or_capital_redeemed, 0)::text as amount_or_capital_redeemed,
                pa.valuation_date,
                pa.asset_class,
                pa.sub_asset_class,
                CONCAT_WS(' ', 
                    NULLIF(cm.first_name, ''), 
                    NULLIF(cm.middle_name, ''), 
                    NULLIF(cm.last_name, '')
                ) AS client_name,
                ROW_NUMBER() OVER (
                    PARTITION BY pa.invest_id, pa.instrument_name 
                    ORDER BY COALESCE(pa.valuation_date, pa.investment_date) DESC
                ) as rn
            FROM 
                position_active pa
            LEFT JOIN 
                client_master cm ON pa.invest_id = cm.invest_id
            WHERE 
                pa.asset_class IN ('Hybrid', 'Balanced')
                AND pa.instrument_name IS NOT NULL
                AND pa.instrument_name != ''
        ),
        hybrid_summary AS (
            SELECT 
                sub_asset_class,
                COUNT(*) as count,
                SUM(market_value::numeric) as total_value,
                SUM(investment_amount::numeric) as total_investment,
                SUM(unrealised_pnl::numeric) as total_unrealised_pnl,
                SUM(realised_pnl::numeric) as total_realised_pnl,
                AVG(xirr_percent::numeric) as avg_xirr
            FROM hybrid_investments
            WHERE rn = 1
            GROUP BY sub_asset_class
        ),
        total_values AS (
            SELECT SUM(total_value) as grand_total
            FROM hybrid_summary
        )
        SELECT 
            json_build_object(
                'details', (
                    SELECT json_agg(
                        json_build_object(
                            'instrument_name', instrument_name,
                            'investment_date', investment_date,
                            'investment_amount', investment_amount,
                            'dividend', dividend,
                            'quantity', quantity,
                            'mtm', mtm,
                            'market_value', market_value,
                            'unrealised_pnl', unrealised_pnl,
                            'realised_pnl', realised_pnl,
                            'xirr_percent', xirr_percent,
                            'amount_or_capital_redeemed', amount_or_capital_redeemed,
                            'valuation_date', valuation_date,
                            'asset_class', asset_class,
                            'sub_asset_class', sub_asset_class,
                            'client_name', client_name
                        ) ORDER BY instrument_name, COALESCE(valuation_date, investment_date) DESC
                    ) FILTER (WHERE rn = 1)
                    FROM hybrid_investments
                ),
                'summary', (
                    SELECT json_agg(
                        json_build_object(
                            'category', s.sub_asset_class,
                            'count', s.count,
                            'total_value', s.total_value::text,
                            'total_investment', s.total_investment::text,
                            'total_unrealised_pnl', s.total_unrealised_pnl::text,
                            'total_realised_pnl', s.total_realised_pnl::text,
                            'avg_xirr', ROUND(s.avg_xirr, 2)::text,
                            'percentage', ROUND((s.total_value::numeric / NULLIF(t.grand_total, 0)) * 100, 2)::text
                        ) ORDER BY s.total_value DESC
                    )
                    FROM hybrid_summary s
                    CROSS JOIN total_values t
                )
            ) as hybrid_data;
    """
    return execute_query(query)[0]

def get_all_investment_summary_data() -> dict:
    """Fetch all data required for the investment summary report"""
    try:
        # Get merged data for all pages
        all_assets_data = get_investment_summary_all_assets()
        liabilities_data = get_liabilities_summary()
        asset_class_summary = get_asset_class_summary()
        instrument_summary = get_instrument_summary()
        client_code_summary = get_client_code_summary()
        investment_details = get_investment_details()
        equity_data = get_equity_investments()
        debt_data = get_debt_investments()
        hybrid_data = get_hybrid_investments()
        
        # Create the complete data structure
        complete_data = {
            "first_page_data": {
                "investment_data": all_assets_data
            },
            "second_page_data": {
                "assets": all_assets_data,
                "liabilities": liabilities_data
            },
            "third_page_data": {
                "asset_summary": asset_class_summary
            },
            "fourth_page_data": {
                "instrument_summary": instrument_summary
            },
            "fifth_page_data": {
                "client_summary": client_code_summary
            },
            "sixth_page_data": {"investment_details": investment_details[0] if investment_details else {}},
            "seventh_page_data": equity_data,
            "eighth_page_data": debt_data,
            "ninth_page_data": hybrid_data
        }
        
        return complete_data
    except Exception as e:
        print(f"Error fetching investment summary data: {str(e)}")
        raise