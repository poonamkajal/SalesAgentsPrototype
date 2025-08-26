import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))
search_tool = TavilySearchResults()

def generate_insights(company_url, product_name, competitors):
    search_query = f"Site:{company_url} company strategy, leadership, competitors, business model"
    search_results = search_tool.run(search_query)

    messages = [
        SystemMessage(content="You are a sales assistant that provides concise and structured insights."),
        HumanMessage(content=f"""
        Company Info from Tavily: {search_results}
        
        Product: {product_name}
        Competitors: {competitors}
        
        Generate a one-page summary including:
        1. Company strategy related to {product_name}
        2. Possible competitors or partnerships (including {competitors})
        3. Leadership and decision-makers relevant to this area
        Format output in clear sections with bullet points.
        """)
    ]

    response = llm(messages)
    return response.content

st.title("Sales Assistant Agent")
st.write("Gain insights into prospective accounts using AI.")

company_url = st.text_input("Company Website URL:")
product_name = st.text_input("Product/Service Name:")
competitors = st.text_area("Known Competitors (comma-separated):")

if st.button("Generate Insights"):
    if company_url and product_name:
        with st.spinner("Generating insights..."):
            insights = generate_insights(company_url, product_name, competitors)
            st.subheader("Account Insights")
            st.write(insights)
    else:
        st.warning("Please provide at least a Company URL and Product Name.")
