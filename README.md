# Properties translator
Translates Java properties into the specified language using Google Translate API. It can also convert the received translation to Unicode.

## Usage

To use the source code, install the following packages:

```
pip install googletrans
pip install tqdm
```

The program saves the result properties in the specified folder, so one can simply create the properties in English and then use the translator.

NOTE:
- Program needs internet connection in order to translate properties using google API.
- Properties need to be named without any language suffixes.

> Program will be applied to all files in a specified directory automatically.
>> Program won't touch any comments (#) or empty lines.

## Program input

1. Input directory where your properties are located:
    ```
    Input source properties file path: <path>
    ```

2. Input language of the source file specified in the first step (e.g. en):
    ```
    Input source language: <language>
    ```

3. Input languages that need to be received separated by space (e.g. en ru es_CR):
    ```
    Input destination languages: <languages>
    ```

4. Program will replace "% s" -> " %s" after google translation as its doesn't translate it in a correct way:
    ```
    Replace string format characters after google translate (\'% s\' -> \' %s\')? [y/n]: <y/any charachter>
    ```

5. Program will encode property values before saving it to the file:
    ```
    Encode? [y/n]: <y/any charachter>
    ```

6. If the previous answer was "y", then one need to specify whether the program should use python unicode-escape encoding:
    ```
    Use unicode-escape? [y/n]: <y/any charachter>
    ```
    > This encoding does not affect frequent characters as well as English but it will use as less data as possible (e.g. \x80 instead of \u0080 or \U00000080), Java does not always handle such encodings.

## Results

Program saves result properties to the specified at the first step folder.
