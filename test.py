import requests
import time

# Test data
data = {
  "title": "Investment Portfolio Report",
  "summary": "This report summarizes the current state of the investment portfolio across different asset classes.",
  "data": {
    "dept": [
      {
        "particulars": "Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "PMS",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Demat Bonds & NCD's",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Fixed Deposits",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Demat Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Demat Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ],
    "equity": [
      {
        "particulars": "Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "PMS",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Cat3 AIF",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Direct Equity",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Demat Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ],
    "hybrid": [
      {
        "particulars": "Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "PMS",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Cat3 AIF",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Demat Mutual Funds",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ],
    "other_atlernatives": [
      {
        "particulars": "Cat 1 AIF",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Cat 2 AIF",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "REITs/INVIT's",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ],
    "gold_silver_or_precious_metal": [
      {
        "particulars": "Gold SGB",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Gold Mutual Funds (Index Funds)",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Gold ETF (Demat)",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Silver Mutual Funds (Index Funds)",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Silver ETF (Demat)",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "ULIP",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      },
      {
        "particulars": "Bank Balance & Deposits",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ],
    "total_assets": [
      {
        "particulars": "Total Assets",
        "invested_amout": 6999950,
        "holdings_cost": 4999950,
        "current_value": 9449950,
        "irr_since_interception": 439953
      }
    ]
  },
  "chart_data": [100, 120, 150, 130, 160],
  "chart_type": "bar",
  "chart_title": "Investment Growth"
}

investment_summary_first_page_data = {
  "first_page_data": {
    "investment_data": [
      {
        "category": "Dept",
        "investment_amount": "69,99,950",
        "holding_cost": "49,99,950",
        "current_value": "94,49,950",
        "irr": "4,39,953",
        "subcategories": [
          {
            "particular": "Mutual Funds",
            "investment_amount": "9,61,739",
            "holding_cost": "9,99,950",
            "current_value": "9,950",
            "irr": "9,61,739"
          },
          {
            "particular": "PMS",
            "investment_amount": "9,950",
            "holding_cost": "9,99,950",
            "current_value": "61,739",
            "irr": "9,99,950"
          },
          {
            "particular": "Demat Bonds & NCD's",
            "investment_amount": "9,61,739",
            "holding_cost": "9,99,950",
            "current_value": "9,950",
            "irr": "9,61,739"
          },
          {
            "particular": "Fixed Deposits",
            "investment_amount": "9,99,950",
            "holding_cost": "1,739",
            "current_value": "9,99,950",
            "irr": "9,99,950"
          },
          {
            "particular": "Demat Mutual Funds",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          }
        ]
      },
      {
        "category": "Equity",
        "investment_amount": "12,39,61,739",
        "holding_cost": "21,26,58,400",
        "current_value": "28,97,94,962",
        "irr": "18.35",
        "subcategories": [
          {
            "particular": "Mutual Funds",
            "investment_amount": "9,61,739",
            "holding_cost": "9,99,950",
            "current_value": "9,950",
            "irr": "9,61,739"
          },
          {
            "particular": "PMS",
            "investment_amount": "9,950",
            "holding_cost": "9,99,950",
            "current_value": "61,739",
            "irr": "9,99,950"
          },
          {
            "particular": "Cat3 AIF",
            "investment_amount": "9,61,739",
            "holding_cost": "9,99,950",
            "current_value": "9,950",
            "irr": "9,61,739"
          },
          {
            "particular": "Direct Equity",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Demat Mutual Funds",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          }
        ]
      },
      {
        "category": "Hybrid",
        "investment_amount": "9,99,950",
        "holding_cost": "9,950",
        "current_value": "6,957",
        "irr": "9,99,950",
        "subcategories": [
          {
            "particular": "Mutual Funds",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "PMS",
            "investment_amount": "9,950",
            "holding_cost": "9,99,950",
            "current_value": "61,739",
            "irr": "9,99,950"
          },
          {
            "particular": "Cat3 AIF",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Demat Mutual Funds",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          }
        ]
      }
    ]
  },
  "second_page_data": {
    "investment_data": [
      {
        "category": "Other Alternatives",
        "investment_amount": "4,79,99,950",
        "holding_cost": "78,20,33,163",
        "current_value": "57,78,54,862",
        "irr": "100",
        "subcategories": [
          {
            "particular": "Cat 1 AIF",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Cat 2 AIF",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "REITs/INVIT's",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          }
        ]
      }, 
      {
        "category": "Gold Silver or Precious Metals",
        "investment_amount": "9,99,950",
        "holding_cost": "9,950",
        "current_value": "6,957",
        "irr": "9,99,950",
        "subcategories": [
          {
            "particular": "Gold SGB",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Gold Mutual Funds (Index Funds)",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Gold ETF (Demat)",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Silver Mutual Funds (Index Funds)",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
          {
            "particular": "Silver ETF (Demat)",
            "investment_amount": "9,99,950",
            "holding_cost": "9,950",
            "current_value": "6,957",
            "irr": "9,99,950"
          },
        ]
          
      }
    ]
  },
  "third_page_data": {
    "assets": [
          {"particular": "Equity", "holding_cost": "78,20,33,163", "current_value": "57,78,54,862", "irr": "100",},
          {"particular": "Hybrid", "holding_cost": "9,61,739", "current_value": "9,61,739", "irr": "9,61,739"},
          {"particular": "ULIP", "holding_cost": "4,769", "current_value": "9,99,950", "irr": "0.0"},
          {"particular": "Assets", "holding_cost": "9,61,739", "current_value": "9,61,739", "irr": "14"},
          {"particular": "Bank Balance & Deposits", "holding_cost": "9,61,739", "current_value": "9,61,739", "irr": "9,61,739"},
          {"particular": "Direct Equity", "holding_cost": "9,61,739", "current_value": "9,99,950", "irr": "50"},
          {"particular": "Demat MF", "holding_cost": "9,61,739", "current_value": "9,61,739", "irr": "9,61,739"},
          {"particular": "Demat Bond", "holding_cost": "4,769", "current_value": "9,99,950", "irr": "0.0"},
          {"particular": "Total Assets", "holding_cost": "78,20,33,163", "current_value": "57,78,54,862", "irr": "50"}
      ],
      "liabilities": [
          {"particular": "Credit Card", "loan_credit_limit": "19,24,111", "outstanding_amount": "50,056"},
          {"particular": "Total Liabilities", "loan_credit_limit": "19,24,111", "outstanding_amount": "50,056"}
      ]
  }
}


# Test all endpoints
endpoints = [
    "/generate-investment-summary-report"
]

for endpoint in endpoints:
  try:
    start_time = time.time()
    response = requests.post(f"http://localhost:8000{endpoint}", json=investment_summary_first_page_data)
    end_time = time.time()
    
    print(f"\nTesting {endpoint}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Status code: {response.status_code}")
    
  except Exception as e:
    print(f"Error: {e}")
    print(f"Response: {response.text}")
    print(f"Status code: {response.status_code}")
        
