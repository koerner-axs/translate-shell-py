# Close translation of file translate-shell/include/LanguageData.awk
#
# Locale and language data from various sources.
import os
import re
import subprocess
import sys

from src.theme import prettify

# Description from source:
# > Initialize all locales supported.
# > Mostly ISO 639-1 codes, with a few ISO 639-3 codes.
# > 'family' : Language family (from Glottolog)
# > 'iso'    : ISO 639-3 code
# > 'glotto' : Glottocode
# > 'script' : Writing system (ISO 15924 script code)
# > See: <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>
# >      <https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes>
# >      <https://en.wikipedia.org/wiki/ISO_15924#List_of_codes>
# >      <http://glottolog.org/>

LOCALES = {}
LOCALE_ALIAS = {}

def _for_code(locale_code: str) -> dict:
    if locale_code in LOCALES:
        return LOCALES[locale_code]
    locale_dict = LOCALES[locale_code] = dict()
    return locale_dict


def init_locales():
    # Afrikaans
    _for_code('af')['name']               = 'Afrikaans'
    _for_code('af')['endonym']            = 'Afrikaans'
    _for_code('af')['translations-of']    = 'Vertalings van %s'
    _for_code('af')['definitions-of']     = 'Definisies van %s'
    _for_code('af')['synonyms']           = 'Sinonieme'
    _for_code('af')['examples']           = 'Voorbeelde'
    _for_code('af')['see-also']           = 'Sien ook'
    _for_code('af')['family']             = 'Indo-European'
    _for_code('af')['branch']             = 'West Germanic'
    _for_code('af')['iso']                = 'afr'
    _for_code('af')['glotto']             = 'afri1274'
    _for_code('af')['script']             = 'Latn'
    _for_code('af')['spoken-in']          = 'South Africa; Namibia'
    _for_code('af')['supported-by']       = 'google; bing; yandex'

    # Albanian
    _for_code('sq')['name']               = 'Albanian'
    _for_code('sq')['endonym']            = 'Shqip'
    _for_code('sq')['endonym2']           = 'Gjuha shqipe'
    _for_code('sq')['translations-of']    = 'Përkthimet e %s'
    _for_code('sq')['definitions-of']     = 'Përkufizime të %s'
    _for_code('sq')['synonyms']           = 'Sinonime'
    _for_code('sq')['examples']           = 'Shembuj'
    _for_code('sq')['see-also']           = 'Shihni gjithashtu'
    _for_code('sq')['family']             = 'Indo-European'
    _for_code('sq')['branch']             = 'Paleo-Balkan'
    _for_code('sq')['iso']                = 'sqi'
    _for_code('sq')['glotto']             = 'alba1267'
    _for_code('sq')['script']             = 'Latn'
    _for_code('sq')['spoken-in']          = 'Albania; Kosovo; Montenegro; North Macedonia'
    _for_code('sq')['supported-by']       = 'google; bing; yandex'

    # Amharic
    _for_code('am')['name']               = 'Amharic'
    _for_code('am')['endonym']            = 'አማርኛ'
    _for_code('am')['translations-of']    = 'የ %s ትርጉሞች'
    _for_code('am')['definitions-of']     = 'የ %s ቃላት ፍችዎች'
    _for_code('am')['synonyms']           = 'ተመሳሳይ ቃላት'
    _for_code('am')['examples']           = 'ምሳሌዎች'
    _for_code('am')['see-also']           = 'የሚከተለውንም ይመልከቱ'
    _for_code('am')['family']             = 'Afro-Asiatic'
    _for_code('am')['branch']             = 'Semitic'
    _for_code('am')['iso']                = 'amh'
    _for_code('am')['glotto']             = 'amha1245'
    _for_code('am')['script']             = 'Ethi'
    _for_code('am')['spoken-in']          = 'Ethiopia'
    _for_code('am')['supported-by']       = 'google; bing; yandex'

    # Arabic (Modern Standard Arabic)
    _for_code('ar')['name']               = 'Arabic'
    _for_code('ar')['endonym']            = 'العربية'
    _for_code('ar')['translations-of']    = 'ترجمات %s'
    _for_code('ar')['definitions-of']     = 'تعريفات %s'
    _for_code('ar')['synonyms']           = 'مرادفات'
    _for_code('ar')['examples']           = 'أمثلة'
    _for_code('ar')['see-also']           = 'انظر أيضًا'
    _for_code('ar')['family']             = 'Afro-Asiatic'
    _for_code('ar')['branch']             = 'Semitic'
    _for_code('ar')['iso']                = 'ara'
    _for_code('ar')['glotto']             = 'stan1318'
    _for_code('ar')['script']             = 'Arab'
    _for_code('ar')['rtl']                = 'true' # RTL language
    _for_code('ar')['spoken-in']          = 'the Arab world'
    _for_code('ar')['supported-by']       = 'google; bing; yandex'

    # Armenian (Eastern Armenian)
    _for_code('hy')['name']               = 'Armenian'
    _for_code('hy')['endonym']            = 'Հայերեն'
    _for_code('hy')['translations-of']    = '%s-ի թարգմանությունները'
    _for_code('hy')['definitions-of']     = '%s-ի սահմանումները'
    _for_code('hy')['synonyms']           = 'Հոմանիշներ'
    _for_code('hy')['examples']           = 'Օրինակներ'
    _for_code('hy')['see-also']           = 'Տես նաև'
    _for_code('hy')['family']             = 'Indo-European'
    #for_code('hy')['branch']            = 'Armenian'
    _for_code('hy')['iso']                = 'hye'
    _for_code('hy')['glotto']             = 'nucl1235'
    _for_code('hy')['script']             = 'Armn'
    _for_code('hy')['spoken-in']          = 'Armenia'
    _for_code('hy')['supported-by']       = 'google; bing; yandex'

    # Assamese
    _for_code('as')['name']               = 'Assamese'
    _for_code('as')['endonym']            = 'অসমীয়া'
    #for_code('as')['translations-of']
    #for_code('as')['definitions-of']
    #for_code('as')['synonyms']
    #for_code('as')['examples']
    #for_code('as')['see-also']
    _for_code('as')['family']             = 'Indo-European'
    _for_code('as')['branch']             = 'Indo-Aryan'
    _for_code('as')['iso']                = 'asm'
    _for_code('as')['glotto']             = 'assa1263'
    _for_code('as')['script']             = 'Beng'
    _for_code('as')['spoken-in']          = 'the northeastern Indian state of Assam'
    _for_code('as')['supported-by']       = 'google; bing'

    # Aymara
    _for_code('ay')['name']               = 'Aymara'
    _for_code('ay')['endonym']            = 'Aymar aru'
    #for_code('ay')['translations-of']
    #for_code('ay')['definitions-of']
    #for_code('ay')['synonyms']
    #for_code('ay')['examples']
    #for_code('ay')['see-also']
    _for_code('ay')['family']             = 'Aymaran'
    #for_code('ay')['branch']            = 'Aymaran'
    _for_code('ay')['iso']                = 'aym'
    _for_code('ay')['glotto']             = 'nucl1667'
    _for_code('ay')['script']             = 'Latn'
    _for_code('ay')['spoken-in']          = 'Bolivia; Peru'
    _for_code('ay')['supported-by']       = 'google'

    # Azerbaijani (North Azerbaijani)
    _for_code('az')['name']               = 'Azerbaijani'
    _for_code('az')['name2']              = 'Azeri'
    _for_code('az')['endonym']            = 'Azərbaycanca'
    _for_code('az')['translations-of']    = '%s sözünün tərcüməsi'
    _for_code('az')['definitions-of']     = '%s sözünün tərifləri'
    _for_code('az')['synonyms']           = 'Sinonimlər'
    _for_code('az')['examples']           = 'Nümunələr'
    _for_code('az')['see-also']           = 'Həmçinin, baxın:'
    _for_code('az')['family']             = 'Turkic'
    _for_code('az')['branch']             = 'Oghuz'
    _for_code('az')['iso']                = 'aze'
    _for_code('az')['glotto']             = 'nort2697'
    _for_code('az')['script']             = 'Latn'
    _for_code('az')['spoken-in']          = 'Azerbaijan'
    _for_code('az')['supported-by']       = 'google; bing; yandex'

    # Bambara
    _for_code('bm')['name']               = 'Bambara'
    _for_code('bm')['endonym']            = 'Bamanankan'
    _for_code('bm')['endonym2']           = 'Bamana'
    #for_code('bm')['translations-of']
    #for_code('bm')['definitions-of']
    #for_code('bm')['synonyms']
    #for_code('bm')['examples']
    #for_code('bm')['see-also']
    _for_code('bm')['family']             = 'Mande'
    _for_code('bm')['branch']             = 'Manding'
    _for_code('bm')['iso']                = 'bam'
    _for_code('bm')['glotto']             = 'bamb1269'
    _for_code('bm')['script']             = 'Latn'
    _for_code('bm')['spoken-in']          = 'Mali'
    _for_code('bm')['supported-by']       = 'google'

    # Bashkir
    _for_code('ba')['name']               = 'Bashkir'
    _for_code('ba')['endonym']            = 'Башҡортса'
    _for_code('ba')['endonym2']           = 'башҡорт теле'
    #for_code('ba')['translations-of']
    #for_code('ba')['definitions-of']
    #for_code('ba')['synonyms']
    #for_code('ba')['examples']
    #for_code('ba')['see-also']
    _for_code('ba')['family']             = 'Turkic'
    _for_code('ba')['branch']             = 'Kipchak'
    _for_code('ba')['iso']                = 'bak'
    _for_code('ba')['glotto']             = 'bash1264'
    _for_code('ba')['script']             = 'Cyrl'
    _for_code('ba')['spoken-in']          = 'the Republic of Bashkortostan in Russia'
    _for_code('ba')['supported-by']       = 'bing; yandex'

    # Basque
    _for_code('eu')['name']               = 'Basque'
    _for_code('eu')['endonym']            = 'Euskara'
    _for_code('eu')['translations-of']    = '%s esapidearen itzulpena'
    _for_code('eu')['definitions-of']     = 'Honen definizioak: %s'
    _for_code('eu')['synonyms']           = 'Sinonimoak'
    _for_code('eu')['examples']           = 'Adibideak'
    _for_code('eu')['see-also']           = 'Ikusi hauek ere'
    _for_code('eu')['family']             = 'Language isolate'
    #for_code('eu')['branch']            = 'Language isolate'
    _for_code('eu')['iso']                = 'eus'
    _for_code('eu')['glotto']             = 'basq1248'
    _for_code('eu')['script']             = 'Latn'
    _for_code('eu')['spoken-in']          = 'Euskal Herria in Spain and France'
    _for_code('eu')['supported-by']       = 'google; bing; yandex'

    # Belarusian, Cyrillic alphabet
    _for_code('be')['name']               = 'Belarusian'
    _for_code('be')['endonym']            = 'беларуская'
    _for_code('be')['translations-of']    = 'Пераклады %s'
    _for_code('be')['definitions-of']     = 'Вызначэннi %s'
    _for_code('be')['synonyms']           = 'Сінонімы'
    _for_code('be')['examples']           = 'Прыклады'
    _for_code('be')['see-also']           = 'Гл. таксама'
    _for_code('be')['family']             = 'Indo-European'
    _for_code('be')['branch']             = 'East Slavic'
    _for_code('be')['iso']                = 'bel'
    _for_code('be')['glotto']             = 'bela1254'
    _for_code('be')['script']             = 'Cyrl'
    _for_code('be')['spoken-in']          = 'Belarus'
    _for_code('be')['supported-by']       = 'google; yandex'

    # Bengali / Bangla
    _for_code('bn')['name']               = 'Bengali'
    _for_code('bn')['name2']              = 'Bangla'
    _for_code('bn')['endonym']            = 'বাংলা'
    _for_code('bn')['translations-of']    = '%s এর অনুবাদ'
    _for_code('bn')['definitions-of']     = '%s এর সংজ্ঞা'
    _for_code('bn')['synonyms']           = 'প্রতিশব্দ'
    _for_code('bn')['examples']           = 'উদাহরণ'
    _for_code('bn')['see-also']           = 'আরো দেখুন'
    _for_code('bn')['family']             = 'Indo-European'
    _for_code('bn')['branch']             = 'Indo-Aryan'
    _for_code('bn')['iso']                = 'ben'
    _for_code('bn')['glotto']             = 'beng1280'
    _for_code('bn')['script']             = 'Beng'
    _for_code('bn')['spoken-in']          = 'Bangladesh; India'
    _for_code('bn')['supported-by']       = 'google; bing; yandex'

    # Bhojpuri
    _for_code('bho')['name']              = 'Bhojpuri'
    _for_code('bho')['endonym']           = 'भोजपुरी'
    #for_code('bho')['translations-of']
    #for_code('bho')['definitions-of']
    #for_code('bho')['synonyms']
    #for_code('bho')['examples']
    #for_code('bho')['see-also']
    _for_code('bho')['family']            = 'Indo-European'
    _for_code('bho')['branch']            = 'Indo-Aryan'
    _for_code('bho')['iso']               = 'bho'
    _for_code('bho')['glotto']            = 'bhoj1246'
    _for_code('bho')['script']            = 'Deva'
    _for_code('bho')['spoken-in']         = 'India; Nepal; Fiji'
    _for_code('bho')['supported-by']      = 'google'

    # Bosnian, Latin alphabet
    _for_code('bs')['name']               = 'Bosnian'
    _for_code('bs')['endonym']            = 'Bosanski'
    _for_code('bs')['translations-of']    = 'Prijevod za: %s'
    _for_code('bs')['definitions-of']     = 'Definicije za %s'
    _for_code('bs')['synonyms']           = 'Sinonimi'
    _for_code('bs')['examples']           = 'Primjeri'
    _for_code('bs')['see-also']           = 'Pogledajte i'
    _for_code('bs')['family']             = 'Indo-European'
    _for_code('bs')['branch']             = 'South Slavic'
    _for_code('bs')['iso']                = 'bos'
    _for_code('bs')['glotto']             = 'bosn1245'
    _for_code('bs')['script']             = 'Latn'
    _for_code('bs')['spoken-in']          = 'Bosnia and Herzegovina'
    _for_code('bs')['supported-by']       = 'google; bing; yandex'

    # Breton
    _for_code('br')['name']               = 'Breton'
    _for_code('br')['endonym']            = 'Brezhoneg'
    #for_code('br')['translations-of']
    #for_code('br')['definitions-of']
    #for_code('br')['synonyms']
    #for_code('br')['examples']
    #for_code('br')['see-also']
    _for_code('br')['family']             = 'Indo-European'
    _for_code('br')['branch']             = 'Celtic'
    _for_code('br')['iso']                = 'bre'
    _for_code('br')['glotto']             = 'bret1244'
    _for_code('br')['script']             = 'Latn'
    _for_code('br')['spoken-in']          = 'Brittany in France'
    _for_code('br')['supported-by']       = ''

    # Bulgarian
    _for_code('bg')['name']               = 'Bulgarian'
    _for_code('bg')['endonym']            = 'български'
    _for_code('bg')['translations-of']    = 'Преводи на %s'
    _for_code('bg')['definitions-of']     = 'Дефиниции за %s'
    _for_code('bg')['synonyms']           = 'Синоними'
    _for_code('bg')['examples']           = 'Примери'
    _for_code('bg')['see-also']           = 'Вижте също'
    _for_code('bg')['family']             = 'Indo-European'
    _for_code('bg')['branch']             = 'South Slavic'
    _for_code('bg')['iso']                = 'bul'
    _for_code('bg')['glotto']             = 'bulg1262'
    _for_code('bg')['script']             = 'Cyrl'
    _for_code('bg')['spoken-in']          = 'Bulgaria'
    _for_code('bg')['supported-by']       = 'google; bing; yandex'

    # Cantonese
    _for_code('yue')['name']              = 'Cantonese'
    _for_code('yue')['endonym']           = '粵語'
    _for_code('yue')['endonym2']          = '廣東話'
    #for_code('yue')['translations-of']
    #for_code('yue')['definitions-of']
    #for_code('yue')['synonyms']
    #for_code('yue')['examples']
    #for_code('yue')['see-also']
    _for_code('yue')['family']            = 'Sino-Tibetan'
    _for_code('yue')['branch']            = 'Sinitic'
    _for_code('yue')['iso']               = 'yue'
    _for_code('yue')['glotto']            = 'cant1236'
    _for_code('yue')['script']            = 'Hant'
    _for_code('yue')['spoken-in']         = 'southeastern China; Hong Kong; Macau'
    _for_code('yue')['supported-by']      = 'bing'

    # Catalan (Standard Catalan)
    _for_code('ca')['name']               = 'Catalan'
    _for_code('ca')['endonym']            = 'Català'
    _for_code('ca')['translations-of']    = 'Traduccions per a %s'
    _for_code('ca')['definitions-of']     = 'Definicions de: %s'
    _for_code('ca')['synonyms']           = 'Sinònims'
    _for_code('ca')['examples']           = 'Exemples'
    _for_code('ca')['see-also']           = 'Vegeu també'
    _for_code('ca')['family']             = 'Indo-European'
    _for_code('ca')['branch']             = 'Western Romance'
    _for_code('ca')['iso']                = 'cat'
    _for_code('ca')['glotto']             = 'stan1289'
    _for_code('ca')['script']             = 'Latn'
    _for_code('ca')['spoken-in']          = 'Països Catalans in Andorra, Spain, France and Italy'
    _for_code('ca')['supported-by']       = 'google; bing; yandex'

    # Cebuano
    _for_code('ceb')['name']              = 'Cebuano'
    _for_code('ceb')['endonym']           = 'Cebuano'
    _for_code('ceb')['translations-of']   = '%s Mga Paghubad sa PULONG_O_HUGPONG SA PAMULONG'
    _for_code('ceb')['definitions-of']    = 'Mga kahulugan sa %s'
    _for_code('ceb')['synonyms']          = 'Mga Kapulong'
    _for_code('ceb')['examples']          = 'Mga pananglitan:'
    _for_code('ceb')['see-also']          = 'Kitaa pag-usab'
    _for_code('ceb')['family']            = 'Austronesian'
    _for_code('ceb')['branch']            = 'Malayo-Polynesian'
    _for_code('ceb')['iso']               = 'ceb'
    _for_code('ceb')['glotto']            = 'cebu1242'
    _for_code('ceb')['script']            = 'Latn'
    _for_code('ceb')['spoken-in']         = 'the southern Philippines'
    _for_code('ceb')['supported-by']      = 'google; yandex'

    # Cherokee
    _for_code('chr')['name']              = 'Cherokee'
    _for_code('chr')['endonym']           = 'ᏣᎳᎩ'
    #for_code('chr')['translations-of']
    #for_code('chr')['definitions-of']
    #for_code('chr')['synonyms']
    #for_code('chr')['examples']
    #for_code('chr')['see-also']
    _for_code('chr')['family']            = 'Iroquoian'
    #for_code('chr')['branch']
    _for_code('chr')['iso']               = 'chr'
    _for_code('chr')['glotto']            = 'cher1273'
    _for_code('chr')['script']            = 'Cher'
    _for_code('chr')['spoken-in']         = 'North America'
    _for_code('chr')['supported-by']      = ''

    # Chichewa
    _for_code('ny')['name']               = 'Chichewa'
    _for_code('ny')['name2']              = 'Chinyanja'
    _for_code('ny')['endonym']            = 'Nyanja'
    _for_code('ny')['translations-of']    = 'Matanthauzidwe a %s'
    _for_code('ny')['definitions-of']     = 'Mamasulidwe a %s'
    _for_code('ny')['synonyms']           = 'Mau ofanana'
    _for_code('ny')['examples']           = 'Zitsanzo'
    _for_code('ny')['see-also']           = 'Onaninso'
    _for_code('ny')['family']             = 'Atlantic-Congo'
    _for_code('ny')['branch']             = 'Bantu'
    _for_code('ny')['iso']                = 'nya'
    _for_code('ny')['glotto']             = 'nyan1308'
    _for_code('ny')['script']             = 'Latn'
    _for_code('ny')['spoken-in']          = 'Malawi; Zambia'
    _for_code('ny')['supported-by']       = 'google'

    # Chinese (Literary)
    _for_code('lzh')['name']              = 'Chinese (Literary)'
    #for_code('lzh')['name2']            = 'Literary Chinese'
    #for_code('lzh')['name3']            = 'Classical Chinese'
    _for_code('lzh')['endonym']           = '文言'
    _for_code('lzh')['endonym2']          = '古漢語'
    #for_code('lzh')['translations-of']
    #for_code('lzh')['definitions-of']
    #for_code('lzh')['synonyms']
    #for_code('lzh')['examples']
    #for_code('lzh')['see-also']
    _for_code('lzh')['family']            = 'Sino-Tibetan'
    _for_code('lzh')['branch']            = 'Sinitic'
    _for_code('lzh')['iso']               = 'lzh'
    _for_code('lzh')['glotto']            = 'lite1248'
    _for_code('lzh')['script']            = 'Hans' # should actually be Hant
    _for_code('lzh')['spoken-in']         = 'ancient China'
    _for_code('lzh')['supported-by']      = 'bing'

    # Chinese (Standard Mandarin), Simplified
    _for_code('zh-CN')['name']            = 'Chinese (Simplified)'
    _for_code('zh-CN')['endonym']         = '简体中文'
    _for_code('zh-CN')['translations-of'] = '%s 的翻译'
    _for_code('zh-CN')['definitions-of']  = '%s的定义'
    _for_code('zh-CN')['synonyms']        = '同义词'
    _for_code('zh-CN')['examples']        = '示例'
    _for_code('zh-CN')['see-also']        = '另请参阅'
    _for_code('zh-CN')['family']          = 'Sino-Tibetan'
    _for_code('zh-CN')['branch']          = 'Sinitic'
    _for_code('zh-CN')['iso']             = 'zho-CN'
    _for_code('zh-CN')['glotto']          = 'mand1415'
    _for_code('zh-CN')['script']          = 'Hans'
    _for_code('zh-CN')['dictionary']      = 'true' # has dictionary
    _for_code('zh-CN')['spoken-in']       = 'the Greater China regions'
    _for_code('zh-CN')['written-in']      = 'mainland China; Singapore'
    _for_code('zh-CN')['supported-by']    = 'google; bing; yandex'

    # Chinese (Standard Mandarin), Traditional
    _for_code('zh-TW')['name']            = 'Chinese (Traditional)'
    _for_code('zh-TW')['endonym']         = '繁體中文'
    _for_code('zh-TW')['endonym2']        = '正體中文'
    _for_code('zh-TW')['translations-of'] = '「%s」的翻譯'
    _for_code('zh-TW')['definitions-of']  = '「%s」的定義'
    _for_code('zh-TW')['synonyms']        = '同義詞'
    _for_code('zh-TW')['examples']        = '例句'
    _for_code('zh-TW')['see-also']        = '另請參閱'
    _for_code('zh-TW')['family']          = 'Sino-Tibetan'
    _for_code('zh-TW')['branch']          = 'Sinitic'
    _for_code('zh-TW')['iso']             = 'zho-TW'
    _for_code('zh-TW')['glotto']          = 'mand1415'
    _for_code('zh-TW')['script']          = 'Hant'
    _for_code('zh-TW')['dictionary']      = 'true' # has dictionary
    _for_code('zh-TW')['spoken-in']       = 'the Greater China regions'
    _for_code('zh-TW')['written-in']      = 'Taiwan (Republic of China); Hong Kong; Macau'
    _for_code('zh-TW')['supported-by']    = 'google; bing'

    # Chuvash
    _for_code('cv')['name']               = 'Chuvash'
    _for_code('cv')['endonym']            = 'Чӑвашла'
    #for_code('cv')['translations-of']
    #for_code('cv')['definitions-of']
    #for_code('cv')['synonyms']
    #for_code('cv')['examples']
    #for_code('cv')['see-also']
    _for_code('cv')['family']             = 'Turkic'
    _for_code('cv')['branch']             = 'Oghur'
    _for_code('cv')['iso']                = 'chv'
    _for_code('cv')['glotto']             = 'chuv1255'
    _for_code('cv')['script']             = 'Cyrl'
    _for_code('cv')['spoken-in']          = 'the Chuvash Republic in Russia'
    _for_code('cv')['supported-by']       = 'yandex'

    # Corsican
    _for_code('co')['name']               = 'Corsican'
    _for_code('co')['endonym']            = 'Corsu'
    _for_code('co')['translations-of']    = 'Traductions de %s'
    _for_code('co')['definitions-of']     = 'Définitions de %s'
    _for_code('co')['synonyms']           = 'Synonymes'
    _for_code('co')['examples']           = 'Exemples'
    _for_code('co')['see-also']           = 'Voir aussi'
    _for_code('co')['family']             = 'Indo-European'
    _for_code('co')['branch']             = 'Italo-Dalmatian'
    _for_code('co')['iso']                = 'cos'
    _for_code('co')['glotto']             = 'cors1241'
    _for_code('co')['script']             = 'Latn'
    _for_code('co')['spoken-in']          = 'Corsica in France; the northern end of the island of Sardinia in Italy'
    _for_code('co')['supported-by']       = 'google'

    # Croatian
    _for_code('hr')['name']               = 'Croatian'
    _for_code('hr')['endonym']            = 'Hrvatski'
    _for_code('hr')['translations-of']    = 'Prijevodi riječi ili izraza %s'
    _for_code('hr')['definitions-of']     = 'Definicije riječi ili izraza %s'
    _for_code('hr')['synonyms']           = 'Sinonimi'
    _for_code('hr')['examples']           = 'Primjeri'
    _for_code('hr')['see-also']           = 'Također pogledajte'
    _for_code('hr')['family']             = 'Indo-European'
    _for_code('hr')['branch']             = 'South Slavic'
    _for_code('hr')['iso']                = 'hrv'
    _for_code('hr')['glotto']             = 'croa1245'
    _for_code('hr')['script']             = 'Latn'
    _for_code('hr')['spoken-in']          = 'Croatia; Bosnia and Herzegovina'
    _for_code('hr')['supported-by']       = 'google; bing; yandex'

    # Czech
    _for_code('cs')['name']               = 'Czech'
    _for_code('cs')['endonym']            = 'Čeština'
    _for_code('cs')['translations-of']    = 'Překlad výrazu %s'
    _for_code('cs')['definitions-of']     = 'Definice výrazu %s'
    _for_code('cs')['synonyms']           = 'Synonyma'
    _for_code('cs')['examples']           = 'Příklady'
    _for_code('cs')['see-also']           = 'Viz také'
    _for_code('cs')['family']             = 'Indo-European'
    _for_code('cs')['branch']             = 'West Slavic'
    _for_code('cs')['iso']                = 'ces'
    _for_code('cs')['glotto']             = 'czec1258'
    _for_code('cs')['script']             = 'Latn'
    _for_code('cs')['spoken-in']          = 'Czechia'
    _for_code('cs')['supported-by']       = 'google; bing; yandex'

    # Danish
    _for_code('da')['name']               = 'Danish'
    _for_code('da')['endonym']            = 'Dansk'
    _for_code('da')['translations-of']    = 'Oversættelser af %s'
    _for_code('da')['definitions-of']     = 'Definitioner af %s'
    _for_code('da')['synonyms']           = 'Synonymer'
    _for_code('da')['examples']           = 'Eksempler'
    _for_code('da')['see-also']           = 'Se også'
    _for_code('da')['family']             = 'Indo-European'
    _for_code('da')['branch']             = 'North Germanic'
    _for_code('da')['iso']                = 'dan'
    _for_code('da')['glotto']             = 'dani1285'
    _for_code('da')['script']             = 'Latn'
    _for_code('da')['spoken-in']          = 'Denmark; Greenland; the Faroe Islands; the northern German region of Southern Schleswig'
    _for_code('da')['supported-by']       = 'google; bing; yandex'

    # Dari (Dari Persian)
    _for_code('prs')['name']              = 'Dari'
    _for_code('prs')['endonym']           = 'دری'
    #for_code('prs')['translations-of']
    #for_code('prs')['definitions-of']
    #for_code('prs')['synonyms']
    #for_code('prs')['examples']
    #for_code('prs')['see-also']
    _for_code('prs')['family']            = 'Indo-European'
    _for_code('prs')['branch']            = 'Iranian'
    _for_code('prs')['iso']               = 'prs'
    _for_code('prs')['glotto']            = 'dari1249'
    _for_code('prs')['script']            = 'Arab'
    _for_code('prs')['rtl']               = 'true' # RTL language
    _for_code('prs')['spoken-in']         = 'Afghanistan; Iran'
    _for_code('prs')['supported-by']      = 'bing'

    # Dhivehi
    _for_code('dv')['name']               = 'Dhivehi'
    _for_code('dv')['name2']              = 'Divehi'
    _for_code('dv')['name3']              = 'Maldivian'
    _for_code('dv')['endonym']            = 'ދިވެހި'
    #for_code('dv')['translations-of']
    #for_code('dv')['definitions-of']
    #for_code('dv')['synonyms']
    #for_code('dv')['examples']
    #for_code('dv')['see-also']
    _for_code('dv')['family']             = 'Indo-European'
    _for_code('dv')['branch']             = 'Indo-Aryan'
    _for_code('dv')['iso']                = 'div'
    _for_code('dv')['glotto']             = 'dhiv1236'
    _for_code('dv')['script']             = 'Thaa'
    _for_code('dv')['rtl']                = 'true' # RTL language
    _for_code('dv')['spoken-in']          = 'the Maldives'
    _for_code('dv')['supported-by']       = 'google; bing'

    # Dogri
    _for_code('doi')['name']              = 'Dogri'
    _for_code('doi')['endonym']           = 'डोगरी'
    #for_code('doi')['translations-of']
    #for_code('doi')['definitions-of']
    #for_code('doi')['synonyms']
    #for_code('doi')['examples']
    #for_code('doi')['see-also']
    _for_code('doi')['family']            = 'Indo-European'
    _for_code('doi')['branch']            = 'Indo-Aryan'
    _for_code('doi')['iso']               = 'doi'
    _for_code('doi')['glotto']            = 'indo1311'
    _for_code('doi')['script']            = 'Deva'
    _for_code('doi')['spoken-in']         = 'the Jammu region in northern India'
    _for_code('doi')['supported-by']      = 'google'

    # Dutch
    _for_code('nl')['name']               = 'Dutch'
    _for_code('nl')['endonym']            = 'Nederlands'
    _for_code('nl')['translations-of']    = 'Vertalingen van %s'
    _for_code('nl')['definitions-of']     = 'Definities van %s'
    _for_code('nl')['synonyms']           = 'Synoniemen'
    _for_code('nl')['examples']           = 'Voorbeelden'
    _for_code('nl')['see-also']           = 'Zie ook'
    _for_code('nl')['family']             = 'Indo-European'
    _for_code('nl')['branch']             = 'West Germanic'
    _for_code('nl')['iso']                = 'nld'
    _for_code('nl')['glotto']             = 'dutc1256'
    _for_code('nl')['script']             = 'Latn'
    _for_code('nl')['dictionary']         = 'true' # has dictionary
    _for_code('nl')['spoken-in']          = 'the Netherlands; Belgium; Suriname; Aruba; Curaçao; Sint Maarten; the Caribbean Netherlands'
    _for_code('nl')['supported-by']       = 'google; bing; yandex'

    # Dzongkha
    _for_code('dz')['name']               = 'Dzongkha'
    _for_code('dz')['endonym']            = 'རྫོང་ཁ'
    #for_code('dz')['translations-of']
    #for_code('dz')['definitions-of']
    #for_code('dz')['synonyms']
    #for_code('dz')['examples']
    #for_code('dz')['see-also']
    _for_code('dz')['family']             = 'Sino-Tibetan'
    _for_code('dz')['branch']             = 'Tibetic'
    _for_code('dz')['iso']                = 'dzo'
    _for_code('dz')['glotto']             = 'nucl1307'
    _for_code('dz')['script']             = 'Tibt'
    _for_code('dz')['spoken-in']          = 'Bhutan'
    _for_code('dz')['supported-by']       = ''

    # English
    _for_code('en')['name']               = 'English'
    _for_code('en')['endonym']            = 'English'
    _for_code('en')['translations-of']    = 'Translations of %s'
    _for_code('en')['definitions-of']     = 'Definitions of %s'
    _for_code('en')['synonyms']           = 'Synonyms'
    _for_code('en')['examples']           = 'Examples'
    _for_code('en')['see-also']           = 'See also'
    _for_code('en')['family']             = 'Indo-European'
    _for_code('en')['branch']             = 'West Germanic'
    _for_code('en')['iso']                = 'eng'
    _for_code('en')['glotto']             = 'stan1293'
    _for_code('en')['script']             = 'Latn'
    _for_code('en')['dictionary']         = 'true' # has dictionary
    _for_code('en')['spoken-in']          = 'worldwide'
    _for_code('en')['supported-by']       = 'google; bing; yandex'

    # Esperanto
    _for_code('eo')['name']               = 'Esperanto'
    _for_code('eo')['endonym']            = 'Esperanto'
    _for_code('eo')['translations-of']    = 'Tradukoj de %s'
    _for_code('eo')['definitions-of']     = 'Difinoj de %s'
    _for_code('eo')['synonyms']           = 'Sinonimoj'
    _for_code('eo')['examples']           = 'Ekzemploj'
    _for_code('eo')['see-also']           = 'Vidu ankaŭ'
    _for_code('eo')['family']             = 'Constructed language'
    #for_code('eo')['branch']
    _for_code('eo')['iso']                = 'epo'
    _for_code('eo')['glotto']             = 'espe1235'
    _for_code('eo')['script']             = 'Latn'
    _for_code('eo')['spoken-in']          = 'worldwide'
    _for_code('eo')['description']        = 'the world\'s most widely spoken constructed international auxiliary language, designed to be a universal second language for international communication'
    _for_code('eo')['supported-by']       = 'google; yandex'

    # Estonian
    _for_code('et')['name']               = 'Estonian'
    _for_code('et')['endonym']            = 'Eesti'
    _for_code('et')['translations-of']    = 'Sõna(de) %s tõlked'
    _for_code('et')['definitions-of']     = 'Sõna(de) %s definitsioonid'
    _for_code('et')['synonyms']           = 'Sünonüümid'
    _for_code('et')['examples']           = 'Näited'
    _for_code('et')['see-also']           = 'Vt ka'
    _for_code('et')['family']             = 'Uralic'
    _for_code('et')['branch']             = 'Finnic'
    _for_code('et')['iso']                = 'est'
    _for_code('et')['glotto']             = 'esto1258'
    _for_code('et')['script']             = 'Latn'
    _for_code('et')['spoken-in']          = 'Estonia'
    _for_code('et')['supported-by']       = 'google; bing; yandex'

    # Ewe
    _for_code('ee')['name']               = 'Ewe'
    _for_code('ee')['endonym']            = 'Eʋegbe'
    #for_code('ee')['translations-of']
    #for_code('ee')['definitions-of']
    #for_code('ee')['synonyms']
    #for_code('ee')['examples']
    #for_code('ee')['see-also']
    _for_code('ee')['family']             = 'Atlantic-Congo'
    _for_code('ee')['branch']             = 'Gbe'
    _for_code('ee')['iso']                = 'ewe'
    _for_code('ee')['glotto']             = 'ewee1241'
    _for_code('ee')['script']             = 'Latn'
    _for_code('ee')['spoken-in']          = 'Ghana; Togo; Benin'
    _for_code('ee')['supported-by']       = 'google'

    # Faroese
    _for_code('fo')['name']               = 'Faroese'
    _for_code('fo')['endonym']            = 'Føroyskt'
    #for_code('fo')['translations-of']
    #for_code('fo')['definitions-of']
    #for_code('fo')['synonyms']
    #for_code('fo')['examples']
    #for_code('fo')['see-also']
    _for_code('fo')['family']             = 'Indo-European'
    _for_code('fo')['branch']             = 'North Germanic'
    _for_code('fo')['iso']                = 'fao'
    _for_code('fo')['glotto']             = 'faro1244'
    _for_code('fo')['script']             = 'Latn'
    _for_code('fo')['spoken-in']          = 'the Faroe Islands'
    _for_code('fo')['supported-by']       = 'bing'

    # Fijian
    _for_code('fj')['name']               = 'Fijian'
    _for_code('fj')['endonym']            = 'Vosa Vakaviti'
    #for_code('fj')['translations-of']
    #for_code('fj')['definitions-of']
    #for_code('fj')['synonyms']
    #for_code('fj')['examples']
    #for_code('fj')['see-also']
    _for_code('fj')['family']             = 'Austronesian'
    _for_code('fj')['branch']             = 'Malayo-Polynesian'
    _for_code('fj')['iso']                = 'fij'
    _for_code('fj')['glotto']             = 'fiji1243'
    _for_code('fj')['script']             = 'Latn'
    _for_code('fj')['spoken-in']          = 'Fiji'
    _for_code('fj')['supported-by']       = 'bing'

    # Filipino / Tagalog
    _for_code('tl')['name']               = 'Filipino'
    _for_code('tl')['name2']              = 'Tagalog'
    _for_code('tl')['endonym']            = 'Filipino'
    _for_code('tl')['endonym2']           = 'Tagalog'
    _for_code('tl')['translations-of']    = 'Mga pagsasalin ng %s'
    _for_code('tl')['definitions-of']     = 'Mga kahulugan ng %s'
    _for_code('tl')['synonyms']           = 'Mga Kasingkahulugan'
    _for_code('tl')['examples']           = 'Mga Halimbawa'
    _for_code('tl')['see-also']           = 'Tingnan rin ang'
    _for_code('tl')['family']             = 'Austronesian'
    _for_code('tl')['branch']             = 'Malayo-Polynesian'
    _for_code('tl')['iso']                = 'fil'
    _for_code('tl')['glotto']             = 'fili1244'
    _for_code('tl')['script']             = 'Latn'
    _for_code('tl')['spoken-in']          = 'the Philippines'
    _for_code('tl')['supported-by']       = 'google; bing; yandex'

    # Finnish
    _for_code('fi')['name']               = 'Finnish'
    _for_code('fi')['endonym']            = 'Suomi'
    _for_code('fi')['translations-of']    = 'Käännökset tekstille %s'
    _for_code('fi')['definitions-of']     = 'Määritelmät kohteelle %s'
    _for_code('fi')['synonyms']           = 'Synonyymit'
    _for_code('fi')['examples']           = 'Esimerkkejä'
    _for_code('fi')['see-also']           = 'Katso myös'
    _for_code('fi')['family']             = 'Uralic'
    _for_code('fi')['branch']             = 'Finnic'
    _for_code('fi')['iso']                = 'fin'
    _for_code('fi')['glotto']             = 'finn1318'
    _for_code('fi')['script']             = 'Latn'
    _for_code('fi')['spoken-in']          = 'Finland'
    _for_code('fi')['supported-by']       = 'google; bing; yandex'

    # French (Standard French)
    _for_code('fr')['name']               = 'French'
    _for_code('fr')['endonym']            = 'Français'
    _for_code('fr')['translations-of']    = 'Traductions de %s'
    _for_code('fr')['definitions-of']     = 'Définitions de %s'
    _for_code('fr')['synonyms']           = 'Synonymes'
    _for_code('fr')['examples']           = 'Exemples'
    _for_code('fr')['see-also']           = 'Voir aussi'
    _for_code('fr')['family']             = 'Indo-European'
    _for_code('fr')['branch']             = 'Western Romance'
    _for_code('fr')['iso']                = 'fra'
    _for_code('fr')['glotto']             = 'stan1290'
    _for_code('fr')['script']             = 'Latn'
    _for_code('fr')['dictionary']         = 'true' # has dictionary
    _for_code('fr')['spoken-in']          = 'France; Switzerland; Belgium; Luxembourg'
    _for_code('fr')['supported-by']       = 'google; bing; yandex'

    # French (Canadian French)
    _for_code('fr-CA')['name']            = 'French (Canadian)'
    _for_code('fr-CA')['endonym']         = 'Français canadien'
    _for_code('fr-CA')['translations-of'] = 'Traductions de %s'
    _for_code('fr-CA')['definitions-of']  = 'Définitions de %s'
    _for_code('fr-CA')['synonyms']        = 'Synonymes'
    _for_code('fr-CA')['examples']        = 'Exemples'
    _for_code('fr-CA')['see-also']        = 'Voir aussi'
    _for_code('fr-CA')['family']          = 'Indo-European'
    _for_code('fr-CA')['branch']          = 'Western Romance'
    _for_code('fr-CA')['iso']             = 'fra-CA'
    _for_code('fr-CA')['glotto']          = 'queb1247'
    _for_code('fr-CA')['script']          = 'Latn'
    _for_code('fr-CA')['spoken-in']       = 'Canada'
    _for_code('fr-CA')['supported-by']    = 'bing'

    # Galician
    _for_code('gl')['name']               = 'Galician'
    _for_code('gl')['endonym']            = 'Galego'
    _for_code('gl')['translations-of']    = 'Traducións de %s'
    _for_code('gl')['definitions-of']     = 'Definicións de %s'
    _for_code('gl')['synonyms']           = 'Sinónimos'
    _for_code('gl')['examples']           = 'Exemplos'
    _for_code('gl')['see-also']           = 'Ver tamén'
    _for_code('gl')['family']             = 'Indo-European'
    _for_code('gl')['branch']             = 'Western Romance'
    _for_code('gl')['iso']                = 'glg'
    _for_code('gl')['glotto']             = 'gali1258'
    _for_code('gl')['script']             = 'Latn'
    _for_code('gl')['spoken-in']          = 'Galicia in northwestern Spain'
    _for_code('gl')['supported-by']       = 'google; bing; yandex'

    # Georgian (Modern Georgian)
    _for_code('ka')['name']               = 'Georgian'
    _for_code('ka')['endonym']            = 'ქართული'
    _for_code('ka')['translations-of']    = '%s-ის თარგმანები'
    _for_code('ka')['definitions-of']     = '%s-ის განსაზღვრებები'
    _for_code('ka')['synonyms']           = 'სინონიმები'
    _for_code('ka')['examples']           = 'მაგალითები'
    _for_code('ka')['see-also']           = 'ასევე იხილეთ'
    _for_code('ka')['family']             = 'Kartvelian'
    _for_code('ka')['branch']             = 'Karto-Zan'
    _for_code('ka')['iso']                = 'kat'
    _for_code('ka')['glotto']             = 'nucl1302'
    _for_code('ka')['script']             = 'Geor'
    _for_code('ka')['spoken-in']          = 'Georgia'
    _for_code('ka')['supported-by']       = 'google; bing; yandex'

    # German (Standard German)
    _for_code('de')['name']               = 'German'
    _for_code('de')['endonym']            = 'Deutsch'
    _for_code('de')['translations-of']    = 'Übersetzungen für %s'
    _for_code('de')['definitions-of']     = 'Definitionen von %s'
    _for_code('de')['synonyms']           = 'Synonyme'
    _for_code('de')['examples']           = 'Beispiele'
    _for_code('de')['see-also']           = 'Siehe auch'
    _for_code('de')['family']             = 'Indo-European'
    _for_code('de')['branch']             = 'West Germanic'
    _for_code('de')['iso']                = 'deu'
    _for_code('de')['glotto']             = 'stan1295'
    _for_code('de')['script']             = 'Latn'
    _for_code('de')['dictionary']         = 'true' # has dictionary
    _for_code('de')['spoken-in']          = 'Central Europe'
    _for_code('de')['supported-by']       = 'google; bing; yandex'

    # Greek (Modern Greek)
    _for_code('el')['name']               = 'Greek'
    _for_code('el')['endonym']            = 'Ελληνικά'
    _for_code('el')['translations-of']    = 'Μεταφράσεις του %s'
    _for_code('el')['definitions-of']     = 'Όρισμοί %s'
    _for_code('el')['synonyms']           = 'Συνώνυμα'
    _for_code('el')['examples']           = 'Παραδείγματα'
    _for_code('el')['see-also']           = 'Δείτε επίσης'
    _for_code('el')['family']             = 'Indo-European'
    _for_code('el')['branch']             = 'Paleo-Balkan'
    _for_code('el')['iso']                = 'ell'
    _for_code('el')['glotto']             = 'mode1248'
    _for_code('el')['script']             = 'Grek'
    _for_code('el')['spoken-in']          = 'Greece; Cyprus; southern Albania'
    _for_code('el')['supported-by']       = 'google; bing; yandex'

    # Greenlandic (West Greenlandic)
    _for_code('kl')['name']               = 'Greenlandic'
    _for_code('kl')['endonym']            = 'Kalaallisut'
    #for_code('kl')['translations-of']
    #for_code('kl')['definitions-of']
    #for_code('kl')['synonyms']
    #for_code('kl')['examples']
    #for_code('kl')['see-also']
    _for_code('kl')['family']             = 'Eskimo-Aleut'
    _for_code('kl')['branch']             = 'Inuit'
    _for_code('kl')['iso']                = 'kal'
    _for_code('kl')['glotto']             = 'kala1399'
    _for_code('kl')['script']             = 'Latn'
    _for_code('kl')['spoken-in']          = 'Greenland'
    _for_code('kl')['supported-by']       = ''

    # Guarani
    _for_code('gn')['name']               = 'Guarani'
    _for_code('gn')['endonym']            = 'Avañe\'ẽ'
    #for_code('gn')['translations-of']
    #for_code('gn')['definitions-of']
    #for_code('gn')['synonyms']
    #for_code('gn')['examples']
    #for_code('gn')['see-also']
    _for_code('gn')['family']             = 'Tupian'
    #for_code('gn')['branch']            = 'Guaraní'
    _for_code('gn')['iso']                = 'gug'
    _for_code('gn')['glotto']             = 'para1311'
    _for_code('gn')['script']             = 'Latn'
    _for_code('gn')['spoken-in']          = 'Paraguay; Bolivia; Argentina; Brazil'
    _for_code('gn')['supported-by']       = 'google'

    # Gujarati
    _for_code('gu')['name']               = 'Gujarati'
    _for_code('gu')['endonym']            = 'ગુજરાતી'
    _for_code('gu')['translations-of']    = '%s ના અનુવાદ'
    _for_code('gu')['definitions-of']     = '%s ની વ્યાખ્યાઓ'
    _for_code('gu')['synonyms']           = 'સમાનાર્થી'
    _for_code('gu')['examples']           = 'ઉદાહરણો'
    _for_code('gu')['see-also']           = 'આ પણ જુઓ'
    _for_code('gu')['family']             = 'Indo-European'
    _for_code('gu')['branch']             = 'Indo-Aryan'
    _for_code('gu')['iso']                = 'guj'
    _for_code('gu')['glotto']             = 'guja1252'
    _for_code('gu')['script']             = 'Gujr'
    _for_code('gu')['spoken-in']          = 'the Indian state of Gujarat'
    _for_code('gu')['supported-by']       = 'google; bing; yandex'

    # Haitian Creole
    _for_code('ht')['name']               = 'Haitian Creole'
    _for_code('ht')['endonym']            = 'Kreyòl Ayisyen'
    _for_code('ht')['translations-of']    = 'Tradiksyon %s'
    _for_code('ht')['definitions-of']     = 'Definisyon nan %s'
    _for_code('ht')['synonyms']           = 'Sinonim'
    _for_code('ht')['examples']           = 'Egzanp:'
    _for_code('ht')['see-also']           = 'Wè tou'
    _for_code('ht')['family']             = 'Indo-European'
    _for_code('ht')['branch']             = 'French Creole'
    _for_code('ht')['iso']                = 'hat'
    _for_code('ht')['glotto']             = 'hait1244'
    _for_code('ht')['script']             = 'Latn'
    _for_code('ht')['spoken-in']          = 'Haiti'
    _for_code('ht')['supported-by']       = 'google; bing; yandex'

    # Hawaiian
    _for_code('haw')['name']              = 'Hawaiian'
    _for_code('haw')['endonym']           = 'ʻŌlelo Hawaiʻi'
    #for_code('haw')['translations-of']
    #for_code('haw')['definitions-of']
    #for_code('haw')['synonyms']
    #for_code('haw')['examples']
    #for_code('haw')['see-also']
    _for_code('haw')['family']            = 'Austronesian'
    _for_code('haw')['branch']            = 'Malayo-Polynesian'
    _for_code('haw')['iso']               = 'haw'
    _for_code('haw')['glotto']            = 'hawa1245'
    _for_code('haw')['script']            = 'Latn'
    _for_code('haw')['spoken-in']         = 'the US state of Hawaii'
    _for_code('haw')['supported-by']      = 'google'

    # Hausa, Latin alphabet
    _for_code('ha')['name']               = 'Hausa'
    _for_code('ha')['endonym']            = 'Hausa'
    _for_code('ha')['translations-of']    = 'Fassarar %s'
    _for_code('ha')['definitions-of']     = 'Ma\'anoni na %s'
    _for_code('ha')['synonyms']           = 'Masu kamancin ma\'ana'
    _for_code('ha')['examples']           = 'Misalai'
    _for_code('ha')['see-also']           = 'Duba kuma'
    _for_code('ha')['family']             = 'Afro-Asiatic'
    _for_code('ha')['branch']             = 'Chadic'
    _for_code('ha')['iso']                = 'hau'
    _for_code('ha')['glotto']             = 'haus1257'
    _for_code('ha')['script']             = 'Latn'
    _for_code('ha')['spoken-in']          = 'Chad; Nigeria; Niger; Ghana; Cameroon; Benin'
    _for_code('ha')['supported-by']       = 'google'

    # Hebrew
    _for_code('he')['name']               = 'Hebrew'
    _for_code('he')['endonym']            = 'עִבְרִית'
    _for_code('he')['translations-of']    = 'תרגומים של %s'
    _for_code('he')['definitions-of']     = 'הגדרות של %s'
    _for_code('he')['synonyms']           = 'מילים נרדפות'
    _for_code('he')['examples']           = 'דוגמאות'
    _for_code('he')['see-also']           = 'ראה גם'
    _for_code('he')['family']             = 'Afro-Asiatic'
    _for_code('he')['branch']             = 'Semitic'
    _for_code('he')['iso']                = 'heb'
    _for_code('he')['glotto']             = 'hebr1245'
    _for_code('he')['script']             = 'Hebr'
    _for_code('he')['rtl']                = 'true' # RTL language
    _for_code('he')['spoken-in']          = 'Israel'
    _for_code('he')['supported-by']       = 'google; bing; yandex'

    # Hill Mari / Western Mari
    _for_code('mrj')['name']              = 'Hill Mari'
    _for_code('mrj')['endonym']           = 'Кырык мары'
    #for_code('mrj')['translations-of']
    #for_code('mrj')['definitions-of']
    #for_code('mrj')['synonyms']
    #for_code('mrj')['examples']
    #for_code('mrj')['see-also']
    _for_code('mrj')['family']            = 'Uralic'
    _for_code('mrj')['branch']            = 'Mari'
    _for_code('mrj')['iso']               = 'mrj'
    _for_code('mrj')['glotto']            = 'west2392'
    _for_code('mrj')['script']            = 'Cyrl'
    _for_code('mrj')['spoken-in']         = 'the Gornomariysky, Yurinsky and Kilemarsky districts of Mari El, Russia'
    _for_code('mrj')['supported-by']      = 'yandex'

    # Hindi
    _for_code('hi')['name']               = 'Hindi'
    _for_code('hi')['endonym']            = 'हिन्दी'
    _for_code('hi')['translations-of']    = '%s के अनुवाद'
    _for_code('hi')['definitions-of']     = '%s की परिभाषाएं'
    _for_code('hi')['synonyms']           = 'समानार्थी'
    _for_code('hi')['examples']           = 'उदाहरण'
    _for_code('hi')['see-also']           = 'यह भी देखें'
    _for_code('hi')['family']             = 'Indo-European'
    _for_code('hi')['branch']             = 'Indo-Aryan'
    _for_code('hi')['iso']                = 'hin'
    _for_code('hi')['glotto']             = 'hind1269'
    _for_code('hi')['script']             = 'Deva'
    _for_code('hi')['spoken-in']          = 'India'
    _for_code('hi')['supported-by']       = 'google; bing; yandex'

    # Hmong (First Vernacular Hmong)
    _for_code('hmn')['name']              = 'Hmong'
    _for_code('hmn')['endonym']           = 'Hmoob'
    _for_code('hmn')['translations-of']   = 'Lus txhais: %s'
    #for_code('hmn')['definitions-of']
    #for_code('hmn')['synonyms']
    #for_code('hmn')['examples']
    #for_code('hmn')['see-also']
    _for_code('hmn')['family']            = 'Hmong-Mien'
    _for_code('hmn')['branch']            = 'Hmongic'
    _for_code('hmn')['iso']               = 'hmn'
    _for_code('hmn')['glotto']            = 'firs1234'
    _for_code('hmn')['script']            = 'Latn'
    _for_code('hmn')['spoken-in']         = 'China; Vietnam; Laos; Myanmar; Thailand'
    _for_code('hmn')['supported-by']      = 'google; bing'

    # Hmong Daw (White Hmong)
    #for_code('mww')['name']              = 'Hmong Daw'
    #for_code('mww')['endonym']           = 'Hmoob Daw'
    #for_code('mww')['family']            = 'Hmong-Mien'
    #for_code('mww')['branch']            = 'Hmongic'
    #for_code('mww')['iso']               = 'mww'
    #for_code('mww')['glotto']            = 'hmon1333'
    #for_code('mww')['script']            = 'Latn'
    #for_code('mww')['spoken-in']         = 'China; Vietnam; Laos; Myanmar; Thailand'
    #for_code('mww')['supported-by']      = 'bing'

    # Hungarian
    _for_code('hu')['name']               = 'Hungarian'
    _for_code('hu')['endonym']            = 'Magyar'
    _for_code('hu')['translations-of']    = '%s fordításai'
    _for_code('hu')['definitions-of']     = '%s jelentései'
    _for_code('hu')['synonyms']           = 'Szinonimák'
    _for_code('hu')['examples']           = 'Példák'
    _for_code('hu')['see-also']           = 'Lásd még'
    _for_code('hu')['family']             = 'Uralic'
    _for_code('hu')['branch']             = 'Ugric'
    _for_code('hu')['iso']                = 'hun'
    _for_code('hu')['glotto']             = 'hung1274'
    _for_code('hu')['script']             = 'Latn'
    _for_code('hu')['spoken-in']          = 'Hungary'
    _for_code('hu')['supported-by']       = 'google; bing; yandex'

    # Icelandic
    _for_code('is')['name']               = 'Icelandic'
    _for_code('is')['endonym']            = 'Íslenska'
    _for_code('is')['translations-of']    = 'Þýðingar á %s'
    _for_code('is')['definitions-of']     = 'Skilgreiningar á'
    _for_code('is')['synonyms']           = 'Samheiti'
    _for_code('is')['examples']           = 'Dæmi'
    _for_code('is')['see-also']           = 'Sjá einnig'
    _for_code('is')['family']             = 'Indo-European'
    _for_code('is')['branch']             = 'North Germanic'
    _for_code('is')['iso']                = 'isl'
    _for_code('is')['glotto']             = 'icel1247'
    _for_code('is')['script']             = 'Latn'
    _for_code('is')['spoken-in']          = 'Iceland'
    _for_code('is')['supported-by']       = 'google; bing; yandex'

    # Igbo
    _for_code('ig')['name']               = 'Igbo'
    _for_code('ig')['endonym']            = 'Igbo'
    _for_code('ig')['translations-of']    = 'Ntụgharị asụsụ nke %s'
    _for_code('ig')['definitions-of']     = 'Nkọwapụta nke %s'
    _for_code('ig')['synonyms']           = 'Okwu oyiri'
    _for_code('ig')['examples']           = 'Ọmụmaatụ'
    _for_code('ig')['see-also']           = 'Hụkwuo'
    _for_code('ig')['family']             = 'Atlantic-Congo'
    _for_code('ig')['branch']             = 'Igboid'
    _for_code('ig')['iso']                = 'ibo'
    _for_code('ig')['glotto']             = 'nucl1417'
    _for_code('ig')['script']             = 'Latn'
    _for_code('ig')['spoken-in']          = 'southeastern Nigeria'
    _for_code('ig')['supported-by']       = 'google'

    # Ilocano
    _for_code('ilo')['name']              = 'Ilocano'
    _for_code('ilo')['endonym']           = 'Ilokano'
    #for_code('ilo')['translations-of']
    #for_code('ilo')['definitions-of']
    #for_code('ilo')['synonyms']
    #for_code('ilo')['examples']
    #for_code('ilo')['see-also']
    _for_code('ilo')['family']            = 'Austronesian'
    _for_code('ilo')['branch']            = 'Malayo-Polynesian'
    _for_code('ilo')['iso']               = 'ilo'
    _for_code('ilo')['glotto']            = 'ilok1237'
    _for_code('ilo')['script']            = 'Latn'
    _for_code('ilo')['spoken-in']         = 'the northern Philippines'
    _for_code('ilo')['supported-by']      = 'google'

    # Indonesian
    _for_code('id')['name']               = 'Indonesian'
    _for_code('id')['endonym']            = 'Bahasa Indonesia'
    _for_code('id')['translations-of']    = 'Terjemahan dari %s'
    _for_code('id')['definitions-of']     = 'Definisi %s'
    _for_code('id')['synonyms']           = 'Sinonim'
    _for_code('id')['examples']           = 'Contoh'
    _for_code('id')['see-also']           = 'Lihat juga'
    _for_code('id')['family']             = 'Austronesian'
    _for_code('id')['branch']             = 'Malayo-Polynesian'
    _for_code('id')['iso']                = 'ind'
    _for_code('id')['glotto']             = 'indo1316'
    _for_code('id')['script']             = 'Latn'
    _for_code('id')['spoken-in']          = 'Indonesia'
    _for_code('id')['supported-by']       = 'google; bing; yandex'

    # Interlingue
    _for_code('ie')['name']               = 'Interlingue'
    _for_code('ie')['name2']              = 'Occidental'
    _for_code('ie')['endonym']            = 'Interlingue'
    #for_code('ie')['translations-of']
    #for_code('ie')['definitions-of']
    #for_code('ie')['synonyms']
    #for_code('ie')['examples']
    #for_code('ie')['see-also']
    _for_code('ie')['family']             = 'Constructed language'
    #for_code('ie')['branch']
    _for_code('ie')['iso']                = 'ile'
    _for_code('ie')['glotto']             = 'occi1241'
    _for_code('ie')['script']             = 'Latn'
    _for_code('ie')['spoken-in']          = 'worldwide'
    _for_code('ie')['description']        = 'an international auxiliary language'
    _for_code('ie')['supported-by']       = ''

    # Inuinnaqtun
    _for_code('ikt')['name']              = 'Inuinnaqtun'
    _for_code('ikt')['endonym']           = 'Inuinnaqtun'
    #for_code('ikt')['translations-of']
    #for_code('ikt')['definitions-of']
    #for_code('ikt')['synonyms']
    #for_code('ikt')['examples']
    #for_code('ikt')['see-also']
    _for_code('ikt')['family']            = 'Eskimo-Aleut'
    _for_code('ikt')['branch']            = 'Inuit'
    _for_code('ikt')['iso']               = 'ikt'
    _for_code('ikt')['glotto']            = 'copp1244'
    _for_code('ikt')['script']            = 'Latn'
    _for_code('ikt')['spoken-in']         = 'the Canadian Arctic'
    _for_code('ikt')['supported-by']      = 'bing'

    # Inuktitut (Eastern Canadian Inuktitut)
    _for_code('iu')['name']               = 'Inuktitut'
    _for_code('iu')['endonym']            = 'ᐃᓄᒃᑎᑐᑦ'
    #for_code('iu')['translations-of']
    #for_code('iu')['definitions-of']
    #for_code('iu')['synonyms']
    #for_code('iu')['examples']
    #for_code('iu')['see-also']
    _for_code('iu')['family']             = 'Eskimo-Aleut'
    _for_code('iu')['branch']             = 'Inuit'
    _for_code('iu')['iso']                = 'iku'
    _for_code('iu')['glotto']             = 'east2534'
    _for_code('iu')['script']             = 'Cans'
    _for_code('iu')['spoken-in']          = 'the Canadian Arctic'
    _for_code('iu')['supported-by']       = 'bing'

    # Inuktitut (Eastern Canadian Inuktitut), Latin alphabet
    _for_code('iu-Latn')['name']          = 'Inuktitut (Latin)'
    _for_code('iu-Latn')['endonym']       = 'Inuktitut'
    #for_code('iu-Latn')['translations-of']
    #for_code('iu-Latn')['definitions-of']
    #for_code('iu-Latn')['synonyms']
    #for_code('iu-Latn')['examples']
    #for_code('iu-Latn')['see-also']
    _for_code('iu-Latn')['family']        = 'Eskimo-Aleut'
    _for_code('iu-Latn')['branch']        = 'Inuit'
    _for_code('iu-Latn')['iso']           = 'iku'
    _for_code('iu-Latn')['glotto']        = 'east2534'
    _for_code('iu-Latn')['script']        = 'Latn'
    _for_code('iu-Latn')['spoken-in']     = 'the Canadian Arctic'
    _for_code('iu-Latn')['supported-by']  = 'bing'

    # Irish
    _for_code('ga')['name']               = 'Irish'
    _for_code('ga')['name2']              = 'Gaelic'
    _for_code('ga')['endonym']            = 'Gaeilge'
    _for_code('ga')['translations-of']    = 'Aistriúcháin ar %s'
    _for_code('ga')['definitions-of']     = 'Sainmhínithe ar %s'
    _for_code('ga')['synonyms']           = 'Comhchiallaigh'
    _for_code('ga')['examples']           = 'Samplaí'
    _for_code('ga')['see-also']           = 'féach freisin'
    _for_code('ga')['family']             = 'Indo-European'
    _for_code('ga')['branch']             = 'Celtic'
    _for_code('ga')['iso']                = 'gle'
    _for_code('ga')['glotto']             = 'iris1253'
    _for_code('ga')['script']             = 'Latn'
    _for_code('ga')['spoken-in']          = 'Ireland'
    _for_code('ga')['supported-by']       = 'google; bing; yandex'

    # Italian
    _for_code('it')['name']               = 'Italian'
    _for_code('it')['endonym']            = 'Italiano'
    _for_code('it')['translations-of']    = 'Traduzioni di %s'
    _for_code('it')['definitions-of']     = 'Definizioni di %s'
    _for_code('it')['synonyms']           = 'Sinonimi'
    _for_code('it')['examples']           = 'Esempi'
    _for_code('it')['see-also']           = 'Vedi anche'
    _for_code('it')['family']             = 'Indo-European'
    _for_code('it')['branch']             = 'Italo-Dalmatian'
    _for_code('it')['iso']                = 'ita'
    _for_code('it')['glotto']             = 'ital1282'
    _for_code('it')['script']             = 'Latn'
    _for_code('it')['dictionary']         = 'true' # has dictionary
    _for_code('it')['spoken-in']          = 'Italy; Switzerland; San Marino; Vatican City'
    _for_code('it')['supported-by']       = 'google; bing; yandex'

    # Japanese
    _for_code('ja')['name']               = 'Japanese'
    _for_code('ja')['endonym']            = '日本語'
    _for_code('ja')['translations-of']    = '「%s」の翻訳'
    _for_code('ja')['definitions-of']     = '%s の定義'
    _for_code('ja')['synonyms']           = '同義語'
    _for_code('ja')['examples']           = '例'
    _for_code('ja')['see-also']           = '関連項目'
    _for_code('ja')['family']             = 'Japonic'
    #for_code('ja')['branch']
    _for_code('ja')['iso']                = 'jpn'
    _for_code('ja')['glotto']             = 'nucl1643'
    _for_code('ja')['script']             = 'Jpan'
    _for_code('ja')['dictionary']         = 'true' # has dictionary
    _for_code('ja')['spoken-in']          = 'Japan'
    _for_code('ja')['supported-by']       = 'google; bing; yandex'

    # Javanese, Latin alphabet
    _for_code('jv')['name']               = 'Javanese'
    _for_code('jv')['endonym']            = 'Basa Jawa'
    _for_code('jv')['translations-of']    = 'Terjemahan %s'
    _for_code('jv')['definitions-of']     = 'Arti %s'
    _for_code('jv')['synonyms']           = 'Sinonim'
    _for_code('jv')['examples']           = 'Conto'
    _for_code('jv')['see-also']           = 'Deleng uga'
    _for_code('jv')['family']             = 'Austronesian'
    _for_code('jv')['branch']             = 'Malayo-Polynesian'
    _for_code('jv')['iso']                = 'jav'
    _for_code('jv')['glotto']             = 'java1254'
    _for_code('jv')['script']             = 'Latn'
    _for_code('jv')['spoken-in']          = 'Java, Indonesia'
    _for_code('jv')['supported-by']       = 'google; yandex'

    # Kannada (Modern Kannada)
    _for_code('kn')['name']               = 'Kannada'
    _for_code('kn')['endonym']            = 'ಕನ್ನಡ'
    _for_code('kn')['translations-of']    = '%s ನ ಅನುವಾದಗಳು'
    _for_code('kn')['definitions-of']     = '%s ನ ವ್ಯಾಖ್ಯಾನಗಳು'
    _for_code('kn')['synonyms']           = 'ಸಮಾನಾರ್ಥಕಗಳು'
    _for_code('kn')['examples']           = 'ಉದಾಹರಣೆಗಳು'
    _for_code('kn')['see-also']           = 'ಇದನ್ನೂ ಗಮನಿಸಿ'
    _for_code('kn')['family']             = 'Dravidian'
    _for_code('kn')['branch']             = 'South Dravidian'
    _for_code('kn')['iso']                = 'kan'
    _for_code('kn')['glotto']             = 'nucl1305'
    _for_code('kn')['script']             = 'Knda'
    _for_code('kn')['spoken-in']          = 'the southwestern India'
    _for_code('kn')['supported-by']       = 'google; bing; yandex'

    # Kazakh, Cyrillic alphabet
    _for_code('kk')['name']               = 'Kazakh'
    _for_code('kk')['endonym']            = 'Қазақ тілі'
    _for_code('kk')['translations-of']    = '%s аудармалары'
    _for_code('kk')['definitions-of']     = '%s анықтамалары'
    _for_code('kk')['synonyms']           = 'Синонимдер'
    _for_code('kk')['examples']           = 'Мысалдар'
    _for_code('kk')['see-also']           = 'Келесі тізімді де көріңіз:'
    _for_code('kk')['family']             = 'Turkic'
    _for_code('kk')['branch']             = 'Kipchak'
    _for_code('kk')['iso']                = 'kaz'
    _for_code('kk')['glotto']             = 'kaza1248'
    _for_code('kk')['script']             = 'Cyrl'
    _for_code('kk')['spoken-in']          = 'Kazakhstan; China; Mongolia; Russia; Kyrgyzstan; Uzbekistan'
    _for_code('kk')['supported-by']       = 'google; bing; yandex'

    # Khmer (Central Khmer)
    _for_code('km')['name']               = 'Khmer'
    _for_code('km')['endonym']            = 'ភាសាខ្មែរ'
    _for_code('km')['translations-of']    = 'ការ​បក​ប្រែ​នៃ %s'
    _for_code('km')['definitions-of']     = 'និយមន័យ​នៃ​ %s'
    _for_code('km')['synonyms']           = 'សទិសន័យ'
    _for_code('km')['examples']           = 'ឧទាហរណ៍'
    _for_code('km')['see-also']           = 'មើល​ផង​ដែរ'
    _for_code('km')['family']             = 'Austroasiatic'
    _for_code('km')['branch']             = 'Khmeric'
    _for_code('km')['iso']                = 'khm'
    _for_code('km')['glotto']             = 'cent1989'
    _for_code('km')['script']             = 'Khmr'
    _for_code('km')['spoken-in']          = 'Cambodia; Thailand; Vietnam'
    _for_code('km')['supported-by']       = 'google; bing; yandex'

    # Kinyarwanda
    _for_code('rw')['name']               = 'Kinyarwanda'
    _for_code('rw')['endonym']            = 'Ikinyarwanda'
    #for_code('rw')['translations-of']
    #for_code('rw')['definitions-of']
    #for_code('rw')['synonyms']
    #for_code('rw')['examples']
    #for_code('rw')['see-also']
    _for_code('rw')['family']             = 'Atlantic-Congo'
    _for_code('rw')['branch']             = 'Bantu'
    _for_code('rw')['iso']                = 'kin'
    _for_code('rw')['glotto']             = 'kiny1244'
    _for_code('rw')['script']             = 'Latn'
    _for_code('rw')['spoken-in']          = 'Rwanda; Uganda; DR Congo; Tanzania'
    _for_code('rw')['supported-by']       = 'google'

    # Klingon, Latin alphabet
    _for_code('tlh-Latn')['name']         = 'Klingon'
    _for_code('tlh-Latn')['endonym']      = 'tlhIngan Hol'
    _for_code('tlh-Latn')['family']       = 'Constructed language'
    #for_code('tlh-Latn')['branch']
    _for_code('tlh-Latn')['iso']          = 'tlh-Latn'
    _for_code('tlh-Latn')['glotto']       = 'klin1234'
    _for_code('tlh-Latn')['script']       = 'Latn'
    _for_code('tlh-Latn')['spoken-in']    = 'the Star Trek universe'
    _for_code('tlh-Latn')['description']  = 'a fictional language spoken by the Klingons in the Star Trek universe'
    _for_code('tlh-Latn')['supported-by'] = 'bing'

    ## Klingon, pIqaD
    #for_code('tlh-Piqd')['name']         = 'Klingon (pIqaD)'
    #for_code('tlh-Piqd')['endonym']      = ' '
    #for_code('tlh-Piqd')['family']       = 'Constructed language'
    ##for_code('tlh-Piqd')['branch']
    #for_code('tlh-Piqd')['iso']          = 'tlh-Piqd'
    #for_code('tlh-Piqd')['glotto']       = 'klin1234'
    #for_code('tlh-Piqd')['script']       = 'Piqd'
    #for_code('tlh-Piqd')['spoken-in']    = 'the Star Trek universe'
    #for_code('tlh-Piqd')['description']  = 'a fictional language spoken by the Klingons in the Star Trek universe'
    #for_code('tlh-Piqd')['supported-by'] = 'bing'

    # Konkani (Goan Konkani)
    _for_code('gom')['name']              = 'Konkani'
    _for_code('gom')['endonym']           = 'कोंकणी'
    #for_code('gom')['translations-of']
    #for_code('gom')['definitions-of']
    #for_code('gom')['synonyms']
    #for_code('gom')['examples']
    #for_code('gom')['see-also']
    _for_code('gom')['family']            = 'Indo-European'
    _for_code('gom')['branch']            = 'Indo-Aryan'
    _for_code('gom')['iso']               = 'gom'
    _for_code('gom')['glotto']            = 'goan1235'
    _for_code('gom')['script']            = 'Deva'
    _for_code('gom')['spoken-in']         = 'the western coastal region of India'
    _for_code('gom')['supported-by']      = 'google'

    # Korean
    _for_code('ko')['name']               = 'Korean'
    _for_code('ko')['endonym']            = '한국어'
    _for_code('ko')['translations-of']    = '%s의 번역'
    _for_code('ko')['definitions-of']     = '%s의 정의'
    _for_code('ko')['synonyms']           = '동의어'
    _for_code('ko')['examples']           = '예문'
    _for_code('ko')['see-also']           = '참조'
    _for_code('ko')['family']             = 'Koreanic'
    #for_code('ko')['branch']
    _for_code('ko')['iso']                = 'kor'
    _for_code('ko')['glotto']             = 'kore1280'
    _for_code('ko')['script']             = 'Kore'
    _for_code('ko')['dictionary']         = 'true' # has dictionary
    _for_code('ko')['spoken-in']          = 'South Korea; North Korea; China'
    _for_code('ko')['supported-by']       = 'google; bing; yandex'

    # Krio
    _for_code('kri')['name']              = 'Krio'
    _for_code('kri')['endonym']           = 'Krio'
    #for_code('kri')['translations-of']
    #for_code('kri')['definitions-of']
    #for_code('kri')['synonyms']
    #for_code('kri')['examples']
    #for_code('kri')['see-also']
    _for_code('kri')['family']            = 'Indo-European'
    _for_code('kri')['branch']            = 'English Creole'
    _for_code('kri')['iso']               = 'kri'
    _for_code('kri')['glotto']            = 'krio1253'
    _for_code('kri')['script']            = 'Latn'
    _for_code('kri')['spoken-in']         = 'Sierra Leone'
    _for_code('kri')['supported-by']      = 'google'

    # Kurdish (Northern Kurdish) / Kurmanji
    _for_code('ku')['name']               = 'Kurdish (Northern)'
    _for_code('ku')['name2']              = 'Kurmanji'
    _for_code('ku')['endonym']            = 'Kurmancî'
    _for_code('ku')['endonym2']           = 'Kurdî'
    #for_code('ku')['translations-of']
    #for_code('ku')['definitions-of']
    #for_code('ku')['synonyms']
    #for_code('ku')['examples']
    #for_code('ku')['see-also']
    _for_code('ku')['family']             = 'Indo-European'
    _for_code('ku')['branch']             = 'Iranian'
    _for_code('ku')['iso']                = 'kmr'
    _for_code('ku')['glotto']             = 'nort2641'
    _for_code('ku')['script']             = 'Latn'
    _for_code('ku')['spoken-in']          = 'southeast Turkey; northwest and northeast Iran; northern Iraq; northern Syria; the Caucasus and Khorasan regions'
    _for_code('ku')['supported-by']       = 'google'

    # Kurdish (Central Kurdish) / Sorani
    _for_code('ckb')['name']              = 'Kurdish (Central)'
    _for_code('ckb')['name2']             = 'Sorani'
    _for_code('ckb')['endonym']           = 'سۆرانی'
    _for_code('ckb')['endonym2']          = 'کوردیی ناوەندی'
    #for_code('ckb')['translations-of']
    #for_code('ckb')['definitions-of']
    #for_code('ckb')['synonyms']
    #for_code('ckb')['examples']
    #for_code('ckb')['see-also']
    _for_code('ckb')['family']            = 'Indo-European'
    _for_code('ckb')['branch']            = 'Iranian'
    _for_code('ckb')['iso']               = 'ckb'
    _for_code('ckb')['glotto']            = 'cent1972'
    _for_code('ckb')['script']            = 'Arab'
    _for_code('ckb')['rtl']               = 'true' # RTL language
    _for_code('ckb')['spoken-in']         = 'Iraqi Kurdistan; western Iran'
    _for_code('ckb')['supported-by']      = 'google'

    # Kyrgyz, Cyrillic alphabet
    _for_code('ky')['name']               = 'Kyrgyz'
    _for_code('ky')['endonym']            = 'Кыргызча'
    _for_code('ky')['translations-of']    = '%s котормосу'
    _for_code('ky')['definitions-of']     = '%s аныктамасы'
    _for_code('ky')['synonyms']           = 'Синонимдер'
    _for_code('ky')['examples']           = 'Мисалдар'
    _for_code('ky')['see-also']           = 'Дагы караңыз'
    _for_code('ky')['family']             = 'Turkic'
    _for_code('ky')['branch']             = 'Kipchak'
    _for_code('ky')['iso']                = 'kir'
    _for_code('ky')['glotto']             = 'kirg1245'
    _for_code('ky')['script']             = 'Cyrl'
    _for_code('ky')['spoken-in']          = 'Kyrgyzstan; China; Tajikistan; Afghanistan; Pakistan'
    _for_code('ky')['supported-by']       = 'google; bing; yandex'

    # Lao
    _for_code('lo')['name']               = 'Lao'
    _for_code('lo')['endonym']            = 'ລາວ'
    _for_code('lo')['translations-of']    = 'ຄຳ​ແປ​ສຳລັບ %s'
    _for_code('lo')['definitions-of']     = 'ຄວາມໝາຍຂອງ %s'
    _for_code('lo')['synonyms']           = 'ຄຳທີ່ຄ້າຍກັນ %s'
    _for_code('lo')['examples']           = 'ຕົວຢ່າງ'
    _for_code('lo')['see-also']           = 'ເບິ່ງ​ເພີ່ມ​ເຕີມ'
    _for_code('lo')['family']             = 'Kra-Dai'
    _for_code('lo')['branch']             = 'Tai'
    _for_code('lo')['iso']                = 'lao'
    _for_code('lo')['glotto']             = 'laoo1244'
    _for_code('lo')['script']             = 'Laoo'
    _for_code('lo')['spoken-in']          = 'Laos; Thailand; Cambodia'
    _for_code('lo')['supported-by']       = 'google; bing; yandex'

    # Latin
    _for_code('la')['name']               = 'Latin'
    _for_code('la')['endonym']            = 'Latina'
    _for_code('la')['translations-of']    = 'Versio de %s'
    #for_code('la')['definitions-of']
    #for_code('la')['synonyms']
    #for_code('la')['examples']
    #for_code('la')['see-also']
    _for_code('la')['family']             = 'Indo-European'
    _for_code('la')['branch']             = 'Latino-Faliscan'
    _for_code('la')['iso']                = 'lat'
    _for_code('la')['glotto']             = 'lati1261'
    _for_code('la')['script']             = 'Latn'
    _for_code('la')['spoken-in']          = 'ancient Rome'
    _for_code('la')['supported-by']       = 'google; yandex'

    # Latvian
    _for_code('lv')['name']               = 'Latvian'
    _for_code('lv')['endonym']            = 'Latviešu'
    _for_code('lv')['translations-of']    = '%s tulkojumi'
    _for_code('lv')['definitions-of']     = '%s definīcijas'
    _for_code('lv')['synonyms']           = 'Sinonīmi'
    _for_code('lv')['examples']           = 'Piemēri'
    _for_code('lv')['see-also']           = 'Skatiet arī'
    _for_code('lv')['family']             = 'Indo-European'
    _for_code('lv')['branch']             = 'Eastern Baltic'
    _for_code('lv')['iso']                = 'lav'
    _for_code('lv')['glotto']             = 'latv1249'
    _for_code('lv')['script']             = 'Latn'
    _for_code('lv')['spoken-in']          = 'Latvia'
    _for_code('lv')['supported-by']       = 'google; bing; yandex'

    # Lingala
    _for_code('ln')['name']               = 'Lingala'
    _for_code('ln')['endonym']            = 'Lingála'
    #for_code('ln')['translations-of']
    #for_code('ln')['definitions-of']
    #for_code('ln')['synonyms']
    #for_code('ln')['examples']
    #for_code('ln')['see-also']
    _for_code('ln')['family']             = 'Atlantic-Congo'
    _for_code('ln')['branch']             = 'Bantu'
    _for_code('ln')['iso']                = 'lin'
    _for_code('ln')['glotto']             = 'ling1269'
    _for_code('ln')['script']             = 'Latn'
    _for_code('ln')['spoken-in']          = 'DR Congo; Republic of the Congo; Angola; Central African Republic; southern South Sudan'
    _for_code('ln')['supported-by']       = 'google'

    # Lithuanian
    _for_code('lt')['name']               = 'Lithuanian'
    _for_code('lt')['endonym']            = 'Lietuvių'
    _for_code('lt')['translations-of']    = '„%s“ vertimai'
    _for_code('lt')['definitions-of']     = '„%s“ apibrėžimai'
    _for_code('lt')['synonyms']           = 'Sinonimai'
    _for_code('lt')['examples']           = 'Pavyzdžiai'
    _for_code('lt')['see-also']           = 'Taip pat žiūrėkite'
    _for_code('lt')['family']             = 'Indo-European'
    _for_code('lt')['branch']             = 'Eastern Baltic'
    _for_code('lt')['iso']                = 'lit'
    _for_code('lt')['glotto']             = 'lith1251'
    _for_code('lt')['script']             = 'Latn'
    _for_code('lt')['spoken-in']          = 'Lithuania'
    _for_code('lt')['supported-by']       = 'google; bing; yandex'

    # Luganda
    _for_code('lg')['name']               = 'Luganda'
    _for_code('lg')['endonym']            = 'Luganda'
    _for_code('lg')['endonym2']           = 'Oluganda'
    #for_code('lg')['translations-of']
    #for_code('lg')['definitions-of']
    #for_code('lg')['synonyms']
    #for_code('lg')['examples']
    #for_code('lg')['see-also']
    _for_code('lg')['family']             = 'Atlantic-Congo'
    _for_code('lg')['branch']             = 'Bantu'
    _for_code('lg')['iso']                = 'lug'
    _for_code('lg')['glotto']             = 'gand1255'
    _for_code('lg')['script']             = 'Latn'
    _for_code('lg')['spoken-in']          = 'Uganda; Rwanda'
    _for_code('lg')['supported-by']       = 'google'

    # Luxembourgish
    _for_code('lb')['name']               = 'Luxembourgish'
    _for_code('lb')['endonym']            = 'Lëtzebuergesch'
    #for_code('lb')['translations-of']
    #for_code('lb')['definitions-of']
    #for_code('lb')['synonyms']
    #for_code('lb')['examples']
    #for_code('lb')['see-also']
    _for_code('lb')['family']             = 'Indo-European'
    _for_code('lb')['branch']             = 'West Germanic'
    _for_code('lb')['iso']                = 'ltz'
    _for_code('lb')['glotto']             = 'luxe1241'
    _for_code('lb')['script']             = 'Latn'
    _for_code('lb')['spoken-in']          = 'Luxembourg'
    _for_code('lb')['supported-by']       = 'google; yandex'

    # Macedonian
    _for_code('mk')['name']               = 'Macedonian'
    _for_code('mk')['endonym']            = 'Македонски'
    _for_code('mk')['translations-of']    = 'Преводи на %s'
    _for_code('mk')['definitions-of']     = 'Дефиниции на %s'
    _for_code('mk')['synonyms']           = 'Синоними'
    _for_code('mk')['examples']           = 'Примери'
    _for_code('mk')['see-also']           = 'Види и'
    _for_code('mk')['family']             = 'Indo-European'
    _for_code('mk')['branch']             = 'South Slavic'
    _for_code('mk')['iso']                = 'mkd'
    _for_code('mk')['glotto']             = 'mace1250'
    _for_code('mk')['script']             = 'Cyrl'
    _for_code('mk')['spoken-in']          = 'North Macedonia; Albania; Bosnia and Herzegovina; Romania; Serbia'
    _for_code('mk')['supported-by']       = 'google; bing; yandex'

    # Maithili
    _for_code('mai')['name']              = 'Maithili'
    _for_code('mai')['endonym']           = 'मैथिली'
    #for_code('mai')['translations-of']
    #for_code('mai')['definitions-of']
    #for_code('mai')['synonyms']
    #for_code('mai')['examples']
    #for_code('mai')['see-also']
    _for_code('mai')['family']            = 'Indo-European'
    _for_code('mai')['branch']            = 'Indo-Aryan'
    _for_code('mai')['iso']               = 'mai'
    _for_code('mai')['glotto']            = 'mait1250'
    _for_code('mai')['script']            = 'Deva'
    _for_code('mai')['spoken-in']         = 'the Mithila region in India and Nepal'
    _for_code('mai')['supported-by']      = 'google'

    # Malagasy (Plateau Malagasy)
    _for_code('mg')['name']               = 'Malagasy'
    _for_code('mg')['endonym']            = 'Malagasy'
    _for_code('mg')['translations-of']    = 'Dikan\'ny %s'
    _for_code('mg')['definitions-of']     = 'Famaritana ny %s'
    _for_code('mg')['synonyms']           = 'Mitovy hevitra'
    _for_code('mg')['examples']           = 'Ohatra'
    _for_code('mg')['see-also']           = 'Jereo ihany koa'
    _for_code('mg')['family']             = 'Austronesian'
    _for_code('mg')['branch']             = 'Malayo-Polynesian'
    _for_code('mg')['iso']                = 'mlg'
    _for_code('mg')['glotto']             = 'plat1254'
    _for_code('mg')['script']             = 'Latn'
    _for_code('mg')['spoken-in']          = 'Madagascar; the Comoros; Mayotte'
    _for_code('mg')['supported-by']       = 'google; bing; yandex'

    # Malay (Standard Malay), Latin alphabet
    _for_code('ms')['name']               = 'Malay'
    _for_code('ms')['endonym']            = 'Bahasa Melayu'
    _for_code('ms')['translations-of']    = 'Terjemahan %s'
    _for_code('ms')['definitions-of']     = 'Takrif %s'
    _for_code('ms')['synonyms']           = 'Sinonim'
    _for_code('ms')['examples']           = 'Contoh'
    _for_code('ms')['see-also']           = 'Lihat juga'
    _for_code('ms')['family']             = 'Austronesian'
    _for_code('ms')['branch']             = 'Malayo-Polynesian'
    _for_code('ms')['iso']                = 'msa'
    _for_code('ms')['glotto']             = 'stan1306'
    _for_code('ms')['script']             = 'Latn'
    _for_code('ms')['spoken-in']          = 'Malaysia; Singapore; Indonesia; Brunei; East Timor'
    _for_code('ms')['supported-by']       = 'google; bing; yandex'

    # Malayalam
    _for_code('ml')['name']               = 'Malayalam'
    _for_code('ml')['endonym']            = 'മലയാളം'
    _for_code('ml')['translations-of']    = '%s എന്നതിന്റെ വിവർത്തനങ്ങൾ'
    _for_code('ml')['definitions-of']     = '%s എന്നതിന്റെ നിർവ്വചനങ്ങൾ'
    _for_code('ml')['synonyms']           = 'പര്യായങ്ങള്‍'
    _for_code('ml')['examples']           = 'ഉദാഹരണങ്ങള്‍'
    _for_code('ml')['see-also']           = 'ഇതും കാണുക'
    _for_code('ml')['family']             = 'Dravidian'
    _for_code('ml')['branch']             = 'South Dravidian'
    _for_code('ml')['iso']                = 'mal'
    _for_code('ml')['glotto']             = 'mala1464'
    _for_code('ml')['script']             = 'Mlym'
    _for_code('ml')['spoken-in']          = 'Kerala, Lakshadweep and Puducherry in India'
    _for_code('ml')['supported-by']       = 'google; bing; yandex'

    # Maltese
    _for_code('mt')['name']               = 'Maltese'
    _for_code('mt')['endonym']            = 'Malti'
    _for_code('mt')['translations-of']    = 'Traduzzjonijiet ta\' %s'
    _for_code('mt')['definitions-of']     = 'Definizzjonijiet ta\' %s'
    _for_code('mt')['synonyms']           = 'Sinonimi'
    _for_code('mt')['examples']           = 'Eżempji'
    _for_code('mt')['see-also']           = 'Ara wkoll'
    _for_code('mt')['family']             = 'Afro-Asiatic'
    _for_code('mt')['branch']             = 'Semitic'
    _for_code('mt')['iso']                = 'mlt'
    _for_code('mt')['glotto']             = 'malt1254'
    _for_code('mt')['script']             = 'Latn'
    _for_code('mt')['spoken-in']          = 'Malta'
    _for_code('mt')['supported-by']       = 'google; bing; yandex'

    # Maori
    _for_code('mi')['name']               = 'Maori'
    _for_code('mi')['endonym']            = 'Māori'
    _for_code('mi')['translations-of']    = 'Ngā whakamāoritanga o %s'
    _for_code('mi')['definitions-of']     = 'Ngā whakamārama o %s'
    _for_code('mi')['synonyms']           = 'Ngā Kupu Taurite'
    _for_code('mi')['examples']           = 'Ngā Tauira:'
    _for_code('mi')['see-also']           = 'Tiro hoki:'
    _for_code('mi')['family']             = 'Austronesian'
    _for_code('mi')['branch']             = 'Malayo-Polynesian'
    _for_code('mi')['iso']                = 'mri'
    _for_code('mi')['glotto']             = 'maor1246'
    _for_code('mi')['script']             = 'Latn'
    _for_code('mi')['spoken-in']          = 'New Zealand'
    _for_code('mi')['supported-by']       = 'google; bing; yandex'

    # Marathi
    _for_code('mr')['name']               = 'Marathi'
    _for_code('mr')['endonym']            = 'मराठी'
    _for_code('mr')['translations-of']    = '%s ची भाषांतरे'
    _for_code('mr')['definitions-of']     = '%s च्या व्याख्या'
    _for_code('mr')['synonyms']           = 'समानार्थी शब्द'
    _for_code('mr')['examples']           = 'उदाहरणे'
    _for_code('mr')['see-also']           = 'हे देखील पहा'
    _for_code('mr')['family']             = 'Indo-European'
    _for_code('mr')['branch']             = 'Indo-Aryan'
    _for_code('mr')['iso']                = 'mar'
    _for_code('mr')['glotto']             = 'mara1378'
    _for_code('mr')['script']             = 'Deva'
    _for_code('mr')['spoken-in']          = 'the Indian state of Maharashtra'
    _for_code('mr')['supported-by']       = 'google; bing; yandex'

    # Mari (Eastern Mari / Meadow Mari)
    _for_code('mhr')['name']              = 'Eastern Mari'
    _for_code('mhr')['name2']             = 'Meadow Mari'
    _for_code('mhr')['endonym']           = 'Олык марий'
    #for_code('mhr')['translations-of']
    #for_code('mhr')['definitions-of']
    #for_code('mhr')['synonyms']
    #for_code('mhr')['examples']
    #for_code('mhr')['see-also']
    _for_code('mhr')['family']            = 'Uralic'
    _for_code('mhr')['branch']            = 'Mari'
    _for_code('mhr')['iso']               = 'mhr'
    _for_code('mhr')['glotto']            = 'east2328'
    _for_code('mhr')['script']            = 'Cyrl'
    _for_code('mhr')['spoken-in']         = 'Mari El, Russia'
    _for_code('mhr')['supported-by']      = 'yandex'

    # Meiteilon / Manipuri
    _for_code('mni-Mtei')['name']         = 'Meiteilon'
    _for_code('mni-Mtei')['name2']        = 'Manipuri'
    _for_code('mni-Mtei')['name3']        = 'Meitei'
    _for_code('mni-Mtei')['name4']        = 'Meetei'
    _for_code('mni-Mtei')['endonym']      = 'ꯃꯤꯇꯩꯂꯣꯟ'
    #for_code('mni-Mtei')['translations-of']
    #for_code('mni-Mtei')['definitions-of']
    #for_code('mni-Mtei')['synonyms']
    #for_code('mni-Mtei')['examples']
    #for_code('mni-Mtei')['see-also']
    _for_code('mni-Mtei')['family']       = 'Sino-Tibetan'
    _for_code('mni-Mtei')['branch']       = 'Tibeto-Burman'
    _for_code('mni-Mtei')['iso']          = 'mni'
    _for_code('mni-Mtei')['glotto']       = 'mani1292'
    _for_code('mni-Mtei')['script']       = 'Mtei'
    _for_code('mni-Mtei')['spoken-in']    = 'the northeastern India; Bangladesh; Myanmar'
    _for_code('mni-Mtei')['supported-by'] = 'google'

    # Mizo
    _for_code('lus')['name']              = 'Mizo'
    _for_code('lus')['endonym']           = 'Mizo ṭawng'
    #for_code('lus')['translations-of']
    #for_code('lus')['definitions-of']
    #for_code('lus')['synonyms']
    #for_code('lus')['examples']
    #for_code('lus')['see-also']
    _for_code('lus')['family']            = 'Sino-Tibetan'
    _for_code('lus')['branch']            = 'Tibeto-Burman'
    _for_code('lus')['iso']               = 'lus'
    _for_code('lus')['glotto']            = 'lush1249'
    _for_code('lus')['script']            = 'Latn'
    _for_code('lus')['spoken-in']         = 'the Indian state of Mizoram'
    _for_code('lus')['supported-by']      = 'google'

    # Mongolian, Cyrillic alphabet
    _for_code('mn')['name']               = 'Mongolian'
    _for_code('mn')['endonym']            = 'Монгол'
    _for_code('mn')['translations-of']    = '%s-н орчуулга'
    _for_code('mn')['definitions-of']     = '%s үгийн тодорхойлолт'
    _for_code('mn')['synonyms']           = 'Ойролцоо утгатай'
    _for_code('mn')['examples']           = 'Жишээнүүд'
    _for_code('mn')['see-also']           = 'Мөн харах'
    _for_code('mn')['family']             = 'Mongolic'
    #for_code('mn')['branch']
    _for_code('mn')['iso']                = 'mon'
    _for_code('mn')['glotto']             = 'mong1331'
    _for_code('mn')['script']             = 'Cyrl'
    _for_code('mn')['spoken-in']          = 'Mongolia; Inner Mongolia in China'
    _for_code('mn')['supported-by']       = 'google; bing; yandex'

    # Mongolian, traditional Mongolian alphabet
    _for_code('mn-Mong')['name']          = 'Mongolian (Traditional)'
    _for_code('mn-Mong')['endonym']       = 'ᠮᠣᠩᠭᠣᠯ'
    #for_code('mn-Mong')['translations-of']
    #for_code('mn-Mong')['definitions-of']
    #for_code('mn-Mong')['synonyms']
    #for_code('mn-Mong')['examples']
    #for_code('mn-Mong')['see-also']
    _for_code('mn-Mong')['family']        = 'Mongolic'
    #for_code('mn-Mong')['branch']
    _for_code('mn-Mong')['iso']           = 'mon-Mong'
    _for_code('mn-Mong')['glotto']        = 'mong1331'
    _for_code('mn-Mong')['script']        = 'Mong'
    _for_code('mn-Mong')['spoken-in']     = 'Mongolia; Inner Mongolia in China'
    _for_code('mn-Mong')['supported-by']  = 'bing'

    # Myanmar / Burmese
    _for_code('my')['name']               = 'Myanmar'
    _for_code('my')['name2']              = 'Burmese'
    _for_code('my')['endonym']            = 'မြန်မာစာ'
    _for_code('my')['translations-of']    = '%s၏ ဘာသာပြန်ဆိုချက်များ'
    _for_code('my')['definitions-of']     = '%s၏ အနက်ဖွင့်ဆိုချက်များ'
    _for_code('my')['synonyms']           = 'ကြောင်းတူသံကွဲများ'
    _for_code('my')['examples']           = 'ဥပမာ'
    _for_code('my')['see-also']           = 'ဖော်ပြပါများကိုလဲ ကြည့်ပါ'
    _for_code('my')['family']             = 'Sino-Tibetan'
    _for_code('my')['branch']             = 'Tibeto-Burman'
    _for_code('my')['iso']                = 'mya'
    _for_code('my')['glotto']             = 'nucl1310'
    _for_code('my')['script']             = 'Mymr'
    _for_code('my')['spoken-in']          = 'Myanmar'
    _for_code('my')['supported-by']       = 'google; bing; yandex'

    # Nepali
    _for_code('ne')['name']               = 'Nepali'
    _for_code('ne')['endonym']            = 'नेपाली'
    _for_code('ne')['translations-of']    = '%sका अनुवाद'
    _for_code('ne')['definitions-of']     = '%sको परिभाषा'
    _for_code('ne')['synonyms']           = 'समानार्थीहरू'
    _for_code('ne')['examples']           = 'उदाहरणहरु'
    _for_code('ne')['see-also']           = 'यो पनि हेर्नुहोस्'
    _for_code('ne')['family']             = 'Indo-European'
    _for_code('ne')['branch']             = 'Indo-Aryan'
    _for_code('ne')['iso']                = 'nep'
    _for_code('ne')['glotto']             = 'nepa1254'
    _for_code('ne')['script']             = 'Deva'
    _for_code('ne')['spoken-in']          = 'Nepal; India'
    _for_code('ne')['supported-by']       = 'google; bing; yandex'

    # Norwegian
    _for_code('no')['name']               = 'Norwegian'
    _for_code('no')['endonym']            = 'Norsk'
    _for_code('no')['translations-of']    = 'Oversettelser av %s'
    _for_code('no')['definitions-of']     = 'Definisjoner av %s'
    _for_code('no')['synonyms']           = 'Synonymer'
    _for_code('no')['examples']           = 'Eksempler'
    _for_code('no')['see-also']           = 'Se også'
    _for_code('no')['family']             = 'Indo-European'
    _for_code('no')['branch']             = 'North Germanic'
    _for_code('no')['iso']                = 'nor'
    _for_code('no')['glotto']             = 'norw1258'
    _for_code('no')['script']             = 'Latn'
    _for_code('no')['spoken-in']          = 'Norway'
    _for_code('no')['supported-by']       = 'google; bing; yandex'

    # Occitan
    _for_code('oc')['name']               = 'Occitan'
    _for_code('oc')['endonym']            = 'Occitan'
    #for_code('oc')['translations-of']
    #for_code('oc')['definitions-of']
    #for_code('oc')['synonyms']
    #for_code('oc')['examples']
    #for_code('oc')['see-also']
    _for_code('oc')['family']             = 'Indo-European'
    _for_code('oc')['branch']             = 'Western Romance'
    _for_code('oc')['iso']                = 'oci'
    _for_code('oc')['glotto']             = 'occi1239'
    _for_code('oc')['script']             = 'Latn'
    _for_code('oc')['spoken-in']          = 'Occitania in France, Monaco, Italy and Spain'
    _for_code('oc')['supported-by']       = ''

    # Odia / Oriya
    _for_code('or')['name']               = 'Odia'
    _for_code('or')['name2']              = 'Oriya'
    _for_code('or')['endonym']            = 'ଓଡ଼ିଆ'
    #for_code('or')['translations-of']
    #for_code('or')['definitions-of']
    #for_code('or')['synonyms']
    #for_code('or')['examples']
    #for_code('or')['see-also']
    _for_code('or')['family']             = 'Indo-European'
    _for_code('or')['branch']             = 'Indo-Aryan'
    _for_code('or')['iso']                = 'ori'
    _for_code('or')['glotto']             = 'macr1269'
    _for_code('or')['script']             = 'Orya'
    _for_code('or')['spoken-in']          = 'the Indian state of Odisha'
    _for_code('or')['supported-by']       = 'google; bing'

    # Oromo
    _for_code('om')['name']               = 'Oromo'
    _for_code('om')['endonym']            = 'Afaan Oromoo'
    #for_code('om')['translations-of']
    #for_code('om')['definitions-of']
    #for_code('om')['synonyms']
    #for_code('om')['examples']
    #for_code('om')['see-also']
    _for_code('om')['family']             = 'Afro-Asiatic'
    _for_code('om')['branch']             = 'Cushitic'
    _for_code('om')['iso']                = 'orm'
    _for_code('om')['glotto']             = 'nucl1736'
    _for_code('om')['script']             = 'Latn'
    _for_code('om')['spoken-in']          = 'the Ethiopian state of Oromia; northeastern Kenya'
    _for_code('om')['supported-by']       = 'google'

    # Papiamento
    _for_code('pap')['name']              = 'Papiamento'
    _for_code('pap')['endonym']           = 'Papiamentu'
    #for_code('pap')['translations-of']
    #for_code('pap')['definitions-of']
    #for_code('pap')['synonyms']
    #for_code('pap')['examples']
    #for_code('pap')['see-also']
    _for_code('pap')['family']            = 'Indo-European'
    _for_code('pap')['branch']            = 'Portuguese Creole'
    _for_code('pap')['iso']               = 'pap'
    _for_code('pap')['glotto']            = 'papi1253'
    _for_code('pap')['script']            = 'Latn'
    _for_code('pap')['spoken-in']         = 'the Dutch Caribbean'
    _for_code('pap')['supported-by']      = 'yandex'

    # Pashto / Pushto
    _for_code('ps')['name']               = 'Pashto'
    _for_code('ps')['name2']              = 'Pushto'
    _for_code('ps')['endonym']            = 'پښتو'
    _for_code('ps')['translations-of']    = 'د %sژباړې'
    _for_code('ps')['definitions-of']     = 'د%s تعریفونه'
    _for_code('ps')['synonyms']           = 'مترادف لغتونه'
    _for_code('ps')['examples']           = 'بېلګې'
    _for_code('ps')['see-also']           = 'دا هم ووینئ'
    _for_code('ps')['family']             = 'Indo-European'
    _for_code('ps')['branch']             = 'Iranian'
    _for_code('ps')['iso']                = 'pus'
    _for_code('ps')['glotto']             = 'pash1269'
    _for_code('ps')['script']             = 'Arab'
    _for_code('ps')['rtl']                = 'true' # RTL language
    _for_code('ps')['spoken-in']          = 'Afghanistan; Pakistan'
    _for_code('ps')['supported-by']       = 'google; bing'

    # Persian / Farsi (Western Farsi / Iranian Persian)
    _for_code('fa')['name']               = 'Persian'
    _for_code('fa')['name2']              = 'Farsi'
    _for_code('fa')['endonym']            = 'فارسی'
    _for_code('fa')['translations-of']    = 'ترجمه‌های %s'
    _for_code('fa')['definitions-of']     = 'تعریف‌های %s'
    _for_code('fa')['synonyms']           = 'مترادف‌ها'
    _for_code('fa')['examples']           = 'مثال‌ها'
    _for_code('fa')['see-also']           = 'همچنین مراجعه کنید به'
    _for_code('fa')['family']             = 'Indo-European'
    _for_code('fa')['branch']             = 'Iranian'
    _for_code('fa')['iso']                = 'fas'
    _for_code('fa')['glotto']             = 'west2369'
    _for_code('fa')['script']             = 'Arab'
    _for_code('fa')['rtl']                = 'true' # RTL language
    _for_code('fa')['spoken-in']          = 'Iran'
    _for_code('fa')['supported-by']       = 'google; bing; yandex'

    # Polish
    _for_code('pl')['name']               = 'Polish'
    _for_code('pl')['endonym']            = 'Polski'
    _for_code('pl')['translations-of']    = 'Tłumaczenia %s'
    _for_code('pl')['definitions-of']     = '%s – definicje'
    _for_code('pl')['synonyms']           = 'Synonimy'
    _for_code('pl')['examples']           = 'Przykłady'
    _for_code('pl')['see-also']           = 'Zobacz też'
    _for_code('pl')['family']             = 'Indo-European'
    _for_code('pl')['branch']             = 'West Slavic'
    _for_code('pl')['iso']                = 'pol'
    _for_code('pl')['glotto']             = 'poli1260'
    _for_code('pl')['script']             = 'Latn'
    _for_code('pl')['spoken-in']          = 'Poland'
    _for_code('pl')['supported-by']       = 'google; bing; yandex'

    # Portuguese (Brazilian)
    _for_code('pt-BR')['name']            = 'Portuguese (Brazilian)'
    _for_code('pt-BR')['endonym']         = 'Português Brasileiro'
    _for_code('pt-BR')['translations-of'] = 'Traduções de %s'
    _for_code('pt-BR')['definitions-of']  = 'Definições de %s'
    _for_code('pt-BR')['synonyms']        = 'Sinônimos'
    _for_code('pt-BR')['examples']        = 'Exemplos'
    _for_code('pt-BR')['see-also']        = 'Veja também'
    _for_code('pt-BR')['family']          = 'Indo-European'
    _for_code('pt-BR')['branch']          = 'Western Romance'
    _for_code('pt-BR')['iso']             = 'por'
    _for_code('pt-BR')['glotto']          = 'braz1246'
    _for_code('pt-BR')['script']          = 'Latn'
    _for_code('pt-BR')['dictionary']      = 'true' # has dictionary
    _for_code('pt-BR')['spoken-in']       = 'Portugal; Brazil; Cape Verde; Angola; Mozambique; Guinea-Bissau; Equatorial Guinea; São Tomé and Príncipe; East Timor; Macau'
    _for_code('pt-BR')['supported-by']    = 'google; bing; yandex'

    # Portuguese (European)
    _for_code('pt-PT')['name']            = 'Portuguese (European)'
    _for_code('pt-PT')['endonym']         = 'Português Europeu'
    _for_code('pt-PT')['translations-of'] = 'Traduções de %s'
    _for_code('pt-PT')['definitions-of']  = 'Definições de %s'
    _for_code('pt-PT')['synonyms']        = 'Sinônimos'
    _for_code('pt-PT')['examples']        = 'Exemplos'
    _for_code('pt-PT')['see-also']        = 'Veja também'
    _for_code('pt-PT')['family']          = 'Indo-European'
    _for_code('pt-PT')['branch']          = 'Western Romance'
    _for_code('pt-PT')['iso']             = 'por'
    _for_code('pt-PT')['glotto']          = 'port1283'
    _for_code('pt-PT')['script']          = 'Latn'
    _for_code('pt-PT')['spoken-in']       = 'Portugal; Brazil; Cape Verde; Angola; Mozambique; Guinea-Bissau; Equatorial Guinea; São Tomé and Príncipe; East Timor; Macau'
    _for_code('pt-PT')['supported-by']    = 'bing'

    # Punjabi, Gurmukhī alphabet
    _for_code('pa')['name']               = 'Punjabi'
    _for_code('pa')['endonym']            = 'ਪੰਜਾਬੀ'
    _for_code('pa')['translations-of']    = 'ਦੇ ਅਨੁਵਾਦ%s'
    _for_code('pa')['definitions-of']     = 'ਦੀਆਂ ਪਰਿਭਾਸ਼ਾ %s'
    _for_code('pa')['synonyms']           = 'ਸਮਾਨਾਰਥਕ ਸ਼ਬਦ'
    _for_code('pa')['examples']           = 'ਉਦਾਹਰਣਾਂ'
    _for_code('pa')['see-also']           = 'ਇਹ ਵੀ ਵੇਖੋ'
    _for_code('pa')['family']             = 'Indo-European'
    _for_code('pa')['branch']             = 'Indo-Aryan'
    _for_code('pa')['iso']                = 'pan'
    _for_code('pa')['glotto']             = 'panj1256'
    _for_code('pa')['script']             = 'Guru'
    _for_code('pa')['spoken-in']          = 'the Punjab region of India and Pakistan'
    _for_code('pa')['supported-by']       = 'google; bing; yandex'

    # Quechua
    _for_code('qu')['name']               = 'Quechua'
    _for_code('qu')['endonym']            = 'Runasimi'
    #for_code('qu')['translations-of']
    #for_code('qu')['definitions-of']
    #for_code('qu')['synonyms']
    #for_code('qu')['examples']
    #for_code('qu')['see-also']
    _for_code('qu')['family']             = 'Quechuan'
    #for_code('qu')['branch']
    _for_code('qu')['iso']                = 'que'
    _for_code('qu')['glotto']             = 'quec1387'
    _for_code('qu')['script']             = 'Latn'
    _for_code('qu')['spoken-in']          = 'Peru; Bolivia; Ecuador; surrounding countries'
    _for_code('qu')['supported-by']       = 'google'

    # Querétaro Otomi
    _for_code('otq')['name']              = 'Querétaro Otomi'
    _for_code('otq')['endonym']           = 'Hñąñho'
    _for_code('otq')['family']            = 'Oto-Manguean'
    #for_code('otq')['branch']
    _for_code('otq')['iso']               = 'otq'
    _for_code('otq')['glotto']            = 'quer1236'
    _for_code('otq')['script']            = 'Latn'
    _for_code('otq')['spoken-in']         = 'Querétaro in Mexico'
    _for_code('otq')['supported-by']      = 'bing'

    # Romanian / Moldovan, Latin alphabet
    _for_code('ro')['name']               = 'Romanian'
    _for_code('ro')['endonym']            = 'Română'
    _for_code('ro')['translations-of']    = 'Traduceri pentru %s'
    _for_code('ro')['definitions-of']     = 'Definiții pentru %s'
    _for_code('ro')['synonyms']           = 'Sinonime'
    _for_code('ro')['examples']           = 'Exemple'
    _for_code('ro')['see-also']           = 'Vedeți și'
    _for_code('ro')['family']             = 'Indo-European'
    _for_code('ro')['branch']             = 'Eastern Romance'
    _for_code('ro')['iso']                = 'ron'
    _for_code('ro')['glotto']             = 'roma1327'
    _for_code('ro')['script']             = 'Latn'
    _for_code('ro')['spoken-in']          = 'Romania; Moldova'
    _for_code('ro')['supported-by']       = 'google; bing; yandex'

    # Romansh
    _for_code('rm')['name']               = 'Romansh'
    _for_code('rm')['endonym']            = 'Rumantsch'
    #for_code('rm')['translations-of']
    #for_code('rm')['definitions-of']
    #for_code('rm')['synonyms']
    #for_code('rm')['examples']
    #for_code('rm')['see-also']
    _for_code('rm')['family']             = 'Indo-European'
    _for_code('rm')['branch']             = 'Western Romance'
    _for_code('rm')['iso']                = 'roh'
    _for_code('rm')['glotto']             = 'roma1326'
    _for_code('rm')['script']             = 'Latn'
    _for_code('rm')['spoken-in']          = 'the Swiss canton of the Grisons'
    _for_code('rm')['supported-by']       = ''

    # Russian
    _for_code('ru')['name']               = 'Russian'
    _for_code('ru')['endonym']            = 'Русский'
    _for_code('ru')['translations-of']    = '%s: варианты перевода'
    _for_code('ru')['definitions-of']     = '%s – определения'
    _for_code('ru')['synonyms']           = 'Синонимы'
    _for_code('ru')['examples']           = 'Примеры'
    _for_code('ru')['see-also']           = 'Похожие слова'
    _for_code('ru')['family']             = 'Indo-European'
    _for_code('ru')['branch']             = 'East Slavic'
    _for_code('ru')['iso']                = 'rus'
    _for_code('ru')['glotto']             = 'russ1263'
    _for_code('ru')['script']             = 'Cyrl'
    _for_code('ru')['dictionary']         = 'true' # has dictionary
    _for_code('ru')['spoken-in']          = 'the Russian-speaking world'
    _for_code('ru')['supported-by']       = 'google; bing; yandex'

    # Samoan
    _for_code('sm')['name']               = 'Samoan'
    _for_code('sm')['endonym']            = 'Gagana Sāmoa'
    #for_code('sm')['translations-of']
    #for_code('sm')['definitions-of']
    #for_code('sm')['synonyms']
    #for_code('sm')['examples']
    #for_code('sm')['see-also']
    _for_code('sm')['family']             = 'Austronesian'
    _for_code('sm')['branch']             = 'Malayo-Polynesian'
    _for_code('sm')['iso']                = 'smo'
    _for_code('sm')['glotto']             = 'samo1305'
    _for_code('sm')['script']             = 'Latn'
    _for_code('sm')['spoken-in']          = 'the Samoan Islands'
    _for_code('sm')['supported-by']       = 'google; bing'

    # Sanskrit
    _for_code('sa')['name']               = 'Sanskrit'
    _for_code('sa')['endonym']            = 'संस्कृतम्'
    #for_code('sa')['translations-of']
    #for_code('sa')['definitions-of']
    #for_code('sa')['synonyms']
    #for_code('sa')['examples']
    #for_code('sa')['see-also']
    _for_code('sa')['family']             = 'Indo-European'
    _for_code('sa')['branch']             = 'Indo-Aryan'
    _for_code('sa')['iso']                = 'san'
    _for_code('sa')['glotto']             = 'sans1269'
    _for_code('sa')['script']             = 'Deva'
    _for_code('sa')['spoken-in']          = 'ancient India'
    _for_code('sa')['supported-by']       = 'google'

    # Scots Gaelic / Scottish Gaelic
    _for_code('gd')['name']               = 'Scots Gaelic'
    _for_code('gd')['endonym']            = 'Gàidhlig'
    _for_code('gd')['translations-of']    = 'Eadar-theangachadh airson %s'
    _for_code('gd')['definitions-of']     = 'Deifiniseanan airson %s'
    _for_code('gd')['synonyms']           = 'Co-fhaclan'
    _for_code('gd')['examples']           = 'Buill-eisimpleir'
    _for_code('gd')['see-also']           = 'Faic na leanas cuideachd'
    _for_code('gd')['family']             = 'Indo-European'
    _for_code('gd')['branch']             = 'Celtic'
    _for_code('gd')['iso']                = 'gla'
    _for_code('gd')['glotto']             = 'scot1245'
    _for_code('gd')['script']             = 'Latn'
    _for_code('gd')['spoken-in']          = 'Scotland'
    _for_code('gd')['supported-by']       = 'google; yandex'

    # Sepedi (Northern Sotho)
    _for_code('nso')['name']              = 'Sepedi'
    _for_code('nso')['name2']             = 'Pedi'
    _for_code('nso')['name3']             = 'Northern Sotho'
    _for_code('nso')['endonym']           = 'Sepedi'
    #for_code('nso')['translations-of']
    #for_code('nso')['definitions-of']
    #for_code('nso')['synonyms']
    #for_code('nso')['examples']
    #for_code('nso')['see-also']
    _for_code('nso')['family']            = 'Atlantic-Congo'
    _for_code('nso')['branch']            = 'Bantu'
    _for_code('nso')['iso']               = 'nso'
    _for_code('nso')['glotto']            = 'nort3233'
    _for_code('nso')['script']            = 'Latn'
    _for_code('nso')['spoken-in']         = 'the northeastern provinces of South Africa'
    _for_code('nso')['supported-by']      = 'google'

    # Serbian, Cyrillic alphabet
    _for_code('sr-Cyrl')['name']          = 'Serbian (Cyrillic)'
    _for_code('sr-Cyrl')['endonym']       = 'Српски'
    _for_code('sr-Cyrl')['translations-of'] = 'Преводи за „%s“'
    _for_code('sr-Cyrl')['definitions-of']  = 'Дефиниције за %s'
    _for_code('sr-Cyrl')['synonyms']      = 'Синоними'
    _for_code('sr-Cyrl')['examples']      = 'Примери'
    _for_code('sr-Cyrl')['see-also']      = 'Погледајте такође'
    _for_code('sr-Cyrl')['family']        = 'Indo-European'
    _for_code('sr-Cyrl')['branch']        = 'South Slavic'
    _for_code('sr-Cyrl')['iso']           = 'srp-Cyrl'
    _for_code('sr-Cyrl')['glotto']        = 'serb1264'
    _for_code('sr-Cyrl')['script']        = 'Cyrl'
    _for_code('sr-Cyrl')['spoken-in']     = 'Serbia; Bosnia and Herzegovina; Montenegro; Kosovo'
    _for_code('sr-Cyrl')['supported-by']  = 'google; bing; yandex'

    # Serbian, Latin alphabet
    _for_code('sr-Latn')['name']          = 'Serbian (Latin)'
    _for_code('sr-Latn')['endonym']       = 'Srpski'
    _for_code('sr-Latn')['translations-of'] = 'Prevodi za „%s“'
    _for_code('sr-Latn')['definitions-of']  = 'Definicije za %s'
    _for_code('sr-Latn')['synonyms']      = 'Sinonimi'
    _for_code('sr-Latn')['examples']      = 'Primeri'
    _for_code('sr-Latn')['see-also']      = 'Pogledajte takođe'
    _for_code('sr-Latn')['family']        = 'Indo-European'
    _for_code('sr-Latn')['branch']        = 'South Slavic'
    _for_code('sr-Latn')['iso']           = 'srp-Latn'
    _for_code('sr-Latn')['glotto']        = 'serb1264'
    _for_code('sr-Latn')['script']        = 'Latn'
    _for_code('sr-Latn')['spoken-in']     = 'Serbia; Bosnia and Herzegovina; Montenegro; Kosovo'
    _for_code('sr-Latn')['supported-by']  = 'bing'

    # Sesotho (Southern Sotho)
    _for_code('st')['name']               = 'Sesotho'
    _for_code('st')['name2']              = 'Sotho'
    _for_code('st')['name3']              = 'Southern Sotho'
    _for_code('st')['endonym']            = 'Sesotho'
    _for_code('st')['translations-of']    = 'Liphetolelo tsa %s'
    _for_code('st')['definitions-of']     = 'Meelelo ea %s'
    _for_code('st')['synonyms']           = 'Mantsoe a tšoanang ka moelelo'
    _for_code('st')['examples']           = 'Mehlala'
    _for_code('st')['see-also']           = 'Bona hape'
    _for_code('st')['family']             = 'Atlantic-Congo'
    _for_code('st')['branch']             = 'Bantu'
    _for_code('st')['iso']                = 'sot'
    _for_code('st')['glotto']             = 'sout2807'
    _for_code('st')['script']             = 'Latn'
    _for_code('st')['spoken-in']          = 'Lesotho; South Africa; Zimbabwe'
    _for_code('st')['supported-by']       = 'google'

    # Setswana
    _for_code('tn')['name']               = 'Setswana'
    _for_code('tn')['name2']              = 'Tswana'
    _for_code('tn')['endonym']            = 'Setswana'
    _for_code('tn')['family']             = 'Atlantic-Congo'
    _for_code('tn')['branch']             = 'Bantu'
    _for_code('tn')['iso']                = 'tsn'
    _for_code('tn')['glotto']             = 'tswa1253'
    _for_code('tn')['script']             = 'Latn'
    _for_code('tn')['spoken-in']          = 'Botswana; South Africa'
    _for_code('tn')['supported-by']       = ''

    # Shona
    _for_code('sn')['name']               = 'Shona'
    _for_code('sn')['endonym']            = 'chiShona'
    _for_code('sn')['translations-of']    = 'Shanduro dze %s'
    _for_code('sn')['definitions-of']     = 'Zvinoreva %s'
    _for_code('sn')['synonyms']           = 'Mashoko anoreva zvakafana nemamwe'
    _for_code('sn')['examples']           = 'Mienzaniso'
    _for_code('sn')['see-also']           = 'Onawo'
    _for_code('sn')['family']             = 'Atlantic-Congo'
    _for_code('sn')['branch']             = 'Bantu'
    _for_code('sn')['iso']                = 'sna'
    _for_code('sn')['glotto']             = 'core1255'
    _for_code('sn')['script']             = 'Latn'
    _for_code('sn')['spoken-in']          = 'Zimbabwe'
    _for_code('sn')['supported-by']       = 'google'

    # Sindhi
    _for_code('sd')['name']               = 'Sindhi'
    _for_code('sd')['endonym']            = 'سنڌي'
    _for_code('sd')['translations-of']    = '%s جو ترجمو'
    _for_code('sd')['definitions-of']     = '%s جون وصفون'
    _for_code('sd')['synonyms']           = 'هم معني'
    _for_code('sd')['examples']           = 'مثالون'
    _for_code('sd')['see-also']           = 'به ڏسو'
    _for_code('sd')['family']             = 'Indo-European'
    _for_code('sd')['branch']             = 'Indo-Aryan'
    _for_code('sd')['iso']                = 'snd'
    _for_code('sd')['glotto']             = 'sind1272'
    _for_code('sd')['script']             = 'Arab'
    _for_code('sd')['rtl']                = 'true' # RTL language
    _for_code('sd')['spoken-in']          = 'the region of Sindh in Pakistan; India'
    _for_code('sd')['supported-by']       = 'google'

    # Sinhala / Sinhalese
    _for_code('si')['name']               = 'Sinhala'
    _for_code('si')['name2']              = 'Sinhalese'
    _for_code('si')['endonym']            = 'සිංහල'
    _for_code('si')['translations-of']    = '%s හි පරිවර්තන'
    _for_code('si')['definitions-of']     = '%s හි නිර්වචන'
    _for_code('si')['synonyms']           = 'සමානාර්ථ පද'
    _for_code('si')['examples']           = 'උදාහරණ'
    _for_code('si')['see-also']           = 'මෙයත් බලන්න'
    _for_code('si')['family']             = 'Indo-European'
    _for_code('si')['branch']             = 'Indo-Aryan'
    _for_code('si')['iso']                = 'sin'
    _for_code('si')['glotto']             = 'sinh1246'
    _for_code('si')['script']             = 'Sinh'
    _for_code('si')['spoken-in']          = 'Sri Lanka'
    _for_code('si')['supported-by']       = 'google; yandex'

    # Slovak
    _for_code('sk')['name']               = 'Slovak'
    _for_code('sk')['endonym']            = 'Slovenčina'
    _for_code('sk')['translations-of']    = 'Preklady výrazu: %s'
    _for_code('sk')['definitions-of']     = 'Definície výrazu %s'
    _for_code('sk')['synonyms']           = 'Synonymá'
    _for_code('sk')['examples']           = 'Príklady'
    _for_code('sk')['see-also']           = 'Pozrite tiež'
    _for_code('sk')['family']             = 'Indo-European'
    _for_code('sk')['branch']             = 'West Slavic'
    _for_code('sk')['iso']                = 'slk'
    _for_code('sk')['glotto']             = 'slov1269'
    _for_code('sk')['script']             = 'Latn'
    _for_code('sk')['spoken-in']          = 'Slovakia'
    _for_code('sk')['supported-by']       = 'google; bing; yandex'

    # Slovenian / Slovene
    _for_code('sl')['name']               = 'Slovenian'
    _for_code('sl')['name2']              = 'Slovene'
    _for_code('sl')['endonym']            = 'Slovenščina'
    _for_code('sl')['translations-of']    = 'Prevodi za %s'
    _for_code('sl')['definitions-of']     = 'Razlage za %s'
    _for_code('sl')['synonyms']           = 'Sopomenke'
    _for_code('sl')['examples']           = 'Primeri'
    _for_code('sl')['see-also']           = 'Glejte tudi'
    _for_code('sl')['family']             = 'Indo-European'
    _for_code('sl')['branch']             = 'South Slavic'
    _for_code('sl')['iso']                = 'slv'
    _for_code('sl')['glotto']             = 'slov1268'
    _for_code('sl')['script']             = 'Latn'
    _for_code('sl')['spoken-in']          = 'Slovenia'
    _for_code('sl')['supported-by']       = 'google; bing; yandex'

    # Somali
    _for_code('so')['name']               = 'Somali'
    _for_code('so')['endonym']            = 'Soomaali'
    _for_code('so')['translations-of']    = 'Turjumaada %s'
    _for_code('so')['definitions-of']     = 'Qeexitaannada %s'
    _for_code('so')['synonyms']           = 'La micne ah'
    _for_code('so')['examples']           = 'Tusaalooyin'
    _for_code('so')['see-also']           = 'Sidoo kale eeg'
    _for_code('so')['family']             = 'Afro-Asiatic'
    _for_code('so')['branch']             = 'Cushitic'
    _for_code('so')['iso']                = 'som'
    _for_code('so')['glotto']             = 'soma1255'
    _for_code('so')['script']             = 'Latn'
    _for_code('so')['spoken-in']          = 'Somalia; Somaliland; Ethiopia; Djibouti'
    _for_code('so')['supported-by']       = 'google; bing'

    # Spanish
    _for_code('es')['name']               = 'Spanish'
    _for_code('es')['endonym']            = 'Español'
    _for_code('es')['translations-of']    = 'Traducciones de %s'
    _for_code('es')['definitions-of']     = 'Definiciones de %s'
    _for_code('es')['synonyms']           = 'Sinónimos'
    _for_code('es')['examples']           = 'Ejemplos'
    _for_code('es')['see-also']           = 'Ver también'
    _for_code('es')['family']             = 'Indo-European'
    _for_code('es')['branch']             = 'Western Romance'
    _for_code('es')['iso']                = 'spa'
    _for_code('es')['glotto']             = 'stan1288'
    _for_code('es')['script']             = 'Latn'
    _for_code('es')['dictionary']         = 'true' # has dictionary
    _for_code('es')['spoken-in']          = 'Spain; the Americas'
    _for_code('es')['supported-by']       = 'google; bing; yandex'

    # Sundanese, Latin alphabet
    _for_code('su')['name']               = 'Sundanese'
    _for_code('su')['endonym']            = 'Basa Sunda'
    _for_code('su')['translations-of']    = 'Tarjamahan tina %s'
    _for_code('su')['definitions-of']     = 'Panjelasan tina %s'
    _for_code('su')['synonyms']           = 'Sinonim'
    _for_code('su')['examples']           = 'Conto'
    _for_code('su')['see-also']           = 'Tingali ogé'
    _for_code('su')['family']             = 'Austronesian'
    _for_code('su')['branch']             = 'Malayo-Polynesian'
    _for_code('su')['iso']                = 'sun'
    _for_code('su')['glotto']             = 'sund1252'
    _for_code('su')['script']             = 'Latn'
    _for_code('su')['spoken-in']          = 'Java, Indonesia'
    _for_code('su')['supported-by']       = 'google; yandex'

    # Swahili / Kiswahili, Latin script
    _for_code('sw')['name']               = 'Swahili'
    _for_code('sw')['name2']              = 'Kiswahili'
    _for_code('sw')['endonym']            = 'Kiswahili'
    _for_code('sw')['translations-of']    = 'Tafsiri ya %s'
    _for_code('sw')['definitions-of']     = 'Ufafanuzi wa %s'
    _for_code('sw')['synonyms']           = 'Visawe'
    _for_code('sw')['examples']           = 'Mifano'
    _for_code('sw')['see-also']           = 'Angalia pia'
    _for_code('sw')['family']             = 'Atlantic-Congo'
    _for_code('sw')['branch']             = 'Bantu'
    _for_code('sw')['iso']                = 'swa'
    _for_code('sw')['glotto']             = 'swah1253'
    _for_code('sw')['script']             = 'Latn'
    _for_code('sw')['spoken-in']          = 'the East African coast and litoral islands'
    _for_code('sw')['supported-by']       = 'google; bing; yandex'

    # Swedish
    _for_code('sv')['name']               = 'Swedish'
    _for_code('sv')['endonym']            = 'Svenska'
    _for_code('sv')['translations-of']    = 'Översättningar av %s'
    _for_code('sv')['definitions-of']     = 'Definitioner av %s'
    _for_code('sv')['synonyms']           = 'Synonymer'
    _for_code('sv')['examples']           = 'Exempel'
    _for_code('sv')['see-also']           = 'Se även'
    _for_code('sv')['family']             = 'Indo-European'
    _for_code('sv')['branch']             = 'North Germanic'
    _for_code('sv')['iso']                = 'swe'
    _for_code('sv')['glotto']             = 'swed1254'
    _for_code('sv')['script']             = 'Latn'
    _for_code('sv')['spoken-in']          = 'Sweden; Finland; Estonia'
    _for_code('sv')['supported-by']       = 'google; bing; yandex'

    # Tahitian
    _for_code('ty')['name']               = 'Tahitian'
    _for_code('ty')['endonym']            = 'Reo Tahiti'
    _for_code('ty')['family']             = 'Austronesian'
    _for_code('ty')['branch']             = 'Malayo-Polynesian'
    _for_code('ty')['iso']                = 'tah'
    _for_code('ty')['glotto']             = 'tahi1242'
    _for_code('ty')['script']             = 'Latn'
    _for_code('ty')['spoken-in']          = 'French Polynesia'
    _for_code('ty')['supported-by']       = 'bing'

    # Tajik / Tajiki (Tajiki Persian), Cyrillic alphabet
    _for_code('tg')['name']               = 'Tajik'
    _for_code('tg')['name2']              = 'Tajiki'
    _for_code('tg')['endonym']            = 'Тоҷикӣ'
    _for_code('tg')['translations-of']    = 'Тарҷумаҳои %s'
    _for_code('tg')['definitions-of']     = 'Таърифҳои %s'
    _for_code('tg')['synonyms']           = 'Муродифҳо'
    _for_code('tg')['examples']           = 'Намунаҳо:'
    _for_code('tg')['see-also']           = 'Ҳамчунин Бинед'
    _for_code('tg')['family']             = 'Indo-European'
    _for_code('tg')['branch']             = 'Iranian'
    _for_code('tg')['iso']                = 'tgk'
    _for_code('tg')['glotto']             = 'taji1245'
    _for_code('tg')['script']             = 'Cyrl'
    _for_code('tg')['spoken-in']          = 'Tajikistan; Uzbekistan'
    _for_code('tg')['supported-by']       = 'google; yandex'

    # Tamil
    _for_code('ta')['name']               = 'Tamil'
    _for_code('ta')['endonym']            = 'தமிழ்'
    _for_code('ta')['translations-of']    = '%s இன் மொழிபெயர்ப்புகள்'
    _for_code('ta')['definitions-of']     = '%s இன் வரையறைகள்'
    _for_code('ta')['synonyms']           = 'இணைச்சொற்கள்'
    _for_code('ta')['examples']           = 'எடுத்துக்காட்டுகள்'
    _for_code('ta')['see-also']           = 'இதையும் காண்க'
    _for_code('ta')['family']             = 'Dravidian'
    _for_code('ta')['branch']             = 'South Dravidian'
    _for_code('ta')['iso']                = 'tam'
    _for_code('ta')['glotto']             = 'tami1289'
    _for_code('ta')['script']             = 'Taml'
    _for_code('ta')['spoken-in']          = 'the Indian state of Tamil Nadu; Sri Lanka; Singapore'
    _for_code('ta')['supported-by']       = 'google; bing; yandex'

    # Tatar, Cyrillic alphabet
    _for_code('tt')['name']               = 'Tatar'
    _for_code('tt')['endonym']            = 'татарча'
    #for_code('tt')['translations-of']
    #for_code('tt')['definitions-of']
    #for_code('tt')['synonyms']
    #for_code('tt')['examples']
    #for_code('tt')['see-also']
    _for_code('tt')['family']             = 'Turkic'
    _for_code('tt')['branch']             = 'Kipchak'
    _for_code('tt')['iso']                = 'tat'
    _for_code('tt')['glotto']             = 'tata1255'
    _for_code('tt')['script']             = 'Cyrl'
    _for_code('tt')['spoken-in']          = 'the Republic of Tatarstan in Russia'
    _for_code('tt')['supported-by']       = 'google; bing; yandex'

    # Telugu
    _for_code('te')['name']               = 'Telugu'
    _for_code('te')['endonym']            = 'తెలుగు'
    _for_code('te')['translations-of']    = '%s యొక్క అనువాదాలు'
    _for_code('te')['definitions-of']     = '%s యొక్క నిర్వచనాలు'
    _for_code('te')['synonyms']           = 'పర్యాయపదాలు'
    _for_code('te')['examples']           = 'ఉదాహరణలు'
    _for_code('te')['see-also']           = 'వీటిని కూడా చూడండి'
    _for_code('te')['family']             = 'Dravidian'
    _for_code('te')['branch']             = 'South-Central Dravidian'
    _for_code('te')['iso']                = 'tel'
    _for_code('te')['glotto']             = 'telu1262'
    _for_code('te')['script']             = 'Telu'
    _for_code('te')['spoken-in']          = 'the Indian states of Andhra Pradesh and Telangana'
    _for_code('te')['supported-by']       = 'google; bing; yandex'

    # Thai
    _for_code('th')['name']               = 'Thai'
    _for_code('th')['endonym']            = 'ไทย'
    _for_code('th')['translations-of']    = 'คำแปลของ %s'
    _for_code('th')['definitions-of']     = 'คำจำกัดความของ %s'
    _for_code('th')['synonyms']           = 'คำพ้องความหมาย'
    _for_code('th')['examples']           = 'ตัวอย่าง'
    _for_code('th')['see-also']           = 'ดูเพิ่มเติม'
    _for_code('th')['family']             = 'Kra-Dai'
    _for_code('th')['branch']             = 'Tai'
    _for_code('th')['iso']                = 'tha'
    _for_code('th')['glotto']             = 'thai1261'
    _for_code('th')['script']             = 'Thai'
    _for_code('th')['spoken-in']          = 'Thailand'
    _for_code('th')['supported-by']       = 'google; bing; yandex'

    # Tibetan (Standard Tibetan)
    _for_code('bo')['name']               = 'Tibetan'
    _for_code('bo')['endonym']            = 'བོད་ཡིག'
    #for_code('bo')['translations-of']
    #for_code('bo')['definitions-of']
    #for_code('bo')['synonyms']
    #for_code('bo')['examples']
    #for_code('bo')['see-also']
    _for_code('bo')['family']             = 'Sino-Tibetan'
    _for_code('bo')['branch']             = 'Tibetic'
    _for_code('bo')['iso']                = 'bod'
    _for_code('bo')['glotto']             = 'tibe1272'
    _for_code('bo')['script']             = 'Tibt'
    _for_code('bo')['spoken-in']          = 'the Tibet Autonomous Region of China'
    _for_code('bo')['supported-by']       = 'bing'

    # Tigrinya
    _for_code('ti')['name']               = 'Tigrinya'
    _for_code('ti')['endonym']            = 'ትግርኛ'
    #for_code('ti')['translations-of']
    #for_code('ti')['definitions-of']
    #for_code('ti')['synonyms']
    #for_code('ti')['examples']
    #for_code('ti')['see-also']
    _for_code('ti')['family']             = 'Afro-Asiatic'
    _for_code('ti')['branch']             = 'Semitic'
    _for_code('ti')['iso']                = 'tir'
    _for_code('ti')['glotto']             = 'tigr1271'
    _for_code('ti')['script']             = 'Ethi'
    _for_code('ti')['spoken-in']          = 'Eritrea; the Tigray region of northern Ethiopia'
    _for_code('ti')['supported-by']       = 'google; bing'

    # Tongan
    _for_code('to')['name']               = 'Tongan'
    _for_code('to')['endonym']            = 'Lea faka-Tonga'
    _for_code('to')['family']             = 'Austronesian'
    _for_code('to')['branch']             = 'Malayo-Polynesian'
    _for_code('to')['iso']                = 'ton'
    _for_code('to')['glotto']             = 'tong1325'
    _for_code('to')['script']             = 'Latn'
    _for_code('to')['spoken-in']          = 'Tonga'
    _for_code('to')['supported-by']       = 'bing'

    # Tsonga
    _for_code('ts')['name']               = 'Tsonga'
    _for_code('ts')['endonym']            = 'Xitsonga'
    #for_code('ts')['translations-of']
    #for_code('ts')['definitions-of']
    #for_code('ts')['synonyms']
    #for_code('ts')['examples']
    #for_code('ts')['see-also']
    _for_code('ts')['family']             = 'Atlantic-Congo'
    _for_code('ts')['branch']             = 'Bantu'
    _for_code('ts')['iso']                = 'tso'
    _for_code('ts')['glotto']             = 'tson1249'
    _for_code('ts')['script']             = 'Latn'
    _for_code('ts')['spoken-in']          = 'Eswatini; Mozambique; South Africa; Zimbabwe'
    _for_code('ts')['supported-by']       = 'google'

    # Turkish
    _for_code('tr')['name']               = 'Turkish'
    _for_code('tr')['endonym']            = 'Türkçe'
    _for_code('tr')['translations-of']    = '%s çevirileri'
    _for_code('tr')['definitions-of']     = '%s için tanımlar'
    _for_code('tr')['synonyms']           = 'Eş anlamlılar'
    _for_code('tr')['examples']           = 'Örnekler'
    _for_code('tr')['see-also']           = 'Ayrıca bkz.'
    _for_code('tr')['family']             = 'Turkic'
    _for_code('tr')['branch']             = 'Oghuz'
    _for_code('tr')['iso']                = 'tur'
    _for_code('tr')['glotto']             = 'nucl1301'
    _for_code('tr')['script']             = 'Latn'
    _for_code('tr')['spoken-in']          = 'Türkiye; Cyprus'
    _for_code('tr')['supported-by']       = 'google; bing; yandex'

    # Turkmen, Latin script
    _for_code('tk')['name']               = 'Turkmen'
    _for_code('tk')['endonym']            = 'Türkmen'
    #for_code('tk')['translations-of']
    #for_code('tk')['definitions-of']
    #for_code('tk')['synonyms']
    #for_code('tk')['examples']
    #for_code('tk')['see-also']
    _for_code('tk')['family']             = 'Turkic'
    _for_code('tk')['branch']             = 'Oghuz'
    _for_code('tk')['iso']                = 'tuk'
    _for_code('tk')['glotto']             = 'turk1304'
    _for_code('tk')['script']             = 'Latn'
    _for_code('tk')['spoken-in']          = 'Turkmenistan; Iran; Afghanistan; Pakistan'
    _for_code('tk')['supported-by']       = 'google; bing'

    # Twi
    _for_code('tw')['name']               = 'Twi'
    _for_code('tw')['name2']              = 'Akan Kasa'
    _for_code('tw')['endonym']            = 'Twi'
    #for_code('tw')['translations-of']
    #for_code('tw')['definitions-of']
    #for_code('tw')['synonyms']
    #for_code('tw')['examples']
    #for_code('tw')['see-also']
    _for_code('tw')['family']             = 'Atlantic-Congo'
    _for_code('tw')['branch']             = 'Kwa'
    _for_code('tw')['iso']                = 'twi'
    _for_code('tw')['glotto']             = 'akua1239'
    _for_code('tw')['script']             = 'Latn'
    _for_code('tw')['spoken-in']          = 'Ghana'
    _for_code('tw')['supported-by']       = 'google'

    # Udmurt
    _for_code('udm')['name']              = 'Udmurt'
    _for_code('udm')['endonym']           = 'Удмурт'
    _for_code('udm')['family']            = 'Uralic'
    _for_code('udm')['branch']            = 'Permic'
    _for_code('udm')['iso']               = 'udm'
    _for_code('udm')['glotto']            = 'udmu1245'
    _for_code('udm')['script']            = 'Cyrl'
    _for_code('udm')['spoken-in']         = 'the Republic of Udmurt in Russia'
    _for_code('udm')['supported-by']      = 'yandex'

    # Ukrainian
    _for_code('uk')['name']               = 'Ukrainian'
    _for_code('uk')['endonym']            = 'Українська'
    _for_code('uk')['translations-of']    = 'Переклади слова або виразу \'%s\''
    _for_code('uk')['definitions-of']     = '\'%s\' – визначення'
    _for_code('uk')['synonyms']           = 'Синоніми'
    _for_code('uk')['examples']           = 'Приклади'
    _for_code('uk')['see-also']           = 'Дивіться також'
    _for_code('uk')['family']             = 'Indo-European'
    _for_code('uk')['branch']             = 'East Slavic'
    _for_code('uk')['iso']                = 'ukr'
    _for_code('uk')['glotto']             = 'ukra1253'
    _for_code('uk')['script']             = 'Cyrl'
    _for_code('uk')['spoken-in']          = 'Ukraine'
    _for_code('uk')['supported-by']       = 'google; bing; yandex'

    # Upper Sorbian
    _for_code('hsb')['name']              = 'Upper Sorbian'
    _for_code('hsb')['endonym']           = 'Hornjoserbšćina'
    _for_code('hsb')['family']            = 'Indo-European'
    _for_code('hsb')['branch']            = 'West Slavic'
    _for_code('hsb')['iso']               = 'hsb'
    _for_code('hsb')['glotto']            = 'uppe1395'
    _for_code('hsb')['script']            = 'Latn'
    _for_code('hsb')['spoken-in']         = 'Saxony, Germany'
    _for_code('hsb')['supported-by']      = 'bing'

    # Urdu
    _for_code('ur')['name']               = 'Urdu'
    _for_code('ur')['endonym']            = 'اُردُو'
    _for_code('ur')['translations-of']    = 'کے ترجمے %s'
    _for_code('ur')['definitions-of']     = 'کی تعریفات %s'
    _for_code('ur')['synonyms']           = 'مترادفات'
    _for_code('ur')['examples']           = 'مثالیں'
    _for_code('ur')['see-also']           = 'نیز دیکھیں'
    _for_code('ur')['family']             = 'Indo-European'
    _for_code('ur')['branch']             = 'Indo-Aryan'
    _for_code('ur')['iso']                = 'urd'
    _for_code('ur')['glotto']             = 'urdu1245'
    _for_code('ur')['script']             = 'Arab'
    _for_code('ur')['rtl']                = 'true' # RTL language
    _for_code('ur')['spoken-in']          = 'Pakistan; India'
    _for_code('ur')['supported-by']       = 'google; bing; yandex'

    # Uyghur
    _for_code('ug')['name']               = 'Uyghur'
    _for_code('ug')['endonym']            = 'ئۇيغۇر تىلى'
    #for_code('ug')['translations-of']
    #for_code('ug')['definitions-of']
    #for_code('ug')['synonyms']
    #for_code('ug')['examples']
    #for_code('ug')['see-also']
    _for_code('ug')['family']             = 'Turkic'
    _for_code('ug')['branch']             = 'Karluk'
    _for_code('ug')['iso']                = 'uig'
    _for_code('ug')['glotto']             = 'uigh1240'
    _for_code('ug')['script']             = 'Arab'
    _for_code('ug')['rtl']                = 'true' # RTL language
    _for_code('ug')['spoken-in']          = 'the Xinjiang Uyghur Autonomous Region of China'
    _for_code('ug')['supported-by']       = 'google; bing'

    # Uzbek, Latin alphabet
    _for_code('uz')['name']               = 'Uzbek'
    _for_code('uz')['endonym']            = 'Oʻzbek tili'
    _for_code('uz')['translations-of']    = '%s: tarjima variantlari'
    _for_code('uz')['definitions-of']     = '%s – ta’riflar'
    _for_code('uz')['synonyms']           = 'Sinonimlar'
    _for_code('uz')['examples']           = 'Namunalar'
    _for_code('uz')['see-also']           = 'O‘xshash so‘zlar'
    _for_code('uz')['family']             = 'Turkic'
    _for_code('uz')['branch']             = 'Karluk'
    _for_code('uz')['iso']                = 'uzb'
    _for_code('uz')['glotto']             = 'uzbe1247'
    _for_code('uz')['script']             = 'Latn'
    _for_code('uz')['spoken-in']          = 'Uzbekistan; Afghanistan; Pakistan'
    _for_code('uz')['supported-by']       = 'google; bing; yandex'

    # Vietnamese
    _for_code('vi')['name']               = 'Vietnamese'
    _for_code('vi')['endonym']            = 'Tiếng Việt'
    _for_code('vi')['translations-of']    = 'Bản dịch của %s'
    _for_code('vi')['definitions-of']     = 'Nghĩa của %s'
    _for_code('vi')['synonyms']           = 'Từ đồng nghĩa'
    _for_code('vi')['examples']           = 'Ví dụ'
    _for_code('vi')['see-also']           = 'Xem thêm'
    _for_code('vi')['family']             = 'Austroasiatic'
    _for_code('vi')['branch']             = 'Vietic'
    _for_code('vi')['iso']                = 'vie'
    _for_code('vi')['glotto']             = 'viet1252'
    _for_code('vi')['script']             = 'Latn'
    _for_code('vi')['spoken-in']          = 'Vietnam'
    _for_code('vi')['supported-by']       = 'google; bing; yandex'

    # Volapük
    _for_code('vo')['name']               = 'Volapük'
    _for_code('vo')['endonym']            = 'Volapük'
    #for_code('vo')['translations-of']
    #for_code('vo')['definitions-of']
    #for_code('vo')['synonyms']
    #for_code('vo')['examples']
    #for_code('vo')['see-also']
    _for_code('vo')['family']             = 'Constructed language'
    #for_code('vo')['branch']
    _for_code('vo')['iso']                = 'vol'
    _for_code('vo')['glotto']             = 'vola1234'
    _for_code('vo')['script']             = 'Latn'
    _for_code('vo')['spoken-in']          = 'worldwide'
    _for_code('vo')['description']        = 'an international auxiliary language'
    _for_code('vo')['supported-by']       = ''

    # Welsh
    _for_code('cy')['name']               = 'Welsh'
    _for_code('cy')['endonym']            = 'Cymraeg'
    _for_code('cy')['translations-of']    = 'Cyfieithiadau %s'
    _for_code('cy')['definitions-of']     = 'Diffiniadau %s'
    _for_code('cy')['synonyms']           = 'Cyfystyron'
    _for_code('cy')['examples']           = 'Enghreifftiau'
    _for_code('cy')['see-also']           = 'Gweler hefyd'
    _for_code('cy')['family']             = 'Indo-European'
    _for_code('cy')['branch']             = 'Celtic'
    _for_code('cy')['iso']                = 'cym'
    _for_code('cy')['glotto']             = 'wels1247'
    _for_code('cy')['script']             = 'Latn'
    _for_code('cy')['spoken-in']          = 'Wales in the UK'
    _for_code('cy')['supported-by']       = 'google; bing; yandex'

    # West Frisian
    _for_code('fy')['name']               = 'Frisian'
    _for_code('fy')['endonym']            = 'Frysk'
    _for_code('fy')['translations-of']    = 'Oersettings fan %s'
    _for_code('fy')['definitions-of']     = 'Definysjes fan %s'
    _for_code('fy')['synonyms']           = 'Synonimen'
    _for_code('fy')['examples']           = 'Foarbylden'
    _for_code('fy')['see-also']           = 'Sjoch ek'
    _for_code('fy')['family']             = 'Indo-European'
    _for_code('fy')['branch']             = 'West Germanic'
    _for_code('fy')['iso']                = 'fry'
    _for_code('fy')['glotto']             = 'west2354'
    _for_code('fy')['script']             = 'Latn'
    _for_code('fy')['spoken-in']          = 'Friesland in the Netherlands'
    _for_code('fy')['supported-by']       = 'google'

    # Wolof
    _for_code('wo')['name']               = 'Wolof'
    _for_code('wo')['endonym']            = 'Wollof'
    #for_code('wo')['translations-of']
    #for_code('wo')['definitions-of']
    #for_code('wo')['synonyms']
    #for_code('wo')['examples']
    #for_code('wo')['see-also']
    _for_code('wo')['family']             = 'Atlantic-Congo'
    _for_code('wo')['branch']             = 'Atlantic'
    _for_code('wo')['iso']                = 'wol'
    _for_code('wo')['glotto']             = 'wolo1247'
    _for_code('wo')['script']             = 'Latn'
    _for_code('wo')['spoken-in']          = 'Senegal; Mauritania; the Gambia'
    _for_code('wo')['supported-by']       = ''

    # Xhosa
    _for_code('xh')['name']               = 'Xhosa'
    _for_code('xh')['endonym']            = 'isiXhosa'
    _for_code('xh')['translations-of']    = 'Iinguqulelo zika-%s'
    _for_code('xh')['definitions-of']     = 'Iingcaciso zika-%s'
    _for_code('xh')['synonyms']           = 'Izithethantonye'
    _for_code('xh')['examples']           = 'Imizekelo'
    _for_code('xh')['see-also']           = 'Kwakhona bona'
    _for_code('xh')['family']             = 'Atlantic-Congo'
    _for_code('xh')['branch']             = 'Bantu'
    _for_code('xh')['iso']                = 'xho'
    _for_code('xh')['glotto']             = 'xhos1239'
    _for_code('xh')['script']             = 'Latn'
    _for_code('xh')['spoken-in']          = 'South Africa; Zimbabwe'
    _for_code('xh')['supported-by']       = 'google; yandex'

    # Yakut / Sakha
    _for_code('sah')['name']              = 'Yakut'
    _for_code('sah')['name2']             = 'Sakha'
    _for_code('sah')['endonym']           = 'Sakha'
    _for_code('sah')['family']            = 'Turkic'
    _for_code('sah')['branch']            = 'Siberian Turkic'
    _for_code('sah')['iso']               = 'sah'
    _for_code('sah')['glotto']            = 'yaku1245'
    _for_code('sah')['script']            = 'Latn'
    _for_code('sah')['spoken-in']         = 'the Republic of Sakha (Yakutia) in Russia'
    _for_code('sah')['supported-by']      = 'yandex'

    # Yiddish
    _for_code('yi')['name']               = 'Yiddish'
    _for_code('yi')['endonym']            = 'ייִדיש'
    _for_code('yi')['translations-of']    = 'איבערזעצונגען פון %s'
    _for_code('yi')['definitions-of']     = 'דפיניציונען %s'
    _for_code('yi')['synonyms']           = 'סינאָנימען'
    _for_code('yi')['examples']           = 'ביישפילע'
    _for_code('yi')['see-also']           = 'זייען אויך'
    _for_code('yi')['family']             = 'Indo-European'
    _for_code('yi')['branch']             = 'West Germanic'
    _for_code('yi')['iso']                = 'yid'
    _for_code('yi')['glotto']             = 'yidd1255'
    _for_code('yi')['script']             = 'Hebr'
    _for_code('yi')['rtl']                = 'true' # RTL language
    _for_code('yi')['spoken-in']          = 'worldwide'
    _for_code('yi')['description']        = 'a West Germanic language historically spoken by Ashkenazi Jews'
    _for_code('yi')['supported-by']       = 'google; yandex'

    # Yoruba
    _for_code('yo')['name']               = 'Yoruba'
    _for_code('yo')['endonym']            = 'Yorùbá'
    _for_code('yo')['translations-of']    = 'Awọn itumọ ti %s'
    _for_code('yo')['definitions-of']     = 'Awọn itumọ ti %s'
    _for_code('yo')['synonyms']           = 'Awọn ọrọ onitumọ'
    _for_code('yo')['examples']           = 'Awọn apẹrẹ'
    _for_code('yo')['see-also']           = 'Tun wo'
    _for_code('yo')['family']             = 'Atlantic-Congo'
    #for_code('yo')['branch']
    _for_code('yo')['iso']                = 'yor'
    _for_code('yo')['glotto']             = 'yoru1245'
    _for_code('yo')['script']             = 'Latn'
    _for_code('yo')['spoken-in']          = 'Nigeria; Benin'
    _for_code('yo')['supported-by']       = 'google'

    # Yucatec Maya
    _for_code('yua')['name']              = 'Yucatec Maya'
    _for_code('yua')['endonym']           = 'Màaya T\'àan'
    _for_code('yua')['family']            = 'Mayan'
    #for_code('yua')['branch']
    _for_code('yua')['iso']               = 'yua'
    _for_code('yua')['glotto']            = 'yuca1254'
    _for_code('yua')['script']            = 'Latn'
    _for_code('yua')['spoken-in']         = 'Mexico; Belize'
    _for_code('yua')['supported-by']      = 'bing'

    # Zulu
    _for_code('zu')['name']               = 'Zulu'
    _for_code('zu')['endonym']            = 'isiZulu'
    _for_code('zu')['translations-of']    = 'Ukuhumusha i-%s'
    _for_code('zu')['definitions-of']     = 'Izincazelo ze-%s'
    _for_code('zu')['synonyms']           = 'Amagama afanayo'
    _for_code('zu')['examples']           = 'Izibonelo'
    _for_code('zu')['see-also']           = 'Bheka futhi'
    _for_code('zu')['family']             = 'Atlantic-Congo'
    _for_code('zu')['branch']             = 'Bantu'
    _for_code('zu')['iso']                = 'zul'
    _for_code('zu')['glotto']             = 'zulu1248'
    _for_code('zu')['script']             = 'Latn'
    _for_code('zu')['spoken-in']          = 'South Africa; Lesotho; Eswatini'
    _for_code('zu')['supported-by']       = 'google; bing; yandex'


