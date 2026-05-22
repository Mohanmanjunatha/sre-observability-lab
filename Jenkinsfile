pipeline {
    agent {
    label 'built-in'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                eval $(minikube docker-env)
                docker build -t sre-observability-lab-api-gateway:latest ./api-gateway
                docker build -t sre-observability-lab-order-service:latest ./order-service
                docker build -t sre-observability-lab-payment-service:latest ./payment-service
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/
                kubectl rollout restart deployment api-gateway
                kubectl rollout restart deployment order-service
                kubectl rollout restart deployment payment-service
                '''
            }
        }

        stage('Verify Rollout') {
            steps {
                sh '''
                kubectl rollout status deployment/api-gateway
                kubectl rollout status deployment/order-service
                kubectl rollout status deployment/payment-service
                '''
            }
        }
    }
}
