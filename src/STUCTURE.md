fpoly-happiness-report/
├── data/
│   ├── raw/                  # Dữ liệu gốc
│   └── processed/            # Dữ liệu sạch sau ETL
├── src/
│   ├── __init__.py
│   ├── config.py             # Chứa Metadata, mapping và hằng số
│   ├── etl/                  # Module xử lý dữ liệu (DE)
│   │   ├── __init__.py
│   │   ├── loader.py         # Đọc dữ liệu (CSV/API)
│   │   ├── cleaner.py        # Lọc Trap & Chuẩn hóa
│   │   └── transformer.py    # Reverse coding & Feature engineering
│   ├── analytics/            # Module phân tích (DA)
│   │   ├── __init__.py
│   │   ├── statistics.py     # Tính Mean, Std Dev, Correlation
│   │   └── nlp_engine.py     # Xử lý text điều ước (Word Cloud)
│   └── app.py                # Dashboard (Entry point)
├── docs/                     # METADATA.md, requirement.md...
└── requirements.txt