pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nelerayan/smart-office-backend"
        DOCKER_TAG = "latest"
        // رابط مستودع الـ DevOps الخاص بك
        DEVOPS_REPO_URL = "https://github.com/nelesaleh/smart-office-devops.git"
        K8S_DIR = "k8s_configs"
    }

    stages {
        stage('Checkout DevOps Repo') {
            steps {
                script {
                    // سحب ملفات الكوبرنيتس من المستودع الثاني
                    sh "rm -rf ${K8S_DIR}"
                    dir(K8S_DIR) {
                        git branch: 'main', url: "${DEVOPS_REPO_URL}"
                    }
                }
            }
        }

        stage('Build & Push Docker') {
            steps {
                script {
                    // تسجيل الدخول وبناء الصورة (تأكد من إعداد بيانات الدخول في Jenkins لاحقاً)
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def appImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        appImage.push()
                    }
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                // تطبيق ملفات الـ Deployment والمراقبة
                sh "kubectl apply -f ${K8S_DIR}/backend.yaml"
                sh "kubectl apply -f ${K8S_DIR}/monitor.yaml"
                // انتظار التحديث
                sh "kubectl rollout status deployment/smart-office-backend --timeout=60s"
            }
        }
    }
}
