# Corpus-Linguistics
A repository to store the scripts I write to make corpus linguistics (analyzing bodies of texts) work easier.

<h3>POS Spreadsheet</h3>
<ul>
    <li>This allows you to:
        <ul>
        <li> Create a dictionary that maps each part of speech (POS) to a dictionary containing words with that POS with their frequency, with a separate entry for each POS.</li>
        <li> Sort that dictionary by frequency or by words in alphabetical order</li>
        <li> Store that dictionary in a spreadsheet </li>
        </ul>
    </li>
    <li>Dependencies:
        <ul>
            <li>openpyxl</li>
            <li>You need to have tagged txt files to use</li>
        </ul>
    </li>
</ul>


<h3>abstract_nouns</h3>
<ul>
    <li>This allows you to:
        <ul>
        <li>Get the abstract nouns in a corpus by searching for various suffixes as found in the following website: https://learningenglishgrammar.wordpress.com/suffixes/suffixes-and-how-they-form-abstract-nouns/</li>
        <li>Sort that dictionary by frequency or by words in alphabetical order</li>
        <li>Store that dictionary in a spreadsheet</li>
        </ul>
    </li>
    <li>Dependencies:
        <ul>
        <li>openpyxl</li>
        <li>You need wordlist files created using AntConc (http://www.laurenceanthony.net/software/antconc/)</li>
        </ul>
    </li>
    <li>Note:
        <ul>
        <li>I have done nothing to correct for false positives (nouns that end with the suffixes I'm looking for but that aren't abstract nouns. If you find false positives, please let me know on the issues page, and I'll make a list of false positives.</li>
        </ul>
    </li>
</ul>

<h3>remove_html_tags</h3>
<ul>
    <li>This allows you to:
        <ul>
        <li>Remove all html tags from a file</li>
        </ul>
    </li>
</ul>

<h3>Standalone corpus linguistics</h3>
<ul>
    <li>
        Corpus linguistics programs that use nltk and treetagger but are not dependent on AntConc or TagAnt (no preprocessing required)
    </li>
    <li>
        This allows:
        <ul>
            <li>Calculating and storing word frequencies</li>
            <li>Keyword analysis</li>
            <li>Part of speech tagging and lemmatizing</li>
            <li>Aggregating data from multiple files (individually specify or give a directory)</li>
            <li>Import functions into your Python code, or use the graphical interface found in nlp_gui.py</li>
        </ul>
    </li>
    <li>
        Dependencies:
        <ul>
            <li>nltk - main functionality</li>
            <li>openpyxl - for spreadsheets</li>
            <li>treetagger and treetaggerwrapper - part of speech tagging</li>
            <li>wxPython - for graphical interface</li>
        </ul>
    </li>
    <li>
        Note:
            <ul>
                <li>Some functions are for my own personal use and will not work for you unless your filesystem is identical to mine.</li>
            </ul>
    </li>
</ul>