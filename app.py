import streamlit as st
import os
import time
from pymongo import MongoClient
from mistralai.client import Mistral
import voyageai
from dotenv import load_dotenv

# Load credentials
load_dotenv()

# Connections
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["esg_rag"]
collection = db["documents"]
vc = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Companies list
COMPANIES = [
    "TotalEnergies", "Airbus", "AXA", "BNP Paribas",
    "Capgemini", "Danone", "Engie", "L'Oreal",
    "LVMH", "Orange", "Renault", "Sanofi",
    "Schneider Electric", "Stellantis"
]

# CSRD Checklist
CSRD_CHECKLIST = [
    "Net zero or carbon neutrality target and timeline",
    "Scope 1 and Scope 2 greenhouse gas emissions data",
    "Scope 3 value chain emissions disclosure",
    "Renewable energy usage and targets",
    "Water consumption and reduction targets",
    "Biodiversity impact assessment and commitments",
    "Circular economy and waste reduction strategy",
    "Gender diversity and inclusion metrics",
    "Supply chain human rights due diligence",
    "Employee health safety and wellbeing policy",
    "Anti-corruption and business ethics governance",
    "Board level sustainability oversight"
]

def search_esg(query, company=None, top_k=5):
    query_embedding = vc.embed([query], model="voyage-3").embeddings[0]
    pipeline = [
        {
            "$vectorSearch": {
                "index": "esg_embedding_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": top_k,
                "filter": {"company": company} if company else {}
            }
        },
        {
            "$project": {
                "company": 1,
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def answer_question(query, company=None):
    results = search_esg(query, company=company)
    context = "\n\n".join([f"[{r['company']}]: {r['text']}" for r in results])
    prompt = f"""You are an ESG analyst assistant. Answer the question below using ONLY the context provided.
If the answer is not in the context, say "I could not find this information in the reports."
Always cite the company name and specific numbers when available.

Context:
{context}

Question: {query}

Answer:"""
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, results

def analyze_csrd(company_name):
    results = []
    for requirement in CSRD_CHECKLIST:
        chunks = search_esg(requirement, company=company_name, top_k=3)
        context = "\n\n".join([c["text"] for c in chunks])
        prompt = f"""You are a CSRD compliance expert.
Based ONLY on the context below from {company_name}'s sustainability report, assess this requirement:

Requirement: {requirement}

Context:
{context}

Respond with EXACTLY one of these and a brief one-line reason:
✅ DISCLOSED - Clear evidence found
⚠️ PARTIAL - Some mention but incomplete
❌ MISSING - No evidence found

Format: [STATUS] - [reason]"""
        response = mistral.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()
        results.append({"Requirement": requirement, "Status": answer})
        time.sleep(25)
    return results

# Streamlit UI
st.set_page_config(page_title="CAC40 ESG Intelligence", page_icon="🌱", layout="wide")
st.title("🌱 CAC40 ESG Report Intelligence")
st.caption("Powered by MongoDB Atlas Vector Search, Voyage AI & Mistral")

tab1, tab2 = st.tabs(["💬 Ask ESG Questions", "📊 CSRD Gap Analysis"])

# Tab 1 — Q&A
with tab1:
    st.subheader("Ask any ESG question across 14 CAC40 companies")
    
    company_filter = st.selectbox(
        "Filter by company (optional)",
        ["All Companies"] + COMPANIES
    )
    
    query = st.text_input("Your question", placeholder="What are the net zero targets across CAC40 companies?")
    
    if st.button("Search", key="search"):
        if query:
            with st.spinner("Searching across ESG reports..."):
                company = None if company_filter == "All Companies" else company_filter
                answer, sources = answer_question(query, company=company)
            
            st.markdown("### Answer")
            st.write(answer)
            
            st.markdown("### Sources")
            for s in sources:
                with st.expander(f"{s['company']} — Score: {s['score']:.4f}"):
                    st.write(s['text'][:500])

# Tab 2 — CSRD Gap Analysis
with tab2:
    st.subheader("CSRD Compliance Gap Analysis")
    
    selected_company = st.selectbox("Select a company", COMPANIES)
    
    if st.button("Generate Gap Report", key="gap"):
        with st.spinner(f"Analyzing {selected_company} against CSRD requirements... (this takes ~5 minutes)"):
            results = analyze_csrd(selected_company)
        
        st.markdown(f"### CSRD Gap Report: {selected_company}")
        
        # Count scores
        disclosed = sum(1 for r in results if "✅" in r["Status"])
        partial = sum(1 for r in results if "⚠️" in r["Status"])
        missing = sum(1 for r in results if "❌" in r["Status"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Disclosed", disclosed)
        col2.metric("⚠️ Partial", partial)
        col3.metric("❌ Missing", missing)
        
        st.markdown("### Detailed Results")
        for r in results:
            st.markdown(f"**{r['Requirement']}**")
            st.write(r['Status'])
            st.divider()