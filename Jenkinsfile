pipeline
{
    options
    {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    agent any
    environment 
    {
        VERSION = params.Tag
        PROJECT = 'orca-test'
        IMAGE = 'orca-test:latest'
        ECRURL = 'http://565105851053.dkr.ecr.eu-central-1.amazonaws.com'
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
        stage('Push to ECR') {
           when { 
              expression { param.PushDestination == "ECR" }
              steps {
                 script {
                    // Push the Docker image to ECR
                    docker.withRegistry(ECRURL, ECRCRED) {
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

