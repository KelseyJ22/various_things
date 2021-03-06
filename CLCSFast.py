# Kelsey Josund (kelsey2 05825031) and Gawan Fiore (gfiore 05824232)

import sys
import numpy as np

DIAG = 1
UP = 2
LEFT = 3
longest = 0

# dp_table contains 2 matrices ('c' and 'bp') that are each (m+1) x (n+1)
# they are the cost matrix and the backpointer matrix
dp_tables = {}
# paths is a matrix that is (m+1) x (n) x (2)
# it is called like: paths[source_row][column][0]
# in each tuple is stored the min and max row that the path starting at source_row has at a particular column
paths = {}


# clears a section of the DP tables that was just used to find a pervious path
def clearDPSector(mid, l, u, m, n):
	global dp_tables, paths

	COL_MIN = 0
	COL_MAX = 1

	row = mid
	next_start_col = 1
	while row < mid+m:
		col = next_start_col # Set col to appropriate starting value for next row
		while col <= n:
			if isValidPos(row, col, l, u):
				dp_tables['c'][row,col] = 0
				dp_tables['bp'][row,col] = 0
			else:
				break
			if isOnPath(u, row, col):
				next_start_col = col
			col += 1

		if next_start_col <= n:
			if (row+1) > paths[u-1, next_start_col-1, COL_MAX]:
				next_start_col += 1
		row += 1


# determines if the position is a valid one (between the bounding paths u and l)
def isValidPos(row, col, l, u):
	global paths
	COL_MIN = 0
	COL_MAX = 1

	if row >= paths[l-1, col-1, COL_MIN] and row <= paths[u-1, col-1, COL_MAX]:
		return True
	else:
		return False


# determines if a point is on a particular path
def isOnPath(path, row, col):
	global paths

	COL_MIN = 0
	COL_MAX = 1
	if row <= paths[path-1, col-1, COL_MAX] and row >= paths[path-1, col-1, COL_MIN]:
		return True
	else:
		return False

# finds the shortest path starting at [mid,1] and ending at [mid + m - 1, n]
def SingleShortestPath(A, B, mid, l, u):
	#find shortest path bounded by p_l and p_u
	global DIAG, UP, LEFT, dp_tables, paths

	COL_MIN = 0
	COL_MAX = 1
	m = len(A)
	n = len(B)

	row = mid
	next_start_col = 1
	while row < mid+m:
		col = next_start_col # Set col to appropriate starting value for next row
		while col <= n:
			if isValidPos(row, col, l, u):
				mod_row = (row - m) if row > m else row
				if A[mod_row - 1] == B[col-1]:
					dp_tables['c'][row,col] = dp_tables['c'][row-1, col-1] + 1
					dp_tables['bp'][row,col] = DIAG
				elif dp_tables['c'][row-1, col] >= dp_tables['c'][row, col-1]:
					dp_tables['c'][row,col] = dp_tables['c'][row-1, col]
					dp_tables['bp'][row,col] = UP
				else:
					dp_tables['c'][row,col] = dp_tables['c'][row, col-1]
					dp_tables['bp'][row,col] = LEFT
			else:
				break
			if isOnPath(u, row, col):
				next_start_col = col
			col += 1

		# set next row and column
		if next_start_col <= n:
			if (row+1) > paths[u-1, next_start_col-1, COL_MAX]:
				next_start_col += 1
		row += 1

	# # At end of iteration, record path attributes and clear DP tables
	addPath(mid, m, n)
	updateLongest(mid+m-1, n)
	clearDPSector(mid, l, u, m, n)


# recursively finds the shortest paths for all m
def FindShortestPaths(A, B, l, u):
	if(u-l <= 1):
		return
	mid = (l+u)/2
	SingleShortestPath(A, B, mid, l, u)
	FindShortestPaths(A, B, l, mid)
	FindShortestPaths(A, B, mid, u)


# adds a path to the path matrix
def addPath(source_row, m, n):
	global dp_tables, paths

	COL_MIN = 0
	COL_MAX = 1
	row = m - 1 + source_row
	col = n
	while col > 0 and row >= source_row:
		#record this node in the path
		if paths[source_row-1, col-1, COL_MAX] <= 0:
			paths[source_row-1, col-1, COL_MIN] = row
			paths[source_row-1, col-1, COL_MAX] = row
		elif paths[source_row-1, col-1, COL_MAX] > 0 and row < paths[source_row-1, col-1, COL_MIN]:
			paths[source_row-1, col-1, COL_MIN] = row
		#backtrace to next node
		if dp_tables['bp'][row, col]:
			if dp_tables['bp'][row, col] == 1:
				row -= 1
				col -= 1
			elif dp_tables['bp'][row, col] == 2:
				row -= 1
			elif dp_tables['bp'][row, col] == 3:
				col -= 1
			else:
				pass
		else:
			break
	#fix up end of path where it just runs along the side
	while col > 0:
		paths[source_row-1, col-1, COL_MIN] = row
		paths[source_row-1, col-1, COL_MAX] = row
		col -= 1
	while row > source_row:
		paths[source_row-1, 0, COL_MIN] = row
		if row > paths[source_row-1, 0, COL_MAX]:
			paths[row-1, 0, COL_MAX] = row
		row -= 1
	

# adds the maximum upper bound to the paths matrix
def addPathM(m, n):
	global paths

	COL_MIN = 0
	COL_MAX = 1
	for col in range(0, n):
		paths[m, col, COL_MIN] = paths[0, col, COL_MIN] + m
		paths[m, col, COL_MAX] = paths[0, col, COL_MAX] + m

#updates the longest path seen so far
def updateLongest(row_idx, col_idx):
	global dp_tables, longest

	if dp_tables['c'][row_idx, col_idx] > longest:
		longest = dp_tables['c'][row_idx, col_idx]


# creates initial cost and backpointer tables
# In bp[][], values are 1, 2, or 3. 0 indicates no back pointer.
# 1 = diagonal back pointer
# 2 = up back pointer
# 3 = left back pointer
def createDPTable(A, B):
	global DIAG, UP, LEFT
	m = len(A)
	n = len(B)

	c = np.zeros(((2*m)+1, n+1), dtype=int)
	bp = np.zeros(((2*m)+1, n+1), dtype=int)
	for i in range(1, m+1):
		for j in range(1, n+1):
			mod_i = (i - m) if i > m else i
			if A[mod_i - 1] == B[j - 1]:
				c[i,j] = c[i-1, j-1] + 1
				bp[i,j] = DIAG
			elif c[i-1, j] >= c[i, j-1]:
				c[i,j] = c[i-1, j]
				bp[i,j] = UP
			else:
				c[i,j] = c[i, j-1]
				bp[i,j] = LEFT
	return {'c':c, 'bp':bp}

#calls various functions to extract longest common substring
def CLCS(A, B):
	global dp_tables, paths, longest
	m = len(A)
	n = len(B)

	paths = np.zeros((m+1, n, 2), dtype=int) # m+1 paths because need p_0 / p_m duplicate bounding paths
	dp_tables = createDPTable(A, B) #Time: 7mn

	updateLongest(m, n)
	addPath(1, m, n)
	addPathM(m, n)

	c = np.zeros(((2*m)+1, n+1), dtype=int)
	bp = np.zeros(((2*m)+1, n+1), dtype=int)
	dp_tables = {'c':c, 'bp':bp} #equivalent to calling clearDPSector() at this level

	FindShortestPaths(A, B, 1, len(A)+1)

	return longest

def main():
	global longest
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print CLCS(A,B)
		longest = 0
	return

if __name__ == '__main__':
	main()