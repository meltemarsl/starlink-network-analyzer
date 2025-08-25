# starlink-network-analyzer
Starlink Network Analyzer

## Project Overview

The project implements a **Flask-based orchestrator** that executes network tests sequentially and collects metrics.  
Current MVP includes:

- TCP and UDP throughput tests (using iPerf3)
- IRRT (Instant Round-Trip Time) test
- Results are saved as JSON files in the `results/` folder
- Configurable tests via `config.yaml`
- Flask API endpoints to start tests

---

## Requirements

- Python 3.10+
- Virtual environment recommended
- iPerf3 installed on both client and server machine

## Setup

1. Clone the repository
```bash
git clone https://github.com/meltemarsl/starlink-network-analyzer.git
cd starlink-network-analyzer
```

2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. (Optional) Configure tests in config.yaml


## Usage

1. Start iPerf3 server on the server machine (or your local machine for testing)
```bash
iperf3 -s
```

2. Start the Flask orchestrator
```bash
python3 app.py
```

3. Run all tests via API
```bash
curl -X POST http://127.0.0.1:8000/start
```

4. Results will be saved in results/ folder as JSON files.
