import numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

def one_space(line, sep=" "):
  out = ''   
  indata = 0
  last_char = None
  for char in line:
    if(indata == 1 and char != "'" and last_char != "\\"):
      out = out + char
    elif(indata == 1 and char == "'" and last_char != "\\"):
      out = out + char
      indata = 0
    elif(indata == 2 and char != '"' and last_char != "\\"):
      out = out + char
    elif(indata == 2 and char == '"' and last_char != "\\"):
      out = out + char
      indata = 0
    elif(indata == 0 and not (char == " " and last_char == " ")):
      out = out + char
    last_char = char
  return out


filename = "Fe36MeV.exyz"
depth_limit = 1.0e9


d = {}
d_len = {}
d_pos = {}

in_data = False
fh = open(filename, 'r')
for line in fh:
  if(in_data == False):
    if(line.strip() == ("------- ----------- ---------- ----------- ----------- -----------  ---------------")):
      in_data = True
  else:
    line = one_space(line.strip())
    f = line.split(" ")
    if(len(f)):
      x_depth = float(f[2])
      if(x_depth <= depth_limit):
        ion_number = int(f[0])
        if(ion_number not in d_len.keys()):
          d_len[ion_number] = 0
        d_len[ion_number] = d_len[ion_number] + 1 
fh.close()

for k in d_len.keys():
  d[k] = numpy.zeros((d_len[k], 5,),)


in_data = False
fh = open(filename, 'r')
for line in fh:
  if(in_data == False):
    if(line.strip() == ("------- ----------- ---------- ----------- ----------- -----------  ---------------")):
      in_data = True
  else:
    line = one_space(line.strip())
    f = line.split(" ")
    if(len(f)):
      energy = float(f[1])
      x_depth = float(f[2])
      y = float(f[3])
      z = float(f[4])
      r = numpy.sqrt(x_depth**2 + y**2 + z**2)
      if(x_depth <= depth_limit):
        ion_number = int(f[0])
        if(ion_number not in d_pos.keys()):
          d_pos[ion_number] = 0
        d[ion_number][d_pos[ion_number], 0]  = energy
        d[ion_number][d_pos[ion_number], 1]  = x_depth
        d[ion_number][d_pos[ion_number], 2]  = y
        d[ion_number][d_pos[ion_number], 3]  = z
        d[ion_number][d_pos[ion_number], 4]  = r
        d_pos[ion_number] = d_pos[ion_number] + 1 
fh.close()

de = numpy.zeros(len(d.keys()),)
n = 0
for k in d.keys():
  de[n] = max(d[k][:,0]) - min(d[k][:,0])
  n = n + 1
print(de)


# the histogram of the data
plt.figure(figsize=(12,8))
n, bins, patches = plt.hist(de, 10, density=True, facecolor='g', alpha=0.75)
plt.xlabel('Energy Lost/KeV')
plt.ylabel('Fraction of Ions')
plt.title('Beam Energy Lost in Sample')
plt.grid(True)
plt.savefig('energy_lost.eps', format='eps')
plt.close('all') 


plt.figure(figsize=(12,8))
plt.title('Ion Trajectory')
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('x (depth)/Ang')
ax.set_ylabel('y/ang')
ax.set_zlabel('z/ang')
ax.ticklabel_format(style='sci')
for k in d_len.keys():
  x = d[k][:,1] 
  y = d[k][:,2] 
  z = d[k][:,3] 
  ax.plot(x, y, z)
plt.savefig('trajectory_3d.eps', format='eps')
plt.close('all') 

plt.figure(figsize=(12,8))
plt.title('Ion Energy In Target')
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.xlabel('x (depth)/Ang')
plt.ylabel('Energy/KeV')
for k in d_len.keys():
  x = d[k][:,1] 
  y = d[k][:,0] 
  plt.plot(x,y)
plt.savefig('energy_depth.eps', format='eps')
plt.close('all') 
 
