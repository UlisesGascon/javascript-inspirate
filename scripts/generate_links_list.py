# -*- coding: utf-8 -*-
import os
import re
from bs4 import BeautifulSoup
import requests

headerRegex = r"(#+) (.*)"
linksRegex = r"(?!!).\[([^\[]+)\]\(([^\)]+)\)"
endFile = "# Recursos\n\n"
index = "# Índice\n\n"
content = "# Contido\n"

# URLs that generated exceptions last time... now all are skipped.
ignoreUrls = [
    "https://cylonjs.com/",
    "http://addyosmani.com/resources/essentialjsdesignpatterns/book/",
    "https://www.campus.co/madrid/es/events",
    "https://www.genbeta.com/web/error-404-not-found-historia-y-hazanas-de-este-mitico-codigo",
    "https://jsonformatter.curiousconcept.com/",
    "https://github.com/technoboy10/crossorigin.me",
    "https://ponyfoo.com/articles/es6-generators-in-depth",
    "https://ponyfoo.com/articles/es6-promises-in-depth",
    "https://ponyfoo.com/articles/understanding-javascript-async-await",
    "https://www.genbetadev.com/paradigmas-de-programacion/trabajar-con-microservicios-evitando-la-frustracion-de-las-enormes-aplicaciones-monoliticas",
    "http://ashleynolan.co.uk/blog/frontend-tooling-survey-2015-results",
    "http://blog.codinghorror.com/the-magpie-developer/",
    "http://www.xataka.com/servicios/y-si-el-software-open-source-desapareciera",
    "https://www.meetup.com/es-ES/Open-Source-Weekends/",
    "https://es.wikipedia.org/wiki/Hoja_de_estilos_en_cascada",
    "https://git-scm.com/",
    "https://www.polymer-project.org/1.0/",
    "http://web.archive.org",
    "https://www.ecured.cu/Sentencias_(Programaci%C3%B3n",
    "https://travis-ci.org/"
]

with open("manuscript/Book.txt") as f:
    lines = (line.rstrip() for line in f)
    lines = (line for line in lines if line)
    for line in lines:
        with open("manuscript/" + line) as chapter:
            fileContent = chapter.readlines()
            for line in fileContent:

                # Headers
                headerSearch = re.search(headerRegex, line)
                if headerSearch:
                    headerMatch = re.search(headerRegex, line)
                    if headerMatch.group(1) == "#" or headerMatch.group(1) == "##" or headerMatch.group(1) == "###":
                        if headerMatch.group(1) == "#":
                            index += "- **["+headerMatch.group(2)+"](#"+headerMatch.group(2).strip().lower().replace(" ", "-")+")**\n"

                        headerLink = re.search(linksRegex, headerMatch.group(2))
                        header = ""

                        if headerLink:
                            header = headerLink.group(1)
                        else:
                            header = headerMatch.group(2)

                        currentHeader = "\n" + headerMatch.group(1) + "# " + header
                        content += currentHeader + "\n"

                # Links
                linksSearch = re.findall(linksRegex, line, flags=re.LOCALE)
                if linksSearch:
                    for link in linksSearch:
                        finalTitle = link[0]
                        # scraping
                        if not link[1] in ignoreUrls and re.match(r"^http:\/\/web\.archive\.org", link[1]) is None:
                            try:
                                request = requests.get(link[1], verify=False)
                                if request.status_code == 200:
                                    print "Current URL:", link[1]
                                    #request = request.read()
                                    soup = BeautifulSoup(request.text, "html5lib")
                                    if soup.title:
                                        finalTitle = soup.title.string
                                        finalTitle = str(finalTitle.encode('utf-8')).strip().replace("\n", " ")
                            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
                                print "-- PLEASE REMOVE:", link[1]
                                pass
                        else:
                            print "IGNORED URL:", link[1]

                        content += "- *["+finalTitle+"]("+link[1]+")*\n"
            # End File
            content += "\n\n"

endFile += index + "\n\n" + content

# Save results
text_file = open("extras/recursos.md", "w")
text_file.write(endFile)
text_file.close()
print "extras/recursos.md updated!"
