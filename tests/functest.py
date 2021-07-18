from translator.func import objectify

class TestDict2Obj(object):

    def test_one_level_dict_to_obj(self):
        source_dict = {'A': 1, 'B': 2}
        obj = objectify(source_dict)
        assert obj.A is not None
        assert obj.B is not None
        assert obj.A == 1
        assert obj.B == 2

    def test_list_to_obj(self):
        source_dict = [{'A': 1}, {'A': 2}]
        obj = objectify(source_dict)
        assert obj is not None
        assert isinstance(obj, list)
        assert len(obj) == 2
        assert obj[0].A == 1
        assert obj[1].A == 2

    def test_three_level_dict_to_obj(self):
        source_dict = {
            'response_code': 200,
            'headers': [
                {'title': 'Content-Type', 'value': 'application/json'},
                {'title': 'Content-Encoding', 'value': 'gzip'}
            ],
            'body': {
                'source': 'word',
                'target': 'слово'
            }
        }

        obj = objectify(source_dict)
        assert obj.response_code == 200
        assert len(obj.headers) == 2
        assert obj.headers[0].title == 'Content-Type'
        assert obj.headers[0].value == 'application/json'
        assert obj.headers[1].title == 'Content-Encoding'
        assert obj.headers[1].value == 'gzip'
        assert obj.body.source == 'word'
        assert obj.body.target == 'слово'

    def test_dict_api_response_to_obj(self):
        source_dict = {
            "outputs": [
                {"output":
                    {"matches":
                        [
                            {"auto_complete": False,
                             "model_name": "mono-enru.mod",
                             "other_expressions": [
                                 {"context": "", "source": "spoken word", "target": "устное творчество"},
                                 {"context": "", "source": "strongest possible words", "target": "резких выражениях"}
                             ],
                             "source":
                                 {"inflection": "(pl:words)",
                                  "info": "",
                                  "lemma": "word",
                                  "phonetic": "[wɝd]",
                                  "pos": "noun",
                                  "term": "word"},
                             "targets": [
                                 {"context": "",
                                  "domain": "",
                                  "entry_id": 26692,
                                  "expressions": [
                                      {"source": "key word", "target": "ключевое слово"},
                                      {"source": "english word", "target": "английское слово"},
                                      {"source": "first word", "target": "первое слово"},
                                      {"source": "good word", "target": "хорошее слово"}
                                  ],
                                  "info": "",
                                  "invmeanings": ["speech", "expression", "term"],
                                  "lemma": "слово",
                                  "rank": "100",
                                  "synonym": "",
                                  "variant": ""}
                             ]}
                        ],
                        "sDictSearch": True
                    }
                }
            ]
        }
        obj = objectify(source_dict)
        assert len(obj.outputs) == 1
        output = obj.outputs[0].output
        assert len(output.matches) == 1
        match = output.matches[0]
        assert not match.auto_complete
        assert match.model_name == 'mono-enru.mod'
        assert len(match.other_expressions) == 2
        oe1 = match.other_expressions[0]
        oe2 = match.other_expressions[1]
        assert oe1.context == ''
        assert oe1.source == 'spoken word'
        assert oe1.target == 'устное творчество'
        assert oe2.context == ''
        assert oe2.source == 'strongest possible words'
        assert oe2.target == 'резких выражениях'
        assert match.source.inflection == '(pl:words)'
        assert match.source.info == ''
        assert match.source.lemma == 'word'
        assert match.source.pos == 'noun'
        assert match.source.term == 'word'
        assert len(match.targets) == 1
        target = match.targets[0]
        assert target.context == ''
        assert target.domain == ''
        assert target.entry_id == 26692
        assert len(target.expressions) == 4
        assert target.expressions[0].source == 'key word'
        assert target.expressions[0].target == 'ключевое слово'
        assert target.expressions[1].source == 'english word'
        assert target.expressions[1].target == 'английское слово'
        assert target.expressions[2].source == 'first word'
        assert target.expressions[2].target == 'первое слово'
        assert target.expressions[3].source == 'good word'
        assert target.expressions[3].target == 'хорошее слово'
        assert target.info == ''
        assert len(target.invmeanings) == 3
        assert target.invmeanings[0] == 'speech'
        assert target.invmeanings[1] == 'expression'
        assert target.invmeanings[2] == 'term'
        assert target.lemma == 'слово'
        assert target.rank == '100'
        assert target.synonym == ''
        assert target.variant == ''

    def test_dictionary_supported_lang_json_to_obs(self):
        source_dict = {"languagePairs": [{"source": "en", "target": "ru"}]}
        obj = objectify(source_dict)
        assert len(obj.languagePairs) == 1
        langPair = obj.languagePairs[0]
        assert langPair.source == 'en'
        assert langPair.target == 'ru'
