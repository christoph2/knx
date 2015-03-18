#!/usr/bin/env python
# -*- coding: utf-8 -*-

RAW = """
   Afrikaans af af 1078 436 1252
   Albanian sq sq 1052 1250
   Amharic am am 1118
   Arabic (Algeria ar ar-dz 5121 1401 1256
   Arabic (Bahrain ar ar-bh 15361 1256
   Arabic (Egypt ar ar-eg 3073 1256
   Arabic (Iraq ar ar-iq 2049 801 1256
   Arabic (Jordan ar ar-jo 11265 1256
   Arabic (Kuwait ar ar-kw 13313 3401 1256
   Arabic (Lebanon ar ar-lb 12289 3001 1256
   Arabic (Libya ar ar-ly 4097 1001 1256
   Arabic (Morocco ar ar-ma 6145 1801 1256
   Arabic (Oman ar ar-om 8193 2001 1256
   Arabic (Qatar ar ar-qa 16385 4001 1256
   Arabic (Saudi Arabia ar ar-sa 1025 401 1256
   Arabic (Syria ar ar-sy 10241 2801 1256
   Arabic (Tunisia ar ar-tn 7169 1256
   Arabic (United Arab Emirates ar ar-ae 14337 3801 1256
   Arabic (Yemen ar ar-ye 9217 2401 1256
   Armenian hy hy 1067
   Assamese as as 1101
   Azeri-Cyrillic az az-az 2092 1251
   Azeri-Latin az az-az 1068 1254
   Basque eu eu 1069 1252
   Belarusian be be 1059 423 1251
   Bengali-Bangladesh bn bn 2117 845
   Bengali-India bn bn 1093 445
   Bosnian bs bs 5146
   Bulgarian bg bg 1026 402 1251
   Burmese my my 1109 455
   Catalan ca ca 1027 403 1252
   Chinese-China zh zh-cn 2052 804
   Chinese-Hong Kong SAR zh zh-hk 3076
   Chinese-Macau SAR zh zh-mo 5124 1404
   Chinese-Singapore zh zh-sg 4100 1004
   Chinese-Taiwan zh zh-tw 1028 404
   Croatian hr hr 1050 1250
   Czech cs cs 1029 405 1250
   Danish da da 1030 406 1252
   Divehi; Dhivehi; Maldivian dv dv 1125 465
   Dutch (Belgium nl nl-be 2067 813 1252
   Dutch (Netherlands nl nl-nl 1043 413 1252
   Edo 1126 466
   English (Australia en en-au 3081 1252
   English (Belize en en-bz 10249 2809 1252
   English (Canada en en-ca 4105 1009 1252
   English (Caribbean en en-cb 9225 2409 1252
   English (Great Britain en en-gb 2057 809 1252
   English (India en en-in 16393 4009
   English (Ireland en en-ie 6153 1809 1252
   English (Jamaica en en-jm 8201 2009 1252
   English (New Zealand en en-nz 5129 1409 1252
   English (Phillippines en en-ph 13321 3409 1252
   English (Southern Africa en en-za 7177 1252
   English (Trinidad en en-tt 11273 1252
   English (United States en en-us 1033 409 1252
   English (Zimbabwe en 12297 3009 1252
   Estonian et et 1061 425 1257
   Faroese fo fo 1080 438 1252
   Farsi-Persian fa fa 1065 429 1256
   Filipino 1124 464
   Finnish fi fi 1035 1252
   French (Belgium fr fr-be 2060 1252
   French (Cameroon fr 11276
   French (Canada fr fr-ca 3084 1252
   French (Congo fr 9228
   French (Cote d'Ivoire fr 12300
   French (France fr fr-fr 1036 1252
   French (Luxembourg fr fr-lu 5132 1252
   French (Mali fr 13324
   French (Monaco fr 6156 1252
   French (Morocco fr 14348
   French (Senegal fr 10252
   French (Switzerland fr fr-ch 4108 1252
   French (West Indies fr 7180
   Frisian (Netherlands 1122 462
   FYRO Macedonia mk mk 1071 1251
   Gaelic (Ireland gd gd-ie 2108
   Gaelic (Scotland gd gd 1084
   Galician gl 1110 456 1252
   Georgian ka 1079 437
   German (Austria de de-at 3079 1252
   German (Germany de de-de 1031 407 1252
   German (Liechtenstein de de-li 5127 1407 1252
   German (Luxembourg de de-lu 4103 1007 1252
   German (Switzerland de de-ch 2055 807 1252
   Greek el el 1032 408 1253
   Guarani-Paraguay gn gn 1140 474
   Gujarati gu gu 1095 447
   Hebrew he he 1037 1255
   HID (Human Interface Device) 1279
   Hindi hi hi 1081 439
   Hungarian hu hu 1038 1250
   Icelandic is is 1039 1252
   Igbo-Nigeria 1136 470
   Indonesian id id 1057 421 1252
   Italian (Italy it it-it 1040 410 1252
   Italian (Switzerland it it-ch 2064 810 1252
   Japanese ja ja 1041 411
   Kannada kn kn 1099
   Kashmiri ks ks 1120 460
   Kazakh kk kk 1087 1251
   Khmer km km 1107 453
   Konkani 1111 457
   Korean ko ko 1042 412
   Kyrgyz-Cyrillic 1088 440 1251
   Lao lo lo 1108 454
   Latin la la 1142 476
   Latvian lv lv 1062 426 1257
   Lithuanian lt lt 1063 427 1257
   Malay-Brunei ms ms-bn 2110 1252
   Malay-Malaysia ms ms-my 1086 1252
   Malayalam ml ml 1100
   Maltese mt mt 1082
   Manipuri 1112 458
   Maori mi mi 1153 481
   Marathi mr mr 1102
   Mongolian mn mn 2128 850
   Mongolian mn mn 1104 450 1251
   Nepali ne ne 1121 461
   Norwegian (Bokml nb no-no 1044 414 1252
   Norwegian (Nynorsk nn no-no 2068 814 1252
   Oriya or or 1096 448
   Polish pl pl 1045 415 1250
   Portuguese-Brazil pt pt-br 1046 416 1252
   Portuguese-Portugal pt pt-pt 2070 816 1252
   Punjabi pa pa 1094 446
   Raeto-Romance rm rm 1047 417
   Romanian (Moldova ro ro-mo 2072 818
   Romanian (Romania ro ro 1048 418 1250
   Russian ru ru 1049 419 1251
   Russian - Moldova ru ru-mo 2073 819
   Sami Lappish 1083
   Sanskrit sa sa 1103
   Serbian (Cyrillic sr sr-sp 3098 1251
   Serbian (Latin sr sr-sp 2074 1250
   Sesotho (Sutu) 1072 430
   Setsuana tn tn 1074 432
   Sindhi sd sd 1113 459
   Sinhala; Sinhalese si si 1115
   Slovak sk sk 1051 1250
   Slovenian sl sl 1060 424 1250
   Somali so so 1143 477
   Sorbian sb sb 1070
   Spanish (Argentina es es-ar 11274 1252
   Spanish (Bolivia es es-bo 16394 1252
   Spanish (Chile es es-cl 13322 1252
   Spanish (Colombia es es-co 9226 1252
   Spanish (Costa Rica es es-cr 5130 1252
   Spanish (Dominican Republic es es-do 7178 1252
   Spanish (Ecuador es es-ec 12298 1252
   Spanish (El Salvador es es-sv 17418 1252
   Spanish (Guatemala es es-gt 4106 1252
   Spanish (Honduras es es-hn 18442 1252
   Spanish (Mexico es es-mx 2058 1252
   Spanish (Nicaragua es es-ni 19466 1252
   Spanish (Panama es es-pa 6154 1252
   Spanish (Paraguay es es-py 15370 1252
   Spanish (Peru es es-pe 10250 1252
   Spanish (Puerto Rico es es-pr 20490 1252
   Spanish (Spain (Traditional) es es-es 1034 1252
   Spanish (Uruguay es es-uy 14346 1252
   Spanish (Venezuela es es-ve 8202 1252
   Swahili sw sw 1089 441 1252
   Swedish (Finland sv sv-fi 2077 1252
   Swedish (Sweden sv sv-se 1053 1252
   Syriac 1114
   Tajik tg tg 1064 428
   Tamil ta ta 1097 449
   Tatar tt tt 1092 444 1251
   Telugu te te 1098
   Thai th th 1054
   Tibetan bo bo 1105 451
   Tsonga ts ts 1073 431
   Turkish tr tr 1055 1254
   Turkmen tk tk 1090 442
   Ukrainian uk uk 1058 422 1251
   Urdu ur ur 1056 420 1256
   Uzbek-Cyrillic uz uz-uz 2115 843 1251
   Uzbek-Latin uz uz-uz 1091 443 1254
   Venda 1075 433
   Vietnamese vi vi 1066 1258
   Welsh cy cy 1106 452
   Xhosa xh xh 1076 434
   Yiddish yi yi 1085
   Zulu zu zu 1077 435
"""

