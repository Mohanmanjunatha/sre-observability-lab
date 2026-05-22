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

        stage('Validate Project Structure') {
            steps {
                sh '''
                ls -la
                test -d api-gateway
                test -d order-service
                test -d payment-service
                test -d k8s
                '''
            }
        }

        stage('Validate Kubernetes YAML') {
            steps {
                sh '''
                find k8s -name "*.yaml" -print
                '''
            }
        }

        stage('Validate Dockerfiles') {
            steps {
                sh '''
                test -f api-gateway/Dockerfile
                test -f order-service/Dockerfile
                test -f payment-service/Dockerfile
                '''
            }
        }
    }
}