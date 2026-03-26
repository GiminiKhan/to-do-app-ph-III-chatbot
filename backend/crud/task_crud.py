from sqlmodel import Session, select
from backend.models.task_model import Task

def create_task(session: Session, task_data: Task):
    session.add(task_data)
    session.commit()
    session.refresh(task_data)
    return task_data

def get_tasks(session: Session):
    return session.exec(select(Task)).all()

def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    return task

# MISSING FUNCTION: update_task function add kiya
def update_task(session: Session, task_id: int, title: str = None, description: str = None):
    task = session.get(Task, task_id)
    if not task:
        return None
    
    if title:
        task.title = title
    if description:
        task.description = description
        
    session.add(task)
    session.commit()
    session.refresh(task)
    return task