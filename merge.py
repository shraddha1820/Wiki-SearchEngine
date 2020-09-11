import os

def create_file(fname):
	if(not(os.path.isfile("FinalIndex/"+fname))):
		fout=open("FinalIndex/"+fname,"a+")
		for i in range(10010):
			fout.write('\n')
		fout.close()


fi = open("Info/info.txt","r") 
total_terms=int(fi.readline())  
# print(total_terms)

if not os.path.exists("FinalIndex/"):
	os.makedirs("FinalIndex/")

for dir_name,subdir_name,f_name in os.walk('TempIndex/'):
	for f in f_name:
		fin=open("TempIndex/"+f,"r")
		mul=f.rstrip(".txt")
		mul=1000*int(mul)
		content=fin.read()
		lines=content.split("\n")
		for l in lines:
			entries=l.split(":")
			if(len(entries)>1):
				temp_tid=int(entries[0])
				file_no=int(temp_tid/10000)
				line_no=temp_tid%10000
				# print(line_no)
				t_fname=str(file_no)+".txt"
				create_file(t_fname)
				for e in entries[1:]:
					temp=e.split(",")
					temp[0]=int(temp[0])+mul
					t=""
					for i in temp:
						t+=str(i)+","
					e.rstrip(",")
					with open("FinalIndex/"+t_fname, 'r') as txtfile:
						lines2= txtfile.readlines()
					# line2=lines2.split('\n')
					lines2[line_no-1] = lines2[line_no].replace('\n', ':') + t + '\n'
					with open("FinalIndex/"+t_fname, 'w') as txtfile:
						txtfile.writelines(lines2)
					txtfile.close()



