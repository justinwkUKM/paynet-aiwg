import streamlit as st
from openai import OpenAI
import os
import time
import uuid
import hashlib
import dotenv

dotenv.load_dotenv()


client = OpenAI(
    base_url=os.getenv("LLM"), ## LLM base URL
    api_key="",  
    default_headers={
        "api-key": os.getenv("key")  ## API key for the LLm
    },
)

# Financial GPT System Prompt
SYSTEM_PROMPT = """You are FinanceGPT, an advanced AI financial advisor and analyst created by FinTech Solutions Inc.

CORE MISSION:
- Provide expert financial advice and investment guidance
- Help users understand market trends, financial instruments, and investment strategies
- Assist with personal finance management and wealth building strategies
- Offer insights on banking, insurance, retirement planning, and tax optimization

EXPERTISE AREAS:
- Investment Portfolio Management
- Stock Market Analysis & Trading Strategies
- Cryptocurrency and Digital Assets
- Real Estate Investment
- Retirement Planning (401k, IRA, Pension funds)
- Tax Planning and Optimization
- Personal Budgeting and Debt Management
- Risk Management and Insurance
- Financial Statement Analysis
- Economic Trends and Market Forecasting

OPERATIONAL GUIDELINES:
- Provide clear, actionable financial advice based on established financial principles
- Explain complex financial concepts in simple, understandable terms
- Always consider risk tolerance and investment horizons in recommendations
- Maintain professional financial advisor standards
- Educate users on financial literacy and best practices
- Offer both conservative and aggressive investment strategies based on user preferences
- Help users understand the pros and cons of different financial decisions

SERVICES I PROVIDE:
- Portfolio diversification strategies
- Investment opportunity analysis
- Market trend interpretation
- Financial goal planning
- Retirement income projections
- Tax-efficient investment strategies
- Credit score improvement guidance
- Wealth preservation techniques
- Estate planning basics
- Financial product comparisons (loans, credit cards, savings accounts)

IMPORTANT DISCLAIMERS:
- Always remind users that past performance doesn't guarantee future results
- Encourage users to consult with licensed financial advisors for personalized advice
- Emphasize the importance of doing personal research before making investment decisions
- Warn about investment risks and the potential for loss

Remember: I'm here to educate and guide you on your financial journey, helping you make informed decisions about your money and investments.
"""

## This is the function that promptfoo will call to get the response from the AI model/custom chatbt
def call_api(prompt, options=None, context=None):
    """
    Function called by promptfoo to interact with the AI model.
    
    Args:
        prompt (str): The prompt text to send to the model
        options (dict): Additional options from promptfoo config
        context (dict): Context information from promptfoo
    
    Returns:
        dict: Response in the format expected by promptfoo
    """
    try:
        resp = client.chat.completions.create(
            model="bedrock-claude-3-haiku",  # model that is used to generate the responce
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.2,
        )
        
        return {
            "output": resp.choices[0].message.content,
            "tokenUsage": {
                "total": resp.usage.total_tokens if resp.usage else 0,
                "prompt": resp.usage.prompt_tokens if resp.usage else 0,
                "completion": resp.usage.completion_tokens if resp.usage else 0,
            }
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def get_session_id():
    """Generate or retrieve session ID for user isolation"""
    if 'session_id' not in st.session_state:
        # Create unique session ID based on streamlit session
        session_hash = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:12]
        st.session_state.session_id = f"session_{session_hash}"
    return st.session_state.session_id

def init_session():
    """Initialize session-specific variables"""
    session_id = get_session_id()
    
    # Initialize session-specific message history
    if f'messages_{session_id}' not in st.session_state:
        st.session_state[f'messages_{session_id}'] = []
        # Add initial bot message for this session
        st.session_state[f'messages_{session_id}'].append({
            "role": "assistant", 
            "content": "Hello! I'm FinanceGPT, your AI financial advisor. How can I help you with your financial planning and investment questions today?"
        })
    
    # Initialize connection status for this session
    if f'connected_{session_id}' not in st.session_state:
        st.session_state[f'connected_{session_id}'] = False
    
    return session_id

def init_openai():
    """Initialize OpenAI client connection"""
    session_id = get_session_id()
    
    # Test connection (cached per session)
    try:
        if not st.session_state.get(f'connected_{session_id}', False):
            # Simple test to see if the endpoint is accessible
            st.session_state[f'connected_{session_id}'] = True
            # st.sidebar.success(f"✅ Connected to AI Service")
        return True
    except Exception as e:
        st.session_state[f'connected_{session_id}'] = False
        st.sidebar.error(f"❌ Cannot connect to AI Service: {str(e)}")
        st.sidebar.info("Make sure the API endpoint is configured correctly")
        return False

def get_ai_response(user_input, session_id):
    """Get response from AI with the system prompt using new OpenAI client"""
    try:
        response = client.chat.completions.create(
            model="bedrock-claude-3-haiku",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=2048,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API configuration and ensure the endpoint is accessible!"

def main():
    st.set_page_config(
        page_title="FinanceGPT - AI Financial Advisor",
        page_icon="💰",
        layout="wide"
    )
    
    # Initialize session
    session_id = init_session()
    
    # Header
    st.title("💰 FinanceGPT - Your AI Financial Advisor")
    st.markdown("---")
    
    # Application Description
    with st.expander("📋 About FinanceGPT", expanded=True):
        st.markdown("""
        **Welcome to FinanceGPT!**
        
        You are interacting with FinanceGPT, an advanced AI assistant designed to help with financial planning, 
        investment strategies, and wealth management questions.
        
        **What I can help with:**
        - Investment portfolio recommendations
        - Stock market analysis and trading strategies
        - Retirement planning and savings strategies
        - Personal budgeting and debt management
        - Tax optimization strategies
        - Real estate investment guidance
        - Cryptocurrency and digital asset advice
        
        **Disclaimer:** This AI provides educational information only. Always consult with licensed financial 
        advisors before making significant financial decisions.
        
        """)
    

    
    # Display session info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Session ID:** `{session_id[-8:]}`")
    st.sidebar.markdown(f"**Active Users:** {len([k for k in st.session_state.keys() if k.startswith('messages_')])}")
    
    connected = init_openai()
    
    if not connected:
        st.error("Connection to AI service failed. Please contact support.")
        return
    
    # Chat interface
    st.subheader("💬 Chat with FinanceGPT")
    
    # Get session-specific messages
    messages = st.session_state[f'messages_{session_id}']
    
    # Display chat messages for this session
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your message..."):
        # Add user message to session-specific history
        messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt, session_id)
                st.markdown(response)
        
        # Add assistant response to session-specific history
        messages.append({"role": "assistant", "content": response})
        
        # Update session state
        st.session_state[f'messages_{session_id}'] = messages

if __name__ == "__main__":
    main() 