x = ['the steak', 'the steaks', 'your steak', 'the meat', 'your steaks', 'your meat', 'the beef', 'a steak', 'your beef', 'the chicken', 'the fish', 'each side', 'this steak', 'both sides', 'the food', 'the hamburger', 'your food', 'the meal', 'the grill', 'your dinner', 'the dinner', 'a meal', 'a few', 'any steak', 'the whole', 'the first', 'a little', 'your own', 'the entire', 'the cooked', 'a lot', 'a large', 'a small', 'all day', 'a third', 'a good', 'an entire', 'all the', 'it a', 'up a', 'yourself a']


d = {}
for elem in x: 
    noun = elem.split()[1]
    print(elem, noun)
    if noun in d.keys(): 
       d[noun].append(elem) 
    else: 
       d[noun] = []
       d[noun].append(elem)

print(d)


# CHECK HOW OFTEN EACH WORD OCCURS  steak: "your steak", "the steak"
# IF THE WORD OCCURS EARLIER, SAVE 