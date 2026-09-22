"""
SPECTRA Cloud AI Model Deployment Script.
Enables hosting and serving the trained Signal Intelligence Neural Model
on Modal.com (cloud GPU/CPU serverless) or as a standalone cloud REST microservice.

Usage:
  1. For Modal.com deployment:
     $ pip install modal
     $ modal setup
     $ modal deploy backend/ai_engine/cloud_modal_deploy.py

  2. For Standalone Cloud Container / FastAPI Cloud:
     $ python backend/ai_engine/cloud_modal_deploy.py --serve --port 8080
"""

import sys
import argparse
import numpy as np

# Modal cloud definition (optional if modal package is installed)
try:
    import modal
    app = modal.App("spectra-signal-intelligence-ai")
    image = modal.Image.debian_slim().pip_install("numpy", "scipy", "fastapi", "uvicorn")

    @app.function(image=image, cpu=2, memory=1024)
    @modal.web_endpoint(method="POST")
    def cloud_predict_signal(payload: dict):
        """Cloud Serverless Inference Endpoint."""
        from features import extract_signal_features
        from model import SignalAIModel

        model = SignalAIModel()
        iq_real = np.array(payload.get("real", []), dtype=np.float32)
        iq_imag = np.array(payload.get("imag", []), dtype=np.float32)
        sample_rate = float(payload.get("sample_rate", 1e6))

        samples = iq_real + 1j * iq_imag
        res = model.predict(samples, sample_rate=sample_rate)
        res["cloud_provider"] = "Modal Serverless AI Worker"
        return res

except ImportError:
    modal = None


def run_standalone_cloud_server(port: int = 8080):
    """Run lightweight standalone cloud server."""
    from fastapi import FastAPI
    import uvicorn
    from model import SignalAIModel

    cloud_app = FastAPI(title="SPECTRA Cloud AI Signal Intelligence Worker", version="2.8.0")
    model = SignalAIModel()

    @cloud_app.get("/health")
    def health():
        return {"status": "ONLINE", "model_version": model.version, "accuracy": f"{model.accuracy:.1f}%"}

    @cloud_app.post("/predict")
    def predict(payload: dict):
        iq_real = np.array(payload.get("real", []), dtype=np.float32)
        iq_imag = np.array(payload.get("imag", []), dtype=np.float32)
        sample_rate = float(payload.get("sample_rate", 1e6))

        samples = iq_real + 1j * iq_imag
        res = model.predict(samples, sample_rate=sample_rate)
        res["cloud_provider"] = "SPECTRA Cloud Worker Node"
        return res

    print(f"[*] Starting SPECTRA Cloud AI Inference Server on port {port}...")
    uvicorn.run(cloud_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPECTRA Cloud AI Deployment")
    parser.add_argument("--serve", action="store_true", help="Run local standalone server")
    parser.add_argument("--port", type=int, default=8080, help="Port for standalone server")
    args = parser.parse_args()

    if args.serve:
        run_standalone_cloud_server(args.port)
    else:
        print("To deploy to Modal cloud: modal deploy backend/ai_engine/cloud_modal_deploy.py")
        print("To run as standalone cloud worker: python backend/ai_engine/cloud_modal_deploy.py --serve")
