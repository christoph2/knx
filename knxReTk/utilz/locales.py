#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   Konnex / EIB Reverserz Toolkit

   (C) 2001-2014 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

   s. FLOSS-EXCEPTION.txt
"""
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'

LOCALS = {
    1025: ('Arabic (Saudi-Arabia)', 'ar', 'ar-sa'),
    1026: ('Bulgarian', 'bg', 'bg'),
    1027: ('Catalan', 'ca', 'ca'),
    1028: ('Chinese (Taiwan)', 'zh', 'zh-tw'),
    1029: ('Czech', 'cs', 'cs'),
    1030: ('Danish', 'da', 'da'),
    1031: ('German (Germany)', 'de', 'de-de'),
    1032: ('Greek', 'el', 'el'),
    1033: ('English (United-States)', 'en', 'en-us'),
    1034: ('Spanish (Spain/Traditional)', 'es', 'es-es'),
    1035: ('Finnish', 'fi', 'fi'),
    1036: ('French (France)', 'fr', 'fr-fr'),
    1037: ('Hebrew', 'he', 'he'),
    1038: ('Hungarian', 'hu', 'hu'),
    1039: ('Icelandic', 'is', 'is'),
    1040: ('Italian (Italy)', 'it', 'it-it'),
    1041: ('Japanese', 'ja', 'ja'),
    1042: ('Korean', 'ko', 'ko'),
    1043: ('Dutch (Netherlands)', 'nl', 'nl-nl'),
    1044: ('Norwegian (Bokml)', 'nb', 'no-no'),
    1045: ('Polish', 'pl', 'pl'),
    1046: ('Portuguese-Brazil', 'pt', 'pt-br'),
    1047: ('Raeto-Romance', 'rm', 'rm'),
    1048: ('Romanian (Romania', 'ro', 'ro'),
    1049: ('Russian', 'ru', 'ru'),
    1050: ('Croatian', 'hr', 'hr'),
    1051: ('Slovak', 'sk', 'sk'),
    1052: ('Albanian', 'sq', 'sq'),
    1053: ('Swedish (Sweden)', 'sv', 'sv-se'),
    1054: ('Thai', 'th', 'th'),
    1055: ('Turkish', 'tr', 'tr'),
    1056: ('Urdu', 'ur', 'ur'),
    1057: ('Indonesian', 'id', 'id'),
    1058: ('Ukrainian', 'uk', 'uk'),
    1059: ('Belarusian', 'be', 'be'),
    1060: ('Slovenian', 'sl', 'sl'),
    1061: ('Estonian', 'et', 'et'),
    1062: ('Latvian', 'lv', 'lv'),
    1063: ('Lithuanian', 'lt', 'lt'),
    1064: ('Tajik', 'tg', 'tg'),
    1065: ('Farsi-Persian', 'fa', 'fa'),
    1066: ('Vietnamese', 'vi', 'vi'),
    1067: ('Armenian', 'hy', 'hy'),
    1068: ('Azeri (Latin)', 'az', 'az-az'),
    1069: ('Basque', 'eu', 'eu'),
    1070: ('Sorbian', 'sb', 'sb'),
    1071: ('Fyro (Macedonia)', 'mk', 'mk'),
    1073: ('Tsonga', 'ts', 'ts'),
    1074: ('Setsuana', 'tn', 'tn'),
    1076: ('Xhosa', 'xh', 'xh'),
    1077: ('Zulu', 'zu', 'zu'),
    1078: ('Afrikaans', 'af', 'af'),
    1079: ('Georgian', 'ka', 'ka'),
    1080: ('Faroese', 'fo', 'fo'),
    1081: ('Hindi', 'hi', 'hi'),
    1082: ('Maltese', 'mt', 'mt'),
    1084: ('Gaelic (Scotland)', 'gd', 'gd'),
    1085: ('Yiddish', 'yi', 'yi'),
    1086: ('Malay (Malaysia)', 'ms', 'ms-my'),
    1087: ('Kazakh', 'kk', 'kk'),
    1089: ('Swahili', 'sw', 'sw'),
    1090: ('Turkmen', 'tk', 'tk'),
    1091: ('Uzbek (Latin)', 'uz', 'uz-uz'),
    1092: ('Tatar', 'tt', 'tt'),
    1093: ('Bengali (India)', 'bn', 'bn'),
    1094: ('Punjabi', 'pa', 'pa'),
    1095: ('Gujarati', 'gu', 'gu'),
    1096: ('Oriya', 'or', 'or'),
    1097: ('Tamil', 'ta', 'ta'),
    1098: ('Telugu', 'te', 'te'),
    1099: ('Kannada', 'kn', 'kn'),
    1100: ('Malayalam', 'ml', 'ml'),
    1101: ('Assamese', 'as', 'as'),
    1102: ('Marathi', 'mr', 'mr'),
    1103: ('Sanskrit', 'sa', 'sa'),
    1104: ('Mongolian', 'mn', 'mn'),
    1105: ('Tibetan', 'bo', 'bo'),
    1106: ('Welsh', 'cy', 'cy'),
    1107: ('Khmer', 'km', 'km'),
    1108: ('Lao', 'lo', 'lo'),
    1109: ('Burmese', 'my', 'my'),
    1110: ('Galician', 'gl', 'gl'),
    1113: ('Sindhi', 'sd', 'sd'),
    1115: ('Sinhala (Sinhalese)', 'si', 'si'),
    1118: ('Amharic', 'am', 'am'),
    1120: ('Kashmiri', 'ks', 'ks'),
    1121: ('Nepali', 'ne', 'ne'),
    1125: ('Divehi (Maldivian)', 'dv', 'dv'),
    1140: ('Guarani (Paraguay)', 'gn', 'gn'),
    1142: ('Latin', 'la', 'la'),
    1143: ('Somali', 'so', 'so'),
    1153: ('Maori', 'mi', 'mi'),
    2049: ('Arabic (Iraq)', 'ar', 'ar-iq'),
    2052: ('Chinese (China)', 'zh', 'zh-cn'),
    2055: ('German (Switzerland)', 'de', 'de-ch'),
    2057: ('English (Great-Britain)', 'en', 'en-gb'),
    2058: ('Spanish (Mexico)', 'es', 'es-mx'),
    2060: ('French (Belgium)', 'fr', 'fr-be'),
    2064: ('Italian (Switzerland)', 'it', 'it-ch'),
    2067: ('Dutch (Belgium)', 'nl', 'nl-be'),
    2068: ('Norwegian (Nynorsk)', 'nn', 'no-no'),
    2070: ('Portuguese-Portugal', 'pt', 'pt-pt'),
    2072: ('Romanian (Moldova', 'ro', 'ro-mo'),
    2073: ('Russian (Moldova)', 'ru', 'ru-mo'),
    2074: ('Serbian (Latin)', 'sr', 'sr-sp'),
    2077: ('Swedish (Finland)', 'sv', 'sv-fi'),
    2092: ('Azeri (Cyrillic)', 'az', 'az-az'),
    2108: ('Gaelic (Ireland)', 'gd', 'gd-ie'),
    2110: ('Malay (Brunei)', 'ms', 'ms-bn'),
    2115: ('Uzbek (Cyrillic)', 'uz', 'uz-uz'),
    2117: ('Bengali (Bangladesh)', 'bn', 'bn'),
    2128: ('Mongolian', 'mn', 'mn'),
    3073: ('Arabic (Egypt)', 'ar', 'ar-eg'),
    3076: ('Chinese (Hong-Kong)', 'zh', 'zh-hk'),
    3079: ('German (Austria)', 'de', 'de-at'),
    3081: ('English (Australia)', 'en', 'en-au'),
    3084: ('French (Canada)', 'fr', 'fr-ca'),
    3098: ('Serbian (Cyrillic)', 'sr', 'sr-sp'),
    4097: ('Arabic (Libya)', 'ar', 'ar-ly'),
    4100: ('Chinese (Singapore)', 'zh', 'zh-sg'),
    4103: ('German (Luxembourg)', 'de', 'de-lu'),
    4105: ('English (Canada)', 'en', 'en-ca'),
    4106: ('Spanish (Guatemala)', 'es', 'es-gt'),
    4108: ('French (Switzerland)', 'fr', 'fr-ch'),
    5121: ('Arabic (Algeria)', 'ar', 'ar-dz'),
    5124: ('Chinese (Macau)', 'zh', 'zh-mo'),
    5127: ('German (Liechtenstein)', 'de', 'de-li'),
    5129: ('English (New-Zealand)', 'en', 'en-nz'),
    5130: ('Spanish (Costa-Rica)', 'es', 'es-cr'),
    5132: ('French (Luxembourg)', 'fr', 'fr-lu'),
    5146: ('Bosnian', 'bs', 'bs'),
    6145: ('Arabic (Morocco)', 'ar', 'ar-ma'),
    6153: ('English (Ireland)', 'en', 'en-ie'),
    6154: ('Spanish (Panama)', 'es', 'es-pa'),
    6156: ('French (Monaco)', 'fr', 'fr'),
    7169: ('Arabic (Tunisia)', 'ar', 'ar-tn'),
    7177: ('English (Southern-Africa)', 'en', 'en-za'),
    7178: ('Spanish (Dominican Republic)', 'es', 'es-do'),
    7180: ('French (West-Indies)', 'fr', 'fr'),
    8193: ('Arabic (Oman)', 'ar', 'ar-om'),
    8201: ('English (Jamaica)', 'en', 'en-jm'),
    8202: ('Spanish (Venezuela)', 'es', 'es-ve'),
    9217: ('Arabic (Yemen)', 'ar', 'ar-ye'),
    9225: ('English (Caribbean)', 'en', 'en-cb'),
    9226: ('Spanish (Colombia)', 'es', 'es-co'),
    9228: ('French (Congo)', 'fr', 'fr'),
    10241: ('Arabic (Syria)', 'ar', 'ar-sy'),
    10249: ('English (Belize)', 'en', 'en-bz'),
    10250: ('Spanish (Peru)', 'es', 'es-pe'),
    10252: ('French (Senegal)', 'fr', 'fr'),
    11265: ('Arabic (Jordan)', 'ar', 'ar-jo'),
    11273: ('English (Trinidad)', 'en', 'en-tt'),
    11274: ('Spanish (Argentina)', 'es', 'es-ar'),
    11276: ('French (Cameroon)', 'fr', 'fr'),
    12289: ('Arabic (Lebanon)', 'ar', 'ar-lb'),
    12297: ('English (Zimbabwe)', 'en', 'en'),
    12298: ('Spanish (Ecuador)', 'es', 'es-ec'),
    12300: ("French (Cote-d'Ivoire)", 'fr', 'fr'),
    13313: ('Arabic (Kuwait)', 'ar', 'ar-kw'),
    13321: ('English (Phillippines)', 'en', 'en-ph'),
    13322: ('Spanish (Chile)', 'es', 'es-cl'),
    13324: ('French (Mali)', 'fr', 'fr'),
    14337: ('Arabic (United-Arab-Emirates)', 'ar', 'ar-ae'),
    14346: ('Spanish (Uruguay)', 'es', 'es-uy'),
    14348: ('French (Morocco)', 'fr', 'fr'),
    15361: ('Arabic (Bahrain)', 'ar', 'ar-bh'),
    15370: ('Spanish (Paraguay)', 'es', 'es-py'),
    16385: ('Arabic (Qatar)', 'ar', 'ar-qa'),
    16393: ('English (India)', 'en', 'en-in'),
    16394: ('Spanish (Bolivia)', 'es', 'es-bo'),
    17418: ('Spanish (El-Salvador)', 'es', 'es-sv'),
    18442: ('Spanish (Honduras)', 'es', 'es-hn'),
    19466: ('Spanish (Nicaragua)', 'es', 'es-ni'),
    20490: ('Spanish (Puerto-Rico)', 'es', 'es-pr')
}

def getLocalCode(locale):
    result = LOCALS.get(locale, ('?', '?', '?', ))[2]
    if '-' in result:
        l, r = result.split('-')
        return "%s-%s" % (l.lower(), r.upper())
    else:
        return result

