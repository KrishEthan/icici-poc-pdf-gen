import requests
import time

# Test data

investment_summary_first_page_data = {
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
    "investment_data": []
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
  },
  "fourth_page_data": {
    "assets": [
      {
        "particular": "Life insurance/ULIP",
        "premium_account": "9843",
        "sum_assured": "17823",
        "valuation": "string",
        "due_date": "string"
      }
    ],
    "liabilities": {
      "credit_cards": [
        {
          "particular": "credit cards",
          "available_credit_limit": "23984",
          "total_credit_limit": "4324234",
          "minimum_amount_due": "3422",
          "total_amout_due": "12323"
        }
      ],
      "loans": [
        {
          "particular": "Loans",
          "loan_amount": "332423xxx",
          "emi": "xxxxx",
          "outstanding": "324234",
          "maximum_tenure": "xxxx"
        }
      ]
    },
    "bank_balance": [
      {
        "particular": "xxx",
        "current_value": "098403"
      }
    ]
  },
  "fifth_page_data": {
    "investment_details": [
      {
        "accounts": "1991541 & Krithvek_1991541A Krithvek_1991541",
        "types": "Short dur",
        "scheme_name": "Akheeeeeeel",
        "folio_no": "1049994955224",
        "date_of_investment": "21-09-12",
        "invested_amount": "10000",
        "dividends_received": "490.3",
        "last_updated_nav": "4.4439",
        "no_of_units": "27.73",
        "current_market_value": "27_738_850",
        "unrealized_gain_loss": "10_737_950",
        "irr_since_inception": "7.59",
        "irr_ytd": "0.0"
      }
    ],
    "total_investment": {
      "invested_amount": "3256648",
      "dividends_received": "1850.1",
      "current_market_value": "45_12_750",
      "unrealized_gain_loss": "12_56_102",
      "irr_since_inception": "-0.1",
      "irr_ytd": "0.6"
    }
  },
  "sixth_page_data": {
    "client_name": "RITESH A BHAVSAR RITESH",
    "mid_cap_fund": [
      {
        "scheme_name": "Axis Midcap Reg-G",
        "folio_no": "3874932749",
        "date_of_investment": "22-09-21",
        "Invested_amout": "26,499",
        "devident_or_received": "0",
        "number_of_units": "391.3",
        "last_updated_NAV": "104.0",
        "current_market_value": "40,677",
        "unrealized_gain_or_lose": "14,178",
        "realized_gain_or_lose": "14,178",
        "IRR_since_interception": "26.13",
        "IRR_FYTD": "16.9"
      }
    ],
    "small_cap_fund": [],
    "large_cap_fund": []
  },
  "seventh_page_data": {
    "client_name": "RITESH A BHAVSAR RITESH",
    "multi_asset_allocation": [
      {
        "scheme_name": "ICICi Prudential Contra PMS",
        "folio_no": "3874932749",
        "date_of_investment": "22-09-21",
        "invested_amount": "26,499",
        "dividends_received": "0",
        "no_of_units": "391.3",
        "last_updated_nav": "104.0",
        "current_market_value": "40,677",
        "unrealized_gain_loss": "14,178",
        "realized_gain_loss": "14,178",
        "irr_since_inception": "26.13",
        "irr_fytd": "16.9"
      }
    ]
  },
  "eighth_page_data": [
    {
      "particular": "ICICI Prudential Contra PMS",
      "reference_no": "9837493",
      "investment_date": "2021-11-25",
      "investment_amount": "4532342",
      "valuation_date": "2021-11-25",
      "current_value": "0",
      "unrealized_gain_loss": "12222321",
      "amount_or_capital_redeemed": "0",
      "XIRR": "32.9"
    }
  ],
  "ninth_page_data": {
    "summary": [
      {
        "instument_name": "Equity AIF Fund",
        "fund_name": "Abakkus Emerging Opportunities Fund 1A1",
        "reference_no": "100043284",
        "investment_date": "25-Nov-21",
        "investment_amount": "4532342",
        "return_of_capital": "0",
        "valuation_date": "25-Nov-21",
        "current_value": "0",
        "unrealized_gain_loss": "12222321",
        "realized_gain_loss": "0",
        "xirr": "32.9"
      }
    ]
  },
  "tenth_page_data": [
    {
      "stock_name": "SEPC LTD",
      "date": "26-jan-2024",
      "ISIN": "1.0",
      "no_of_units": "4.32",
      "market_price_per_share": "0",
      "current_market_value": "32.9"
    }
  ],
  "eleventh_page_data": [
    {
      "fund_name": "AIF",
      "asset_class": "267832",
      "ISIN": "1.0",
      "reference_no": "0",
      "no_of_units": "0",
      "market_price_per_share": "4365432",
      "investment_amont": "4532342"
    }
  ],
  "twelveth_page_data": [
    {
      "account_holder_name": "TARA GOPINATH",
      "balance_as_on": "86,87,870",
      "account_number": "345388888258",
      "account_type": "savings",
      "balance": "0"
    }
  ],
  "twelfth_page_data": {
    "policies": [
      {
        "policy_name": "ICICI Pru LifeTime Classic",
        "policy_type": "ULIP",
        "premimum_due_date": "30-Jun-25",
        "policy_no": "LT123456",
        "premium_account": "24,000",
        "sum_assured": "10,00,000",
        "valuation": "12,50,000"
      }
    ]
  },
  "fourteenth_page_data": {
    "credit_cards": [
      {
        "card_type": "Amazon Pay ICICI Bank Credit Card",
        "payment_due_date": "15-Feb-24",
        "credit_card_number": "0050500652452",
        "credit_limit": "1,50,000",
        "cash_limit": "0",
        "available_credit_limit": "13,11,410",
        "minimum_amount_due": "13,460",
        "total_amount_due": "78,200"
      }
    ],
    "total": {
      "credit_limit": "46,43,324",
      "available_credit_limit": "13,11,410",
      "minimum_amount_due": "13,460",
      "total_amount_due": "78,200"
    }
  },
  "fifteenth_page_data": {
    "loans": [
      {
        "loan_type": "Housing Loan",
        "loan_account": "LBMU345388888258",
        "loan_amount": "1,50,000",
        "tenure": "240",
        "maturity": "25-Nov-21",
        "outstanding": "13,11,410",
        "EMI": "13,000",
        "composition": "13,000"
      }
    ],
    "total": {
      "loan_amount": "1,50,000",
      "outstanding": "13,11,410",
      "EMI": "13,000"
    }
  },
  "eighteenth_page_data": [
    {
      "name": "RITESH A BHAVSAR RITESH",
      "risk_profile": "Aggressive",
      "current_value": "1000000",
      "investment_value": "1000000",
      "weightage": "100",
      "total_gain_loss": "1000000",
      "current_asset_allocation": {
        "debt": "10",
        "equity": "20",
        "others": "70"
      },
      "target_asset_allocation": {
        "debt": "10",
        "equity": "20",
        "others": "70"
      }
    }
  ]
}