RAW2="""
   Afrikaans 1078   1025 Arabic (Saudi Arabia)
   Albanian 1052   1026 Bulgarian
   Arabic (Algeria) 5121   1027 Catalan
   Arabic (Bahrain) 15361   1028 Chinese (Taiwan)
   Arabic (Egypt) 3073   1029 Czech
   Arabic (Iraq) 2049   1030 Danish
   Arabic (Jordan) 11265   1031 German (Standard)
   Arabic (Kuwait) 13313   1032 Greek
   Arabic (Lebanon) 12289   1033 English (United States)
   Arabic (Libya) 4097   1034 Spanish (Spain)
   Arabic (Morocco) 6145   1035 Finnish
   Arabic (Oman) 8193   1036 French (Standard)
   Arabic (Qatar) 16385   1037 Hebrew
   Arabic (Saudi Arabia) 1025   1038 Hungarian
   Arabic (Syria) 10241   1039 Icelandic
   Arabic (Tunisia) 7169   1040 Italian (Standard)
   Arabic (U.A.E.) 14337   1041 Japanese
   Arabic (Yemen) 9217   1042 Korean
   Basque 1069   1043 Dutch
   Belarusian 1059   1044 Norwegian (Bokmål)
   Bulgarian 1026   1045 Polish
   Catalan 1027   1046 Portuguese (Brazil)
   Chinese (Hong Kong SAR) 3076   1047 Raeto (Romance)
   Chinese (PRC) 2052   1048 Romanian
   Chinese (Singapore) 4100   1049 Russian
   Chinese (Taiwan) 1028   1050 Croatian
   Croatian 1050   1051 Slovak
   Czech 1029   1052 Albanian
   Danish 1030   1053 Swedish
   Dutch 1043   1054 Thai
   Dutch (Belgium) 2067   1055 Turkish
   English (Australia) 3081   1056 Urdu (Pakistan)
   English (Belize) 10249   1057 Indonesian
   English (Canada) 4105   1058 Ukranian
   English (Ireland) 6153   1059 Belarusian
   English (Jamaica) 8201   1060 Slovenian
   English (New Zealand) 5129   1061 Estonian
   English (South Africa) 7177   1062 Latvian
   English (Trinidad) 11273   1063 Lithuanian
   English (United Kingdom) 2057   1065 Farsi
   English (United States) 1033   1066 Vietnamese
   Estonian 1061   1069 Basque
   Faeroese 1080   1070 Sorbian
   Farsi 1065   1071 Macedonian (FYROM)
   Finnish 1035   1072 Sutu
   French (Standard) 1036   1073 Tsonga
   French (Belgium) 2060   1074 Setsuana
   French (Canada) 3084   1076 Xhosa
   French (Luxembourg) 5132   1077 Zulu
   French (Switzerland) 4108   1078 Afrikaans
   Gaelic (Scotland) 1084   1080 Faeroese
   German (Standard) 1031   1081 Hindi
   German (Austrian) 3079   1082 Maltese
   German (Liechtenstein) 5127   1084 Gaelic (Scotland)
   German (Luxembourg) 4103   1085 Yiddish
   German (Switzerland) 2055   1086 Malay (Malaysia)
   Greek 1032   2049 Arabic (Iraq)
   Hebrew 1037   2052 Chinese (PRC)
   Hindi 1081   2055 German (Switzerland)
   Hungarian 1038   2057 English (United Kingdom)
   Icelandic 1039   2058 Spanish (Mexico)
   Indonesian 1057   2060 French (Belgium)
   Italian (Standard) 1040   2064 Italian (Switzerland)
   Italian (Switzerland) 2064   2067 Dutch (Belgium)
   Japanese 1041   2070 Portuguese (Portugal)
   Korean 1042   2072 Romanian (Moldova)
   Latvian 1062   2073 Russian (Moldova)
   Lithuanian 1063   2077 Swedish (Finland)
   Macedonian (FYROM) 1071   3073 Arabic (Egypt)
   Malay (Malaysia) 1086   3076 Chinese (Hong Kong SAR)
   Maltese 1082   3079 German (Austrian)
   Norwegian (Bokmål) 1044   3081 English (Australia)
   Polish 1045   3084 French (Canada)
   Portuguese (Brazil) 1046   3098 Serbian (Cyrillic)
   Portuguese (Portugal) 2070   4097 Arabic (Libya)
   Raeto (Romance) 1047   4100 Chinese (Singapore)
   Romanian 1048   4103 German (Luxembourg)
   Romanian (Moldova) 2072   4105 English (Canada)
   Russian 1049   4106 Spanish (Guatemala)
   Russian (Moldova) 2073   4108 French (Switzerland)
   Serbian (Cyrillic) 3098   5121 Arabic (Algeria)
   Setsuana 1074   5127 German (Liechtenstein)
   Slovak 1051   5129 English (New Zealand)
   Slovenian 1060   5130 Spanish (Costa Rica)
   Sorbian 1070   5132 French (Luxembourg)
   Spanish (Argentina) 11274   6145 Arabic (Morocco)
   Spanish (Bolivia) 16394   6153 English (Ireland)
   Spanish (Chile) 13322   6154 Spanish (Panama)
   Spanish (Columbia) 9226   7169 Arabic (Tunisia)
   Spanish (Costa Rica) 5130   7177 English (South Africa)
   Spanish (Dominican Republic) 7178   7178 Spanish (Dominican Republic)
   Spanish (Ecuador) 12298   8193 Arabic (Oman)
   Spanish (El Salvador) 17418   8201 English (Jamaica)
   Spanish (Guatemala) 4106   8202 Spanish (Venezuela)
   Spanish (Honduras) 18442   9217 Arabic (Yemen)
   Spanish (Mexico) 2058   9226 Spanish (Columbia)
   Spanish (Nicaragua) 19466   10241 Arabic (Syria)
   Spanish (Panama) 6154   10249 English (Belize)
   Spanish (Paraguay) 15370   10250 Spanish (Peru)
   Spanish (Peru) 10250   11265 Arabic (Jordan)
   Spanish (Puerto Rico) 20490   11273 English (Trinidad)
   Spanish (Spain) 1034   11274 Spanish (Argentina)
   Spanish (Uruguay) 14346   12289 Arabic (Lebanon)
   Spanish (Venezuela) 8202   12298 Spanish (Ecuador)
   Sutu 1072   13313 Arabic (Kuwait)
   Swedish 1053   13322 Spanish (Chile)
   Swedish (Finland) 2077   14337 Arabic (U.A.E.)
   Thai 1054   14346 Spanish (Uruguay)
   Turkish 1055   15361 Arabic (Bahrain)
   Tsonga 1073   15370 Spanish (Paraguay)
   Ukranian 1058   16385 Arabic (Qatar)
   Urdu (Pakistan) 1056   16394 Spanish (Bolivia)
   Vietnamese 1066   17418 Spanish (El Salvador)
   Xhosa 1076   18442 Spanish (Honduras)
   Yiddish 1085   19466 Spanish (Nicaragua)
   Zulu 1077   20490 Spanish (Puerto Rico)
"""

