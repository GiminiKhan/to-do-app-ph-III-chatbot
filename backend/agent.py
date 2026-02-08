import os
from groq import Groq
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- CONFIGURATION ---
GROQ_API_KEY = "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"
DATABASE_URL = "postgresql://neondb_owner:npg_Rl3ZkIj7OnFd@ep-odd-frost-abyohkf7-pooler.eu-west-2.aws.neon.tech/neondb"

# --- DATABASE SETUP ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

# --- TOOLS ---
def add_task_to_db(title: str):
    db = SessionLocal()
    try:
        new_todo = Todo(title=title)
        db.add(new_todo)
        db.commit()
        return f"Successfully added task: '{title}'"
    except Exception as e:
        return f"Error adding task: {str(e)}"
    finally:
        db.close()

def get_tasks_from_db():
    db = SessionLocal()
    try:
        tasks = db.query(Todo).all()
        if not tasks:
            return "No tasks found in the database."
        return "\n".join([f"- {t.title} ({'Done' if t.completed else 'Pending'})" for t in tasks])
    except Exception as e:
        return f"Error fetching tasks: {str(e)}"
    finally:
        db.close()

# --- AGENT LOGIC ---
client = Groq(api_key=GROQ_API_KEY)

def run_todo_agent(user_input: str):
    print(f"🤖 Agent is thinking... Message: {user_input}")
    
    user_input_lower = user_input.lower()
    
    # Simple Router for Task Actions
    if "add" in user_input_lower:
        task_name = user_input.lower().replace("add", "").strip()
        return add_task_to_db(task_name)
    
    elif "list" in user_input_lower or "show" in user_input_lower:
        return get_tasks_from_db()

    # Default Chat Logic
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful Todo-list Assistant. If the user wants to add or list tasks, tell them you can do that."},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    # Test: Add and then List
    print(run_todo_agent("add Finish assignment now"))
    print("\n--- Current List ---")
    print(run_todo_agent("list tasks"))