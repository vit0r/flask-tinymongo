# flask-tinymongo-docker

## Build image
`docker build -t flask_tinymongo:dev .`

## Create volume
`docker volume create volume_mocks`

## Docker Run
`docker run -d --name flasktinymongo --hostname fmhost001 -v volume_mocks:/mock_app/mocks -p 5000:5000 flask_tinymongo:dev`
