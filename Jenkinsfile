
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
                    test -f order-service/tests/test_app.py

                    echo "Project structure validated"
                '''
            }
        }

        stage('Python Syntax Check') {
            steps {
                sh '''
                    for file in \
                        api-gateway/app.py \
                        order-service/app.py \
                        payment-service/app.py \
                        order-service/tests/test_app.py
                    do
                        echo "Checking $file"
                        python3 -m py_compile "$file"
                    done

                    echo "Python syntax validation passed"
                '''
            }
        }

        stage('Order Service Unit Tests') {
            steps {
                sh '''
                    set -e

                    python3 -m venv .venv

                    .venv/bin/python -m pip install \
                        -r order-service/requirements.txt \
                        pytest

                    .venv/bin/python -m pytest \
                        order-service/tests \
                        -v \
                        --junitxml=order-service-test-results.xml
                '''
            }

            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'order-service-test-results.xml'
                    )
                }
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

        always {
            echo 'Jenkins CI execution completed'
        }
    }
}
