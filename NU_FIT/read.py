import utils,time,isolate_overlaps
def readIntervals(FILE):
	FH 	= open(FILE)
	D 	= {"+":{}, "-":{}}
	for line in FH:
		lineArray 	= line.strip("\n").split("\t")
		assert len(lineArray)==5, "strand\tchrom\tstart\t\stop\tname(ID)\n format please..."
		strand, chrom,start, stop,name 	= lineArray
		if strand not in D:
			D[strand] 	= {}
		if chrom not in D[strand]:
			D[strand][chrom] 		= list()
		D[strand][chrom].append((int(start), int(stop), name))
	FH.close()
	#sort
	for strand in D:
		for chrom in D[strand]:
			D[strand][chrom].sort()


			D[strand][chrom] 	= utils.tree(isolate_overlaps.run(D[strand][chrom]))
	return D
class interval:
	def __init__(self, start, stop, name,chrom):
		self.start, self.stop,self.name,self.chrom 	= start, stop, name,chrom
		self.X, self.Y 								= list(),list()
		self.rvs 									= None
	def __str__(self):
		return self.chrom+":"+str(self.start) + "-"+str(self.stop) + ", " + self.name

def insertBedGraphFile(bgFile, D,strand,test=False):
	FH 	= open(bgFile)
	D 	= D[strand]
	prev=""
	H 	= {}
	for line in FH:
		lineArray 	= line.strip('\n').split("\t")
		assert len(lineArray)==4, "error in bedgraph file line, chrom\tstart\tstop\tcoverage\n"
		chrom,start, stop, cov 	= lineArray
		start, stop, cov 		= int(start), int(stop), int(cov)
		F 						= D[chrom].searchInterval((start, stop))
		if test and start > pow(10,7):
			break
	
		if chrom != prev:
			prev=chrom
		if F:
			for st, sp, name in F:
				if name not in H:
					H[name] 	= interval(st, sp, name, chrom)
				H[name].X+=[i for i in range(start, stop)]
				H[name].Y+=[cov for i in range(start, stop)]
	FH.close()
	return H



