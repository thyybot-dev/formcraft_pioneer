#!/bin/sh
# Fails if the Command Centre's script has a syntax error. Run before every publish.
python3 -c "
s=open('command-centre/index.html').read();i=s.index('<script>')+8;j=s.index('</script>',i);open('/tmp/cc_check.js','w').write(s[i:j])" && node --check /tmp/cc_check.js && echo "Command Centre script: syntax OK"
