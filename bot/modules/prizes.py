prizes = [] # Do not touch this

act_prizes = [["example1", 20], ["example2", 1]]

for prize in act_prizes:
	i = prize[1]
	print(prize[0])
	while i > 0:
		prizes.append(prize[0])
		i -= 1



