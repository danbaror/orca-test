node {
   def commit_id
   stage('Preparation') {
     checkout scm
     sh "git rev-parse --short HEAD > .git/commit-id"                        
     commit_id = readFile('.git/commit-id').trim()
   }
   stage('docker build/push') {
     docker.withRegistry('https://index.docker.io/v1/', 'Dockerhub') {
       def app = docker.build("danbaror/orca-app:${commit_id}", '.').push()
     }
   }
}
