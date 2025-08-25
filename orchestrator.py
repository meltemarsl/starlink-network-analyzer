import subprocess, yaml, json, time, os

RESULTS_DIR = "results"

# should check starlink connection
def iface_up(iface, host="8.8.8.8"):
    return True

def run_iperf(server, iface, params):
    cmd = ["iperf3", "-c", server, "-J", "-t", str(params["duration_ms"]//1000)]
    if params["proto"] == "udp":
        cmd.append("-u")
        if "bitrate" in params:
            cmd += ["-b", params["bitrate"]]
    print("Running:", " ".join(cmd))
    try:
        output = subprocess.check_output(cmd, text=True)
        return json.loads(output)
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}
    
def run_irtt(host, params):
    freq = params.get("frequency_ms", 100)
    duration = params.get("duration_ms", 1000) / 1000
    end_time = time.time() + duration
    results = []
    
    while time.time() < end_time:
        start = time.time()
        try:
            subprocess.check_output(["ping", "-c", "1", "-W", "1", host], stderr=subprocess.DEVNULL)
            rtt = (time.time() - start) * 1000  # ms
            results.append(rtt)
        except subprocess.CalledProcessError:
            results.append(None)
        time.sleep(freq/1000)
    
    return {"job":"irtt","status":"success","params":params,"rtt_ms":results}

def save_result(result, job_name):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(RESULTS_DIR, f"{job_name}_{ts}.json")
    with open(path,"w") as f:
        json.dump(result,f,indent=2)
    print(f"Saved result -> {path}")

class Orchestrator:
    def __init__(self, config_path="config.yaml"):
        with open(config_path,"r") as f:
            self.config = yaml.safe_load(f)
        self.server = self.config.get("server_host","127.0.0.1")

    def run_test(self,test):
        job = test["job"]
        iface = test["interface"]
        params = test["parameters"]

        while not iface_up(iface,self.server):
            print(f"Waiting for iface {iface} to come up...")
            time.sleep(2)

        if job == "iperf":
            result = run_iperf(self.server,iface,params)
            save_result(result,f"{job}_{params.get('proto','unknown')}")
            return result
        elif job=="irtt":
            result = run_irtt(self.server, params)
            save_result(result,"irtt")
            return result
        else:
            return {"job":job,"status":"unknown"}

    def run_all_tests(self):
        results=[]
        for test in self.config["tests"]:
            results.append(self.run_test(test))
        return results
