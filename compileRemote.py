import htmlmin, jsmin, sys, re
def cssmin(css):
    # remove comments - this will break a lot of hacks :-P
    css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", css ) # preserve IE<6 comment hack
    css = re.sub( r'/\*[\s\S]*?\*/', "", css )
    css = css.replace( "$$HACK1$$", '/**/' ) # preserve IE<6 comment hack
    # url() doesn't need quotes
    css = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', css )
    # spaces may be safely collapsed as generated content will collapse them anyway
    css = re.sub( r'\s+', ' ', css )
    # shorten collapsable colors: #aabbcc to #abc
    css = re.sub( r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css )
    # fragment values can loose zeros
    css = re.sub( r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css )
    for rule in re.findall( r'([^{]+){([^}]*)}', css ):
        # we don't need spaces around operators
        selectors = [re.sub( r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip() ) for selector in rule[0].split( ',' )]
        # order is important, but we still want to discard repetitions
        properties = {}
        porder = []
        for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
            key = prop[0].strip().lower()
            if key not in porder: porder.append( key )
            properties[ key ] = prop[1].strip()
    return css

index, script, style = '', '', ''
with open('remote/index.html') as f:
    index = htmlmin.minify(f.read(), remove_comments=True, remove_empty_space=True)
with open('remote/style.css') as f:
    style = cssmin(f.read())
with open('remote/script.js') as f:
    script = jsmin.jsmin(f.read())

index = index.replace('<link rel=stylesheet href=style.css>', '<style>' + style + '</style>')
index = index.replace('<script id=mainScript src=script.js></script>', '<script>' + script + '</script>')

f = open("templates/index.html", "w")
f.write(index)
f.close()

print()
print('Remote files Compiled to templates/index.html')