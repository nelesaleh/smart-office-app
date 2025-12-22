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
                sh 'pylint --disable=R,C app.py || true'
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
                    
                    // ✅ التعديل هنا: استخدام الملف الموجود في مساحة العمل (Workspace)
                    env.KUBECONFIG = "${WORKSPACE}/kubeconfig_portable"
                    
                    // ✅ تم إزالة (|| true) لنكتشف الأخطاء الحقيقية إن وجدت
                    sh "kubectl apply -f ${K8S_DIR}/backend.yaml"
                    sh "kubectl apply -f ${K8S_DIR}/monitor.yaml"
                }
            }
        }
    }
}