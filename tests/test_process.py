import io
import pytest
import unittest.mock

from conll2ske.process import transform_conllu_to_vert

def basic_conll_file():
    # https://github.com/pyconll/pyconll/blob/master/tests/fixtures/basic.conll
    return """# sent_id = fr-ud-dev_00001
# text = Aviator, un film sur la vie de Hughes.
1	Aviator	Aviator	PROPN	_	_	0	root	_	SpaceAfter=No
2	,	,	PUNCT	_	_	1	punct	_	_
3	un	un	DET	_	Definite=Ind|Gender=Masc|Number=Sing|PronType=Art	4	det	_	_
4	film	film	NOUN	_	Gender=Masc|Number=Sing	1	appos	_	_
5	sur	sur	ADP	_	_	7	case	_	_
6	la	le	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	7	det	_	_
7	vie	vie	NOUN	_	Gender=Fem|Number=Sing	4	nmod	_	_
8	de	de	ADP	_	_	9	case	_	_
9	Hughes	Hughes	PROPN	_	_	7	nmod	_	SpaceAfter=No
10	.	.	PUNCT	_	_	1	punct	_	_

# sent_id = fr-ud-dev_00002
# text = Les études durent six ans mais leur contenu diffère donc selon les Facultés.
1	Les	le	DET	_	Definite=Def|Gender=Fem|Number=Plur|PronType=Art	2	det	_	_
2	études	étude	NOUN	_	Gender=Fem|Number=Plur	3	nsubj	_	_
3	durent	durer	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	0	root	_	_
4	six	six	NUM	_	_	5	nummod	_	_
5	ans	an	NOUN	_	Gender=Masc|Number=Plur	3	obj	_	_
6	mais	mais	CCONJ	_	_	9	cc	_	_
7	leur	son	DET	_	Gender=Masc|Number=Sing|Poss=Yes|PronType=Prs	8	det	_	_
8	contenu	contenu	NOUN	_	Gender=Masc|Number=Sing	9	nsubj	_	_
9	diffère	différer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	3	conj	_	_
10	donc	donc	ADV	_	_	9	advmod	_	_
11	selon	selon	ADP	_	_	13	case	_	_
12	les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	13	det	_	_
13	Facultés	Facultés	PROPN	_	_	9	obl	_	SpaceAfter=No
14	.	.	PUNCT	_	_	3	punct	_	_"""

def basic_vrt_file():
    return """<doc>
<s id="fr-ud-dev_00001">
Aviator	PROPN	Aviator	_	root
,	PUNCT	,	_	punct
un	DET	un	Definite=Ind|Gender=Masc|Number=Sing|PronType=Art	det
film	NOUN	film	Gender=Masc|Number=Sing	appos
sur	ADP	sur	_	case
la	DET	le	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	det
vie	NOUN	vie	Gender=Fem|Number=Sing	nmod
de	ADP	de	_	case
Hughes	PROPN	Hughes	_	nmod
.	PUNCT	.	_	punct
</s>
<s id="fr-ud-dev_00002">
Les	DET	le	Definite=Def|Gender=Fem|Number=Plur|PronType=Art	det
études	NOUN	étude	Gender=Fem|Number=Plur	nsubj
durent	VERB	durer	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	root
six	NUM	six	_	nummod
ans	NOUN	an	Gender=Masc|Number=Plur	obj
mais	CCONJ	mais	_	cc
leur	DET	son	Gender=Masc|Number=Sing|Poss=Yes|PronType=Prs	det
contenu	NOUN	contenu	Gender=Masc|Number=Sing	nsubj
diffère	VERB	différer	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	conj
donc	ADV	donc	_	advmod
selon	ADP	selon	_	case
les	DET	le	Definite=Def|Number=Plur|PronType=Art	det
Facultés	PROPN	Facultés	_	obl
.	PUNCT	.	_	punct
</s>
</doc>
"""


def test_transform_conllu_to_vert():
    with (unittest.mock.patch("conll2ske.process.sys.stdin",
                              io.StringIO(basic_conll_file())),
          unittest.mock.patch("conll2ske.process.sys.stdout",
                              new_callable=io.StringIO) as mocked_out):
        transform_conllu_to_vert("-", "-")
        mocked_out.close = lambda: None
        assert mocked_out.getvalue() == basic_vrt_file()
