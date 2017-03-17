#!/bin/bash
echo "--> Views"
find . -name 'views.py' | xargs wc -l
echo
echo "--> Models"
find . -name 'models.py' | xargs wc -l
echo
echo "--> Django UnitTests"
find . -name 'tests.py' | xargs wc -l
echo
echo "--> Forms"
find . -name 'forms.py' | xargs wc -l
echo
echo "--> Url Routing"
find . -name 'urls.py' | xargs wc -l
echo
echo "--> HTML"
find . -name '*.html' | xargs wc -l
echo
echo "--> Javascript"
find . -name '*.js' | xargs wc -l
echo
echo "--> All"
find . -not -path "./files/*" \
       -not -path "*__pycache__*" \
       -not -path '*/\.*' \
       -not -path '*.png' \
       -type f -name '*' | xargs wc -l
