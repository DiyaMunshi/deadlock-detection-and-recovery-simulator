# Deadlock Detection and Recovery Simulator

An interactive web-based simulator that allows users to visualize and understand deadlocks in operating systems. The project uses a Wait-For Graph (WFG) model and custom DFS-based logic to detect cycles (deadlocks) and allows users to simulate process termination for recovery.

## 🚀 Features

* Input allocation and request matrices dynamically
* Build and visualize the Wait-For Graph
* Detect cycles (deadlocks) using DFS
* Allow user-driven recovery by terminating a process
* Generate updated execution order
* Real-time graph rendering using Matplotlib

## 🛠️ Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python (Flask)
* **Graph Visualization**: NetworkX + Matplotlib

## 📂 Project Structure

```
├── app.py                  # Main Flask app
├── templates/
│   └── index.html          # Frontend interface
├── static/
│   └── graph.png           # Output image for the WFG
├── venv/                   # Virtual environment (ignored in Git)
└── README.md               # Project documentation
```

## 🔧 Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/DiyaMunshi/deadlock-detection-and-recovery-simulator.git
cd deadlock-simulator
```

2. Create and activate virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python3 app.py
```

5. Open your browser and go to:

```
http://127.0.0.1:5050
```


## 🙋 Team Members

* Diya Munshi (Backend & DFS logic)
* Saniya Parveen (Frontend & Fetch API)
* Jhanvi Agarwal (Routing & Graph Integration)
* Isha Singh (UI/UX Design)


## 📃 License

This project is for educational purposes and is licensed under the MIT License.

---

> Made by Team CodeNomads – GEU
