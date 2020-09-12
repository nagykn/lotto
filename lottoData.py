from random import sample, random
from collections import Counter

VALUES = [l for l in range(1,91)]
PAROS = [l for l in range(2,91,2)]
PARATLAN = [l for l in range(1,91,2)]
TIPPEK = []

def data(file_name):
	try:
		with open(file_name,"r") as file:
			for line in file:
				yield line
	except FileNotFoundError:
		print("[-] A fájlt nem lehetett beolvasni.")

def stat_str(line):
	return line.strip().split(";")

def random_tipp():
	return  sorted(sample(VALUES, k=5))

def random_eros_tipp():
	kimarad = sample([0,1,2,3,4],k=1)[0]
	if round(random()):
		return sorted(sample(PAROS[:kimarad*9]+PAROS[kimarad*9+9:],k=3)+sample(PARATLAN[:kimarad*9]+PARATLAN[kimarad*9+9:],k=2))
	else:
		return sorted(sample(PARATLAN[:kimarad*9]+PARATLAN[kimarad*9+9:],k=2)+sample(PAROS[:kimarad*9]+PAROS[kimarad*9+9:],k=3))


def talalat(tipp,huzas):
	count = Counter(tipp+huzas)
	return sum([1 for i in count.values() if i==2])

def tippek_generalas(n, callback):
	lista = []
	for i in range(n):
		tipp = callback()
		lista.append(tipp)
	return lista


def main():
	TIPPEK = []
	gen = data("lottoDB.csv")

	heti_random = False

	if input("Tippek kézi megadása (N/i)").upper() == "I":
		print("\nSzóközökkel elválasztva adjon meg öt különbüző egész számot [1;90]:")
		print("(nyomjon entert ha vége)")
		n = 0
		while tipp:=input(f"{n+1}. tipp:"):
			try:
				TIPPEK.append([int(tipp.split()[i]) for i in range(4)])
				n+=1
			except ValueError:
				print("Csak számokat adhat meg!")
				continue
			except IndexError:
				print("Öt számot kell megadni!")
				continue
	else:
		print("\nSzámokat random fogjuk generálni!")
		n = 20
		if szam:=input("\nHány számot fog megjátszani? (default=20) "):
			try:
				if int(szam) >= 1:
					n = int(szam)
				else:
					raise ValueError
			except ValueError:
				print("[*] A tippek száma 20 lesz!")

		if input("Erős tipp használata: (I/n)").upper() == "N":
			technika = random_tipp
		else:
			technika = random_eros_tipp


		TIPPEK = tippek_generalas(n,technika)

		for i,v in enumerate(TIPPEK):
			print(f"{i+1}. tipp: {v}")

		if input("\nMinden héten más random tippeket akarsz megjátszani? (I/n)").upper() == "I":
			heti_random = True

	input("\nMehet?")
	talalatok = [0,0,0,0,0,0]
	for value in gen:
		huzas = [int(i) for i in stat_str(value)[11:]]
		
		for tipp in TIPPEK:
			helyes = talalat(tipp,huzas)
			talalatok[helyes]+=1
		if heti_random:
			TIPPEK = tippek_generalas(n,technika)

	print(f"\n\tGratulálok!\n1957 és 2020 között, ha heti {n} szelvényt vettél volna:")
	print(f"{talalatok[5]} telitalálatod;")
	print(f"{talalatok[4]} négyes találatod;")
	print(f"{talalatok[3]} hármastalálatod lehetne.")



if __name__=="__main__":
	main()
