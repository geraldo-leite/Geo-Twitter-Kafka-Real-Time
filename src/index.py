from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
from pykafka import KafkaClient
import json
import preprocessamento
import spacy

# Carregando a Rede Neural
modelo_pln = spacy.load('Mod_twitter')

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092', broker_version='0.10.0')

class StdOutListener(StreamListener):
    def on_data(self, data):
        #print(data)
        message = json.loads(data)

        if message['place'] is not None:

            message['Pre_Txt'] = preprocessamento.preprocessamento(message['text'])
            previsao = modelo_pln(message['Pre_Txt'])
            #print(previsao)
            #print(previsao.cats)

            lista_prev = []
            lista_prev.append(previsao.cats)

            classe_prev = []
            for i in lista_prev:

                if i['POSITIVO'] > 0.70:
                    classe_prev.append(0)
                elif i['NEGATIVO'] > 0.70:
                    classe_prev.append(1)
                else:
                    classe_prev.append(3)

            #print(classe_prev)
            #print(message)
            message['Sentimento'] = classe_prev
            tweet = json.dumps(message)

            client = get_kafka_client()  # Função para instânciar o kafkaclient
            topic = client.topics['twitterdata1']  # Especificamos em qual tópico vamos retornar os dados
            producer = topic.get_sync_producer()  # Depois de obter um Tópico , você pode criar um Produtor para ele e começar a produzir mensagens.
            # Produzindo as mensagens
            producer.produce(tweet.encode('ascii'))

        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)

    listener = StdOutListener()
    stream = Stream(auth, listener)
    #stream.filter(track=['BUSCA-POR-PALAVRA-CHAVE'])
    stream.filter(locations=[-180, -90, 180, 90])  # Filtrando Por localizção
