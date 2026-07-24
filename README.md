# 🌱 CAC40 ESG Report Intelligence

> A Retrieval-Augmented Generation (RAG) tool for semantic search and CSRD compliance analysis across 14 CAC40 sustainability reports.

**🔗 Live Demo:** https://cac40-esg-intelligence.streamlit.app

---

## Problem

With the EU's Corporate Sustainability Reporting Directive (CSRD) now mandatory for large European companies, analysts must compare hundreds of pages of ESG reports across organisations. Manual analysis is slow, inconsistent, and unscalable.

## Solution

An AI-powered tool that:
- Indexes 14 CAC40 ESG reports as semantic vector embeddings in MongoDB Atlas
- Answers natural language questions across all reports simultaneously
- Automatically generates CSRD compliance gap analysis for any company — scoring 12 key disclosure requirements as ✅ Disclosed / ⚠️ Partial / ❌ Missing

---

## Features

- **Cross-company semantic search** — ask any ESG question across all 14 companies at once
- **Company-specific Q&A** — filter by company for focused analysis
- **CSRD gap analysis** — instant compliance scoring across 12 CSRD requirements
- **Source transparency** — every answer shows the exact chunks retrieved with relevance scores

---

## Tech Stack

| Component | Technology |
|---|---|
| Vector Database | MongoDB Atlas Vector Search |
| Embeddings | Voyage AI (voyage-3, 1024 dimensions, cosine similarity) |
| LLM | Mistral AI (mistral-small-latest) |
| Interface | Streamlit |
| Language | Python 3.11 |

---

## Dataset

**14 CAC40 companies** across 10 sectors — **8,441 chunks** indexed in MongoDB Atlas.

| Company | Sector | Chunks |
|---|---|---|
| TotalEnergies | Energy | 383 |
| Airbus | Aerospace | 1,835 |
| AXA | Insurance | 256 |
| BNP Paribas | Banking | 118 |
| Capgemini | Technology & Consulting | 730 |
| Danone | Food & Beverage | 102 |
| Engie | Utilities | 522 |
| L'Oreal | Consumer Goods | 647 |
| LVMH | Luxury | 446 |
| Orange | Telecommunications | 166 |
| Renault | Automotive | 146 |
| Sanofi | Pharmaceuticals | 910 |
| Schneider Electric | Industrial | 1,599 |
| Stellantis | Automotive | 581 |

---

## CSRD Requirements Assessed

1. Net zero or carbon neutrality target and timeline
2. Scope 1 and Scope 2 greenhouse gas emissions data
3. Scope 3 value chain emissions disclosure
4. Renewable energy usage and targets
5. Water consumption and reduction targets
6. Biodiversity impact assessment and commitments
7. Circular economy and waste reduction strategy
8. Gender diversity and inclusion metrics
9. Supply chain human rights due diligence
10. Employee health, safety and wellbeing policy
11. Anti-corruption and business ethics governance
12. Board level sustainability oversight

---

## Architecture

```
User Query
    ↓
Voyage AI embeds the query (1024-dim vector)
    ↓
MongoDB Atlas $vectorSearch finds top-k relevant chunks
    ↓
Retrieved chunks passed as context to Mistral AI
    ↓
Grounded answer returned with source citations
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (free tier)
- Voyage AI API key (free tier)
- Mistral AI API key (free tier)

### Installation

```bash
git clone https://github.com/deepayans/esg-rag-analyzer.git
cd esg-rag-analyzer
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
MONGODB_URI=your_mongodb_connection_string
VOYAGE_API_KEY=your_voyage_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

### Run Locally

```bash
streamlit run app.py
```

---

## Data Sources

All ESG reports are publicly available from official company websites:

| Company | Report | Link |
|---|---|---|
| TotalEnergies | Sustainability & Climate 2024 Progress Report | [Download](https://totalenergies.com/system/files/documents/2024-03/totalenergies_sustainability-climate-2024-progress-report_2024_en_pdf.pdf) |
| Airbus | Annual Report 2024 | [Download](https://www.airbus.com/sites/g/files/jlcbta136/files/2025-04/Airbus%20Annual%20Report%202024.pdf) |
| AXA | Climate & Biodiversity Report 2024 | [Download](https://www-axa-com.cdn.axa-contento-118412.eu/www-axa-com/8b8dfa69-13e3-4c34-bae3-8fb939102a2d_axa_climate_and_biodiversity_report_2024_va.pdf) |
| BNP Paribas | PRB Reporting 2024 | [Download](https://cdn-group.bnpparibas.com/uploads/file/bnp_paribas_2024_prb_reporting.pdf) |
| Capgemini | Universal Registration Document 2024 | [Download](https://investors.capgemini.com/en/file/28667?download=1) |
| Danone | Integrated Annual Report 2024 | [Download](https://www.danone.com/content/dam/corp/global/danonecom/investors/en-sustainability/reports-and-data/cross-topic/danoneiar2024.pdf) |
| Engie | ESG at Engie 2024 | [Download](https://www.engie.com/sites/default/files/assets/documents/2025-04/20250416%20-Engie%20-2024%20ESG%20at%20ENGIE.pdf) |
| L'Oréal | Universal Registration Document 2024 | [Download](https://www.loreal-finance.com/system/files/2025-03/2024_Universal_Registration_Document_LOREAL.pdf) |
| LVMH | Universal Registration Document 2024 | [Download](https://ddd.uab.cat/pub/infsos/146081/irsLVMHa2024ieng.pdf) |
| Orange | Integrated Annual Report 2024-2025 | [Download](https://rai.orange.com/wp-content/uploads/sites/54/2025/06/integrated-annual-report-2024-2025.pdf) |
| Renault | Integrated Report 2023-2024 | [Download](https://assets.renaultgroup.com/uploads/2024/10/2023-2024-integrated-report.pdf) |
| Sanofi | ESG Report 2024 | [Download](https://www.sanofi.com/assets/dotcom/content-app/publications/esg-reports/sustainability-statement-2024--ESG-Report-.pdf) |
| Schneider Electric | Sustainability Report 2024 | [Download](https://www.se.com/ww/en/assets/564/document/513141/2024-sustainability-report.pdf) |
| Stellantis | Expanded Sustainability Statement 2024 | [Download](https://www.stellantis.com/content/dam/stellantis-corporate/sustainability/esg-disclosures/Stellantis-Expanded-Sustainability-Statement-2024.pdf) |

---

## Project Background

Built as a learning project during MSc Data Analytics for Business at KEDGE Business School (2026). The goal was to understand the full RAG pipeline — from PDF ingestion to vector search to LLM generation — without using LangChain or agent frameworks, making every component explicit and understandable.

---

## Author

**Deepayan Sarkar**  
MSc Data Analytics for Business — KEDGE Business School  
4+ years experience as Software Engineer at Accenture  
🔗 [Portfolio](https://deepayan.me) | [GitHub](https://github.com/deepayans)
