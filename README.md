Requests API Documentation
Overview

This Requests API is designed to validate and apply Kubernetes resource manifests, specifically for pods and deployments. It is built using FastAPI and communicates with a Minikube cluster.
Requirements

    Python 3.6+
    Packages from requirements.txt:
        fastapi[all]
        uvicorn
        httpx

Installation

    Install Python dependencies:

    bash

    pip install -r requirements.txt

Running the Application

Execute the following command to run the server:

bash

uvicorn main:app --reload

API Endpoints
Validate and Apply Pod

    URL: /validate-and-apply-pod/
    Method: POST
    Description: Validates a pod manifest and, if valid, applies it to a Minikube cluster.
    Request Body:
        Type: application/json
        Content: An instance of PodManifest representing the pod manifest.
    Responses:
        200 OK: Pod manifest is valid and will be applied to Minikube.
        400 Bad Request: Error details if the pod manifest is invalid.

Validate and Apply Deployment

    URL: /validate-and-apply-deployment/
    Method: POST
    Description: Validates a deployment manifest and, if valid, applies it to a Minikube cluster.
    Request Body:
        Type: application/json
        Content: An instance of DeploymentManifest representing the deployment manifest.
    Responses:
        200 OK: Deployment manifest is valid and will be applied to Minikube.
        400 Bad Request: Error details if the deployment manifest is invalid.

Models
PodManifest

    Fields: apiVersion, kind, metadata, spec
    Description: Represents the structure of a Kubernetes Pod manifest.

DeploymentManifest

    Fields: apiVersion, kind, metadata, spec
    Description: Represents the structure of a Kubernetes Deployment manifest.

Classes
KubeManifestHandler

    Purpose: Base class for handling Kubernetes manifests.
    Methods:
        validate_and_apply(manifest, background_tasks): Validates and applies the manifest asynchronously.
        is_valid_manifest(manifest): Checks if the provided manifest matches the expected apiVersion and kind.
        apply_to_minikube(manifest): Submits the manifest to Minikube for application.

PodHandler

    Inherits From: KubeManifestHandler
    Description: Handles the validation and application of Pod manifests.

DeploymentHandler

    Inherits From: KubeManifestHandler
    Description: Handles the validation and application of Deployment manifests.

Error Handling

    Uses HTTP status codes to indicate the success or failure of an API request.
    Provides detailed error messages for invalid manifests.

Security and Authentication

    This API does not include built-in authentication. Implement appropriate security measures as per your deployment requirements.
