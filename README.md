# Steganography Team Project @HTWG WS2020/21
[![Build Status](https://travis-ci.com/steganographie-HTWG/steganographie.svg?branch=master)](https://travis-ci.com/github/steganographie-HTWG/steganographie)

## Local Setup
1. Clone the repo
2. Install Python 3.8.7 (e.g. with pyenv)
3. Have an IDE ready (e.g. Visual Studio Code or PyCharm)
4. `pip3 install -r requirements.txt` to install dependencies
5. `pytest` executes all test
6. Run __main__ in /hide/app.py
7. Run __main__ in /expose/app.py (not possible yet)
8. For the Frontend `cd app` and then `npm run dev`
9. TODO: shorten: We use tesseract for ocr, so you need to install it (and add it to your $PATH) to use the ocr package.
For Multilanguage-Support you need to download the advanced tessdata folder from Github: https://github.com/tesseract-ocr/tessdata. Now you have to set the TESSDATA_PREFIX path to the tessdata folder.

## Deploy to AWS
### Backend
We use AWS Lambda for the updated embedding process. In order to deploy it, you need credentials (talk to Robert).
If that is set up, execute `sam build && sam deploy` to deploy.
### Frontend
In order to deploy the frontend, `cd app` then `npm run build` then zip the content of the app/public folder and upload it to Amplify.

## TODO: Which problem does the nography project solve?
- hide texts in placeholder texts
- english letters only