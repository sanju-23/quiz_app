pipeline {
    agent any

    environment {
        IMAGE_NAME = "quizapp"
        CONTAINER_NAME = "quizapp"
        ENV_PATH = "/home/ubuntu/quiz_app/.env"
    }

    stages {
        stage('Clone Repository') {
            steps {
               git branch: 'main', url: 'https://github.com/sanju-23/quiz_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }
        
        stage("Push to Docker Hub"){
            steps {
                echo "Pushing the image to docker hub"
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
                sh "docker tag ${IMAGE_NAME}:latest ${env.dockerHubUser}/quizapp:latest"
                sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                sh "docker push ${env.dockerHubUser}/quizapp:latest"
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
                    sh """
                        docker run -d -p 5000:5000 \\
                        --env-file=${ENV_PATH} \\
                        --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }
}
