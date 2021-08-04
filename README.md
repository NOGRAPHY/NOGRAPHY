# NOGRAPHY<br>Team Project @HTWG WS2020/21

## What is NOGRAPHY?

NOGRAPHY is an encoding engine, that uses a placeholder text and assigns different fonts to different letters in order to embed information. These fonts are hardly recognizable by sight but easily differentiable for the neural network of the engine, which also contains an error correction mechanism for better stability.

You can use the app here: [NOGRAPHY App](https://nography.cc/)

Boundaries:
- please use short texts and even shorter secrets
- The website is like an old diesel engine: it is slow in the beginning, but then it speeds up.

## Prepare local setup
1. Clone the repository
2. Install Python 3.8.7 (e.g. with pyenv)
3. Install & run [Docker](https://docs.docker.com/engine/install/)
4. Install & run [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

NOTE: There is no further need to install tesseract locally on your system, since it is shipped within the container.

## Invoke Lambdas locally
In the root folder of the project

1. Run `sam build`
2. Run `sam local invoke ExposeFunction -e expose-event.json` to invoke the expose lambda directly
3. Run `sam local invoke HideFunction -e hide-event.json` to invoke hide lambda directly

## Run frontend locally (with prod backend)
In the app folder of the project

1. Run `npm install`
2. Run `npm run dev`
3. Open http://localhost:5000/ in your browser

## Deploy backend
1. You will need AWS credentials, talk to Robert
2. Run `sam build && sam deploy` 

## Deploy frontend
1. Commit and push to master branch
2. Wait ~ 2 minutes
3. Check [https://nography.cc](https://nography.cc) for your changes