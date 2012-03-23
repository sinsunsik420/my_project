#!/bin/sh

CSV=./data/words.csv

HATENA_FILE=keywordlist_furigana.csv
HATENA_URL=http://d.hatena.ne.jp/images/keyword/${HATENA_FILE}

WIKIPEDIA_FILE=jawiki-latest-all-titles-in-ns0
WIKIPEDIA_URL=http://download.wikimedia.org/jawiki/latest/${WIKIPEDIA_FILE}.gz

	# hatena
wget ${HATENA_URL}

echo "makedic.rb: converting to ${CSV}..."
ruby makedic.rb ${HATENA_FILE} > ${CSV}
echo "makedic.rb: done."

rm -f ${HATENA_FILE}

	# wikipedia
wget ${WIKIPEDIA_URL}
gunzip -v ${WIKIPEDIA_FILE}

echo "makedic.rb: converting to ${CSV}..."
ruby makedic.rb ${WIKIPEDIA_FILE} >> ${CSV}
echo "makedic.rb: done."

rm -f ${WIKIPEDIA_FILE}

/usr/local/libexec/mecab/mecab-dict-index -d /usr/local/lib/mecab/dic/naist-jdic/ -u ./data/words.dic -f utf-8 -t utf-8 ./data/words.csv
