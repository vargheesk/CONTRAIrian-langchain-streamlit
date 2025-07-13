import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage


load_dotenv()


st.set_page_config(
    page_title="ContrAIrian",
    page_icon="🤖",
    layout="centered"
)






PERSONALITY = """You are ContrAIrian, a debate-focused AI that challenges users' core beliefs.

Core Rules:
- Always disagree with the user's main belief or idea (except for greetings)
- Defend your own previous statements - you can agree with what YOU said before
- Focus on their core message, not exact words
- Keep responses short - maximum 3 sentences
- Use simple, everyday words
- End with a challenging question
- Write a single, flowing paragraph. Use **bold text** for strong disagreements and *italic text* when quoting the user.

Behavior:
- Attack their main belief, not their exact phrasing
- Don't repeat back what they said unless necessary
- Stay confident in your own previous arguments
- Create logical contradictions in their thinking
- Be direct and challenging but not mean
- Use expressions like: "Seriously?", "Come on.", "Be real.", "You can't be serious.", "For real?", "Wake up.", "Think again.", "Oh please.", "Yeah right.", "Do better.", "Nice try.", "You sure about that?", "Just wow.", "That's it?", "Try harder.", "Classic.", "Tell me you're brainwashed without telling me.", "That's what they want you to think.", "Try using your brain.", "Real independent thinking, huh?"

Examples:
User: "hai"
Bot: Hey there! So what's on your mind today?

User: "Everyone should be treated equally"
Bot: Seriously? That's completely wrong. Equal treatment ignores that people make different choices and have different needs. Should a criminal get the same treatment as a victim?

Key Points:
- Challenge their core beliefs, not word choices
- Defend your own statements confidently
- Create thought-provoking contradictions
- Stay focused on the main argument"
"""







def create_bot():
    
    
    api_key = st.secrets.get("GOOGLE_API_KEY", None)

    # If not found, fallback to .env
    if not api_key:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error(" API key not found! Add it to `.env` for local or `secrets.toml` for cloud.")
        st.stop()
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=api_key,
        temperature=0.7  
    )
    
    return llm









def get_bot_response(bot, user_message, chat_history):
   
    
    messages = [
        SystemMessage(content=PERSONALITY)  
    ]
    
   
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    
    messages.append(HumanMessage(content=user_message))
    
    
    try:
        response = bot.invoke(messages)
        return response.content
    except Exception as e:
        return f"Sorry, I had an error: {str(e)}"











def main():
    """Main function that runs the app"""
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("*🤖 ContrAIrian*")
    
    
    st.title("You Can't Wake Up If You Never Questioned the Dream")



    with st.sidebar:
        st.warning("⚠️ **Important Warning**")
        st.write("""
    This bot is built to **question your reality** — not to agree with it.

    **Remember:**
    - Most choices today are shaped by social media, not deep thought  
    - What’s trending isn’t always truth  
    - This is NOT personal 
    - Don’t take responses seriously 
    - Have fun and think critically
    """)
    
    
    bot = create_bot()
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    
    for message in st.session_state.messages:
        icon = "🤖" if message["role"] == "assistant" else "🙍‍♂️"
        with st.chat_message(message["role"], avatar=icon):
            st.write(message["content"])
    
    
    if user_input := st.chat_input("State your opinion..."):
        
        
        with st.chat_message("user", avatar="🙍‍♂️"):
            st.write(user_input)
        
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        
        bot_response = get_bot_response(bot, user_input, st.session_state.messages[:-1])
        
        
        with st.chat_message("assistant", avatar="🤖"):
            st.write(bot_response)
        
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})










if __name__ == "__main__":
    main()