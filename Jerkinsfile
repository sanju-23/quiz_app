pipeline {
    agent any

    environment {
        IMAGE_NAME = "quizapp"
        CONTAINER_NAME = "quizapp"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/sanju-23/quiz_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Stop Old Container (if running)') {
            steps {
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                }
            }
        }

        stage('Run New Container') {
            steps {
                script {
                    sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }
}

