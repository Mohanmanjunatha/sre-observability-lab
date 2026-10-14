pipeline {
    agent { label 'built-in' }

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'GitHub checkout completed'
            }
        }

        stage('Validate Project Structure') {
            steps {
                sh '''
                    test -d api-gateway
                    test -d order-service
                    test -d payment-service
                    test -d k8s
                    echo "Project structure validated"
                '''
            }
        }

        stage('Python Syntax Check') {
            steps {
                sh '''
                    for file in api-gateway/app.py order-service/app.py payment-service/app.py; do
                        echo "Checking $file"
                        python3 -m py_compile "$file"
                    done
                '''
            }
        }

        stage('Validate Dockerfiles') {
            steps {
                sh '''
                    test -f api-gateway/Dockerfile
                    test -f order-service/Dockerfile
                    test -f payment-service/Dockerfile
                    echo "All Dockerfiles found"
                '''
            }
        }

        stage('Failure Simulation') {
            steps {
                sh '''
                    if [ -f fail-build.txt ]; then
                        echo "ERROR: Intentional failure detected"
                        exit 1
                    fi
                    echo "Failure simulation passed"
                '''
            }
        }
    }

    post {
        success {
            echo 'PIPELINE SUCCESSFUL'
        }
        failure {
            echo 'PIPELINE FAILED - Check Console Output'
        }
    }
}