# operator/operator.py
import kopf
import logging
from kubernetes import client, config

# Load Kubernetes config
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()

@kopf.on.startup()
def startup_fn(**kwargs):
    logging.info("DroneOperator: Ready. Watching for new drones...")

@kopf.on.create('simulator.example.com', 'v1', 'drones')
def create_drone(spec, name, namespace, logger, **kwargs):
    drone_id = spec.get('droneID')
    mission = spec.get('mission')
    logger.info(f"Launching drone: {drone_id} | Mission: {mission}")

    # Define pod to launch
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': f'drone-pod-{name}',
            'namespace': namespace,  # Use the namespace passed by Kopf
            'labels': {'app': 'drone-sim', 'drone_cr': name}
        },
        'spec': {
            'containers': [{
                'name': 'drone-sim',
                'image': 'espressored/pdw-drone-sim:latest',  # Your simulator image
                'ports': [{'containerPort': 5000}],
                'env': [{'name': 'DRONE_ID', 'value': drone_id}],
                'resources': {
                    'requests': {'memory': '128Mi', 'cpu': '100m'},
                    'limits': {'memory': '256Mi', 'cpu': '200m'}
                }
            }],
            'restartPolicy': 'Never'
        }
    }

    # Create the pod
    v1.create_namespaced_pod(namespace=namespace, body=pod_manifest)

    # Update Drone status
    return {'phase': 'running', 'podName': f'drone-pod-{name}'}

@kopf.on.delete('simulator.example.com', 'v1', 'drones')
def delete_drone(name, namespace, logger, **kwargs):
    pod_name = f'drone-pod-{name}'
    logger.info(f"Deleting pod: {pod_name}")
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
    except client.ApiException as e:
        if e.status != 404:
            logger.error(f"Failed to delete pod: {e}")
