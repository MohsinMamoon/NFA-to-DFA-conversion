# NFA-to-DFA-conversion
A Python Script to convert an NFA (without epsilon transitions) to DFA

#### Usage:
***
1. Put the formal definition of NFA as an json object in a file input.json.
> Sample input.json: 
> Image here
2. Run the script by: `python3 script.py`
3. Formal definition of DFA will be printed to output file: output.json
> Sample output.json:
> Image here
+ To test the NFA and created DFA on some input strings, uncomment line 242 in the script:
> `# testNFA_DFA()`
