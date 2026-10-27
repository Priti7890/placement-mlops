pipeline {
    agent any

    environment {
        IMAGE_NAME     = 'placement-predictor'
        CONTAINER_NAME = 'placement-app'
        APP_PORT       = '5000'
        PATH           = "C:\Program Files\Docker\Docker\resources\bin;${env.PATH}"
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker run --rm %IMAGE_NAME%:latest python -m pytest -v'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                    docker rm -f %CONTAINER_NAME%
                    docker run -d --name %CONTAINER_NAME% -p %APP_PORT%:5000 %IMAGE_NAME%:latest
                    ping -n 8 127.0.0.1 > nul
                    curl.exe -f http://localhost:%APP_PORT%/health
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