#lines = RAW.splitlines()
#for line in lines:
    #print '='.join(line.strip().split(' '))
#    print tuple(line.strip().split(' '))

CODES = (
    ("Afrikaans", "af", "af", 1078), 
    ("Albanian", "sq", "sq", 1052), 
    ("Amharic", "am", "am", 1118), 
    ("Arabic (Algeria)", "ar", "ar-dz", 5121), 
    ("Arabic (Bahrain)", "ar", "ar-bh", 15361), 
    ("Arabic (Egypt)", "ar", "ar-eg", 3073), 
    ("Arabic (Iraq)", "ar", "ar-iq", 2049), 
    ("Arabic (Jordan)", "ar", "ar-jo", 11265), 
    ("Arabic (Kuwait)", "ar", "ar-kw", 13313), 
    ("Arabic (Lebanon)", "ar", "ar-lb", 12289), 
    ("Arabic (Libya)", "ar", "ar-ly", 4097), 
    ("Arabic (Morocco)", "ar", "ar-ma", 6145), 
    ("Arabic (Oman)", "ar", "ar-om", 8193), 
    ("Arabic (Qatar)", "ar", "ar-qa", 16385), 
    ("Arabic (Saudi-Arabia)", "ar", "ar-sa", 1025), 
    ("Arabic (Syria)", "ar", "ar-sy", 10241), 
    ("Arabic (Tunisia)", "ar", "ar-tn", 7169), 
    ("Arabic (United-Arab-Emirates)", "ar", "ar-ae", 14337), 
    ("Arabic (Yemen)", "ar", "ar-ye", 9217), 
    ("Armenian", "hy", "hy", 1067), 
    ("Assamese", "as", "as", 1101), 
    ("Azeri (Cyrillic)", "az", "az-az", 2092), 
    ("Azeri (Latin)", "az", "az-az", 1068), 
    ("Basque", "eu", "eu", 1069), 
    ("Belarusian", "be", "be", 1059), 
    ("Bengali (Bangladesh)", "bn", "bn", 2117), 
    ("Bengali (India)", "bn", "bn", 1093), 
    ("Bosnian", "bs", "bs", 5146), 
    ("Bulgarian", "bg", "bg", 1026), 
    ("Burmese", "my", "my", 1109), 
    ("Catalan", "ca", "ca", 1027), 
    ("Chinese (China)", "zh", "zh-cn", 2052), 
    ("Chinese (Hong-Kong)", "zh", "zh-hk", 3076), 
    ("Chinese (Macau)", "zh", "zh-mo", 5124), 
    ("Chinese (Singapore)", "zh", "zh-sg", 4100), 
    ("Chinese (Taiwan)", "zh", "zh-tw", 1028), 
    ("Croatian", "hr", "hr", 1050), 
    ("Czech", "cs", "cs", 1029), 
    ("Danish", "da", "da", 1030), 
    ("Divehi (Maldivian)", "dv", "dv", 1125), 
    ("Dutch (Belgium)", "nl", "nl-be", 2067), 
    ("Dutch (Netherlands)", "nl", "nl-nl", 1043), 
    ("English (Australia)", "en", "en-au", 3081), 
    ("English (Belize)", "en", "en-bz", 10249), 
    ("English (Canada)", "en", "en-ca", 4105), 
    ("English (Caribbean)", "en", "en-cb", 9225), 
    ("English (Great-Britain)", "en", "en-gb", 2057), 
    ("English (India)", "en", "en-in", 16393), 
    ("English (Ireland)", "en", "en-ie", 6153), 
    ("English (Jamaica)", "en", "en-jm", 8201), 
    ("English (New-Zealand)", "en", "en-nz", 5129), 
    ("English (Phillippines)", "en", "en-ph", 13321), 
    ("English (Southern-Africa)", "en", "en-za", 7177), 
    ("English (Trinidad)", "en", "en-tt", 11273), 
    ("English (United-States)", "en", "en-us", 1033), 
    ("English (Zimbabwe)", "en", "en", 12297), 
    ("Estonian", "et", "et", 1061), 
    ("Faroese", "fo", "fo", 1080), 
    ("Farsi-Persian", "fa", "fa", 1065), 
    ("Finnish", "fi", "fi", 1035), 
    ("French (Belgium)", "fr", "fr-be", 2060), 
    ("French (Cameroon)", "fr", "fr", 11276), 
    ("French (Canada)", "fr", "fr-ca", 3084), 
    ("French (Congo)", "fr", "fr", 9228), 
    ("French (Cote-d'Ivoire)", "fr", "fr", 12300), 
    ("French (France)", "fr", "fr-fr", 1036), 
    ("French (Luxembourg)", "fr", "fr-lu", 5132), 
    ("French (Mali)", "fr", "fr", 13324), 
    ("French (Monaco)", "fr", "fr", 6156), 
    ("French (Morocco)", "fr", "fr", 14348), 
    ("French (Senegal)", "fr", "fr", 10252), 
    ("French (Switzerland)", "fr", "fr-ch", 4108), 
    ("French (West-Indies)", "fr", "fr", 7180), 
    ("Fyro (Macedonia)", "mk", "mk", 1071), 
    ("Gaelic (Ireland)", "gd", "gd-ie", 2108), 
    ("Gaelic (Scotland)", "gd", "gd", 1084), 
    ("Galician", "gl", "gl", 1110), 
    ("Georgian", "ka", "ka", 1079), 
    ("German (Austria)", "de", "de-at", 3079), 
    ("German (Germany)", "de", "de-de", 1031), 
    ("German (Liechtenstein)", "de", "de-li", 5127), 
    ("German (Luxembourg)", "de", "de-lu", 4103), 
    ("German (Switzerland)", "de", "de-ch", 2055), 
    ("Greek", "el", "el", 1032), 
    ("Guarani (Paraguay)", "gn", "gn", 1140), 
    ("Gujarati", "gu", "gu", 1095), 
    ("Hebrew", "he", "he", 1037), 
    ("Hindi", "hi", "hi", 1081), 
    ("Hungarian", "hu", "hu", 1038), 
    ("Icelandic", "is", "is", 1039), 
    ("Indonesian", "id", "id", 1057), 
    ("Italian (Italy)", "it", "it-it", 1040), 
    ("Italian (Switzerland)", "it", "it-ch", 2064), 
    ("Japanese", "ja", "ja", 1041), 
    ("Kannada", "kn", "kn", 1099), 
    ("Kashmiri", "ks", "ks", 1120), 
    ("Kazakh", "kk", "kk", 1087), 
    ("Khmer", "km", "km", 1107), 
    ("Korean", "ko", "ko", 1042), 
    ("Lao", "lo", "lo", 1108), 
    ("Latin", "la", "la", 1142), 
    ("Latvian", "lv", "lv", 1062), 
    ("Lithuanian", "lt", "lt", 1063), 
    ("Malay (Brunei)", "ms", "ms-bn", 2110), 
    ("Malay (Malaysia)", "ms", "ms-my", 1086), 
    ("Malayalam", "ml", "ml", 1100), 
    ("Maltese", "mt", "mt", 1082), 
    ("Maori", "mi", "mi", 1153), 
    ("Marathi", "mr", "mr", 1102), 
    ("Mongolian", "mn", "mn", 2128), 
    ("Mongolian", "mn", "mn", 1104), 
    ("Nepali", "ne", "ne", 1121), 
    ("Norwegian (Bokml)", "nb", "no-no", 1044), 
    ("Norwegian (Nynorsk)", "nn", "no-no", 2068), 
    ("Oriya", "or", "or", 1096), 
    ("Polish", "pl", "pl", 1045), 
    ("Portuguese-Brazil", "pt", "pt-br", 1046), 
    ("Portuguese-Portugal", "pt", "pt-pt", 2070), 
    ("Punjabi", "pa", "pa", 1094), 
    ("Raeto-Romance", "rm", "rm", 1047), 
    ("Romanian (Moldova", "ro", "ro-mo", 2072), 
    ("Romanian (Romania", "ro", "ro", 1048), 
    ("Russian", "ru", "ru", 1049), 
    ("Russian (Moldova)", "ru", "ru-mo", 2073), 
    ("Sanskrit", "sa", "sa", 1103), 
    ("Serbian (Cyrillic)", "sr", "sr-sp", 3098), 
    ("Serbian (Latin)", "sr", "sr-sp", 2074), 
    ("Setsuana", "tn", "tn", 1074), 
    ("Sindhi", "sd", "sd", 1113), 
    ("Sinhala (Sinhalese)", "si", "si", 1115), 
    ("Slovak", "sk", "sk", 1051), 
    ("Slovenian", "sl", "sl", 1060), 
    ("Somali", "so", "so", 1143), 
    ("Sorbian", "sb", "sb", 1070), 
    ("Spanish (Argentina)", "es", "es-ar", 11274), 
    ("Spanish (Bolivia)", "es", "es-bo", 16394), 
    ("Spanish (Chile)", "es", "es-cl", 13322), 
    ("Spanish (Colombia)", "es", "es-co", 9226), 
    ("Spanish (Costa-Rica)", "es", "es-cr", 5130), 
    ("Spanish (Dominican Republic)", "es", "es-do", 7178), 
    ("Spanish (Ecuador)", "es", "es-ec", 12298), 
    ("Spanish (El-Salvador)", "es", "es-sv", 17418), 
    ("Spanish (Guatemala)", "es", "es-gt", 4106), 
    ("Spanish (Honduras)", "es", "es-hn", 18442), 
    ("Spanish (Mexico)", "es", "es-mx", 2058), 
    ("Spanish (Nicaragua)", "es", "es-ni", 19466), 
    ("Spanish (Panama)", "es", "es-pa", 6154), 
    ("Spanish (Paraguay)", "es", "es-py", 15370), 
    ("Spanish (Peru)", "es", "es-pe", 10250), 
    ("Spanish (Puerto-Rico)", "es", "es-pr", 20490), 
    ("Spanish (Spain/Traditional)", "es", "es-es", 1034), 
    ("Spanish (Uruguay)", "es", "es-uy", 14346), 
    ("Spanish (Venezuela)", "es", "es-ve", 8202), 
    ("Swahili", "sw", "sw", 1089), 
    ("Swedish (Finland)", "sv", "sv-fi", 2077), 
    ("Swedish (Sweden)", "sv", "sv-se", 1053), 
    ("Tajik", "tg", "tg", 1064), 
    ("Tamil", "ta", "ta", 1097), 
    ("Tatar", "tt", "tt", 1092), 
    ("Telugu", "te", "te", 1098), 
    ("Thai", "th", "th", 1054), 
    ("Tibetan", "bo", "bo", 1105), 
    ("Tsonga", "ts", "ts", 1073), 
    ("Turkish", "tr", "tr", 1055), 
    ("Turkmen", "tk", "tk", 1090), 
    ("Ukrainian", "uk", "uk", 1058), 
    ("Urdu", "ur", "ur", 1056), 
    ("Uzbek (Cyrillic)", "uz", "uz-uz", 2115), 
    ("Uzbek (Latin)", "uz", "uz-uz", 1091), 
    ("Vietnamese", "vi", "vi", 1066), 
    ("Welsh", "cy", "cy", 1106), 
    ("Xhosa", "xh", "xh", 1076), 
    ("Yiddish", "yi", "yi", 1085), 
    ("Zulu", "zu", "zu", 1077),
)

result = {}

for rec in CODES:
    a, b, c, d = rec
    result[d] = (a, b, c)
    #print '("%s", "%s", "%s", %u), ' % (a, b, c, int(d))

pprint(result)

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

print getLocalCode(13324)
print getLocalCode(1033)
print getLocalCode(1031)