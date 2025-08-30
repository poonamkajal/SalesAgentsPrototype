import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_tavily import TavilySearch
from fpdf import FPDF
import os, io
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM and Tools
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
search_tool = TavilySearch(topic="general", max_results=2)

# Function to generate insights
def generate_insights(company_name, company_url, product_name, product_category, competitors):
    # Perform web search to gather company info
    search_query = f"Site:{company_url} company strategy, leadership, competitors, business model"
    search_results = search_tool.invoke(search_query)
    print("\n Search Results: ", search_results)    

    # Create prompt for LLM
    messages = [
        SystemMessage(content="You are a sales assistant that provides concise and structured insights."),
        HumanMessage(content=f"""
        Company Info from Tavily: {search_results}
        
        Company: {company_name}
        Product: {product_name}
        Product Category: {product_category}
        Competitors: {competitors}
        
        Generate a one-page summary including:
        1. Company strategy related to {product_name}
        2. Possible competitors or partnerships (including {competitors})
        3. Leadership and decision-makers relevant to this area
        4. Product/Strategy Summary
        5. Article/Source Links
        Format output in clear sections with bullet points.
        """)
    ]

    model_response = llm.invoke(messages)
    print("\n Model Response: ", model_response.content)
    return model_response.content

# Function to create PDF from text
def create_pdf(report_content, company_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'Sales Insights Report - {company_name}', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', '', 12)
    lines = report_content.split('\n')
    for line in lines:
        if line.strip():
            pdf.cell(0, 6, line.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
        else:
            pdf.ln(3)
    
    pdf_output = io.BytesIO()
    pdf_string = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_string)
    pdf_output.seek(0)
    return pdf_output.getvalue()



# Streamlit UI
st.set_page_config(page_title="Sales Agent Prototype", page_icon="📊", layout="centered")
st.title("📊 Sales Assistant Agent")
st.write("Gain insights into prospective accounts using AI.")

with st.form("sales_form"):
    company_name = st.text_input("Company Name", placeholder="e.g., Snowflake, Redhat")
    company_url = st.text_input("Company URL", placeholder="e.g., https://www.snowflake.com, https://www.redhat.com")
    product_name = st.text_input("Product Name", placeholder="e.g., Data Cloud, OpenShift")
    product_category = st.text_input("Product Category", placeholder="e.g., Data Platform, Cloud Computing")
    competitors = st.text_area("Competitors (comma-separated URLs)", placeholder="e.g., https://www.databricks.com, https://www.cloudera.com")
    value_proposition = st.text_input("Value Proposition", placeholder="e.g., Cost Savings, Scalability")
    target_customer = st.text_input("Target Customer", placeholder="e.g., Enterprises, SMBs")
    submit = st.form_submit_button("Generate Insights")

report = None
download_pdf = False
download_text = False

if submit:
    if company_url and company_name:
        with st.spinner("Generating insights..."):
            result = generate_insights(company_name, company_url, product_name, product_category, competitors)
            st.subheader("Account Insights")
            st.divider()
            st.write(result)

        report = result
        if report is not None:
            # download as a text file
            st.download_button(
                    "Download Report", 
                    report, 
                    file_name="sales_report.txt", 
                    mime="text/plain")
                       
            # download as a pdf file
            pdf_data = create_pdf(report, company_name)
            st.download_button(
                "Download Report as PDF",
                pdf_data,
                file_name=f"sales_report_{company_name}.pdf",
                mime="application/pdf"
            )
        st.toast("📥 Generate Insights Report", icon="✅")
        
    else:
        st.warning("Please provide at least a Company URL and Company Name.")


