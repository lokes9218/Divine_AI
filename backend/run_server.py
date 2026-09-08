import sys
import os
import logging
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    print("Starting Uvicorn Server on http://127.0.0.1:8001 ...", flush=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False, log_level="info")
