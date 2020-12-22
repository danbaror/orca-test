pipeline
{
    options
    {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    parameters {
        string(name: 'TAG', defaultValue: 'v01', description: 'Image Tag')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy this image')
        choice(name: 'PUSH_TO', choices: ['ECR', 'Dockerhub', 'All', 'None'], description: 'Push Image to Dockerhub or ECR')

    }
    agent any
    environment 
    {
        VERSION = 'latest'
        PROJECT = 'orca-test'
        IMAGE = 'orca-test:latest'
        ECRURL = 'http://565105851053.dkr.ecr.eu-central-1.amazonaws.com'
        DOCKERHUB_URL = 'https://index.docker.io/v1/'
        ECRCRED = 'ecr:eu-central-1:aws-orca'
    }
    stages
    {
        stage('Build preparations')
        {
            steps
            {
                script 
                {
                    // calculate GIT lastest commit short-hash
                    gitCommitHash = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    shortCommitHash = gitCommitHash.take(7)
                    // calculate a sample version tag
                    VERSION = shortCommitHash
                    // set the build display name
                    currentBuild.displayName = "#${BUILD_ID}-${VERSION}"
                    // IMAGE = "$PROJECT:$VERSION"
                    IMAGE = "$PROJECT:latest"
                }
            }
        }
        stage('Docker build')
        {
            steps
            {
                script {
                   if ( params.PUSH_TO == 'Dockerhub' ) {
                      IMAGE = "$REPO:" + params.TAG
                   } 
                   docker.build("$IMAGE","app")
               }
            }
        }

        stage('Push to ECR/Dockerhub') {
           steps {
              script {
                 if ( params.PUSH_TO == 'ECR' ) {
                    // Push the Docker image to ECR
                    docker.withRegistry(ECRURL, ECRCRED) {
                       def app = docker.image(IMAGE).push()
                    }
                 }
                 if ( params.PUSH_TO == 'Dockerhub' ) {
                    // Push the Docker image to Dockerhub
                    docker.withRegistry(DOCKERHUB_URL, 'Dockerhub') {
                       def app = docker.image(IMAGE).push()
                    } 
                 }
              }
           }
        }
    }
    
    post
    {
        always
        {
            // make sure that the Docker image is removed
            sh "docker rmi $IMAGE | true"
        }
    }
} 

