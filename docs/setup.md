# pdw-c100-isr-sim

This project is a cloud-native simulation system built using Kubernetes operators. It simulates drones performing missions and provides real-time telemetry data. The system demonstrates skills in Kubernetes, automation, and real-time data processing—key requirements for roles in cloud infrastructure and gaming platforms.

---

## **Setup**

### **Prerequisites**
- Kubernetes cluster (local or remote).
- `kubectl` configured to connect to your cluster.
- Docker installed.
- A [Docker Hub](https://hub.docker.com/) account.

### **Steps**
1. Clone the repository:
```bash
   git clone https://github.com/LatteRed/pdw-c100-isr-sim.git
   cd pdw-c100-isr-sim
```

2. Build and upload Docker imagess:
```bash
    docker build -t <your-dockerhub-username>/drone-operator:latest ./operator
```

Build the simulator image:
```bash
docker build -t <your-dockerhub-username>/drone-simulator:latest ./simulator
```

Login to docker hub:
```bash
docker login
```

Push the images you just built
```bash
docker push <yourdockerhub-username>/drone-operator:latest
docker push <your-dockerhub-username>/drone-simulator:latest
```

3. Update image references:
Open the <manifest/operator-deployment.yaml> file and update the image field to point to your upploaded image:
```yaml
image: <your-dockerhub-username>/drone-operator:latest
```

Open the instances/drone1.yaml file and update the image field to point to your uploaded simulator image:

```yaml
image: <your-dockerhub-username>/drone-simulator:latest
```

4. Deploy tthe operator
```bash
kubectl apply -f manifests/operator-rbac.yaml
kubectl apply -f manifests/operator-deployment.yaml
```

5. Create a drone resource:
```bash
kubectl apply -f instances/drone1.yaml
```

6. Fetch telemetry data:
```bash
kubectl port-forward -n drone-sim drone-pod-drone1 5000:5000
curl http://localhost:5000/telemetry
```

Congrats you are now collecting telemetry data from your first drone campaign.

### Teardown
as1. Delete the Drone resource
```bash
kubectl delete -f instances/drone1.yaml
```

2. Delete the operator
```bash
kubectl delete -f manifests/operator-deployment.yaml
kubectl delete -f manifests/operator-rbac.yaml
```

3. Optional. Delete the namespace.
```bash
kubectl delete namespace drone-sim
``` 
