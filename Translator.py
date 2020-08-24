from google.cloud import translate
from oauth2client import service_account
import json

def translate_text(text,target='en'):
    client_credentials = json.load(open("C:\\Users\\sanam\\Desktop\\AttomusFiles\\CuriousHenry-beta-5153a5857731.json"))

    credentials_token = service_account._JWTAccessCredentials.from_json_keyfile_dict(client_credentials)
    translate_client = translate.Client(credentials_token)
    result = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))

def translate_(text,credentials):
    client_credentials = json.load(open(credentials))

    credentials_token = service_account._JWTAccessCredentials.from_json_keyfile_dict(client_credentials)
    translate_client = translate.Client(credentials_token)
    result = translate_client.translate(text,target_language='en')
    return result['translatedText']


def isEnglishText(text, credentials):
    isEnglish = False
    client_credentials = json.load(open(credentials))
    credentials_token = service_account._JWTAccessCredentials.from_json_keyfile_dict(client_credentials)
    translate_client = translate.Client(credentials_token)
    result = translate_client.translate(text, target_language='en')
    if (result['detectedSourceLanguage']  == "en"):
        isEnglish = True

    return isEnglish


if __name__ == '__main__':
  #main()
  print(translate_text("lisüult_de tekkimisel, anurtisatsioonitumide ja ekspluatatsiomikulude muuturnisel.","en"))