pipeline {
    agent {
        // Real-world: Running pipeline steps inside an isolated Docker container
        // Requires Docker Pipeline plugin
        docker { 
            image 'python:3.10-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_IMAGE = 'devops-quickcart'
        DOCKER_TAG = "v${env.BUILD_ID}"
        DOCKER_HUB_USER = 'hetshahrock'
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
            }
        }

        stage('Parallel Code Checks') {
            parallel {
                stage('Linting (Flake8)') {
                    steps {
                        sh 'pip install flake8'
                        sh 'flake8 app.py database.py seed.py || true'
                    }
                }
                stage('Security Scan (Bandit)') {
                    steps {
                        sh 'pip install bandit'
                        sh 'bandit -r app.py database.py seed.py || true'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                // Real docker build execution
                sh "docker build -t ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:latest"
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Authenticating and pushing image to Docker Hub"
                // Requires Jenkins credentials setup
                /*
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_HUB_USER}/${DOCKER_IMAGE}:latest"
                }
                */
                echo "[Mock] Pushed successfully for local dev."
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Applying K8s manifests..."
                /* Real K8s apply using kubectl (assuming kubeconfig is mounted or set)
                sh 'kubectl apply -f k8s/pv-pvc.yaml'
                sh 'kubectl apply -f k8s/secret.yaml'
                sh 'kubectl apply -f k8s/configmap.yaml'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                
                sh "kubectl set image deployment/quickcart-deployment quickcart-app=${DOCKER_HUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "kubectl rollout status deployment/quickcart-deployment"
                */
                echo "[Mock] Kubernetes resources updated!"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline Finished Successfully!"
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
