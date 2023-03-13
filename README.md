# SCP Cognitohazard Generator

An SCP cognitohazard generator. Run `py galileo.py` or run `galileo.exe` to start. You can make a custom image with Python using:

```
import coghaz

gen = coghaz.PerlmanGreeneGenerator('your text here', 'path/to/font.ttf')
gen.generate('path/to/output.png', height, width)
```

![example](killagent.png)
![example](killagent2.png)