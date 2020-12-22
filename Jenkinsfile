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
                    IMAGE = "$PROJECT:$VERSION"
                }
            }
        }
        stage('Docker build')
        {
            steps
            {
                script
                {
                    // Build the docker image using a Dockerfile
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
                       docker.image(IMAGE).push()
                    }
                 }
                 if ( params.PUSH_TO == 'Dockerhub' ) {
                    // Push the Docker image to Dockerhub
                    docker.withRegistry(DOCKERHUB_URL, 'Dockerhub') {
                    IMAGE = 'danbaror/' + "$PROJECT:" + params.TAG
                    // docker.withRegistry('https://index.docker.io/v1/', 'Dockerhub') {
                       docker.image(IMAGE).push()
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

