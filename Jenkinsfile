pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nelerayan/smart-office-backend"
        DOCKER_TAG = "latest"
        DEVOPS_REPO_URL = "https://github.com/nelesaleh/smart-office-devops.git"
        K8S_DIR = "k8s_configs"
        DOCKER_CREDS = credentials('docker-hub-credentials')
        
        // ⚠️ Ensure this ID matches the one you created in Jenkins for your kubeconfig
        K8S_CRED_ID = 'k8s-kubeconfig' 
    }

    stages {
        stage('Checkout DevOps Repo') {
            steps {
                script {
                    // Pulling the K8s YAML files from the DevOps repo
                    sh "rm -rf ${K8S_DIR}"
                    dir(K8S_DIR) {
                        git branch: 'main', url: "${DEVOPS_REPO_URL}"
                    }
                }
            }
        }

        stage('Lint Code') {
            steps {
                // 📂 UPDATED: Using 'smart-office-app' since the folder was not renamed
                dir('smart-office-app') { 
                    echo '🔍 Linting Code...'
                    sh 'pip install pylint flask || true'
                    // Using run.py as discussed previously
                    sh 'pylint --disable=R,C run.py || true'
                }
            }
        }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    // 📂 UPDATED: Pointing to 'smart-office-app' to find the Dockerfile
                    dir('smart-office-app') {
                        echo "🐳 Logging into Docker Hub..."
                        sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
                        
                        echo "🔨 Building Image..."
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        
                        echo "🚀 Pushing Image..."
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    }
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                script {
                    echo "☸️ Deploying to Kubernetes..."
                    
                    // ✅ FIXED: Using withKubeConfig to inject credentials securely
                    // This prevents the HTML/Login error you saw earlier
                    withKubeConfig([credentialsId: K8S_CRED_ID]) {
                        
                        // Apply the configuration
                        sh "kubectl apply -f ${WORKSPACE}/${K8S_DIR}/backend.yaml --validate=false"
                        
                        // Force restart to pull the new image
                        sh "kubectl rollout restart deployment smart-office-backend"
                        
                        // Optional: Check status to see if pods are coming up
                        sh "kubectl get pods"
                    }
                    
                    echo "✅ Deploy Finished!"
                }
            }
        }
    }
}