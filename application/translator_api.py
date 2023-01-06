from os import getenv, environ
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from boto3 import client


def translate_en(word):
    translate = client(service_name='translate',
                        region_name='us-west-2',
                        use_ssl=True)
    result = translate.translate_text(Text=word,
                                    SourceLanguageCode="en",
                                    TargetLanguageCode="es")
    translation = result.get("TranslatedText")
    print(translation)
    return translation

def translate_es(word):
    translate = client(service_name='translate',
                        region_name='us-west-2',
                        use_ssl=True)
    result = translate.translate_text(Text=word,
                                    SourceLanguageCode="es",
                                    TargetLanguageCode="en")
    translation = result.get("TranslatedText")
    print(translation)
    return translation


