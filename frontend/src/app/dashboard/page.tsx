"use client";
import { useState, useEffect } from "react";
import { Search, Plus, Trash2, LogOut, CheckCircle, Circle, Pencil } from "lucide-react";

// Helper function to decode JWT token
const decodeToken = (token) => {
  if (!token) return null;
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("All"); // Added priority filter state
  const [sortBy, setSortBy] = useState("Newest"); // Added sort by state
  const [newTask, setNewTask] = useState({ title: "", description: "", priority: "Medium" });
  const [editingTask, setEditingTask] = useState(null);
  const [editTaskData, setEditTaskData] = useState({ title: "", description: "", priority: "Medium" });

  const fetchTasks = async () => {
    try {
      // Extract user_id from the JWT token
      const token = localStorage.getItem("access_token");
      const tokenPayload = decodeToken(token);
      const userId = tokenPayload?.sub || "";

      const res = await fetch(`http://127.0.0.1:8000/api/${userId}/tasks`, { headers: { "Authorization": "Bearer " + token, "Content-Type": "application/json" } });
      if (res.ok) {
        const responseData = await res.json();
        // Extract tasks from the standardized response format
        setTasks(Array.isArray(responseData.data) ? responseData.data : []);
      } else {
        setTasks([]); // Set to empty array on error
      }
    } catch (err) { console.error(err); }
  };

  useEffect(() => { fetchTasks(); }, []);

  const handleCreate = async () => {
    if(!newTask.title) return alert("Title required");
    try {
      // Extract user_id from the JWT token
      const token = localStorage.getItem("access_token");
      const tokenPayload = decodeToken(token);
      const userId = tokenPayload?.sub || "";

      const res = await fetch(`http://127.0.0.1:8000/api/${userId}/tasks`, { method: "POST", headers: { "Authorization": "Bearer " + token, "Content-Type": "application/json" }, body: JSON.stringify({ title: newTask.title, description: newTask.description, priority: newTask.priority.toLowerCase() }) });
      if (res.ok) { setShowModal(false); fetchTasks(); setNewTask({title:"", description:"", priority:"Medium"}); } else { alert("Error saving task"); }
    } catch (err) { alert("Error saving task"); }
  };

  const deleteTodo = async (id) => {
    // Extract user_id from the JWT token
    const token = localStorage.getItem("access_token");
    const tokenPayload = decodeToken(token);
    const userId = tokenPayload?.sub || "";

    const res = await fetch(`http://127.0.0.1:8000/api/${userId}/tasks/${id}`, { method: "DELETE", headers: { "Authorization": "Bearer " + token, "Content-Type": "application/json" } });
    if (res.ok) {
      fetchTasks();
    } else {
      console.error('Failed to delete task');
    }
  };

  const toggleTaskCompletion = async (task) => {
    // Extract user_id from the JWT token
    const token = localStorage.getItem("access_token");
    const tokenPayload = decodeToken(token);
    const userId = tokenPayload?.sub || "";

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/${userId}/tasks/${task.id}/complete`, {
        method: "PATCH",
        headers: {
          "Authorization": "Bearer " + token,
          "Content-Type": "application/json"
        }
      });

      if (res.ok) {
        fetchTasks(); // Refresh the task list
      } else {
        console.error('Failed to update task completion status');
      }
    } catch (err) {
      console.error('Error updating task completion status:', err);
    }
  };

  const startEditing = (task) => {
    setEditingTask(task.id);
    setEditTaskData({
      title: task.title,
      description: task.description,
      priority: task.priority
    });
  };

  const cancelEditing = () => {
    setEditingTask(null);
    setEditTaskData({ title: "", description: "", priority: "Medium" });
  };

  const handleUpdate = async () => {
    if (!editTaskData.title) {
      alert("Title required");
      return;
    }

    // Extract user_id from the JWT token
    const token = localStorage.getItem("access_token");
    const tokenPayload = decodeToken(token);
    const userId = tokenPayload?.sub || "";

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/${userId}/tasks/${editingTask}`, {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: editTaskData.title,
          description: editTaskData.description,
          priority: editTaskData.priority.toLowerCase()
        })
      });

      if (res.ok) {
        setEditingTask(null);
        setEditTaskData({ title: "", description: "", priority: "Medium" });
        fetchTasks(); // Refresh the task list
      } else {
        alert("Error updating task");
      }
    } catch (err) {
      alert("Error updating task");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex text-slate-800">
      <aside className="w-64 bg-indigo-700 p-8 text-white hidden md:block">
        <h2 className="text-2xl font-bold mb-10 italic uppercase">TASKIFY</h2>
        <nav className="space-y-4">
          <div className="bg-indigo-800 p-3 rounded-xl flex items-center gap-3"><CheckCircle size={20}/> All Tasks</div>
          <div onClick={() => {localStorage.clear(); window.location.href="/login"}} className="p-3 flex items-center gap-3 cursor-pointer hover:bg-indigo-600 rounded-xl text-rose-300 mt-10 font-bold"><LogOut size={20}/> Logout</div>
        </nav>
      </aside>
      <main className="flex-1 p-8">
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-10 gap-4">
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <div className="relative flex-1 max-w-xs">
              <Search className="absolute left-3 top-3 text-slate-400" size={20}/>
              <input className="w-full pl-10 pr-4 py-3 rounded-xl border text-black outline-none" placeholder="Search tasks..." onChange={(e)=>setSearch(e.target.value)} value={search} />
            </div>
            <div className="relative">
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="w-full sm:w-auto px-4 py-3 rounded-xl border text-black outline-none appearance-none bg-white"
              >
                <option value="All">All Priorities</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full sm:w-auto px-4 py-3 rounded-xl border text-black outline-none appearance-none bg-white"
              >
                <option value="Newest">Newest</option>
                <option value="Priority">Priority</option>
              </select>
            </div>
          </div>
          <button onClick={()=>setShowModal(true)} className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg whitespace-nowrap">+ Add Task</button>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Array.isArray(tasks) ? [...tasks].filter(t => {
            const matchesSearch = t.title.toLowerCase().includes(search.toLowerCase());
            const matchesPriority = priorityFilter === "All" || t.priority.toLowerCase() === priorityFilter.toLowerCase();
            return matchesSearch && matchesPriority;
          }).sort((a, b) => {
            if (sortBy === "Newest") {
              // Sort by creation date (assuming created_at field exists and is in ISO format)
              return new Date(b.created_at || b.updated_at || 0) - new Date(a.created_at || a.updated_at || 0);
            } else if (sortBy === "Priority") {
              // Define priority order: High > Medium > Low > Others
              const priorityOrder = { "high": 3, "medium": 2, "low": 1 };
              const aPriorityValue = priorityOrder[a.priority.toLowerCase()] || 0;
              const bPriorityValue = priorityOrder[b.priority.toLowerCase()] || 0;

              // If priorities are the same, sort by creation date
              if (aPriorityValue === bPriorityValue) {
                return new Date(b.created_at || b.updated_at || 0) - new Date(a.created_at || a.updated_at || 0);
              }
              return bPriorityValue - aPriorityValue; // Higher priority first
            }
            return 0;
          }).map(task => (
            <div key={task.id} className={`bg-white p-6 rounded-3xl shadow-sm border-l-4 ${task.status === 'completed' ? 'border-green-500 bg-green-50' : 'border-indigo-500'} hover:shadow-md`}>
              {editingTask === task.id ? (
                // Editing mode
                <>
                  <div className="flex justify-between mb-4 text-[10px] font-bold uppercase">
                    <select
                      value={editTaskData.priority}
                      onChange={(e) => setEditTaskData({...editTaskData, priority: e.target.value})}
                      className="bg-slate-100 rounded px-2 py-1 text-indigo-400 focus:outline-none"
                    >
                      <option value="Low">LOW</option>
                      <option value="Medium">MEDIUM</option>
                      <option value="High">HIGH</option>
                    </select>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={handleUpdate}
                        className="text-green-600 hover:text-green-800"
                        aria-label="Save changes"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEditing}
                        className="text-red-600 hover:text-red-800 ml-2"
                        aria-label="Cancel editing"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                  <input
                    type="text"
                    value={editTaskData.title}
                    onChange={(e) => setEditTaskData({...editTaskData, title: e.target.value})}
                    className={`w-full text-lg font-bold mb-2 p-1 border-b ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-black'}`}
                    autoFocus
                  />
                  <textarea
                    value={editTaskData.description}
                    onChange={(e) => setEditTaskData({...editTaskData, description: e.target.value})}
                    className={`w-full text-sm p-1 border-b ${task.status === 'completed' ? 'line-through text-gray-400' : 'text-slate-500'}`}
                    rows={3}
                  />
                </>
              ) : (
                // Display mode
                <>
                  <div className="flex justify-between mb-4 text-[10px] font-bold uppercase">
                    <span className={task.status === 'completed' ? 'text-green-600' : 'text-indigo-400'}>
                      {task.priority} {task.status === 'completed' ? '(COMPLETED)' : ''}
                    </span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => startEditing(task)}
                        className="focus:outline-none"
                        aria-label="Edit task"
                      >
                        <Pencil size={16} className="text-blue-500 hover:text-blue-700" />
                      </button>
                      <button
                        onClick={() => toggleTaskCompletion(task)}
                        className="focus:outline-none"
                        aria-label={task.status === 'completed' ? "Mark as incomplete" : "Mark as complete"}
                      >
                        {task.status === 'completed' ? (
                          <CheckCircle size={18} className="text-green-600" />
                        ) : (
                          <Circle size={18} className="text-gray-400 hover:text-indigo-600" />
                        )}
                      </button>
                      <Trash2 className="cursor-pointer hover:text-rose-500" size={18} onClick={()=>deleteTodo(task.id)}/>
                    </div>
                  </div>
                  <h3 className={`text-lg font-bold ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-black'}`}>
                    {task.title}
                  </h3>
                  <p className={`${task.status === 'completed' ? 'line-through text-gray-400' : 'text-slate-500'} text-sm`}>
                    {task.description}
                  </p>
                </>
              )}
            </div>
          )) : []}
        </div>
      </main>
      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-[40px] w-full max-w-md p-10 relative">
            <button onClick={()=>setShowModal(false)} className="absolute top-6 right-8 text-2xl text-black">×</button>
            <h2 className="text-2xl font-bold mb-8 text-indigo-600">New Task</h2>
            <input className="w-full p-4 bg-slate-100 rounded-2xl mb-4 text-black border" placeholder="Task Title" onChange={e=>setNewTask({...newTask, title:e.target.value})} />
            <textarea className="w-full p-4 bg-slate-100 rounded-2xl mb-4 text-black h-24 border" placeholder="Description" onChange={e=>setNewTask({...newTask, description:e.target.value})}></textarea>
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value})}
              className="w-full p-4 bg-slate-100 rounded-2xl mb-4 text-black border outline-none"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
            <button onClick={handleCreate} className="w-full py-4 bg-indigo-600 text-white rounded-2xl font-bold">SAVE TASK</button>
          </div>
        </div>
      )}
    </div>
  );
}