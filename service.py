from student import Student
from os.path import isfile
from hash import hash

DB_PATH = 'db.txt'

class Service:
	def __init__(self, encryption_key : int):
		self.key = encryption_key

		self.init_file()

	@staticmethod
	def __encrypt(text : str, key : int):
		new_text = [None] * len(text)
		for i, c in enumerate(text):
			if 'A' <= c and c <= 'Z':
				new_text[i] = chr((ord(c) + key - ord('A')) % (ord('Z') - ord('A') + 1) + ord('A'))
			elif 'a' <= c and c <= 'z':
				new_text[i] = chr((ord(c) + key - ord('a')) % (ord('z') - ord('a') + 1) + ord('a'))
			elif '0' <= c and c <= '9':
				new_text[i] = chr((ord(c) + key - ord('0')) % (ord('9') - ord('0') + 1) + ord('0'))
			else:
				new_text[i] = c
		return ''.join(new_text)

	def encrypt(self, text : str):
		return Service.__encrypt(text, self.key)

	def decrypt(self, text : str):
		return Service.__encrypt(text, -self.key)

	def init_file(self):
		if isfile(DB_PATH):
			with open(DB_PATH, 'r') as f:
				try:
					keyhash = int(f.readline())
				except:
					raise ValueError(f'Invalid database format ({DB_PATH}) delete the file and rerun the program')
				
				if keyhash != hash(self.key):
					raise ValueError('Encryption keys do not match')
		else:
			with open(DB_PATH, 'w') as f:
				f.write(str(hash(self.key)) + '\n')

	def add_student(self, student):
		self.init_file()

		with open(DB_PATH, 'a') as f:
			f.write(self.encrypt(f'{student}\n'))

	def get_students(self) -> list[Student]:
		self.init_file()

		ret = []
		with open(DB_PATH, 'r') as f:
			for line in f.readlines()[1:]:
				try:
					student = Student.parse(self.decrypt(line.strip()))
				except:
					student = Student.invalid()
				
				ret.append(student)
		return ret
	
	def remove_student(self, idx):
		self.init_file()
		
		with open(DB_PATH, 'r') as f:
			lines = f.readlines()
		
		with open(DB_PATH, 'w') as f:
			for i, line in enumerate(lines):
				if i != idx + 1:
					f.write(line)

	def find_students(self, **by):
		ret = []
		for s in self.get_students():
			if vars(s).items() >= by.items():
				ret.append(s)
		return ret