def init_locale_alias():
    """Initialize aliases of all locales supported."""
    for i in LOCALES:
        # ISO 639-3 codes as aliases
        if 'iso' in LOCALES[i]:
            LOCALE_ALIAS[LOCALES[i]['iso']] = i
        # Names and endonyms as aliases
        if 'name' in LOCALES[i]:
            LOCALE_ALIAS[LOCALES[i]['name'].lower()] = i
        if 'name2' in LOCALES[i]:
            LOCALE_ALIAS[LOCALES[i]['name2'].lower()] = i
        if 'endonym' in LOCALES[i]:
            LOCALE_ALIAS[LOCALES[i]['endonym'].lower()] = i
        if 'endonym2' in LOCALES[i]:
            LOCALE_ALIAS[LOCALES[i]['endonym2'].lower()] = i

    # Other aliases
    # See: <http://www.loc.gov/standards/iso639-2/php/code_changes.php>
    LOCALE_ALIAS['in'] = 'id'  # withdrawn language code for Indonesian
    LOCALE_ALIAS['iw'] = 'he'  # withdrawn language code for Hebrew
    LOCALE_ALIAS['ji'] = 'yi'  # withdrawn language code for Yiddish
    LOCALE_ALIAS['jw'] = 'jv'  # withdrawn language code for Javanese
    LOCALE_ALIAS['kurdish'] = 'ku'  # Kurdish: default to 'ku' (N.B. Google uses this code for Kurmanji)
    LOCALE_ALIAS['mari'] = 'mhr'  # Mari: default to 'mhr' (Eastern Mari)
    LOCALE_ALIAS['mo'] = 'ro'  # Moldavian or Moldovan considered a variant of the Romanian language
    LOCALE_ALIAS['moldavian'] = 'ro'
    LOCALE_ALIAS['moldovan'] = 'ro'
    LOCALE_ALIAS['mww'] = 'hmn'  # mww (Hmong Daw) treated the same as hmn (the inclusive code for Hmong)
    LOCALE_ALIAS['nb'] = 'no'  # Google Translate does not distinguish between Bokmål and Nynorsk (but Bing does!)
    LOCALE_ALIAS['nn'] = 'no'
    LOCALE_ALIAS['pt'] = 'pt-BR'  # Portuguese: default to Brazilian Portuguese (as in Google Translate)
    LOCALE_ALIAS['portuguese'] = 'pt-BR'
    LOCALE_ALIAS['sh'] = 'sr-Cyrl'  # Serbo-Croatian: default to Serbian
    LOCALE_ALIAS['sr'] = 'sr-Cyrl'  # Serbian: default to Serbian Cyrillic
    LOCALE_ALIAS['srp'] = 'sr-Cyrl'
    LOCALE_ALIAS['serbian'] = 'sr-Cyrl'
    LOCALE_ALIAS['zh'] = 'zh-CN'  # Chinese: default to Chinese Simplified
    LOCALE_ALIAS['zh-CHS'] = 'zh-CN'
    LOCALE_ALIAS['zh-CHT'] = 'zh-TW'
    LOCALE_ALIAS['zh-Hans'] = 'zh-CN'
    LOCALE_ALIAS['zh-Hant'] = 'zh-TW'
    LOCALE_ALIAS['zho'] = 'zh-CN'
    LOCALE_ALIAS['chinese'] = 'zh-CN'
    LOCALE_ALIAS['tlh'] = 'tlh-Latn'
    LOCALE_ALIAS['mni'] = 'mni-Mtei'  # Meitei: default to Meitei Mayek
    # TODO: more aliases (sic!)


