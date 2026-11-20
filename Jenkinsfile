pipeline {
    agent any

    environment {
        APP_NAME = "app-devsecops-ev3"
        NETWORK_NAME = "devsecops-net"
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('3. SAST - Bandit') {
            steps {
                script {
                    def status = sh(script: 'bandit -r . -ll -f txt -o bandit-report.txt', returnStatus: true)
                    sh 'cat bandit-report.txt || true'
                    archiveArtifacts artifacts: 'bandit-report.txt', allowEmptyArchive: true
                    if (status != 0) {
                        unstable("SAST (Bandit) detectó vulnerabilidades en el código fuente.")
                    }
                }
            }
        }

        stage('4. Deploy Temporal') {
            steps {
                sh '''
                    docker network create ${NETWORK_NAME} || true
                    docker rm -f ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} --network ${NETWORK_NAME} -p 5050:5000 ${APP_NAME}:${BUILD_NUMBER}
                    sleep 5
                '''
            }
        }

        stage('5. DAST - OWASP ZAP') {
            steps {
                script {
                    def zapStatus = sh(
                        script: '''
                            mkdir -p zap-wrk
                            chmod 777 zap-wrk
                            docker run --rm --network ${NETWORK_NAME} -v $(pwd)/zap-wrk:/zap/wrk:rw ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://${APP_NAME}:5000 -r zap-report.html -I
                        ''',
                        returnStatus: true
                    )
                    archiveArtifacts artifacts: 'zap-wrk/zap-report.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f ${APP_NAME} || true
                docker network rm ${NETWORK_NAME} || true
            '''
        }
    }
}