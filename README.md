# EDR Prototype for Windows

This repository contains a prototype of an Endpoint Detection and Response (EDR) system for Windows, designed to monitor and analyze 50 critical security events.

## Project Structure

```
edr-github-project/
├── edr-backend/             # Flask backend for API
├── edr-dashboard/           # React frontend for the dashboard
├── agent/                   # Agent-related files (to be created)
│   ├── event_collector.py   # Python script for collecting Windows Event Logs
│   └── analysis_module.py   # Python script for analyzing events and generating alerts
├── data/                    # Sample data files
│   ├── security_events.json
│   └── security_alerts.json
├── docs/                    # Project documentation
│   ├── edr_overview.md
│   ├── edr_architecture_design.md
│   ├── windows_event_collection_methods.md
│   └── edr_documentation.md
├── scripts/                 # Deployment scripts
│   └── deploy_agent.ps1     # PowerShell script to deploy the agent
├── .gitignore               # Git ignore file
├── README.md                # Project README
└── project_summary.md       # Project summary
```

## Features

- **Event Collection:** Gathers 50 critical Windows Event IDs.
- **Analysis & Alerting:** Detects suspicious activities and generates alerts based on predefined rules.
- **Web Dashboard:** Provides a real-time overview of security events and alerts.
- **RESTful API:** Enables integration with other security systems.

## Getting Started

### Prerequisites

- **Windows OS:** Windows 10/11 or Windows Server 2016/2019/2022
- **Python 3.8+:** For backend and agent scripts.
- **Node.js 16+:** For frontend development.
- **Git:** For cloning the repository.
- **Administrator privileges:** Required for agent deployment and Event Log access.

### Installation and Deployment

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/edr-prototype.git
cd edr-prototype
```

#### 2. Deploy the Agent (on Windows Endpoints)

On each Windows endpoint you wish to monitor, open PowerShell as an **Administrator** and run the following command:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
./scripts/deploy_agent.ps1
```

This script will:
- Install necessary Python dependencies (`pywin32`).
- Configure the `event_collector.py` to run as a scheduled task or service (future enhancement).
- Start the agent to collect and send data.

#### 3. Set up the Backend (Server)

```bash
cd edr-backend
python -m venv venv
.\venv\Scripts\activate # On Windows
pip install -r requirements.txt
python src/main.py
```

#### 4. Set up the Frontend (Dashboard)

```bash
cd edr-dashboard
pnpm install # or npm install
pnpm run dev # or npm start
```

Access the dashboard at `http://localhost:5173` (or the port indicated by Vite).

## Usage

Once the agent and backend are running, the dashboard will display real-time security events and alerts. You can navigate through different tabs to view recent alerts, event distributions, and analytics.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.

## Contact

For any questions or support, please open an issue on GitHub.


