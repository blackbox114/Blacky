sudo date -s "$(curl -s --head http://google.com | grep ^Date: | sed 's/Date: //g')"
