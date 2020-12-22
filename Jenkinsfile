pipeline {

   options {
      buildDiscarder(logRotator(numToKeepStr: '3'))
   }
   agent any
   environment {
      IMAGE = 'orca-test:v05'
      ECR_URL = '565105851053.dkr.ecr.eu-central-1.amazonaws.com/orca-test'
      ECR_CRED = 'aws:orca'
   }
   stages {
      def commit_id
      stage('Preparation') {
         checkout scm
         sh "git rev-parse --short HEAD > .git/commit-id"                        
         commit_id = readFile('.git/commit-id').trim()
      }
      stage('Dockerhub build/push') {
         when {
            expression { params.PushDestination == 'Dockerhub' }
         }
         steps {
            docker.withRegistry('https://index.docker.io/v1/', 'Dockerhub') {
               def app = docker.build("danbaror/orca-app:${commit_id}", './app').push()
            }
         }
      }
      stage('ECR build/push') {
         when {
            expression { params.PushDestination == 'ECR' }
         }
         steps {
            // sh("eval \$(aws ecr get-login --no-include-email | sed 's|https://||')")
            docker.withRegistry( ECR_URL, ECR_CRED) {
               // Build the docker image using a Dockerfile
               def app = docker.build("danbaror/orca-app:${commit_id}", './app').push()
            }
         }
      }
   }
}

