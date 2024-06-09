import random

lyrics = open('../lyrics.json')
jake = lyrics.readline()[1:]
jake = jake[:-78]
line = ""
line_pick = random.randint(0,len(jake)-6)
print(line_pick)

while jake[line_pick] != "\\":
    line_pick -= 1
line_pick += 2
while jake[line_pick] != "\\":
    line = line + jake[line_pick]
    line_pick += 1

print(jake.count("\\n") - 3)
print(jake)
print(line)

poop = "...\n\n******* This Lyrics is NOT for Commercial use *******\n(1409622393015)"
print(len(poop))