def init_locale_display():
    """Initialize strings for displaying endonyms of all locales supported."""
    for i in LOCALES:
        if 'endonym' in LOCALES[i]:
            LOCALES[i]['display'] = show(LOCALES[i]['endonym'], i)


Cache = {}
UserLang = None
UserLocale = None
# TODO: Load
FriBidi = False
BiDi = None
BiDiNoPad = None


def get_code(code):
    """Get locale key by language code or alias."""
    if code == 'auto' or code in LOCALES:
        return code
    elif code in LOCALE_ALIAS:
        return LOCALE_ALIAS[code]
    elif code.lower() in LOCALE_ALIAS:
        return LOCALE_ALIAS[code.lower()]

    # Remove unidentified region or script code
    match = re.match(r'^([a-zA-Z]{2,3})-(.*)$', code)
    if match:
        return match.group(1)

    return None  # return None if not found


def get_name(code):
    """Return the name of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('name', '')
    return ''


def get_names(code):
    """Return all the names of a language, separated by '/'."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        locale = LOCALES[locale_code]
        if 'name2' in locale:
            return f'{locale['name']} / {locale['name2']}'
        else:
            return locale.get('name', '')
    return ''


def get_endonym(code):
    """Return the endonym of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('endonym', '')
    return ''


def get_display(code):
    """Return the string for displaying the endonym of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('display', '')
    return ''


