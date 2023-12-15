pipeline {
    agent any

    environment {
        registry = "752914553472.dkr.ecr.ap-south-1.amazonaws.com"
        awscredential = 'asbm-aws-access-credentials'
        dockerImage = ''
        clusterName = 'asbm_odoo_cluster'
        serviceName = 'asbm-odoo-service'
        awsAccessKeyIdCredential = 'ASBM_AWS_ACCESS_KEY_ID'
        awsSecretAccessKeyCredential = 'ASBM_AWS_SECRET_ACCESS_KEY'
        awsRegion = 'ap-south-1'
        
    }

    stages {

        stage('Pull from GitHub') {
            steps {
                // Wipe out the existing workspace (optional)
                deleteDir()
                // Clone the GitHub repository
                sh "echo 'Checking out the ${branch}.....'"
                checkout([$class: 'GitSCM', branches: [[name: branch]], userRemoteConfigs: [[url: ssh_url]]])
                sh "git checkout main"
            }
        }


        // stage('Push to CodeCommit') {
        //     steps {
        //         // Set the CodeCommit repo as a new remote
        //         sh 'git remote add codecommit ssh://git-codecommit.ap-south-1.amazonaws.com/v1/repos/asbm-odoo'
        //         // Push the branch to CodeCommit
        //         sh 'GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git push codecommit main'
        //     }
        // }

        stage('Building Odoo image') {
                    steps{
                        script {
                            dockerImage = docker.build registry + "/asbm_odoo:latest"
                        }
                    }
                }

        stage('Pushing Odoo image') {
            steps{
                script {
                    docker.withRegistry( 'https://'+ registry, "ecr:ap-south-1:" + awscredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Building Nginx image') {
                steps{
                    dir('nginx'){
                        script {
                            nginxDockerImage = docker.build registry + "/asbm_nginx:latest"
                        }
                    }
                }
            }

        stage('Pushing Nginx image') {
            steps{
                script {
                    docker.withRegistry( 'https://'+ registry, "ecr:ap-south-1:" + awscredential ) {
                        nginxDockerImage.push()
                    }
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
  post {
            always {
                // Send a Slack direct message to the committers about the build status.
                script {
                    def buildStatus = currentBuild.currentResult == 'SUCCESS' ? 'good' : currentBuild.currentResult == 'ABORTED' ? 'warning' : 'danger'
                    def userId = slackUserIdFromEmail(email)
                    def update_message = "Github Repo Name: $repo_name \n\n Commit by: <@$userId> \n\n Commit message : ${commit_message} \n\n Build status of \n${env.JOB_NAME} #${env.BUILD_NUMBER} \n(${env.BUILD_URL}) \nwas *${currentBuild.currentResult}*."
                    slackSend(color: buildStatus, message: update_message, notifyCommitters:true)
                }
            }
            // Your other post-build actions here (e.g., email notifications, cleanup tasks).
        }
}
