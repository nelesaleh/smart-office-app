pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nelerayan/smart-office-backend"
        DOCKER_TAG = "latest"
        DEVOPS_REPO_URL = "https://github.com/nelesaleh/smart-office-devops.git"
        K8S_DIR = "k8s_configs"
        DOCKER_CREDS = credentials('docker-hub-credentials')
    }

    stages {
        stage('Checkout DevOps Repo') {
            steps {
                script {
                    sh "rm -rf ${K8S_DIR}"
                    dir(K8S_DIR) {
                        git branch: 'main', url: "${DEVOPS_REPO_URL}"
                    }
                }
            }
        }

        stage('Lint Code') {
            steps {
                echo '🔍 Linting Code...'
                sh 'pip install pylint flask || true'
                
                // UPDATE 1: Changed to 'run.py' because 'app.py' no longer exists or is not the main entry point
                sh 'pylint --disable=R,C run.py || true'
            }
        }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    echo "🐳 Logging into Docker Hub..."
                    sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
                    
                    echo "🔨 Building Image..."
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    echo "🚀 Pushing Image..."
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                script {
                    echo "☸️ Deploying to Kubernetes..."
                    
                    env.KUBECONFIG = "${WORKSPACE}/kubeconfig_portable"
                    
                    // Apply the configuration (using validate=false to skip strict API checks)
                    sh "kubectl apply -f ${K8S_DIR}/backend.yaml --validate=false"
                    // sh "kubectl apply -f ${K8S_DIR}/monitor.yaml --validate=false"

                    // UPDATE 2: Force Kubernetes to restart the pods to pull the new image
                    // Without this, K8s might keep running the old image since the YAML didn't change
                    sh "kubectl rollout restart deployment smart-office-backend"
                    
                    echo "✅ Deploy Finished!"
                }
            }
        }
    }
}