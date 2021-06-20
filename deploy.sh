#!/bin/sh
USER=victor
HOST=victorbilgin.com
DIR=/var/www/victorbilgin.com/html

jekyll build && rsync -avz --delete _site/ ${USER}@${HOST}:${DIR}

exit 0