def show_translations_of(code):
    """Return localized version of 'translations of'."""
    locale_code = get_code(code)
    localized = None
    if locale_code and locale_code in LOCALES:
        localized = LOCALES[locale_code].get('translations-of')
    if not localized:
        localized = LOCALES['en'].get('translations-of')
    return localized


def show_definitions_of(code):
    """Return localized version of 'definitions of'."""
    locale_code = get_code(code)
    localized = None
    if locale_code and locale_code in LOCALES:
        localized = LOCALES[locale_code].get('definitions-of')
    if not localized:
        localized = LOCALES['en'].get('definitions-of')
    return localized


def show_synonyms(code):
    """Return a string of 'synonyms'."""
    locale_code = get_code(code)
    tmp = None
    if locale_code and locale_code in LOCALES:
        tmp = LOCALES[locale_code].get('synonyms')
    if not tmp and 'en' in LOCALES:
        tmp = LOCALES['en'].get('synonyms')
    return tmp or ''


def show_examples(code):
    """Return a string of 'examples'."""
    locale_code = get_code(code)
    tmp = None
    if locale_code and locale_code in LOCALES:
        tmp = LOCALES[locale_code].get('examples')
    if not tmp and 'en' in LOCALES:
        tmp = LOCALES['en'].get('examples')
    return tmp or ''


