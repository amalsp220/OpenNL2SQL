"""OpenNL2SQL Streamlit Frontend
Professional dashboard UI for Natural Language to SQL
"""

import streamlit as st
import requests
import pandas as pd
import os
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="OpenNL2SQL - AI Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1F77B4;
    text-align: center;
    padding: 1rem 0;
}
.sub-header {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<div class="main-header">🚀 OpenNL2SQL</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Natural Language to SQL Analytics</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/database.png", width=80)
    st.title("Controls")
    
    if st.button("\u267b\ufe0f New Session", use_container_width=True):
        st.session_state.session_id = None
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    
    st.subheader("📊 Session Info")
    if st.session_state.session_id:
        st.success(f"Active Session")
        st.caption(f"ID: {st.session_state.session_id[:8]}...")
    else:
        st.info("No active session")
    
    st.divider()
    
    st.subheader("ℹ️ About")
    st.markdown("""
    **OpenNL2SQL** converts your questions into SQL queries using AI.
    
    **Features:**
    - 🧠 AI-powered query generation
    - 🛡️ SQL injection protection
    - 🔄 Auto-recovery system
    - 💬 Context-aware conversations
    """)
    
    st.divider()
    st.caption("Built with FastAPI, Streamlit & Groq")
    st.caption("© 2025 OpenNL2SQL")

# Main content
tab1, tab2, tab3 = st.tabs(["💬 Ask Question", "📊 Query History", "⚙️ Settings"])

with tab1:
    st.subheader("📝 Ask Your Question")
    st.markdown("Enter your question in plain English, and AI will convert it to SQL.")
    
    # Question input
    question = st.text_area(
        "Your Question:",
        placeholder="E.g., How many customers do we have?\nShow me top 5 products by revenue\nWhat are the sales trends last month?",
        height=100,
        key="question_input"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit_btn = st.button("🚀 Generate SQL & Execute", type="primary", use_container_width=True)
    
    with col2:
        example_btn = st.button("💡 Example Questions", use_container_width=True)
    
    if example_btn:
        with st.expander("Example Questions", expanded=True):
            st.markdown("""
            **Aggregations:**
            - How many orders were placed last month?
            - What is the total revenue this year?
            
            **Top N Queries:**
            - Show me the top 10 customers by spending
            - Which products have the highest ratings?
            
            **Filters:**
            - List all orders over $1000
            - Show me customers from California
            
            **Joins:**
            - Show me customer names with their order totals
            - List products and their categories
            """)
    
    if submit_btn and question:
        with st.spinner("🧠 AI is thinking..."):
            try:
                # Make API request
                response = requests.post(
                    f"{BACKEND_URL}/query",
                    json={
                        "question": question,
                        "session_id": st.session_state.session_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data["success"]:
                        # Update session
                        st.session_state.session_id = data["session_id"]
                        st.session_state.history.append(data)
                        
                        # Success message
                        st.success("✅ Query executed successfully!")
                        
                        # Results display
                        col_sql, col_explain = st.columns(2)
                        
                        with col_sql:
                            with st.expander("📝 Generated SQL", expanded=True):
                                st.code(data["sql"], language="sql")
                        
                        with col_explain:
                            with st.expander("💡 SQL Explanation", expanded=True):
                                st.info(data["sql_explanation"])
                        
                        # Results
                        st.subheader("📊 Query Results")
                        
                        if data["results"]:
                            df = pd.DataFrame(data["results"])
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Rows Returned", len(df))
                            with col2:
                                st.metric("Columns", len(df.columns))
                            
                            # Table
                            st.dataframe(
                                df,
                                use_container_width=True,
                                height=400
                            )
                            
                            # Results explanation
                            with st.expander("💬 Results Summary"):
                                st.success(data["results_explanation"])
                        else:
                            st.warning("No results found.")
                    else:
                        st.error(f"❌ Error: {data['error']}")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    elif submit_btn:
        st.warning("⚠️ Please enter a question first.")

with tab2:
    st.subheader("📊 Query History")
    
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Query #{len(st.session_state.history) - idx + 1}: {item.get('sql', 'N/A')[:50]}..."):
                st.markdown(f"**Question:** {item.get('question', 'N/A')}")
                st.code(item.get('sql', 'N/A'), language="sql")
                st.caption(f"Session: {item.get('session_id', 'N/A')[:16]}...")
    else:
        st.info("📋 No queries yet. Ask a question to get started!")

with tab3:
    st.subheader("⚙️ Settings")
    
    st.markdown("**Backend Configuration**")
    backend_url = st.text_input("Backend API URL", value=BACKEND_URL)
    
    if st.button("Test Connection"):
        try:
            response = requests.get(f"{backend_url}/")
            if response.status_code == 200:
                st.success("✅ Backend connected successfully!")
            else:
                st.error("❌ Connection failed")
        except:
            st.error("❌ Cannot reach backend")
    
    st.divider()
    
    st.markdown("**Display Options**")
    max_rows = st.slider("Maximum rows to display", 10, 1000, 100)
    
    st.divider()
    
    st.markdown("**System Info**")
    st.info(f"""
    **Version:** 1.0.0  
    **Backend:** {BACKEND_URL}  
    **Session Active:** {bool(st.session_state.session_id)}  
    **Total Queries:** {len(st.session_state.history)}
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Made with ❤️ using <b>FastAPI</b>, <b>Streamlit</b> & <b>Groq</b></p>
    <p>🔒 All queries are validated for security | 🚀 Auto-recovery enabled</p>
</div>
""", unsafe_allow_html=True)
