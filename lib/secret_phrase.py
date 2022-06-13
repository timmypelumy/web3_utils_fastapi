from bitcoinlib.mnemonic import Mnemonic

ALLOWED_PHRASE_LANGS = ('english', 'french', 'italian',
                        'japanese', 'spanish', 'chinese')


def generate_secret_phrase(lang='english'):
    if ALLOWED_PHRASE_LANGS.index(lang.lower()) == -1:
        raise ValueError("Invalid Language Type For Secret Phrase")

    passphrase = Mnemonic(language=lang).generate()

    return passphrase