def show_see_also(code):
    """Return a string of 'see also'."""
    locale_code = get_code(code)
    tmp = None
    if locale_code and locale_code in LOCALES:
        tmp = LOCALES[locale_code].get('see-also')
    if not tmp and 'en' in LOCALES:
        tmp = LOCALES['en'].get('see-also')
    return tmp or ''


def get_family(code):
    """Return the family of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('family', '')
    return ''


def get_branch(code):
    """Return the branch of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('branch', '')
    return ''


def get_iso(code):
    """Return the ISO 639-3 code of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('iso', '')
    return ''


def get_glotto(code):
    """Return the Glottocode of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('glotto', '')
    return ''


def get_script(code):
    """Return the ISO 15924 script code of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('script', '')
    return ''


def is_rtl(code):
    """Return True if a language is R-to-L; otherwise return False."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return bool(LOCALES[locale_code].get('rtl', False))
    return False


def has_dictionary(code):
    """Return True if Google provides dictionary data for a language; otherwise return False."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return bool(LOCALES[locale_code].get('dictionary', False))
    return False


def script_name(code):
    """Return the name of script (writing system)."""
    script_names = {
        'Arab': 'Arabic',
        'Armn': 'Armenian',
        'Beng': 'Bengali',
        'Cans': 'Canadian Aboriginal Syllabics',
        'Cher': 'Cherokee',
        'Cyrl': 'Cyrillic',
        'Deva': 'Devanagari',
        'Ethi': 'Ethiopic (Geʻez)',
        'Geor': 'Georgian (Mkhedruli)',
        'Grek': 'Greek',
        'Gujr': 'Gujarati',
        'Guru': 'Gurmukhi',
        'Hani': 'Han',
        'Hans': 'Han (Simplified)',
        'Hant': 'Han (Traditional)',
        'Hebr': 'Hebrew',
        'Jpan': 'Japanese (Han + Hiragana + Katakana)',
        'Khmr': 'Khmer',
        'Knda': 'Kannada',
        'Kore': 'Korean (Hangul + Han)',
        'Laoo': 'Lao',
        'Latn': 'Latin',
        'Mlym': 'Malayalam',
        'Mong': 'Mongolian',
        'Mtei': 'Meitei Mayek',
        'Mymr': 'Myanmar',
        'Orya': 'Oriya',
        'Sinh': 'Sinhala',
        'Taml': 'Tamil',
        'Telu': 'Telugu',
        'Thaa': 'Thaana',
        'Thai': 'Thai',
        'Tibt': 'Tibetan'
    }
    return script_names.get(code, 'Unknown')


def get_spoken_in(code):
    """Return the regions that a language is spoken in, as an English string."""
    locale_code = get_code(code)
    if not locale_code or locale_code not in LOCALES:
        return ''

    spoken_in = LOCALES[locale_code].get('spoken-in', '')
    if not spoken_in:
        return ''

    regions = [region.strip() for region in spoken_in.split(';')]
    if len(regions) == 1:
        return regions[0]
    elif len(regions) == 2:
        return f'{regions[0]} and {regions[1]}'
    else:
        return ', '.join(regions[:-1]) + f' and {regions[-1]}'


def get_written_in(code):
    """Return the regions that a script is written in, as an English string."""
    locale_code = get_code(code)
    if not locale_code or locale_code not in LOCALES:
        return ''

    written_in = LOCALES[locale_code].get('written-in', '')
    if not written_in:
        return ''

    regions = [region.strip() for region in written_in.split(';')]
    if len(regions) == 1:
        return regions[0]
    elif len(regions) == 2:
        return f'{regions[0]} and {regions[1]}'
    else:
        return ', '.join(regions[:-1]) + f' and {regions[-1]}'


def get_description(code):
    """Return the extra description of a language."""
    locale_code = get_code(code)
    if locale_code and locale_code in LOCALES:
        return LOCALES[locale_code].get('description', '')
    return ''


def is_supported_by_google(code):
    """Return True if a language is supported by Google; otherwise return False."""
    locale_code = get_code(code)
    if not locale_code or locale_code not in LOCALES:
        return False

    supported_by = LOCALES[locale_code].get('supported-by', '')
    if supported_by:
        engines = [engine.strip() for engine in supported_by.split(';')]
        return 'google' in engines
    return False


def is_supported_by_bing(code):
    """Return True if a language is supported by Bing; otherwise return False."""
    locale_code = get_code(code)
    if not locale_code or locale_code not in LOCALES:
        return False

    supported_by = LOCALES[locale_code].get('supported-by', '')
    if supported_by:
        engines = [engine.strip() for engine in supported_by.split(';')]
        return 'bing' in engines
    return False


def e(text):
    """Print error message to stderr."""
    print(text, file=sys.stderr)


def w(text):
    """Print warning message to stderr."""
    print(text, file=sys.stderr)


def get_details(code):
    """Return detailed information of a language as a string."""
    if code == 'auto' or not get_code(code):
        e(f'[ERROR] Language not found: {code}\n'
          '        Run \'-reference / -R\' to see a list of available languages.')
        sys.exit(1)

    locale_code = get_code(code)
    script = script_name(get_script(code))
    if is_rtl(code):
        script += ' (R-to-L)'

    iso_parts = get_iso(code).split('-')
    iso = iso_parts[0] if iso_parts else ''

    name = get_name(code)
    names = get_names(code)
    writing = ''

    # Extract writing system from parentheses in name
    paren_match = re.search(r'\(.*\)', name)
    if paren_match:
        writing = paren_match.group(0)[1:-1]  # Remove parentheses
        name = name[:paren_match.start()].strip()

    # Build description
    if get_description(code):
        desc = f'{names} is {get_description(code)}.'
    elif get_branch(code):
        article = 'an' if get_branch(code).lower().startswith(('a', 'e', 'i', 'o', 'u')) else 'a'
        if iso == 'eng':
            desc = f'{names} is {article} {get_branch(code)} language spoken {get_spoken_in(code)}.'
        else:
            desc = f'{names} is {article} {get_branch(code)} language spoken mainly in {get_spoken_in(code)}.'
    elif not get_family(code) or get_family(code).lower() == 'language isolate':
        desc = f'{names} is a language spoken mainly in {get_spoken_in(code)}.'
    else:
        desc = f'{names} is a language of the {get_family(code)} family, spoken mainly in {get_spoken_in(code)}.'

    if writing and get_written_in(code):
        desc += f' The {writing.lower()} writing system is officially used in {get_written_in(code)}.'

    # Build the detailed information string
    result_parts = []
    result_parts.append(prettify('information-value', get_display(code)))
    result_parts.append(prettify('information-key', f'{'Name':<22}') + prettify('information-value', names))
    result_parts.append(prettify('information-key', f'{'Family':<22}') + prettify('information-value', get_family(code)))
    result_parts.append(prettify('information-key', f'{'Writing system':<22}') + prettify('information-value', script))
    result_parts.append(prettify('information-key', f'{'Code':<22}') + prettify('information-value', get_code(code)))
    result_parts.append(prettify('information-key', f'{'ISO 639-3':<22}') + prettify('information-value', iso))
    result_parts.append(prettify('information-key', f'{'SIL':<22}') + prettify('information-value', f'https://iso639-3.sil.org/code/{iso}'))

    if get_glotto(code):
        result_parts.append(prettify('information-key', f'{'Glottolog':<22}')
                            + prettify('information-value', f'https://glottolog.org/resource/languoid/id/{get_glotto(code)}'))
    else:
        result_parts.append(prettify('information-key', f'{'Glottolog':<22}'))

    result_parts.append(prettify('information-key', f'{'Wikipedia':<22}')
                        + prettify('information-value', f'https://en.wikipedia.org/wiki/ISO_639:{iso}'))

    if LOCALES[locale_code].get('supported-by'):
        # TODO: what about Yandex?
        google_check = '✔' if is_supported_by_google(code) else '✘'
        bing_check = '✔' if is_supported_by_bing(code) else '✘'
        result_parts.append(prettify('information-key', f'{'Translator support':<22}')
                            + prettify('information-value', f'Google [{google_check}]    Bing [{bing_check}]'))

    if LOCALES[locale_code].get('spoken-in'):
        result_parts.append(prettify('information-value', desc))

    return '\n'.join(result_parts)


def show_phonetics(phonetics, code):
    """Add /slashes/ for IPA phonemic notations and (parentheses) for others."""
    if code and get_code(code) == 'en':
        return f'/{phonetics}/'
    else:
        return f'({phonetics})'


def show(text, code=None):
    """Convert a logical string to visual; don't right justify RTL lines."""
    if not code or is_rtl(code):
        if text in Cache and 0 in Cache[text]:
            return Cache[text][0]
        else:
            if (FriBidi or (code and is_rtl(code))) and BiDiNoPad:
                try:
                    result = subprocess.run(
                        f'echo {parameterize(text)} | {BiDiNoPad}',
                        shell=True, capture_output=True, text=True
                    )
                    temp = result.stdout.strip()
                except:
                    temp = text
            else:  # non-RTL language, or FriBidi not installed
                temp = text

            if text not in Cache:
                Cache[text] = {}
            Cache[text][0] = temp
            return temp
    else:
        return text


