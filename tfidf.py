import os
import math as m


fo=open("Info/info.txt","r")
info_lines=fo.readlines()
N=int(info_lines[0])
total_doc_count=int(info_lines[1])
# print(total_doc_count)
for dir_name,subdir_name,f_name in os.walk('FinalIndex/'):
	for f in f_name:
		with open("FinalIndex/"+f, 'r') as txtfile:
			lines= txtfile.readlines()
			k=1
			for line in lines:
				x=line
				line=line.split(":")
				ldoc=len(line)-1
				rec=[]
				for entry in line[1:]:
					entry=entry.split(",")
					t1=[]
					for e in entry:
						if e!=''  and e!='\n':
							t1.append(int(e))
					rec.append(t1)
					t1.clear()
				if ldoc!=0:
					idf=m.log(total_doc_count/ldoc)
				else:
					idf=0
				t=""
				for i in rec:
					for j in i:
						tf=1+m.log(N/j)
						tfidf=tf*idf
						t+=str(t)+","
						t.rstrip(",")
					t+=":"
				t.rstrip(":")
				rec.clear()
				lines[k]=lines[k].replace(x,t)
				k=(k+1)%len(lines)
		with open("FinalIndex/"+f, 'w') as txtfile:
			txtfile.writelines(lines)





					
					

					



		