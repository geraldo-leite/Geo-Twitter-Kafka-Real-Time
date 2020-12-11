# Artigo de lista de Emoticons
## https://homepages.dcc.ufmg.br/~fabricio/download/webmedia13%20(1).pdf Artigo Emoticons

from spacy.lang.pt import stop_words
import spacy
import re
import string

modelo_pln = spacy.load('rede-neural-twitter')

pln = spacy.load('pt_core_news_sm')
stop_words = spacy.lang.pt.stop_words.STOP_WORDS

def preprocessamento(texto):
    # convertendo em mínusculas
    texto = texto.lower()

    # remover nome de usuário usando expressão regular
    texto = re.sub(r"@[A-Za-z0-9$-_@.&+]+", ' ', texto)

    # removerndo URL
    texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto)

    # remover espaços em branco
    texto = re.sub(r" +", ' ', texto)

    # remover emoticons
    neutro = 'emocaoneutra'
    positivo = 'emocaopositiva'
    negativo = 'emocaonegativa'

    lista_emoticons = {':)': positivo, ':d': positivo, ':D': positivo, ':]': positivo, ':}': positivo, ':o)': positivo,
                       ':o]': positivo, ':o}': positivo, ':-]': positivo, ':-)': positivo, ':-}': positivo,
                       '=)': positivo,
                       '=]': positivo, '=}': positivo, '=^]': positivo, '=^)': positivo, ':B': positivo,
                       ':-D': positivo,
                       ':-B': positivo, ':^D': positivo, ':^D': positivo, ':^B': positivo, '=B': positivo,
                       '=^B': positivo,
                       '=^D': positivo, ':’)': positivo, ':’]': positivo, ':’}': positivo, '=’)': positivo,
                       '=’]': positivo,
                       '=’}': positivo, '<3': positivo, '^.^': positivo, '^-^': positivo, '^_^': positivo,
                       '^^': positivo,
                       ':*': positivo, '=*': positivo, ':-*': positivo, ';)': positivo, ';]': positivo, ';}': positivo,
                       ':-p': positivo, ':-P': positivo, ':-b': positivo, ':^p': positivo, ':^P': positivo,
                       ':^b': positivo,
                       '=P': positivo, '=p': positivo, ':P': positivo, ':p': positivo, ':b': positivo, '=b': positivo,
                       '=^p': positivo, '=^P': positivo, '=^b': positivo, '\o/': positivo, '\\o\\': positivo,
                       '//o//': positivo,
                       ':(': negativo, 'D:': negativo, 'D=': negativo, 'D-:': negativo, 'D^:': negativo,
                       'D^=': negativo,
                       ':(': negativo, ':[': negativo, ':{': negativo, ':o(': negativo, ':o[': negativo,
                       ':^(': negativo,
                       ':^[': negativo, ':^{': negativo, '=^(': negativo, '=^{': negativo, '>=(': negativo,
                       '>=[': negativo,
                       '>={': negativo, '>=(': negativo, '>:-{': negativo, '>:-[': negativo, '>:-(': negativo,
                       '>=^[': negativo, '>:-(': negativo, ':-[': negativo, ':-(': negativo, '=(': negativo,
                       '=[': negativo,
                       '={': negativo, '=^[': negativo, '>:-=(': negativo, '>=[': negativo, ':’(': negativo,
                       ':’[': negativo,
                       ':’{': negativo, '=’{': negativo, '=’(': negativo, '=’[': negativo, '=\\': negativo,
                       ':\\': negativo,
                       '=/': negativo, ':/': negativo, '=$': negativo, 'o.O': negativo, 'O_o': negativo, 'Oo': negativo,
                       ':$:-{': negativo, '>:-{': negativo, '>=^(': negativo, '>=^{': negativo, ':o{': negativo,
                       ':|': neutro,
                       '=|': neutro, ':-|': neutro, '>.<': neutro, '><': neutro, '>_<': neutro, ':o': neutro,
                       ':0': neutro,
                       '=O': neutro, ':@': neutro, '=@': neutro, ':^o': neutro, ':^@': neutro, '-.-': neutro,
                       '-.-’': neutro,
                       '-_-': neutro, '-_-’': neutro, ':x': neutro, '=X': neutro, '=#': neutro, ':-x': neutro,
                       ':-@': neutro,
                       ':-#': neutro, ':^x': neutro, ':^#': neutro, ':#': neutro}

    for emoticons in lista_emoticons:
        texto = texto.replace(emoticons, lista_emoticons[emoticons])

    # token e lemmatizacao
    documento = pln(texto)

    lista = []
    for token in documento:
        lista.append(token.lemma_)

    # remover stop_words e pontuação
    lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in string.punctuation]

    # retornando ao formato de frase e removendo valores numéricos
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])
    return lista

teste = 'A vida é boa com cerveja'
pre = preprocessamento(teste)
final = modelo_pln(pre)

print('Resultado 1:{}, Resultado 2: {}'.format(pre, final.cats))

