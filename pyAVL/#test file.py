#test file

# I am currently resisting the urge to name my functions "vibe check"
# or "cock check". I'm seriously trying to make all of this readable by
# other people, which is why all the variables aren't named some variation
# of "bullshit123". 

a = [[' '],[''],['a']]
print(a)
b = []
for i,str in enumerate(a):
    print(i)
    if str[0].split() == []:
        continue
    else:
        b.append(str)
print(b)
