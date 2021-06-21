# Stepik Bioinformatics Contest 2021 - Question 3

Place files and test5, test6, test7 into the same directory.

test5 and test6 should take under 2 seconds on a standard laptop... 

From a Python command line (Python 3.6.9) `python3`:

```
import settings
import q3end

settings.init()
q3end.readfile("test5", 120001)
q3end.save_answers("out5.txt")

settings.init()
q3end.readfile("test6", 1)
q3end.save_answers("out6.txt")

# this only reads test7 and doesn't get all the cases correct
settings.init()
q3end.readfile()
q3end.save_answers("out7.txt") 
```
