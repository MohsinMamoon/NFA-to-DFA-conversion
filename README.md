# NFA-to-DFA-conversion
A Python Script to convert an NFA (without epsilon transitions) to DFA

#### Usage:
***
1. Put the formal definition of NFA as an json object in a file input.json.
> Sample input.json:


> ![Sample Input](https://user-images.githubusercontent.com/43738980/63222029-78233b80-c1bf-11e9-9ec9-73b4b5681222.png)
2. Run the script by: `python3 script.py`
3. Formal definition of DFA will be printed to output file: output.json
> Sample output.json:


> ![Sample Output](https://user-images.githubusercontent.com/43738980/63222041-9c7f1800-c1bf-11e9-98e9-a4190e54eaf7.png)
+ To test the NFA and created DFA on some input strings, uncomment line 242 in the script:
`# testNFA_DFA()`
+ To know about the working of the script, refer to report.pdf