def s(text, code=None, width=None):
    """Convert a logical string to visual and right justify RTL lines."""
    if not code or is_rtl(code):
        width = width or 80
        if text in Cache and width in Cache[text]:
            return Cache[text][width]
        else:
            if (FriBidi or (code and is_rtl(code))) and BiDi:
                try:
                    result = subprocess.run(
                        f'echo {parameterize(text)} | {BiDi % width}',
                        shell=True, capture_output=True, text=True
                    )
                    temp = result.stdout.strip()
                except:
                    temp = text
            else:  # non-RTL language, or FriBidi not installed
                temp = text

            if text not in Cache:
                Cache[text] = {}
            Cache[text][width] = temp
            return temp
    else:
        return text


def parse_lang(lang):
    """Parse a POSIX locale identifier and return the language code."""
    match = re.match(r'^([a-z]{2,3})(_|$)', lang)
    if not match:
        return 'en'  # Default fallback

    code = get_code(match.group(1))

    # Detect region identifier
    if re.match(r'^zh_(CN|SG)', lang):  # Regions using Chinese Simplified
        code = 'zh-CN'
    elif re.match(r'^zh_(TW|HK)', lang):  # Regions using Chinese Traditional
        code = 'zh-TW'

    # Handle unrecognized language code
    if not code:
        code = 'en'

    return code


def init_user_lang():
    """Initialize UserLang."""
    global UserLang, UserLocale

    utf = False

    if 'LC_ALL' in os.environ:
        lang = os.environ['LC_ALL']
        if not UserLocale:
            UserLocale = lang
        utf = utf or re.search(r'utf-?8$', lang.lower()) is not None

    if 'LANG' in os.environ:
        lang = os.environ['LANG']
        if not UserLocale:
            UserLocale = lang
        utf = utf or re.search(r'utf-?8$', lang.lower()) is not None

    if not UserLocale:
        UserLocale = 'en_US.UTF-8'
        utf = True

    if not utf:
        w(f'[WARNING] Your locale codeset ({UserLocale}) is not UTF-8.')

    UserLang = parse_lang(UserLocale)


def parameterize(text):
    """Parameterize text for shell commands (placeholder implementation)."""
    # This would need to be implemented based on your shell escaping needs
    return f'\'{text}\''


init_locales()
init_locale_alias()
init_locale_display()
init_user_lang()
