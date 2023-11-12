from fastapi import FastAPI, HTTPException, BackgroundTasks
import httpx
from typing import Dict, Any
from models.models import PodManifest, DeploymentManifest

app = FastAPI()
MINIKUBE_CONNECTOR_URL = "http://localhost:8001"

class KubeManifestHandler:
    def __init__(self, api_version: str, kind: str, endpoint: str):
        self.api_version = api_version
        self.kind = kind
        self.endpoint = endpoint

    async def validate_and_apply(self, manifest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
        """Validates the structure of the request and sends the body to appl"""
        if not self.is_valid_manifest(manifest):
            raise HTTPException(status_code=400, detail=f"Invalid {self.kind} manifest.")
        background_tasks.add_task(self.apply_to_minikube, manifest.dict())
        return {"status": f"{self.kind} manifest is valid. Applying to Minikube."}

    def is_valid_manifest(self, manifest) -> bool:
        return manifest.apiVersion == self.api_version and manifest.kind == self.kind

    async def apply_to_minikube(self, manifest: Dict[str, Any]) -> None:
        """Applies the pod of deployment to minikube"""
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{MINIKUBE_CONNECTOR_URL}{self.endpoint}", json=manifest)
            if response.status_code != 200:
                print(f"Failed to apply to Minikube. Reason: {response.text}")

class PodHandler(KubeManifestHandler):
    def __init__(self):
        super().__init__(api_version="v1", kind="Pod", endpoint="/apply-pod/")

class DeploymentHandler(KubeManifestHandler):
    def __init__(self):
        super().__init__(api_version="apps/v1", kind="Deployment", endpoint="/apply-deployment/")

@app.post("/validate-and-apply-pod/")
async def validate_and_apply_pod(manifest: PodManifest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    handler = PodHandler()
    return await handler.validate_and_apply(manifest, background_tasks)

@app.post("/validate-and-apply-deployment/")
async def validate_and_apply_deployment(manifest: DeploymentManifest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    handler = DeploymentHandler()
    return await handler.validate_and_apply(manifest, background_tasks)
