pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nelerayan/smart-office-backend"
        DOCKER_TAG = "latest"
        DEVOPS_REPO_URL = "https://github.com/nelesaleh/smart-office-devops.git"
        K8S_DIR = "k8s_configs"
        DOCKER_CREDS = credentials('docker-hub-credentials')
        K8S_CRED_ID = 'k8s-kubeconfig' 
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
                // ✅ تم التعديل: إزالة dir لأن الملفات في المجلد الرئيسي
                echo '🔍 Linting Code...'
                sh 'pip install pylint flask || true'
                sh 'pylint --disable=R,C run.py || true'
            }
        }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    // ✅ تم التعديل: إزالة dir لأن الـ Dockerfile في المجلد الرئيسي
                    echo "🐳 Logging into Docker Hub..."
                    sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
                    
                    echo "🔨 Building Image..."
                    // الآن سيبحث عن Dockerfile في المكان الحالي (.)
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
                    withKubeConfig([credentialsId: K8S_CRED_ID]) {
                        sh "kubectl apply -f ${WORKSPACE}/${K8S_DIR}/backend.yaml --validate=false"
                        sh "kubectl rollout restart deployment smart-office-backend"
                    }
                    echo "✅ Deploy Finished!"
                }
            }
        }
    }
}