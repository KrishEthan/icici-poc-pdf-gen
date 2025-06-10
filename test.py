import requests
import time

# Test data

investment_summary_payload = {
    "first_page_data": {
        "investment_data": [
            {
                "category": "Dept",
                "investment_amount": "69,99,950",
                "holding_cost": "49,99,950",
                "current_value": "94,49,950",
                "irr": "88.99",
                "subcategories": [
                    {
                        "particular": "Mutual Funds",
                        "investment_amount": "9,61,739",
                        "holding_cost": "9,99,950",
                        "current_value": "9,950",
                        "irr": "-99.00"
                    },
                    {
                        "particular": "PMS",
                        "investment_amount": "9,950",
                        "holding_cost": "9,99,950",
                        "current_value": "61,739",
                        "irr": "-93.82"
                    },
                    {
                        "particular": "Demat Bonds & NCD's",
                        "investment_amount": "9,61,739",
                        "holding_cost": "9,99,950",
                        "current_value": "9,950",
                        "irr": "-99.00"
                    },
                    {
                        "particular": "Fixed Deposits",
                        "investment_amount": "9,99,950",
                        "holding_cost": "1,739",
                        "current_value": "9,99,950",
                        "irr": "57499.13"
                    },
                    {
                        "particular": "Demat Mutual Funds",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
                    }
                ]
            },
            {
                "category": "Equity",
                "investment_amount": "12,39,61,739",
                "holding_cost": "21,26,58,400",
                "current_value": "28,97,94,962",
                "irr": "36.26",
                "subcategories": [
                    {
                        "particular": "Mutual Funds",
                        "investment_amount": "9,61,739",
                        "holding_cost": "9,99,950",
                        "current_value": "9,950",
                        "irr": "-99.00"
                    },
                    {
                        "particular": "PMS",
                        "investment_amount": "9,950",
                        "holding_cost": "9,99,950",
                        "current_value": "61,739",
                        "irr": "-93.82"
                    },
                    {
                        "particular": "Cat3 AIF",
                        "investment_amount": "9,61,739",
                        "holding_cost": "9,99,950",
                        "current_value": "9,950",
                        "irr": "-99.00"
                    },
                    {
                        "particular": "Direct Equity",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
                    },
                    {
                        "particular": "Demat Mutual Funds",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
                    }
                ]
            },
            {
                "category": "Hybrid",
                "investment_amount": "9,99,950",
                "holding_cost": "9,950",
                "current_value": "6,957",
                "irr": "-30.10",
                "subcategories": [
                    {
                        "particular": "Mutual Funds",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
                    },
                    {
                        "particular": "PMS",
                        "investment_amount": "9,950",
                        "holding_cost": "9,99,950",
                        "current_value": "61,739",
                        "irr": "-93.82"
                    },
                    {
                        "particular": "Cat3 AIF",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
                    },
                    {
                        "particular": "Demat Mutual Funds",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "-30.10"
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
                "irr": "81.00",
                "subcategories": [
                    {
                        "particular": "Cat 1 AIF",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "10.00"
                    },
                    {
                        "particular": "Cat 2 AIF",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "61.00"
                    },
                    {
                        "particular": "REITs/INVIT's",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "34.00"
                    }
                ]
            },
            {
                "category": "Gold Silver or Precious Metals",
                "investment_amount": "9,99,950",
                "holding_cost": "9,950",
                "current_value": "6,957",
                "irr": "93.00",
                "subcategories": [
                    {
                        "particular": "Gold SGB",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "75.00"
                    },
                    {
                        "particular": "Gold Mutual Funds (Index Funds)",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "90.00"
                    },
                    {
                        "particular": "Gold ETF (Demat)",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "12.00"
                    },
                    {
                        "particular": "Silver Mutual Funds (Index Funds)",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "21.00"
                    },
                    {
                        "particular": "Silver ETF (Demat)",
                        "investment_amount": "9,99,950",
                        "holding_cost": "9,950",
                        "current_value": "6,957",
                        "irr": "56.00"
                    }
                ]
            }
        ],
        "total": {
            "particular": "Total Assets",
            "investment_amount": "9,99,9500",
            "holding_cost": "9,9500",
            "current_value": "6,9577",
            "irr": "76.00"
        }
    },
    "third_page_data": {
        "assets": [
            {
                "particular": "Equity",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "10.00"
            },
            {
                "particular": "Hybrid",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "32.00"
            },
            {
                "particular": "ULIP",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "18.34"
            },
            {
                "particular": "Assets",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "72.5"
            },
            {
                "particular": "Bank Balance &Deposits",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "54.86"
            },
            {
                "particular": "Direct Equity",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "15.87"
            },
            {
                "particular": "Demat MF",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "19.99"
            },
            {
                "particular": "Demat Bond",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "36.00"
            },
            {
                "particular": "Total Assets",
                "holding_cost": "78,20,33,163",
                "current_value": "57,78,54,862",
                "irr": "50.90"
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
                "valuation": "87465843",
                "due_date": "12/04/2030"
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
                    "loan_amount": "332423",
                    "emi": "8745",
                    "outstanding": "324234",
                    "maximum_tenure": "534732"
                }
            ]
        },
        "bank_balance": [
            {
                "particular": "7683",
                "current_value": "098403"
            }
        ]
    },
    "fifth_page_data": {
        "investment_details": [
            {
                "accounts": "2901342 & Krithvek_2901342A Krithvek_2901342",
                "types": "Short dur",
                "scheme_name": "debt_mutual_fund_instrument_level_summary",
                "folio_no": "1042439598889",
                "date_of_investment": "25-05-17",
                "invested_amount": "14768",
                "dividends_received": "820.6",
                "last_updated_nav": "7.8345",
                "no_of_units": "35.78",
                "current_market_value": "3_050_847",
                "unrealized_gain_loss": "1_843_220",
                "irr_since_inception": "8.35",
                "irr_ytd": "2.4"
            },
            {
                "accounts": "2901342 & Krithvek_2901342A",
                "types": "Long term",
                "scheme_name": "DSP Corporate Bond Fund - Direct - Growth",
                "folio_no": "1053829409293",
                "date_of_investment": "11-09-19",
                "invested_amount": "12562",
                "dividends_received": "460.7",
                "last_updated_nav": "5.1043",
                "no_of_units": "27.91",
                "current_market_value": "2_366_830",
                "unrealized_gain_loss": "801_130",
                "irr_since_inception": "9.12",
                "irr_ytd": "4.1"
            },
            {
                "accounts": "",
                "types": "",
                "scheme_name": "Baroda BNP Paribas Large and Mid Cap Fund- Direct Plan -Growth Option",
                "folio_no": "1046739803855",
                "date_of_investment": "21-08-20",
                "invested_amount": "13892",
                "dividends_received": "765.9",
                "last_updated_nav": "6.4928",
                "no_of_units": "21.39",
                "current_market_value": "2_319_046",
                "unrealized_gain_loss": "780_415",
                "irr_since_inception": "7.89",
                "irr_ytd": "3.0"
            },
            {
                "accounts": "",
                "types": "Liquid",
                "scheme_name": "Mirae Asset Cash Management-G",
                "folio_no": "1065923819201",
                "date_of_investment": "14-11-18",
                "invested_amount": "16384",
                "dividends_received": "503.2",
                "last_updated_nav": "5.9923",
                "no_of_units": "32.42",
                "current_market_value": "3_100_652",
                "unrealized_gain_loss": "1_501_221",
                "irr_since_inception": "6.51",
                "irr_ytd": "1.3"
            },
            {
                "accounts": "",
                "types": "",
                "scheme_name": "HDFC Equity Savings Fund - Growth Option - Direct Plan",
                "folio_no": "1059738461920",
                "date_of_investment": "23-09-16",
                "invested_amount": "13988",
                "dividends_received": "720.1",
                "last_updated_nav": "7.0349",
                "no_of_units": "29.85",
                "current_market_value": "3_226_431",
                "unrealized_gain_loss": "1_457_222",
                "irr_since_inception": "7.43",
                "irr_ytd": "2.2"
            },
            {
                "accounts": "",
                "types": "",
                "scheme_name": "DSP Nifty Smallcap250 Quality 50 Index Fund - Direct - Growth",
                "folio_no": "1045837293082",
                "date_of_investment": "10-04-19",
                "invested_amount": "11456",
                "dividends_received": "497.9",
                "last_updated_nav": "6.6035",
                "no_of_units": "23.98",
                "current_market_value": "2_057_760",
                "unrealized_gain_loss": "734_215",
                "irr_since_inception": "6.79",
                "irr_ytd": "1.9"
            },
            {
                "accounts": "",
                "types": "",
                "scheme_name": "Bajaj Finserv Flexi Cap Fund -Regular Plan-Growth",
                "folio_no": "1073719024923",
                "date_of_investment": "03-07-17",
                "invested_amount": "12533",
                "dividends_received": "380.8",
                "last_updated_nav": "5.7563",
                "no_of_units": "28.62",
                "current_market_value": "2_669_143",
                "unrealized_gain_loss": "937_431",
                "irr_since_inception": "8.61",
                "irr_ytd": "2.6"
            },
            {
                "accounts": "",
                "types": "",
                "scheme_name": "Axis Bluechip Fund - Direct Plan - Growth",
                "folio_no": "1044830292834",
                "date_of_investment": "29-12-16",
                "invested_amount": "11298",
                "dividends_received": "642.5",
                "last_updated_nav": "8.2356",
                "no_of_units": "27.63",
                "current_market_value": "2_277_452",
                "unrealized_gain_loss": "964_268",
                "irr_since_inception": "9.75",
                "irr_ytd": "2.8"
            }
        ],
        "total_investment": {
            "scheme_name": "Total",
            "invested_amount": "153249",
            "dividends_received": "4924.5",
            "no_of_unit": "0",
            "current_market_value": "45_218_725",
            "unrealized_gain_loss": "12_214_480",
            "irr_since_inception": "8.15",
            "irr_ytd": "3.4"
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
                "scheme_name": "ICICI Pru Midcap-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "29,875",
                "devident_or_received": "50",
                "number_of_units": "310.6",
                "last_updated_NAV": "109.5",
                "current_market_value": "44,213",
                "unrealized_gain_or_lose": "14,338",
                "realized_gain_or_lose": "14,338",
                "IRR_since_interception": "28.41",
                "IRR_FYTD": "18.1"
            },
            {
                "scheme_name": "Mirae Asset Emerging Bluechip Fund - Direct Plan",
                "folio_no": "3874932749",
                "date_of_investment": "10-01-20",
                "Invested_amout": "35,224",
                "devident_or_received": "0",
                "number_of_units": "250.8",
                "last_updated_NAV": "140.2",
                "current_market_value": "35,149",
                "unrealized_gain_or_lose": "-75",
                "realized_gain_or_lose": "-75",
                "IRR_since_interception": "12.18",
                "IRR_FYTD": "8.5"
            }
        ],
        "small_cap_fund": [
            {
                "scheme_name": "Axis Small Cap Reg-G",
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
                "scheme_name": "Quant Small Cap-G",
                "folio_no": "3874932749",
                "date_of_investment": "22-09-21",
                "Invested_amout": "23,435",
                "devident_or_received": "0",
                "number_of_units": "218.2",
                "last_updated_NAV": "108.0",
                "current_market_value": "23,580",
                "unrealized_gain_or_lose": "145",
                "realized_gain_or_lose": "145",
                "IRR_since_interception": "20.25",
                "IRR_FYTD": "19.2"
            },
            {
                "scheme_name": "Franklin India Smaller Companies Fund - Direct Plan - Growth",
                "folio_no": "3874932749",
                "date_of_investment": "15-03-19",
                "Invested_amout": "30,642",
                "devident_or_received": "0",
                "number_of_units": "239.5",
                "last_updated_NAV": "128.5",
                "current_market_value": "30,736",
                "unrealized_gain_or_lose": "94",
                "realized_gain_or_lose": "94",
                "IRR_since_interception": "19.8",
                "IRR_FYTD": "10.3"
            }
        ],
        "large_cap_fund": [
            {
                "scheme_name": "HDFC Large Cap-G",
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
                "scheme_name": "ICICI Pru Large Cap-G",
                "folio_no": "3874932749",
                "date_of_investment": "15-02-19",
                "Invested_amout": "40,298",
                "devident_or_received": "0",
                "number_of_units": "389.5",
                "last_updated_NAV": "112.3",
                "current_market_value": "43,674",
                "unrealized_gain_or_lose": "3,376",
                "realized_gain_or_lose": "3,376",
                "IRR_since_interception": "18.54",
                "IRR_FYTD": "14.8"
            },
            {
                "scheme_name": "SBI Bluechip Fund - Direct Plan",
                "folio_no": "3874932749",
                "date_of_investment": "03-07-18",
                "Invested_amout": "35,456",
                "devident_or_received": "0",
                "number_of_units": "315.8",
                "last_updated_NAV": "130.4",
                "current_market_value": "41,219",
                "unrealized_gain_or_lose": "5,763",
                "realized_gain_or_lose": "5,763",
                "IRR_since_interception": "22.46",
                "IRR_FYTD": "12.0"
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
                "scheme_name": "Franklin India Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "03-05-18",
                "invested_amount": "40,000",
                "dividends_received": "500.3",
                "no_of_units": "400.2",
                "last_updated_nav": "110.7",
                "current_market_value": "44,235",
                "unrealized_gain_loss": "4,235",
                "realized_gain_loss": "4,235",
                "irr_since_inception": "20.4",
                "irr_fytd": "12.3"
            },
            {
                "scheme_name": "HDFC Asset Allocation Fund",
                "folio_no": "3874932749",
                "date_of_investment": "22-08-19",
                "invested_amount": "22,000",
                "dividends_received": "50.8",
                "no_of_units": "301.1",
                "last_updated_nav": "112.0",
                "current_market_value": "33,740",
                "unrealized_gain_loss": "11,740",
                "realized_gain_loss": "9,950",
                "irr_since_inception": "18.7",
                "irr_fytd": "7.9"
            },
            {
                "scheme_name": "ICICI Pru Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "12-03-19",
                "invested_amount": "50,342",
                "dividends_received": "230.9",
                "no_of_units": "460.8",
                "last_updated_nav": "120.4",
                "current_market_value": "55,432",
                "unrealized_gain_loss": "5,090",
                "realized_gain_loss": "5,090",
                "irr_since_inception": "22.4",
                "irr_fytd": "9.2"
            },
            {
                "scheme_name": "DSP Multi Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "28-07-18",
                "invested_amount": "35,800",
                "dividends_received": "800.5",
                "no_of_units": "432.6",
                "last_updated_nav": "106.3",
                "current_market_value": "45,900",
                "unrealized_gain_loss": "10,100",
                "realized_gain_loss": "7,500",
                "irr_since_inception": "25.6",
                "irr_fytd": "13.8"
            },
            {
                "scheme_name": "Axis Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "02-11-17",
                "invested_amount": "28,675",
                "dividends_received": "110.2",
                "no_of_units": "385.7",
                "last_updated_nav": "109.8",
                "current_market_value": "42,242",
                "unrealized_gain_loss": "13,567",
                "realized_gain_loss": "13,567",
                "irr_since_inception": "23.7",
                "irr_fytd": "15.5"
            },
            {
                "scheme_name": "L&T Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "14-06-18",
                "invested_amount": "38,900",
                "dividends_received": "400.1",
                "no_of_units": "490.2",
                "last_updated_nav": "115.2",
                "current_market_value": "56,537",
                "unrealized_gain_loss": "17,637",
                "realized_gain_loss": "15,500",
                "irr_since_inception": "26.4",
                "irr_fytd": "20.8"
            },
            {
                "scheme_name": "Franklin India Equity Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "06-10-19",
                "invested_amount": "41,210",
                "dividends_received": "120.7",
                "no_of_units": "459.8",
                "last_updated_nav": "111.4",
                "current_market_value": "50,800",
                "unrealized_gain_loss": "9,590",
                "realized_gain_loss": "9,590",
                "irr_since_inception": "22.0",
                "irr_fytd": "17.4"
            },
            {
                "scheme_name": "ICICI Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "03-03-20",
                "invested_amount": "34,215",
                "dividends_received": "80.3",
                "no_of_units": "410.9",
                "last_updated_nav": "118.7",
                "current_market_value": "48,800",
                "unrealized_gain_loss": "14,585",
                "realized_gain_loss": "12,410",
                "irr_since_inception": "28.7",
                "irr_fytd": "13.2"
            },
            {
                "scheme_name": "SBI Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "29-01-20",
                "invested_amount": "26,000",
                "dividends_received": "95.6",
                "no_of_units": "400.1",
                "last_updated_nav": "116.3",
                "current_market_value": "45,492",
                "unrealized_gain_loss": "19,492",
                "realized_gain_loss": "16,500",
                "irr_since_inception": "25.5",
                "irr_fytd": "18.6"
            },
            {
                "scheme_name": "Mirae Asset Multi-Asset Fund",
                "folio_no": "3874932749",
                "date_of_investment": "15-08-18",
                "invested_amount": "27,850",
                "dividends_received": "134.5",
                "no_of_units": "380.5",
                "last_updated_nav": "103.2",
                "current_market_value": "39,350",
                "unrealized_gain_loss": "11,500",
                "realized_gain_loss": "9,740",
                "irr_since_inception": "21.3",
                "irr_fytd": "10.9"
            },
            {
                "scheme_name": "Total",
                "folio_no": "3874932749",
                "date_of_investment": "15-11-20",
                "invested_amount": "30,492",
                "dividends_received": "120.5",
                "no_of_units": "456.7",
                "last_updated_nav": "115.2",
                "current_market_value": "52,500",
                "unrealized_gain_loss": "22,178",
                "realized_gain_loss": "8,320",
                "irr_since_inception": "24.11",
                "irr_fytd": "19.8"
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
        },
        {
            "particular": "Aditya Birla Multi-Asset Fund",
            "reference_no": "4579821",
            "investment_date": "2021-10-19",
            "investment_amount": "1234567",
            "valuation_date": "2022-04-30",
            "current_value": "1456789",
            "unrealized_gain_loss": "222222",
            "amount_or_capital_redeemed": "0",
            "XIRR": "15.4"
        },
        {
            "particular": "DSP Multi-Asset Fund",
            "reference_no": "4928631",
            "investment_date": "2021-12-05",
            "investment_amount": "876543",
            "valuation_date": "2022-03-30",
            "current_value": "1023456",
            "unrealized_gain_loss": "146913",
            "amount_or_capital_redeemed": "0",
            "XIRR": "18.7"
        },
        {
            "particular": "ICICI Prudential Equity Fund",
            "reference_no": "9328742",
            "investment_date": "2020-09-15",
            "investment_amount": "3245600",
            "valuation_date": "2022-02-25",
            "current_value": "4678900",
            "unrealized_gain_loss": "1433300",
            "amount_or_capital_redeemed": "0",
            "XIRR": "22.6"
        },
        {
            "particular": "Mirae Asset Multi-Asset Fund",
            "reference_no": "8742356",
            "investment_date": "2021-11-22",
            "investment_amount": "982134",
            "valuation_date": "2022-04-20",
            "current_value": "1122567",
            "unrealized_gain_loss": "140433",
            "amount_or_capital_redeemed": "0",
            "XIRR": "17.3"
        },
        {
            "particular": "Franklin India Balanced Fund",
            "reference_no": "2348756",
            "investment_date": "2020-11-09",
            "investment_amount": "2896543",
            "valuation_date": "2022-05-30",
            "current_value": "3587654",
            "unrealized_gain_loss": "691111",
            "amount_or_capital_redeemed": "0",
            "XIRR": "24.2"
        },
        {
            "particular": "HDFC Multi-Cap Fund",
            "reference_no": "9827456",
            "investment_date": "2021-03-16",
            "investment_amount": "5689321",
            "valuation_date": "2022-02-10",
            "current_value": "6845200",
            "unrealized_gain_loss": "1155879",
            "amount_or_capital_redeemed": "0",
            "XIRR": "19.5"
        },
        {
            "particular": "Kotak Multi-Asset Fund",
            "reference_no": "2345639",
            "investment_date": "2020-06-30",
            "investment_amount": "4567890",
            "valuation_date": "2022-01-20",
            "current_value": "5634789",
            "unrealized_gain_loss": "1066899",
            "amount_or_capital_redeemed": "0",
            "XIRR": "21.0"
        },
        {
            "particular": "Axis Growth Equity Fund",
            "reference_no": "7568932",
            "investment_date": "2020-08-12",
            "investment_amount": "3145678",
            "valuation_date": "2022-03-15",
            "current_value": "3752432",
            "unrealized_gain_loss": "607754",
            "amount_or_capital_redeemed": "0",
            "XIRR": "16.8"
        },
        {
            "particular": "SBI Bluechip Fund",
            "reference_no": "9876543",
            "investment_date": "2019-11-09",
            "investment_amount": "4123456",
            "valuation_date": "2022-04-15",
            "current_value": "4857623",
            "unrealized_gain_loss": "734167",
            "amount_or_capital_redeemed": "0",
            "XIRR": "23.3"
        },
        {
            "particular": "L&T Multi-Asset Fund",
            "reference_no": "2349817",
            "investment_date": "2021-09-18",
            "investment_amount": "2145689",
            "valuation_date": "2022-02-10",
            "current_value": "2465678",
            "unrealized_gain_loss": "320989",
            "amount_or_capital_redeemed": "0",
            "XIRR": "20.7"
        },
        {
            "particular": "Bajaj Finserv Multi-Cap Fund",
            "reference_no": "4872641",
            "investment_date": "2021-04-08",
            "investment_amount": "3578901",
            "valuation_date": "2022-03-22",
            "current_value": "4067382",
            "unrealized_gain_loss": "488481",
            "amount_or_capital_redeemed": "0",
            "XIRR": "25.1"
        }
    ],
    "ninth_page_data": {
        "summary": [
            {
                "instument_name": "Abakkus Emerging Opportunities Fund 1A1",
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
                "instument_name": "ICICI Pru CompAct Fund Series 2",
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
                "instument_name": "HDFC Equity Growth Fund",
                "fund_name": "HDFC Equity Fund",
                "reference_no": "100347567",
                "investment_date": "12-Mar-20",
                "investment_amount": "2456789",
                "return_of_capital": "0",
                "valuation_date": "15-Mar-22",
                "current_value": "3123456",
                "unrealized_gain_loss": "666667",
                "realized_gain_loss": "0",
                "xirr": "21.3"
            },
            {
                "instument_name": "Axis Long-Term Equity Fund",
                "fund_name": "Axis Growth Fund",
                "reference_no": "100542890",
                "investment_date": "10-Jan-20",
                "investment_amount": "3456721",
                "return_of_capital": "0",
                "valuation_date": "01-Feb-22",
                "current_value": "4321987",
                "unrealized_gain_loss": "865266",
                "realized_gain_loss": "0",
                "xirr": "18.5"
            },
            {
                "instument_name": "ICICI Pru Balanced Fund",
                "fund_name": "ICICI Pru Balanced Fund",
                "reference_no": "100672981",
                "investment_date": "05-Oct-20",
                "investment_amount": "5245678",
                "return_of_capital": "0",
                "valuation_date": "22-Mar-22",
                "current_value": "6212345",
                "unrealized_gain_loss": "967667",
                "realized_gain_loss": "0",
                "xirr": "20.1"
            },
            {
                "instument_name": "Mirae Asset Emerging Bluechip Fund",
                "fund_name": "Mirae Asset Fund",
                "reference_no": "100372654",
                "investment_date": "15-Feb-19",
                "investment_amount": "3249875",
                "return_of_capital": "0",
                "valuation_date": "28-Apr-22",
                "current_value": "4236750",
                "unrealized_gain_loss": "986875",
                "realized_gain_loss": "0",
                "xirr": "22.3"
            },
            {
                "instument_name": "Franklin India Equity Fund",
                "fund_name": "Franklin Templeton Fund",
                "reference_no": "100998745",
                "investment_date": "10-Jun-18",
                "investment_amount": "4567890",
                "return_of_capital": "0",
                "valuation_date": "05-May-22",
                "current_value": "5123456",
                "unrealized_gain_loss": "555566",
                "realized_gain_loss": "0",
                "xirr": "19.9"
            },
            {
                "instument_name": "DSP Top 100 Equity Fund",
                "fund_name": "DSP Mutual Fund",
                "reference_no": "101234789",
                "investment_date": "12-Aug-19",
                "investment_amount": "6789102",
                "return_of_capital": "0",
                "valuation_date": "18-Jan-22",
                "current_value": "7323450",
                "unrealized_gain_loss": "534348",
                "realized_gain_loss": "0",
                "xirr": "16.4"
            },
            {
                "instument_name": "Kotak Standard Multicap Fund",
                "fund_name": "Kotak Fund",
                "reference_no": "100567892",
                "investment_date": "30-Sep-20",
                "investment_amount": "1234567",
                "return_of_capital": "0",
                "valuation_date": "23-Apr-22",
                "current_value": "1578900",
                "unrealized_gain_loss": "344333",
                "realized_gain_loss": "0",
                "xirr": "14.7"
            },
            {
                "instument_name": "SBI Bluechip Fund",
                "fund_name": "SBI Mutual Fund",
                "reference_no": "100876531",
                "investment_date": "18-May-18",
                "investment_amount": "3987654",
                "return_of_capital": "0",
                "valuation_date": "02-Dec-21",
                "current_value": "4598765",
                "unrealized_gain_loss": "611111",
                "realized_gain_loss": "0",
                "xirr": "21.2"
            },
            {
                "instument_name": "L&T Multicap Fund",
                "fund_name": "L&T Growth Fund",
                "reference_no": "100123456",
                "investment_date": "15-Mar-19",
                "investment_amount": "2547893",
                "return_of_capital": "0",
                "valuation_date": "12-Jan-22",
                "current_value": "3245678",
                "unrealized_gain_loss": "698785",
                "realized_gain_loss": "0",
                "xirr": "20.6"
            },
            {
                "instument_name": "Mirae Asset Multicap Fund",
                "fund_name": "Mirae Asset Fund",
                "reference_no": "100998123",
                "investment_date": "07-Sep-19",
                "investment_amount": "2765432",
                "return_of_capital": "0",
                "valuation_date": "16-Feb-22",
                "current_value": "3287654",
                "unrealized_gain_loss": "522222",
                "realized_gain_loss": "0",
                "xirr": "17.3"
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
        },
        {
            "stock_name": "INFOSYS LTD",
            "date": "26-jan-2024",
            "ISIN": "INFY12345",
            "no_of_units": "32.5",
            "market_price_per_share": "1800",
            "current_market_value": "58500"
        },
        {
            "stock_name": "RELIANCE INDUSTRIES LTD",
            "date": "26-jan-2024",
            "ISIN": "RELI12345",
            "no_of_units": "50",
            "market_price_per_share": "2600",
            "current_market_value": "130000"
        },
        {
            "stock_name": "TCS LTD",
            "date": "26-jan-2024",
            "ISIN": "TCS12345",
            "no_of_units": "10.0",
            "market_price_per_share": "3500",
            "current_market_value": "35000"
        },
        {
            "stock_name": "HDFC BANK LTD",
            "date": "26-jan-2024",
            "ISIN": "HDFCB123",
            "no_of_units": "15.5",
            "market_price_per_share": "1400",
            "current_market_value": "21700"
        },
        {
            "stock_name": "ASIAN PAINTS LTD",
            "date": "26-jan-2024",
            "ISIN": "ASPN12345",
            "no_of_units": "12.0",
            "market_price_per_share": "3000",
            "current_market_value": "36000"
        },
        {
            "stock_name": "ITC LTD",
            "date": "26-jan-2024",
            "ISIN": "ITC12345",
            "no_of_units": "8.0",
            "market_price_per_share": "250",
            "current_market_value": "2000"
        },
        {
            "stock_name": "HUL LTD",
            "date": "26-jan-2024",
            "ISIN": "HUL12345",
            "no_of_units": "9.0",
            "market_price_per_share": "2300",
            "current_market_value": "20700"
        },
        {
            "stock_name": "MUTHOOT FINANCE LTD",
            "date": "26-jan-2024",
            "ISIN": "MUT12345",
            "no_of_units": "30.0",
            "market_price_per_share": "1200",
            "current_market_value": "36000"
        },
        {
            "stock_name": "MAHINDRA & MAHINDRA LTD",
            "date": "26-jan-2024",
            "ISIN": "M&M12345",
            "no_of_units": "18.0",
            "market_price_per_share": "850",
            "current_market_value": "15300"
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
            "fund_name": "HDFC Gold ETF",
            "asset_class": "267833",
            "ISIN": "HDFCGETF123",
            "reference_no": "654123",
            "no_of_units": "25",
            "market_price_per_share": "4850",
            "investment_amont": "121250"
        },
        {
            "fund_name": "SBI Bluechip Fund",
            "asset_class": "267834",
            "ISIN": "SBI12345",
            "reference_no": "236567",
            "no_of_units": "18",
            "market_price_per_share": "1300",
            "investment_amont": "23400"
        },
        {
            "fund_name": "ICICI Prudential Equity Fund",
            "asset_class": "267835",
            "ISIN": "ICICI12345",
            "reference_no": "2365678",
            "no_of_units": "32",
            "market_price_per_share": "1900",
            "investment_amont": "60800"
        },
        {
            "fund_name": "Mirae Asset Emerging Bluechip Fund",
            "asset_class": "267836",
            "ISIN": "MIRA12345",
            "reference_no": "23456789",
            "no_of_units": "50",
            "market_price_per_share": "3600",
            "investment_amont": "180000"
        },
        {
            "fund_name": "Franklin India Growth Fund",
            "asset_class": "267837",
            "ISIN": "FRANK12345",
            "reference_no": "97823456",
            "no_of_units": "100",
            "market_price_per_share": "2750",
            "investment_amont": "275000"
        },
        {
            "fund_name": "Aditya Birla Sun Life Balanced Fund",
            "asset_class": "267838",
            "ISIN": "ABSL12345",
            "reference_no": "36789234",
            "no_of_units": "15",
            "market_price_per_share": "2200",
            "investment_amont": "33000"
        },
        {
            "fund_name": "HDFC Mutual Fund",
            "asset_class": "267839",
            "ISIN": "HDFC123456",
            "reference_no": "54367289",
            "no_of_units": "40",
            "market_price_per_share": "1450",
            "investment_amont": "58000"
        },
        {
            "fund_name": "Reliance Multi-Cap Fund",
            "asset_class": "267840",
            "ISIN": "RELI12345",
            "reference_no": "67543829",
            "no_of_units": "70",
            "market_price_per_share": "2300",
            "investment_amont": "161000"
        },
        {
            "fund_name": "Kotak Standard Multicap Fund",
            "asset_class": "267841",
            "ISIN": "KOTAK12345",
            "reference_no": "12398765",
            "no_of_units": "25",
            "market_price_per_share": "3100",
            "investment_amont": "77500"
        },
        {
            "fund_name": "Tata Balanced Fund",
            "asset_class": "267842",
            "ISIN": "TATA12345",
            "reference_no": "32487632",
            "no_of_units": "60",
            "market_price_per_share": "1200",
            "investment_amont": "72000"
        },
        {
            "fund_name": "ICICI Prudential Multi-Asset Fund",
            "asset_class": "267843",
            "ISIN": "ICICI1234567",
            "reference_no": "98765432",
            "no_of_units": "20",
            "market_price_per_share": "2150",
            "investment_amont": "43000"
        },
        {
            "fund_name": "Muthoot Finance Gold Fund",
            "asset_class": "267844",
            "ISIN": "MUTH12345",
            "reference_no": "23467890",
            "no_of_units": "35",
            "market_price_per_share": "5500",
            "investment_amont": "192500"
        },
        {
            "fund_name": "Axis Equity Fund",
            "asset_class": "267845",
            "ISIN": "AXIS12345",
            "reference_no": "78965432",
            "no_of_units": "45",
            "market_price_per_share": "2050",
            "investment_amont": "92250"
        },
        {
            "fund_name": "SBI Small Cap Fund",
            "asset_class": "267846",
            "ISIN": "SBI1234567",
            "reference_no": "87654321",
            "no_of_units": "20",
            "market_price_per_share": "2100",
            "investment_amont": "42000"
        },
        {
            "fund_name": "Total",
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
                "policy_name": "Housing LaaIICICI PRU SARAL PENSION",
                "policy_type": "ULIP",
                "premimum_due_date": "30-Jun-25",
                "policy_no": "LT123456",
                "premium_account": "24,000",
                "sum_assured": "10,00,000",
                "valuation": "12,50,000"
            },
            {
                "policy_name": "ICICI Pru-Signature - UW#",
                "policy_type": "Traditional",
                "premimum_due_date": "15-Jul-25",
                "policy_no": "SP987654",
                "premium_account": "18,000",
                "sum_assured": "8,00,000",
                "valuation": "9,20,000"
            },
            {
                "policy_name": "Bajaj Allianz Life Smart Protect",
                "policy_type": "ULIP",
                "premimum_due_date": "01-Jan-25",
                "policy_no": "BAL123456",
                "premium_account": "20,000",
                "sum_assured": "9,00,000",
                "valuation": "10,50,000"
            },
            {
                "policy_name": "SBI Life Smart Shield",
                "policy_type": "Traditional",
                "premimum_due_date": "15-Mar-25",
                "policy_no": "SBI123456",
                "premium_account": "18,000",
                "sum_assured": "6,50,000",
                "valuation": "7,50,000"
            },
            {
                "policy_name": "Kotak Life Secure",
                "policy_type": "Traditional",
                "premimum_due_date": "20-May-25",
                "policy_no": "KOTAK12345",
                "premium_account": "22,500",
                "sum_assured": "11,00,000",
                "valuation": "13,00,000"
            },
            {
                "policy_name": "Max Life Online Term Plan",
                "policy_type": "Traditional",
                "premimum_due_date": "25-Jul-25",
                "policy_no": "MAXL12345",
                "premium_account": "12,000",
                "sum_assured": "5,00,000",
                "valuation": "5,50,000"
            },
            {
                "policy_name": "HDFC Life Click2Protect",
                "policy_type": "ULIP",
                "premimum_due_date": "05-Aug-25",
                "policy_no": "HDFC234567",
                "premium_account": "25,000",
                "sum_assured": "12,00,000",
                "valuation": "14,00,000"
            },
            {
                "policy_name": "LIC Jeevan Anand",
                "policy_type": "Traditional",
                "premimum_due_date": "10-Sep-25",
                "policy_no": "LIC123456",
                "premium_account": "13,500",
                "sum_assured": "6,50,000",
                "valuation": "7,20,000"
            },
            {
                "policy_name": "Tata AIG Life Insurance",
                "policy_type": "ULIP",
                "premimum_due_date": "30-Oct-25",
                "policy_no": "TATA123456",
                "premium_account": "18,500",
                "sum_assured": "9,50,000",
                "valuation": "11,20,000"
            },
            {
                "policy_name": "Aditya Birla Sun Life Secure",
                "policy_type": "Traditional",
                "premimum_due_date": "15-Nov-25",
                "policy_no": "ABSL12345",
                "premium_account": "19,000",
                "sum_assured": "8,00,000",
                "valuation": "9,10,000"
            },
            {
                "policy_name": "ICICI Pru Life Protection Plus",
                "policy_type": "ULIP",
                "premimum_due_date": "20-Dec-25",
                "policy_no": "ICICI54321",
                "premium_account": "24,500",
                "sum_assured": "10,00,000",
                "valuation": "12,30,000"
            },
            {
                "policy_name": "Reliance Life Insurance",
                "policy_type": "Traditional",
                "premimum_due_date": "18-Jan-25",
                "policy_no": "RELI12345",
                "premium_account": "20,000",
                "sum_assured": "9,00,000",
                "valuation": "10,00,000"
            },
            {
                "policy_name": "Birla Sun Life Smart Protection",
                "policy_type": "ULIP",
                "premimum_due_date": "28-Feb-25",
                "policy_no": "BSL123456",
                "premium_account": "22,000",
                "sum_assured": "11,00,000",
                "valuation": "13,00,000"
            },
            {
                "policy_name": "Bajaj Allianz Life Term Plan",
                "policy_type": "Traditional",
                "premimum_due_date": "05-Mar-25",
                "policy_no": "BAL567890",
                "premium_account": "19,000",
                "sum_assured": "8,50,000",
                "valuation": "9,80,000"
            },
            {
                "policy_name": "SBI Life Saral Pension",
                "policy_type": "ULIP",
                "premimum_due_date": "25-Apr-25",
                "policy_no": "SBI234567",
                "premium_account": "23,500",
                "sum_assured": "10,50,000",
                "valuation": "12,60,000"
            },
            {
                "policy_name": "Tata AIG Life Term Plan",
                "policy_type": "Traditional",
                "premimum_due_date": "10-May-25",
                "policy_no": "TATA123678",
                "premium_account": "15,000",
                "sum_assured": "7,00,000",
                "valuation": "7,80,000"
            },
            {
                "policy_name": "Kotak Life Gold Plan",
                "policy_type": "ULIP",
                "premimum_due_date": "12-Jun-25",
                "policy_no": "KOTAK54321",
                "premium_account": "17,000",
                "sum_assured": "8,50,000",
                "valuation": "9,70,000"
            }
        ]
    },
    "thirteenth_page_data": [
        {
            "account_holder_name": "RAHUL MEHTA",
            "balance_as_on": "12,45,300",
            "account_number": "345388888259",
            "account_type": "current",
            "balance": "5,000"
        },
        {
            "account_holder_name": "PRIYA SHARMA",
            "balance_as_on": "5,67,890",
            "account_number": "345388888260",
            "account_type": "savings",
            "balance": "2,000"
        },
        {
            "account_holder_name": "AMIT KUMAR",
            "balance_as_on": "9,12,430",
            "account_number": "345388888261",
            "account_type": "current",
            "balance": "8,000"
        },
        {
            "account_holder_name": "NEHA VERMA",
            "balance_as_on": "1,23,456",
            "account_number": "345388888262",
            "account_type": "savings",
            "balance": "1,000"
        },
        {
            "account_holder_name": "VIKAS YADAV",
            "balance_as_on": "10,00,000",
            "account_number": "345388888263",
            "account_type": "current",
            "balance": "9,000"
        },
        {
            "account_holder_name": "DIVYA NAIK",
            "balance_as_on": "1,11,111",
            "account_number": "345388888272",
            "account_type": "savings",
            "balance": "900"
        },
        {
            "account_holder_name": "AMIT KUMAR",
            "balance_as_on": "3,21,500",
            "account_number": "345388888301",
            "account_type": "savings",
            "balance": "4,000"
        },
        {
            "account_holder_name": "NEHA VERMA",
            "balance_as_on": "4,50,000",
            "account_number": "345388888302",
            "account_type": "current",
            "balance": "7,500"
        },
        {
            "account_holder_name": "RAHUL MEHTA",
            "balance_as_on": "6,78,900",
            "account_number": "345388888303",
            "account_type": "savings",
            "balance": "3,200"
        },
        {
            "account_holder_name": "DIVYA NAIK",
            "balance_as_on": "2,22,222",
            "account_number": "345388888304",
            "account_type": "current",
            "balance": "1,100"
        }
    ],
    "fourteenth_page_data": {
        "credit_cards": [
            {
                "card_type": "Mastercard Gold",
                "payment_due_date": "15-Feb-24",
                "credit_card_number": "5100123412341234",
                "credit_limit": "1,20,000",
                "cash_limit": "25,000",
                "available_credit_limit": "85,000",
                "minimum_amount_due": "3,000",
                "total_amount_due": "12,000"
            },
            {
                "card_type": "Visa Platinum",
                "payment_due_date": "10-Mar-24",
                "credit_card_number": "4111111111111111",
                "credit_limit": "2,00,000",
                "cash_limit": "40,000",
                "available_credit_limit": "1,50,000",
                "minimum_amount_due": "5,000",
                "total_amount_due": "20,000"
            },
            {
                "card_type": "Mastercard World Elite",
                "payment_due_date": "01-Mar-24",
                "credit_card_number": "5200555566667777",
                "credit_limit": "3,00,000",
                "cash_limit": "50,000",
                "available_credit_limit": "2,40,000",
                "minimum_amount_due": "10,000",
                "total_amount_due": "40,000"
            },
            {
                "card_type": "American Express Gold",
                "payment_due_date": "07-Mar-24",
                "credit_card_number": "378282246310005",
                "credit_limit": "2,50,000",
                "cash_limit": "0",
                "available_credit_limit": "2,00,000",
                "minimum_amount_due": "7,500",
                "total_amount_due": "30,000"
            },
            {
                "card_type": "Amazon Pay ICICI Bank Credit Card",
                "payment_due_date": "12-Mar-24",
                "credit_card_number": "0050500652452",
                "credit_limit": "1,50,000",
                "cash_limit": "0",
                "available_credit_limit": "1,10,000",
                "minimum_amount_due": "3,500",
                "total_amount_due": "13,000"
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
                "loan_type": "Home Loan",
                "loan_account": "LBMU345388888258",
                "loan_amount": "25,00,000",
                "tenure": "240",
                "maturity": "15-Dec-35",
                "outstanding": "18,75,000",
                "EMI": "18,900",
                "composition": "14,000 Principal + 4,900 Interest"
            },
            {
                "loan_type": "Personal Loan",
                "loan_account": "PLMU456789123456",
                "loan_amount": "3,00,000",
                "tenure": "60",
                "maturity": "10-Jan-27",
                "outstanding": "1,95,000",
                "EMI": "6,800",
                "composition": "5,500 Principal + 1,300 Interest"
            },
            {
                "loan_type": "Car Loan",
                "loan_account": "CLMU123456789012",
                "loan_amount": "7,50,000",
                "tenure": "84",
                "maturity": "01-Aug-31",
                "outstanding": "5,60,000",
                "EMI": "10,500",
                "composition": "8,200 Principal + 2,300 Interest"
            },
            {
                "loan_type": "Home Loan",
                "loan_account": "HLAC654321987654",
                "loan_amount": "40,00,000",
                "tenure": "300",
                "maturity": "20-Oct-44",
                "outstanding": "36,80,000",
                "EMI": "29,000",
                "composition": "21,500 Principal + 7,500 Interest"
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
            "name": "NEHA VERMA",
            "risk_profile": "Conservative",
            "current_value": "1547527",
            "investment_value": "1300760",
            "weightage": "100",
            "total_gain_loss": "246767",
            "current_asset_allocation": {
                "debt": "70",
                "equity": "20",
                "others": "10"
            },
            "target_asset_allocation": {
                "debt": "70",
                "equity": "20",
                "others": "10"
            }
        },
        {
            "name": "RAHUL MEHTA",
            "risk_profile": "Aggressive",
            "current_value": "809369",
            "investment_value": "625517",
            "weightage": "100",
            "total_gain_loss": "183852",
            "current_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            },
            "target_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            }
        },
        {
            "name": "DIVYA NAIK",
            "risk_profile": "Conservative",
            "current_value": "673443",
            "investment_value": "759308",
            "weightage": "100",
            "total_gain_loss": "-85865",
            "current_asset_allocation": {
                "debt": "70",
                "equity": "20",
                "others": "10"
            },
            "target_asset_allocation": {
                "debt": "70",
                "equity": "20",
                "others": "10"
            }
        },
        {
            "name": "AMIT KUMAR",
            "risk_profile": "Aggressive",
            "current_value": "1336971",
            "investment_value": "917695",
            "weightage": "100",
            "total_gain_loss": "419276",
            "current_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            },
            "target_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            }
        },
        {
            "name": "PRIYA SHARMA",
            "risk_profile": "Aggressive",
            "current_value": "1761388",
            "investment_value": "1647080",
            "weightage": "100",
            "total_gain_loss": "114308",
            "current_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            },
            "target_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            }
        },
        {
            "name": "VIKAS YADAV",
            "risk_profile": "Aggressive",
            "current_value": "1343101",
            "investment_value": "1534649",
            "weightage": "100",
            "total_gain_loss": "-191548",
            "current_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
            },
            "target_asset_allocation": {
                "debt": "10",
                "equity": "70",
                "others": "20"
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
                        "particulars": "Debt Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Debts AIF",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Corporate Bonds",
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
                        "particulars": "Equity Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Equity AIF",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Listed Stocks",
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
                        "particulars": "Hybrid Mutual Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Balanced Funds",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Dynamic Asset Allocation",
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
                "category": "Other Alternatives",
                "holdings_cost": "4999950",
                "current_value": "9449950",
                "holdings": "9449950",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "0",
                "gain_or_lose_unrealized": "0",
                "irr_since_interception": "439953",
                "subcategories": [
                    {
                        "particulars": "Fixed Deposits",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "Structured Products",
                        "holdings_cost": "4999950",
                        "current_value": "9449950",
                        "holdings": "9449950",
                        "gain_or_lose_realized": "0",
                        "devident_or_interest": "0",
                        "gain_or_lose_unrealized": "0",
                        "irr_since_interception": "439953"
                    },
                    {
                        "particulars": "REITs",
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
                    }
                ]
            }
        ]
    },
    "twenteeth_page_data": {
        "debt_analysis_response": [
            {
                "particulars": "Debt Mutual Funds - WMS",
                "holdings_cost": "1000000.0",
                "current_value": "1050000.0",
                "holdings": "10.0",
                "gain_or_lose_realized": "50000.0",
                "devident_or_interest": "30000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "7.5"
            },
            {
                "particulars": "Debt AF - WMS",
                "holdings_cost": "500000",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            },
            {
                "particulars": "Debt Corporate Bonds",
                "holdings_cost": "2000000.0",
                "current_value": "2100000.0",
                "holdings": "20.0",
                "gain_or_lose_realized": "80000.0",
                "devident_or_interest": "45000.0",
                "gain_or_lose_unrealized": "50000.0",
                "irr": "7.8"
            },
            {
                "particulars": "Debt Government Securities",
                "holdings_cost": "1500000.0",
                "current_value": "1550000.0",
                "holdings": "15.0",
                "gain_or_lose_realized": "30000.0",
                "devident_or_interest": "20000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "6.5"
            },
            {
                "particulars": "Debt Fixed Deposits",
                "holdings_cost": "750000.0",
                "current_value": "780000.0",
                "holdings": "7.5",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "25000.0",
                "gain_or_lose_unrealized": "10000.0",
                "irr": "6.8"
            },
            {
                "particulars": "Debt Liquid Funds",
                "holdings_cost": "600000.0",
                "current_value": "610000.0",
                "holdings": "6.0",
                "gain_or_lose_realized": "5000.0",
                "devident_or_interest": "12000.0",
                "gain_or_lose_unrealized": "4000.0",
                "irr": "5.9"
            },
            {
                "particulars": "Debt Short Term Funds",
                "holdings_cost": "850000.0",
                "current_value": "880000.0",
                "holdings": "8.5",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "16000.0",
                "gain_or_lose_unrealized": "14000.0",
                "irr": "7.0"
            },
            {
                "particulars": "Debt Ultra Short Term Funds",
                "holdings_cost": "300000.0",
                "current_value": "310000.0",
                "holdings": "3.0",
                "gain_or_lose_realized": "3000.0",
                "devident_or_interest": "7000.0",
                "gain_or_lose_unrealized": "4000.0",
                "irr": "6.3"
            },
            {
                "particulars": "Debt Money Market Funds",
                "holdings_cost": "450000.0",
                "current_value": "460000.0",
                "holdings": "4.5",
                "gain_or_lose_realized": "4000.0",
                "devident_or_interest": "9000.0",
                "gain_or_lose_unrealized": "3000.0",
                "irr": "6.1"
            },
            {
                "particulars": "Debt Bank Fixed Deposits",
                "holdings_cost": "1200000.0",
                "current_value": "1230000.0",
                "holdings": "12.0",
                "gain_or_lose_realized": "20000.0",
                "devident_or_interest": "35000.0",
                "gain_or_lose_unrealized": "10000.0",
                "irr": "7.2"
            },
            {
                "particulars": "Debt PSU Bonds",
                "holdings_cost": "900000.0",
                "current_value": "930000.0",
                "holdings": "9.0",
                "gain_or_lose_realized": "12000.0",
                "devident_or_interest": "22000.0",
                "gain_or_lose_unrealized": "10000.0",
                "irr": "6.7"
            },
            {
                "particulars": "Debt Tax Saving Bonds",
                "holdings_cost": "400000.0",
                "current_value": "420000.0",
                "holdings": "4.0",
                "gain_or_lose_realized": "8000.0",
                "devident_or_interest": "11000.0",
                "gain_or_lose_unrealized": "3000.0",
                "irr": "6.9"
            },
            {
                "particulars": "Debt Infrastructure Bonds",
                "holdings_cost": "550000.0",
                "current_value": "580000.0",
                "holdings": "5.5",
                "gain_or_lose_realized": "9000.0",
                "devident_or_interest": "13000.0",
                "gain_or_lose_unrealized": "2000.0",
                "irr": "7.1"
            },
            {
                "particulars": "Debt Municipal Bonds",
                "holdings_cost": "650000.0",
                "current_value": "670000.0",
                "holdings": "6.5",
                "gain_or_lose_realized": "7000.0",
                "devident_or_interest": "14000.0",
                "gain_or_lose_unrealized": "1000.0",
                "irr": "6.4"
            },
            {
                "particulars": "Debt Corporate Fixed Deposits",
                "holdings_cost": "800000.0",
                "current_value": "830000.0",
                "holdings": "8.0",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "18000.0",
                "gain_or_lose_unrealized": "2000.0",
                "irr": "7.3"
            },
            {
                "particulars": "Debt National Savings Certificates",
                "holdings_cost": "350000.0",
                "current_value": "365000.0",
                "holdings": "3.5",
                "gain_or_lose_realized": "4000.0",
                "devident_or_interest": "9000.0",
                "gain_or_lose_unrealized": "1500.0",
                "irr": "6.2"
            },
            {
                "particulars": "Total",
                "holdings_cost": "500000",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            }
        ]
    },
    "twentyone_page_data": {
        "debt_mutual_fund_allocation_response": [
            {
                "mutual_fund": "Banking and PSU",
                "holdings_cost": "7,15,780",
                "current_value": "11,79,579",
                "holdings": "100",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.31",
                "gain_or_lose_unrealized": "4,55,332",
                "xirr": "55.3"
            },
            {
                "mutual_fund": "Corporate Bond",
                "holdings_cost": "11,79,579",
                "current_value": "7,15,780",
                "holdings": "61,739",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.55",
                "gain_or_lose_unrealized": "61,739",
                "xirr": "3.2"
            },
            {
                "mutual_fund": "Equity Large Cap",
                "holdings_cost": "9,00,000",
                "current_value": "12,50,000",
                "holdings": "150",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "2.75",
                "gain_or_lose_unrealized": "3,50,000",
                "xirr": "12.4"
            },
            {
                "mutual_fund": "Debt Short Term",
                "holdings_cost": "5,50,000",
                "current_value": "5,80,000",
                "holdings": "75",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "1.95",
                "gain_or_lose_unrealized": "30,000",
                "xirr": "6.8"
            }
        ],
        "debt_mutual_fund_pie_chart": {
            "labels": [
                "Banking and PSU",
                "Corporate Bond",
                "Equity Large Cap"
            ],
            "values": [
                "1179579",
                "715780",
                "8736482"
            ],
            "colors": []
        }
    },
    "twentytwo_page_data": {
        "hybrid_analysis_response": [
            {
                "particulars": "Equity Mutual Funds - WMS",
                "holdings_cost": "1000000.0",
                "current_value": "1050000.0",
                "holdings": "10.0",
                "gain_or_lose_realized": "50000.0",
                "devident_or_interest": "30000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "7.5"
            },
            {
                "particulars": "Equity AIF - WMS",
                "holdings_cost": "500000.0",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            },
            {
                "particulars": "Equity Large Cap Funds",
                "holdings_cost": "1200000.0",
                "current_value": "1300000.0",
                "holdings": "12.0",
                "gain_or_lose_realized": "40000.0",
                "devident_or_interest": "25000.0",
                "gain_or_lose_unrealized": "30000.0",
                "irr": "8.0"
            },
            {
                "particulars": "Equity Mid Cap Funds",
                "holdings_cost": "800000.0",
                "current_value": "850000.0",
                "holdings": "8.0",
                "gain_or_lose_realized": "20000.0",
                "devident_or_interest": "10000.0",
                "gain_or_lose_unrealized": "15000.0",
                "irr": "7.2"
            },
            {
                "particulars": "Equity Small Cap Funds",
                "holdings_cost": "600000.0",
                "current_value": "650000.0",
                "holdings": "6.0",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "8000.0",
                "gain_or_lose_unrealized": "12000.0",
                "irr": "7.0"
            },
            {
                "particulars": "Equity Sector Funds",
                "holdings_cost": "700000.0",
                "current_value": "720000.0",
                "holdings": "7.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "5000.0",
                "gain_or_lose_unrealized": "10000.0",
                "irr": "6.5"
            },
            {
                "particulars": "Equity ELSS Funds",
                "holdings_cost": "900000.0",
                "current_value": "940000.0",
                "holdings": "9.0",
                "gain_or_lose_realized": "18000.0",
                "devident_or_interest": "12000.0",
                "gain_or_lose_unrealized": "16000.0",
                "irr": "7.3"
            },
            {
                "particulars": "Equity Index Funds",
                "holdings_cost": "1100000.0",
                "current_value": "1150000.0",
                "holdings": "11.0",
                "gain_or_lose_realized": "22000.0",
                "devident_or_interest": "13000.0",
                "gain_or_lose_unrealized": "18000.0",
                "irr": "7.8"
            },
            {
                "particulars": "Equity International Funds",
                "holdings_cost": "500000.0",
                "current_value": "540000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "6000.0",
                "gain_or_lose_unrealized": "9000.0",
                "irr": "6.7"
            },
            {
                "particulars": "Equity Thematic Funds",
                "holdings_cost": "400000.0",
                "current_value": "430000.0",
                "holdings": "4.0",
                "gain_or_lose_realized": "8000.0",
                "devident_or_interest": "5000.0",
                "gain_or_lose_unrealized": "7000.0",
                "irr": "6.6"
            },
            {
                "particulars": "Equity Hybrid Funds",
                "holdings_cost": "650000.0",
                "current_value": "680000.0",
                "holdings": "6.5",
                "gain_or_lose_realized": "11000.0",
                "devident_or_interest": "7000.0",
                "gain_or_lose_unrealized": "9000.0",
                "irr": "6.9"
            },
            {
                "particulars": "Equity Arbitrage Funds",
                "holdings_cost": "300000.0",
                "current_value": "310000.0",
                "holdings": "3.0",
                "gain_or_lose_realized": "4000.0",
                "devident_or_interest": "2000.0",
                "gain_or_lose_unrealized": "3000.0",
                "irr": "6.2"
            },
            {
                "particulars": "Equity Multi Cap Funds",
                "holdings_cost": "950000.0",
                "current_value": "1000000.0",
                "holdings": "9.5",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "9000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "7.4"
            },
            {
                "particulars": "Equity Value Funds",
                "holdings_cost": "700000.0",
                "current_value": "730000.0",
                "holdings": "7.0",
                "gain_or_lose_realized": "9000.0",
                "devident_or_interest": "4000.0",
                "gain_or_lose_unrealized": "8000.0",
                "irr": "6.8"
            },
            {
                "particulars": "Equity Growth Funds",
                "holdings_cost": "850000.0",
                "current_value": "900000.0",
                "holdings": "8.5",
                "gain_or_lose_realized": "14000.0",
                "devident_or_interest": "7000.0",
                "gain_or_lose_unrealized": "16000.0",
                "irr": "7.1"
            },
            {
                "particulars": "Equity Sectoral Funds",
                "holdings_cost": "600000.0",
                "current_value": "620000.0",
                "holdings": "6.0",
                "gain_or_lose_realized": "6000.0",
                "devident_or_interest": "3000.0",
                "gain_or_lose_unrealized": "7000.0",
                "irr": "6.3"
            },
            {
                "particulars": "Total",
                "holdings_cost": "500000",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            }
        ],
        "chart_data": {
            "labels": [
                "Stocks",
                "Bonds",
                "Real Estate",
                "Cash",
                "Commodities",
                "Other"
            ],
            "values": [
                10,
                20,
                20,
                5,
                25,
                20
            ]
        }
    },
    "twentythree_page_data": {
        "hybrid_mutual_fund_allocation_response": [
            {
                "mutual_fund": "Large Cap Fund",
                "holdings_cost": "11,79,579",
                "current_value": "7,15,780",
                "holdings": "61,739",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.55",
                "gain_or_lose_unrealized": "61,739",
                "xirr": "3.2"
            },
            {
                "mutual_fund": "Mid Cap Fund",
                "holdings_cost": "9,50,000",
                "current_value": "10,20,000",
                "holdings": "85,000",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "2.80",
                "gain_or_lose_unrealized": "70,000",
                "xirr": "10.5"
            },
            {
                "mutual_fund": "Small Cap Fund",
                "holdings_cost": "5,40,000",
                "current_value": "6,00,000",
                "holdings": "55,000",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "2.50",
                "gain_or_lose_unrealized": "60,000",
                "xirr": "9.8"
            },
            {
                "mutual_fund": "Total",
                "holdings_cost": "11,79,579",
                "current_value": "7,15,780",
                "holdings": "61,739",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.55",
                "gain_or_lose_unrealized": "61,739",
                "xirr": "3.2"
            }
        ],
        "hybrid_mutual_fund_pie_chart": {
            "labels": [
                "Large Cap Fund",
                "Mid Cap Fund",
                "Small Cap Fund"
            ],
            "values": [
                "1179579",
                "715780",
                "320065"
            ],
            "colors": []
        }
    },
    "twentyfour_page_data": {
        "equity_analysis_response": [
            {
                "particulars": "Equity Mutual Funds - WMS",
                "holdings_cost": "1000000.0",
                "current_value": "1050000.0",
                "holdings": "10.0",
                "gain_or_lose_realized": "50000.0",
                "devident_or_interest": "30000.0",
                "gain_or_lose_unrealized": "20000.0",
                "irr": "7.5"
            },
            {
                "particulars": "Equity AIF - WMS",
                "holdings_cost": "500000.0",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            },
            {
                "particulars": "Large Cap Equity Funds",
                "holdings_cost": "1200000.0",
                "current_value": "1250000.0",
                "holdings": "12.0",
                "gain_or_lose_realized": "40000.0",
                "devident_or_interest": "25000.0",
                "gain_or_lose_unrealized": "30000.0",
                "irr": "7.8"
            },
            {
                "particulars": "Mid Cap Equity Funds",
                "holdings_cost": "800000.0",
                "current_value": "860000.0",
                "holdings": "8.0",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "12000.0",
                "gain_or_lose_unrealized": "13000.0",
                "irr": "7.0"
            },
            {
                "particulars": "Small Cap Equity Funds",
                "holdings_cost": "600000.0",
                "current_value": "630000.0",
                "holdings": "6.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "9000.0",
                "gain_or_lose_unrealized": "12000.0",
                "irr": "6.5"
            },
            {
                "particulars": "Sectoral Equity Funds",
                "holdings_cost": "700000.0",
                "current_value": "720000.0",
                "holdings": "7.0",
                "gain_or_lose_realized": "8000.0",
                "devident_or_interest": "7000.0",
                "gain_or_lose_unrealized": "9000.0",
                "irr": "6.3"
            },
            {
                "particulars": "Equity Index Funds",
                "holdings_cost": "1100000.0",
                "current_value": "1150000.0",
                "holdings": "11.0",
                "gain_or_lose_realized": "18000.0",
                "devident_or_interest": "16000.0",
                "gain_or_lose_unrealized": "21000.0",
                "irr": "7.6"
            },
            {
                "particulars": "Equity ELSS Funds",
                "holdings_cost": "900000.0",
                "current_value": "940000.0",
                "holdings": "9.0",
                "gain_or_lose_realized": "15000.0",
                "devident_or_interest": "12000.0",
                "gain_or_lose_unrealized": "19000.0",
                "irr": "7.1"
            },
            {
                "particulars": "International Equity Funds",
                "holdings_cost": "500000.0",
                "current_value": "530000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "9000.0",
                "devident_or_interest": "7000.0",
                "gain_or_lose_unrealized": "8000.0",
                "irr": "6.8"
            },
            {
                "particulars": "Thematic Equity Funds",
                "holdings_cost": "450000.0",
                "current_value": "470000.0",
                "holdings": "4.5",
                "gain_or_lose_realized": "7000.0",
                "devident_or_interest": "6000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.4"
            },
            {
                "particulars": "Hybrid Equity Funds",
                "holdings_cost": "650000.0",
                "current_value": "680000.0",
                "holdings": "6.5",
                "gain_or_lose_realized": "9000.0",
                "devident_or_interest": "8000.0",
                "gain_or_lose_unrealized": "7000.0",
                "irr": "6.9"
            },
            {
                "particulars": "Equity Arbitrage Funds",
                "holdings_cost": "300000.0",
                "current_value": "315000.0",
                "holdings": "3.0",
                "gain_or_lose_realized": "5000.0",
                "devident_or_interest": "3000.0",
                "gain_or_lose_unrealized": "2000.0",
                "irr": "6.1"
            },
            {
                "particulars": "Multi Cap Equity Funds",
                "holdings_cost": "950000.0",
                "current_value": "1000000.0",
                "holdings": "9.5",
                "gain_or_lose_realized": "12000.0",
                "devident_or_interest": "11000.0",
                "gain_or_lose_unrealized": "18000.0",
                "irr": "7.3"
            },
            {
                "particulars": "Value Equity Funds",
                "holdings_cost": "700000.0",
                "current_value": "730000.0",
                "holdings": "7.0",
                "gain_or_lose_realized": "8000.0",
                "devident_or_interest": "6500.0",
                "gain_or_lose_unrealized": "9000.0",
                "irr": "6.7"
            },
            {
                "particulars": "Growth Equity Funds",
                "holdings_cost": "850000.0",
                "current_value": "900000.0",
                "holdings": "8.5",
                "gain_or_lose_realized": "14000.0",
                "devident_or_interest": "11000.0",
                "gain_or_lose_unrealized": "17000.0",
                "irr": "7.2"
            },
            {
                "particulars": "Sectoral Equity Funds",
                "holdings_cost": "600000.0",
                "current_value": "620000.0",
                "holdings": "6.0",
                "gain_or_lose_realized": "6000.0",
                "devident_or_interest": "4000.0",
                "gain_or_lose_unrealized": "7000.0",
                "irr": "6.3"
            },
            {
                "particulars": "Emerging Markets Equity",
                "holdings_cost": "550000.0",
                "current_value": "570000.0",
                "holdings": "5.5",
                "gain_or_lose_realized": "5000.0",
                "devident_or_interest": "3500.0",
                "gain_or_lose_unrealized": "6000.0",
                "irr": "6.4"
            },
            {
                "particulars": "Total",
                "holdings_cost": "500000",
                "current_value": "510000.0",
                "holdings": "5.0",
                "gain_or_lose_realized": "10000.0",
                "devident_or_interest": "15000.0",
                "gain_or_lose_unrealized": "5000.0",
                "irr": "6.0"
            }
        ]
    },
    "twentyfive_page_data": {
        "equity_mutual_fund_allocation_response": [
            {
                "mutual_fund": "Flexi Cap Fund",
                "holdings_cost": "7,15,780",
                "current_value": "11,79,579",
                "holdings": "100",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.31",
                "gain_or_lose_unrealized": "4,55,332",
                "xirr": "55.3"
            },
            {
                "mutual_fund": "Large Cap Fund",
                "holdings_cost": "11,79,579",
                "current_value": "7,15,780",
                "holdings": "61,739",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.55",
                "gain_or_lose_unrealized": "61,739",
                "xirr": "3.2"
            },
            {
                "mutual_fund": "Mid Cap Fund",
                "holdings_cost": "9,50,000",
                "current_value": "10,20,000",
                "holdings": "85,000",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "2.80",
                "gain_or_lose_unrealized": "70,000",
                "xirr": "10.5"
            },
            {
                "mutual_fund": "Total",
                "holdings_cost": "11,79,579",
                "current_value": "7,15,780",
                "holdings": "61,739",
                "gain_or_lose_realized": "0",
                "devident_or_interest": "3.55",
                "gain_or_lose_unrealized": "61,739",
                "xirr": "3.2"
            }
        ],
        "equity_mutual_fund_pie_chart": {
            "labels": [
                "Flexi Cap Fund",
                "Large Cap Fund",
                "Mid Cap Fund"
            ],
            "values": [
                "1179579",
                "715780",
                "532000"
            ],
            "colors": []
        }
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
    if response.status_code > 400:
        print(f"Error: {response.text}")
  except Exception as e:
    print(f"Error: {e}")
    print(f"Response: {response.text}")
    print(f"Status code: {response.status_code}")