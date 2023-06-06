The challenge provides some subkeys of HKEY_LOCAL_MACHINE hive. Looking at the description, "PERSIST" is capitalized as a hint, so we focus on finding the persistence in those subkeys.

You can easily find some common paths that persistence loads in by doing some google search. Then you can see a suspect value in `SOFTWARE\Microsoft\Windows\CurrentVersion\Run`:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/7a4af49b-0871-4c20-88da-ef65db63451d)

Decode the base64 string:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/d0f5fd5b-571f-43a1-8595-8b3031c09cd9)

This is a powershell command line to download a file and save it to drive D:.

Let's see what file has been downloaded:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/9e013a30-bbd6-483a-8b81-420498e45e46)

A text file, if you common with file header, you can recognize that is the magic number of a zip file. Decode the hex and get the zip file:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/741b03bb-0a28-4a3a-ab29-ccfa1a96754a)

Take a look to zip file we got, the zip comment looks weird:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/5cd57b81-dc38-4991-8f63-0ba9603be951)

You can notice that when merge the characters together, it's make sense. So we gonna remove the "dot" that separated the original line:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/f61414b6-6d7e-4f4a-a92e-1ef4ef96b9a8)

Since the zip is password protected, the meaningful zip comment we got looks like a hint to the pass. So you need to come up with making your own wordlist and using it to crack the zip file:

```
#the hint told you about 4 digits after "Samsara", so we do a loop from 0000 to 9999:
def lenbuff(set):
        while len(set) < 4:
                set = '0' + set
        return set
with open("wordlist.txt", "w") as f:
        for i in range(10000):
                f.write("Samsara" + lenbuff(str(i)) + "\n")
```

Run `johntheripper` with above output wordlist:

![Screenshot (4109)](https://github.com/NVex0/LearningFunStuff/assets/113530029/90ed58da-3697-4ed2-8193-f66389af5f7b)

Yes, we got the password. Open it and we got 2 pictures:

![ScaraBoard1](https://github.com/NVex0/LearningFunStuff/assets/113530029/0dbc0d7a-6c26-4f3a-8328-7e705a4d05f5)

![ScaraBoard2](https://github.com/NVex0/LearningFunStuff/assets/113530029/b2e4edcf-1a79-43b7-a6dc-0841827c4741)

You can realize that we need to combine them to be able to read the text on it. Using below script:

```
from PIL import Image

img1 = Image.open("D:\Downloads\ScaraBoard1.png")
img2 = Image.open("D:\Downloads\ScaraBoard2.png")

result = Image.new(img1.mode, img1.size)
respix = result.load()

for x in range(img1.size[0]):
    for y in range(img1.size[1]):
        r1,g1,b1 = img1.getpixel((x, y))
        r2,g2,b2 = img2.getpixel((x, y))
        if (r1, g1, b1) != (0, 0, 0):
            respix[x, y] = r1, g1, b1
        else:
            respix[x, y] = r2, g2, b2

result.show()
```

Or you can simply "Xoring" them using `Stegsolve` tool:

![image](https://github.com/NVex0/LearningFunStuff/assets/113530029/4ea61d3c-e287-47f3-99eb-df972c50a650)


Now you can see the text, it is the flag:

![scaraboss](https://github.com/NVex0/LearningFunStuff/assets/113530029/ad2dfaa0-4354-45ce-a008-31150b2255c8)

Flag: `Flag{B3h0lD_tH3_ev3rla$t1nG_L()rd}`
