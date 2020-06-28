# Properties translator
Translates Java properties into the specified languages using the Google Translate API and encodes them in Unicode.

## Usage

To use the source code, install the Google Translate API package:

```
pip install googletrans
```

The program takes the path to the directory as input and stores the result in the same directory, so it can be used directly inside the Java project.

## Notes
- Program needs internet connection in order to translate properties using Google Translate API.
- The program will be applied to all files with the specified suffix of the source language in the name in the specified directory automatically.
- Program won't translate any comments (#).

## Program entries

After starting the program one need to answer the following questions:

1. Enter the source directory where the source properties files are located:
   ```
   Enter the source directory with the properties files: <directory>
   ```

2. Enter the source language or leave it blank for auto selection: (e.g. en):
   ```
   Enter the source language or leave it blank for auto selection: <language>
   ```
   > If the user left this field empty, each file in the directory will be processed. Otherwise, files containing the entered language suffix in the name will be selected as source files.

3. Enter, separated by spaces, the languages to be received (e.g. en ru es_CR):
   ```
   Enter destination languages: <languages>
   ```
   > If the language of the specified region is not found, translates into the language of the country.

   After the translation, the program also applies the following formatting to the results:
   - Replaces "% s" with " %s".
   - Applies sentences capitalization in accordance with source value.
   - Adds missing points at the end of the sentences in accordance with source value.
   - Adds missing trailing spaces in accordance with source value.
    
4. The program will keep the format of the output file as it was in the input file, otherwise there will be no empty lines or spaces:
   ```
   Keep source file format? [y/n]: <y/any>
   ```

5. Program will encode property values before saving them to the file:
   ```
   Encode values? [y/n]: <y/any>
   ```

6. If the previous answer was "y", then one need to specify whether the program should use python unicode-escape encoding:
   ```
   Use unicode-escape to encode values? [y/n]: <y/any>
   ```
   > This encoding does not affect frequent punctuation marks, as well as English characters, but it will use as less data as possible (e.g. \x80 instead of \u0080 or \U00000080). Java does not always handle such encodings.

## Results

The program saves the properties files in the folder specified in the first step, naming them according to the specified destination languages.