investment_summary_payload = {
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
                    }
                ]
            }
        ]
    },
    "third_page_data": {
        "assets": [
            {
                "particular": "Equity",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Hybrid",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "ULIP",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Assets",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Bank Balance &Deposits",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Direct Equity",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Demat MF",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Demat Bond",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "100"
            },
            {
                "particular": "Total Assets",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "50"
            }
        ],
        "liabilities": [
            {
                "particular": "Credit Card",
                "loan_credit_limit": "19,24,111",
                "outstanding_amount": "50,056"
            },
            {
                "particular": "Total Liabilities",
                "loan_credit_limit": "19,24,111",
                "outstanding_amount": "150,056"
            }
        ]
    },
    "fourth_page_data": {
        "assets": [
            {
                "particular": "Life insurance/ULIP",
                "premium_account": "9843",
                "sum_assured": "17823",
                "valuation": "string",
                "due_date": "string"
            }
        ],
        "liabilities": {
            "credit_cards": [
                {
                    "particular": "credit cards",
                    "available_credit_limit": "23984",
                    "total_credit_limit": "4324234",
                    "minimum_amount_due": "3422",
                    "total_amout_due": "12323"
                }
            ],
            "loans": [
                {
                    "particular": "Loans",
                    "loan_amount": "332423xxx",
                    "emi": "xxxxx",
                    "outstanding": "324234",
                    "maximum_tenure": "xxxx"
                }
            ]
        },
        "bank_balance": [
            {
                "particular": "xxx",
                "current_value": "098403"
            }
        ]
    },
    "fifth_page_data": {
        "investment_details": [
            {
                "accounts": "1991541 & Krithvek_1991541A Krithvek_1991541",
                "types": "Short dur",
                "scheme_name": "Akheeeeeeel",
                "folio_no": "1049994955224",
                "date_of_investment": "21-09-12",
                "invested_amount": "10000",
                "dividends_received": "490.3",
                "last_updated_nav": "4.4439",
                "no_of_units": "27.73",
                "current_market_value": "27_738_850",
                "unrealized_gain_loss": "10_737_950",
                "irr_since_inception": "7.59",
                "irr_ytd": "0.0"
            },
            {
                "accounts": "",
                "types": "Liquid",
                "scheme_name": "Akheeeeeeel",
                "folio_no": "1049994955224",
                "date_of_investment": "21-09-12",
                "invested_amount": "10000",
                "dividends_received": "490.3",
                "last_updated_nav": "4.4439",
                "no_of_units": "27.73",
                "current_market_value": "27_738_850",
                "unrealized_gain_loss": "10_737_950",
                "irr_since_inception": "7.59",
                "irr_ytd": "0.0"
            }
        ],
        "total_investment": {
            "invested_amount": "3256648",
            "dividends_received": "1850.1",
            "current_market_value": "45_12_750",
            "unrealized_gain_loss": "12_56_102",
            "irr_since_inception": "-0.1",
            "irr_ytd": "0.6"
        }
    },
    "sixth_page_data": {
        "client_name": "RITESH A BHAVSAR RITESH",
        "mid_cap_fund": [
            {
                "scheme_name": "Axis Midcap Reg-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "26,499",
                "devident_or_received": "0",
                "number_of_units": "391.3",
                "last_updated_NAV": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_or_lose": "14,178",
                "realized_gain_or_lose": "14,178",
                "IRR_since_interception": "26.13",
                "IRR_FYTD": "16.9"
            },
            {
                "scheme_name": "Axis Midcap Reg-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "26,499",
                "devident_or_received": "0",
                "number_of_units": "391.3",
                "last_updated_NAV": "104.0,",
                "current_market_value": "40,677",
                "unrealized_gain_or_lose": "14,178",
                "realized_gain_or_lose": "14,178",
                "IRR_since_interception": "26.13",
                "IRR_FYTD": " 16.9"
            }
        ],
        "small_cap_fund": [
            {
                "scheme_name": "Axis Midcap Reg-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "26,499",
                "devident_or_received": "0",
                "number_of_units": "391.3",
                "last_updated_NAV": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_or_lose": "14,178",
                "realized_gain_or_lose": "14,178",
                "IRR_since_interception": "26.13",
                "IRR_FYTD": "16.9"
            },
            {
                "scheme_name": "Axis Midcap Reg-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "26,499",
                "devident_or_received": "0",
                "number_of_units": "391.3",
                "last_updated_NAV": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_or_lose": "14,178",
                "realized_gain_or_lose": "14,178",
                "IRR_since_interception": "26.13",
                "IRR_FYTD": "16.9"
            }
        ],
        "large_cap_fund": [
            {
                "scheme_name": "Axis Midcap Reg-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "26,499",
                "devident_or_received": "0",
                "number_of_units": "391.3",
                "last_updated_NAV": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_or_lose": "14,178",
                "realized_gain_or_lose": "14,178",
                "IRR_since_interception": "26.13",
                "IRR_FYTD": "16.9"
            }
        ]
    },
    "seventh_page_data": {
        "client_name": "RITESH A BHAVSAR RITESH",
        "multi_asset_allocation": [
            {
                "scheme_name": "ICICi Prudential Contra PMS",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "invested_amount": "26,499",
                "dividends_received": "0",
                "no_of_units": "391.3",
                "last_updated_nav": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_loss": "14,178",
                "realized_gain_loss": "14,178",
                "irr_since_inception": "26.13",
                "irr_fytd": "16.9"
            },
            {
                "scheme_name": "Total",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "invested_amount": "26,499",
                "dividends_received": "0",
                "no_of_units": "391.3",
                "last_updated_nav": "104.0",
                "current_market_value": "40,677",
                "unrealized_gain_loss": "14,178",
                "realized_gain_loss": "14,178",
                "irr_since_inception": "26.13",
                "irr_fytd": "16.9"
            }
        ]
    },
    "eighth_page_data": [
        {
            "particular": "ICICI Prudential Contra PMS",
            "reference_no": "9837493",
            "investment_date": "2021-11-25",
            "investment_amount": "4532342",
            "valuation_date": "2021-11-25",
            "current_value": "0",
            "unrealized_gain_loss": "12222321",
            "amount_or_capital_redeemed": "0",
            "XIRR": "32.9"
        },
        {
            "particular": "Marcellus Consistent Compounders PMS",
            "reference_no": "9837493",
            "investment_date": "2021-11-25",
            "investment_amount": "4532342",
            "valuation_date": "2021-11-25",
            "current_value": "0",
            "unrealized_gain_loss": "12222321",
            "amount_or_capital_redeemed": "0",
            "XIRR": "32.9"
        },
        {
            "particular": "Consistents Compounders PMS",
            "reference_no": "9837493",
            "investment_date": "2021-11-25",
            "investment_amount": "4532342",
            "valuation_date": "2021-11-25",
            "current_value": "0",
            "unrealized_gain_loss": "12222321",
            "amount_or_capital_redeemed": "0",
            "XIRR": "32.9"
        }
    ],
    "ninth_page_data": {
        "summary": [
            {
                "instument_name": "Equity AIF Fund",
                "fund_name": "Abakkus Emerging Opportunities Fund 1A1",
                "reference_no": "100043284",
                "investment_date": "25-Nov-21",
                "investment_amount": "4532342",
                "return_of_capital": "0",
                "valuation_date": "25-Nov-21",
                "current_value": "0",
                "unrealized_gain_loss": "12222321",
                "realized_gain_loss": "0",
                "xirr": "32.9"
            },
            {
                "instument_name": "Equity AIF Fund",
                "fund_name": "Abakkus Emerging Opportunities Fund 1A1",
                "reference_no": "100043284",
                "investment_date": "25-Nov-21",
                "investment_amount": "4532342",
                "return_of_capital": "0",
                "valuation_date": "25-Nov-21",
                "current_value": "0",
                "unrealized_gain_loss": "12222321",
                "realized_gain_loss": "0",
                "xirr": "32.9"
            }
        ]
    },
    "tenth_page_data": [
        {
            "stock_name": "SEPC LTD",
            "date": "26-jan-2024",
            "ISIN": "1.0",
            "no_of_units": "4.32",
            "market_price_per_share": "0",
            "current_market_value": "32.9"
        },
        {
            "stock_name": "TAKE SOLUTIONS LTD",
            "date": "26-jan-2024",
            "ISIN": "1.0",
            "no_of_units": "4.32",
            "market_price_per_share": "0",
            "current_market_value": "32.9"
        },
        {
            "stock_name": "BALAJ HOTELS & ENTERPRISES LTD",
            "date": "26-jan-2024",
            "ISIN": "1.0",
            "no_of_units": "4.32",
            "market_price_per_share": "0",
            "current_market_value": "32.9"
        },
        {
            "stock_name": "NEPC AGRO FOODS LTD",
            "date": "26-jan-2024",
            "ISIN": "1.0",
            "no_of_units": "4.32",
            "market_price_per_share": "0",
            "current_market_value": "32.9"
        },
        {
            "stock_name": "PALRED TECHNOLOGIES LTD",
            "date": "26-jan-2024",
            "ISIN": "1.0",
            "no_of_units": "4.32",
            "market_price_per_share": "0",
            "current_market_value": "32.9"
        }
    ],
    "eleventh_page_data": [
        {
            "fund_name": "AIF",
            "asset_class": "267832",
            "ISIN": "1.0",
            "reference_no": "0",
            "no_of_units": "0",
            "market_price_per_share": "4365432",
            "investment_amont": "4532342"
        },
        {
            "fund_name": "Nippon India ETF Gold BeES",
            "asset_class": "267832",
            "ISIN": "1.0",
            "reference_no": "0",
            "no_of_units": "0",
            "market_price_per_share": "4365432",
            "investment_amont": "4532342"
        },
        {
            "fund_name": "Total Inv",
            "asset_class": "267832",
            "ISIN": "1.0",
            "reference_no": "0",
            "no_of_units": "0",
            "market_price_per_share": "4365432",
            "investment_amont": "4532342"
        }
    ],
    "twelfth_page_data": {
        "policies": [
            {
                "policy_name": "ICICI Pru LifeTime Classic",
                "policy_type": "ULIP",
                "premimum_due_date": "30-Jun-25",
                "policy_no": "LT123456",
                "premium_account": "24,000",
                "sum_assured": "10,00,000",
                "valuation": "12,50,000"
            },
            {
                "policy_name": "HDFC Life Sanchay Plus",
                "policy_type": "Traditional",
                "premimum_due_date": "15-Jul-25",
                "policy_no": "SP987654",
                "premium_account": "18,000",
                "sum_assured": "8,00,000",
                "valuation": "9,20,000"
            }
        ]
    },
    "thirteenth_page_data": [
        {
            "account_holder_name": "TARA GOPINATH",
            "balance_as_on": "86,87,870",
            "account_number": "345388888258",
            "account_type": "savings",
            "balance": "0"
        },
        {
            "account_holder_name": "MADHUSUDAN GOPINATH",
            "balance_as_on": "86,87,870",
            "account_number": "345388888258",
            "account_type": "savings",
            "balance": "0"
        },
        {
            "account_holder_name": "Total",
            "balance_as_on": "86,87,870",
            "account_number": "345388888258",
            "account_type": "savings",
            "balance": "0"
        }
    ],
    "fourteenth_page_data": {
        "credit_cards": [
            {
                "card_type": "Amazon Pay ICICI Bank Credit Card",
                "payment_due_date": "15-Feb-24",
                "credit_card_number": "0050500652452",
                "credit_limit": "1,50,000",
                "cash_limit": "0",
                "available_credit_limit": "13,11,410",
                "minimum_amount_due": "13,460",
                "total_amount_due": "78,200"
            }
        ],
        "total": {
            "credit_limit": "46,43,324",
            "available_credit_limit": "13,11,410",
            "minimum_amount_due": "13,460",
            "total_amount_due": "78,200"
        }
    },
    "fifteenth_page_data": {
        "loans": [
            {
                "loan_type": "Housing Loan",
                "loan_account": "LBMU345388888258",
                "loan_amount": "1,50,000",
                "tenure": "240",
                "maturity": "25-Nov-21",
                "outstanding": "13,11,410",
                "EMI": "13,000",
                "composition": "13,000"
            },
            {
                "loan_type": "Housing Loan",
                "loan_account": "LBMU345388888258",
                "loan_amount": "1,50,000",
                "tenure": "240",
                "maturity": "25-Nov-21",
                "outstanding": "13,11,410",
                "EMI": "13,000",
                "composition": "13,000"
            }
        ],
        "total": {
            "loan_type": "Total",
            "loan_amount": "1,50,000",
            "outstanding": "13,11,410",
            "EMI": "13,000"
        }
    },
    "eighteenth_page_data": [
        {
            "name": "RITESH A BHAVSAR RITESH",
            "risk_profile": "Aggressive",
            "current_value": "1000000",
            "investment_value": "1000000",
            "weightage": "100",
            "total_gain_loss": "1000000",
            "current_asset_allocation": {
                "debt": "10",
                "equity": "20",
                "others": "70"
            },
            "target_asset_allocation": {
                "debt": "10",
                "equity": "20",
                "others": "70"
            }
        }
    ],
    "nineteenth_page_data": {
        "investment_data": [
            {
                "category": "Dept",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    }
                ]
            },
            {
                "category": "Equity",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    }
                ]
            },
            {
                "category": "Hybrid",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    }
                ]
            },
            {
                "category": "other_alternatives",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    }
                ]
            },
            {
                "category": "ULIP",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    }
                ]
            }
        ]
    },
    "twenteeth_page_data": {
        "debt_analysis_response": [
            {
                "particulars": "Corporate Bond A",
                "holdings_cost": "1000000.0",
                "current_value": "1050000.0",
                "holdings": "10.0",
                "gain_or_lose_realized": "50000.0",
                "devident_or_interest": "30000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "7.5"
            },
            {
                "particulars": "Government Bond B",
                "holdings_cost": "500000",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            }
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
    response = requests.post(f"http://localhost:8000{endpoint}", json=investment_summary_payload)
    end_time = time.time()
    
    print(f"\nTesting {endpoint}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print(f"Status code: {response.status_code}")
    print(response.text)
  except Exception as e:
    print(f"Error: {e}")
    print(f"Response: {response.text}")
    print(f"Status code: {response.status_code}")