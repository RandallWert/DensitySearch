import searchTermEntry

quitRunning = searchTermEntry.quitRunning
searchTerms = searchTermEntry.searchTerms

nextPageStartValue = 0

if quitRunning == False:
    
    import requests
    import bs4
    from bs4 import BeautifulSoup
    from tkinter import filedialog
    from tkinter import messagebox

    # This gets rid of the pointless "root window":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    # Read vocabulary terms from file into list:
    #
    # To create this text file:
    # (1) Make a special Word doc with all of the variations of the vocab terms that you want to search for.
    # (2) Use www.online-convert.com to convert that Word doc to txt. This will be in the UTF-8 format (instead of
    #     the troublesome Mac Extended Ascii character set used by TextEdit).
    vocabTermsFromFile = []
    filename = filedialog.askopenfilename()
    with open(filename,encoding='utf-8-sig') as Datei:
        for line in Datei:
            rightStrippedLine = line.strip()
            if len(rightStrippedLine) > 0:
                vocabTermsFromFile.append(rightStrippedLine)

    # Concatenate search terms (entered above) into a search string:
    searchString = "(site:.de OR site:.ch OR site:.at)"
    for term in searchTerms:
        searchString = searchString + " +" + str(term)

    # Carry out the Google search
    getString = "https://www.google.com/search?client=safari&rls=en&q=" + searchString + "&ie=UTF-8&oe=UTF-8"
    originalGetString = getString

while quitRunning == False:
    
    res = requests.get(getString)
    res.raise_for_status()

    # Create a Beautiful Soup object that represents the text (i.e., the HTML source code) of the search result page
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # First select all <a> tags with href attributes
    linkElems = soup.select('a[href]')

    # Get href attributes from the <a> tags:
    onlyURLs = []
    for element in linkElems:
        onlyURLs.append(element.get('href'))

    # Accept only href's that begin with /url?q= and chop that part off the beginning
    only_selected_URLs = []
    for pos in range(0,len(onlyURLs)):
        wholeString = onlyURLs[pos]
        if wholeString[0:7] == '/url?q=':
            only_selected_URLs.append(wholeString[7:])

    # Chop off everything beginning with &sa= from the end of each of these href's:
    for pos in range(0,len(only_selected_URLs)):
        wholeString = only_selected_URLs[pos]                
        if "&sa=" in wholeString:
            garbageStart = wholeString.index("&sa=")
            only_selected_URLs[pos] = wholeString[0:garbageStart]

    # Eliminate PDFs from the list:
    onlyURLsMinusPDFs = []
    for element in only_selected_URLs:
        if element[-4:] != ".pdf" and element[-4:] != ".PDF":
            onlyURLsMinusPDFs.append(element)
            
    # Loop through the URLs, determining the statistics and report them to the user:
    for element in onlyURLsMinusPDFs:
        msgBoxString = element
        try:
            r = requests.get(element)
            r.raise_for_status()
        except:
            continue
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        if soup.find_all('p') == []:
            msgBoxString = msgBoxString + "\n" + " \n" + "No paragraph content on this web page!"
        else:
            # Collect all the paragraph text and count the total words in it:
            pString = ""
            for p in soup.find_all('p'):
                  pString = pString + p.text
            pListe = pString.split(" ")
            wordCount = len(pListe)
            # Create a list of the vocab terms that are actually found and a count of these occurrences:
            termsFound = []
            foundCounts = []
            for term in vocabTermsFromFile:
                if term in pString:
                    termsFound.append(term)
                    foundCounts.append(pString.count(term))
            # Print a list of all of the terms that were actually found:
            if len(termsFound) == 0:
                msgBoxString = msgBoxString + "\n" + "\n" + "No vocabulary terms found." + "\n" + "\n"
            else:
                msgBoxString = msgBoxString + "\n" + "\n" + "Vocabulary terms found:" + "\n"
                termsListedSoFar = 0
                for term in termsFound:
                    termsListedSoFar += 1
                    if termsListedSoFar < 25:
                        msgBoxString = msgBoxString + " - " + term + "\n"
                    else:
                        if termsListedSoFar == 25:
                            msgBoxString = msgBoxString + " - and MORE!" + "\n"
            if len(termsFound) > 0:
                # Calculate the statistics, then print them:
                msgBoxString = msgBoxString + "\n" + "Statistics:" + "\n" + "\n"
                # How many total examples of vocab terms were found, and how many unique occurrences were found?
                totalFound = 0
                for count in foundCounts:
                    totalFound = totalFound + count
                outputStr = str(totalFound) + " total examples of vocabulary terms "
                outputStr = outputStr + "(" + str(len(termsFound)) + " of which are unique) out of "
                outputStr = outputStr + str(wordCount) + " total words"
                msgBoxString = msgBoxString + outputStr + "\n" + "\n"
                # How many overall / unique occurrences per total word count?
                overallDensity = int(100 * (totalFound / wordCount))
                uniqueDensity = int(100 * (len(termsFound) / wordCount))
                densityString = "Density of overall examples: " + str(overallDensity) + "% ; density of unique examples: " + str(uniqueDensity) + "%"
                msgBoxString = msgBoxString + densityString
        messagebox.showinfo(message=msgBoxString)

    # Ask if user would like additional pages of search results
    getAnotherPage = messagebox.askyesno(message='Get another page of results?',icon='question',title='Another page?')
    if getAnotherPage == True:
        nextPageStartValue += 10
        getString = originalGetString + "&start=" + str(nextPageStartValue)
    else:
        quitRunning = True
