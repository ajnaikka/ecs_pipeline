pipeline {
    agent any

    environment {
        registry = "381492301317.dkr.ecr.ap-south-1.amazonaws.com"
        awscredential = 'gautham-aws-root-id'
        dockerImage = ''
        clusterName = 'ecs_odoo_cluster'
        serviceName = 'ecs-odoo-service'
        awsAccessKeyIdCredential = 'AWS_ACCESS_KEY_ID'
        awsSecretAccessKeyCredential = 'AWS_SECRET_ACCESS_KEY'
        awsRegion = 'ap-south-1'
        
    }

    stages {

            stage('Checkout') {
                 steps {
                     script {
                    def gitInfo = checkout scm
                    env.repo_name = gitInfo.GIT_URL.split('/')[-1].replace('.git', '')
                }
            }
        }
    


        // stage('Push to CodeCommit') {
        //     steps {
        //         // Set the CodeCommit repo as a new remote
        //         sh 'git remote add codecommit ssh://git-codecommit.ap-south-1.amazonaws.com/v1/repos/ecs-odoo'
        //         // Push the branch to CodeCommit
        //         sh 'GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git push codecommit main'
        //     }
        // }

        stage('Building Odoo image') {
                    steps{
                        script {
                            dockerImage = docker.build registry + "/ecs_odoo:latest"
                        }
                    }
                }

        stage('Pushing Odoo image') {
            steps{
                script {
                   sh "docker push 381492301317.dkr.ecr.ap-south-1.amazonaws.com/ecs_odoo:latest"
                }
            }
        }
        stage('Building Nginx image') {
                steps{
                    dir('nginx'){
                        script {
                            nginxDockerImage = docker.build registry + "/ecs_nginx:latest"
                        }
                    }
                }
            }

        stage('Pushing Nginx image') {
            steps{
                script {
                     sh "docker push 381492301317.dkr.ecr.ap-south-1.amazonaws.com/ecs_nginx:latest"
                }
            }
        }
        stage('Deploy to ECS') {
            steps {
                script {
                    withCredentials([string(credentialsId: awsAccessKeyIdCredential, variable: 'AWS_ACCESS_KEY_ID'),
                                     string(credentialsId: awsSecretAccessKeyCredential, variable: 'AWS_SECRET_ACCESS_KEY')]) {
                        // Update ECS service with the new task definition
                        sh "aws ecs update-service --cluster ${clusterName} --service ${serviceName} --force-new-deployment --region ${awsRegion}"

                        // Wait for the deployment to complete
                        sh "aws ecs wait services-stable --cluster ${clusterName} --services ${serviceName} --region ${awsRegion}"
                    }
                }
            }
        }
    }
}
