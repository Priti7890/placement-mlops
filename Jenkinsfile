pipeline {
    agent any

    environment {
        IMAGE_NAME     = 'placement-predictor'
        CONTAINER_NAME = 'placement-app'
        APP_PORT       = '5000'
    }

    triggers {
        // Poll GitHub every 2 minutes (use a webhook instead if Jenkins is publicly reachable)
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:latest
                    sleep 5
                    curl -f http://localhost:${APP_PORT}/health
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. App running at http://localhost:${APP_PORT}"
        }
        failure {
            echo 'Pipeline failed. Check the console output above.'
        }
    }
}
