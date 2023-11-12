from pydantic import BaseModel

class PodManifest(BaseModel):
    apiVersion: str
    kind: str
    metadata: dict
    spec: dict

class DeploymentManifest(BaseModel):
    apiVersion: str
    kind: str
    metadata: dict
    spec: dict