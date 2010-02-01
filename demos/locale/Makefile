#
# Copyright 2009-2010 W-Mark Kubacki; wmark@hurrikane.de
#

GETTEXT_EXTRACTOR=pybabel
MESSAGES_POT=locales/messages.pot

i18n:
	${GETTEXT_EXTRACTOR} extract -F babel.conf -c "TRANSLATORS:" \
	--output=${MESSAGES_POT} .
	sed -i  -e 's:PROJECT:Localedemo:g' \
		${MESSAGES_POT}

dep:
	emerge -1n dev-python/tornado dev-python/babel dev-python/beaker
